#!/usr/bin/env bash
#
# cwatch — watch the dissertation's .tex files for inline author notes of the
# form [C: ...] and have a headless Claude Code resolve each one in place.
#
#   bash tools/cwatch.sh start     start the daemon in the background
#   bash tools/cwatch.sh stop      stop it
#   bash tools/cwatch.sh status    is it running, and what notes are outstanding
#   bash tools/cwatch.sh once      one pass in the foreground (dry run: once -n)
#   bash tools/cwatch.sh log       tail the log
#   bash tools/cwatch.sh reset     clear the give-up counters
#
# Tunables (environment):
#   CWATCH_POLL=5           seconds between scans
#   CWATCH_SETTLE=15        a file must be untouched this long before it is edited
#   CWATCH_MAX_ATTEMPTS=2   give up on a note after this many failed passes
#   CWATCH_MODEL=opus       model for the headless run
#   CWATCH_BACKUP_DIR       override the local backup directory outside OneDrive
#
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="$ROOT/.cwatch"
BACKUPS="${CWATCH_BACKUP_DIR:-$HOME/Thesis_Backups/$(basename "$ROOT")/cwatch}"
ATTEMPTS="$STATE/attempts"
LOG="$STATE/cwatch.log"
PIDFILE="$STATE/cwatch.pid"

POLL="${CWATCH_POLL:-5}"
SETTLE="${CWATCH_SETTLE:-15}"
MAX_ATTEMPTS="${CWATCH_MAX_ATTEMPTS:-2}"
MODEL="${CWATCH_MODEL:-opus}"

DRY_RUN=0

mkdir -p "$BACKUPS" "$ATTEMPTS"

log() {
  printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >>"$LOG"
  printf '%s  %s\n' "$(date '+%H:%M:%S')" "$*"
}

mtime() { stat -f %m "$1" 2>/dev/null || echo 0; }

# All .tex files that mention a note at all. Whether the note is closed is
# decided per file by markers_in, which is the thing that can see across lines.
scan_files() {
  grep -rl --include='*.tex' \
       --exclude-dir=build --exclude-dir=.git --exclude-dir=.cwatch \
       -e '\[C:' "$ROOT" 2>/dev/null
}

# Notes may wrap across source lines, so match against the whole file rather than
# line by line. Each note is printed on one line with its newlines folded away, so
# it stays usable as a log entry and as a hash key.
markers_in() {
  perl -0777 -ne 'while (/\[C:[^\]]*\]/gs) { $m = $&; $m =~ s/\s+/ /g; print "$m\n" }' \
       "$1" 2>/dev/null
}

key_of() { printf '%s' "$1" | shasum | cut -d' ' -f1; }

# ---------------------------------------------------------------- the prompt --
build_prompt() {
  local rel="$1"
  cat <<EOF
The file $rel contains one or more inline author notes written as [C: ...].
Each note is an instruction from the dissertation's author about the sentence or
paragraph it sits in. The notes may be written in English, Chinese, or both.

For each note in that file:
  1. Read the paragraph it sits in, and enough of the surrounding chapter to know
     what the note is objecting to.
  2. Revise the prose so it satisfies the note. A note is an instruction about
     the text, never text to be inserted into the document.
  3. Delete the note itself, brackets included, and clean up any doubled space or
     stray punctuation its removal leaves behind.

Rules:
  - Edit only $rel. Do not touch any other file. Do not build, do not run git.
  - Change only what the note asks for. Every other sentence in the file, and
    every paragraph the note does not concern, must stay byte-identical.
  - Keep the academic voice of the surrounding chapter, and keep all LaTeX markup,
    custom macros, \\citep/\\citet keys, \\ref targets and \\label names intact.
  - If a note is too ambiguous to act on confidently, leave both the note and the
    prose untouched and say so.

Report one line per note: quote the note, then state in one sentence what you
changed, or why you left it alone.
EOF
}

# --------------------------------------------------------------- one file ----
process_file() {
  local file="$1"
  local rel="${file#"$ROOT"/}"
  local now age
  now="$(date +%s)"
  age=$(( now - $(mtime "$file") ))

  # Still being typed in? Wait until the file has settled.
  if (( age < SETTLE )); then
    return 0
  fi

  # Skip notes we have already failed on, so a stubborn one cannot loop forever.
  local pending=0 mk k n
  while IFS= read -r mk; do
    [ -n "$mk" ] || continue
    k="$(key_of "$rel|$mk")"
    n=0
    [ -f "$ATTEMPTS/$k" ] && n="$(cat "$ATTEMPTS/$k")"
    if (( n >= MAX_ATTEMPTS )); then
      continue
    fi
    pending=1
  done < <(markers_in "$file")

  (( pending )) || return 0

  log "note found in $rel:"
  markers_in "$file" | sed 's/^/                      /' | tee -a "$LOG" >/dev/null
  markers_in "$file" | sed 's/^/    /'

  if (( DRY_RUN )); then
    log "dry run — not calling claude"
    return 0
  fi

  local stamp backup
  stamp="$(date '+%Y%m%d-%H%M%S')"
  backup="$BACKUPS/$stamp-$(echo "$rel" | tr '/' '_')"
  cp "$file" "$backup"
  log "backup -> ${backup#"$ROOT"/}"

  local out
  out="$(cd "$ROOT" && build_prompt "$rel" | claude -p \
          --model "$MODEL" \
          --permission-mode acceptEdits \
          --allowedTools Read Edit Grep Glob \
          --disallowedTools Bash Write WebFetch WebSearch Task \
          2>&1)"

  printf '%s\n' "$out" >>"$LOG"
  printf '%s\n' "$out" | sed 's/^/    /'

  # Did the notes actually go away? If not, count a strike against each survivor.
  local left
  left="$(markers_in "$file")"
  if [ -z "$left" ]; then
    log "resolved all notes in $rel"
    # Clear the strike counters for this file's old notes.
    return 0
  fi

  while IFS= read -r mk; do
    [ -n "$mk" ] || continue
    k="$(key_of "$rel|$mk")"
    n=0
    [ -f "$ATTEMPTS/$k" ] && n="$(cat "$ATTEMPTS/$k")"
    n=$(( n + 1 ))
    echo "$n" >"$ATTEMPTS/$k"
    if (( n >= MAX_ATTEMPTS )); then
      log "giving up on $rel: $mk  (edit or remove the note by hand)"
    else
      log "note survived in $rel, will retry: $mk"
    fi
  done <<<"$left"
}

pass() {
  local f
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    process_file "$f"
  done < <(scan_files)
}

loop() {
  log "cwatch started (pid $$) — watching $ROOT for [C: ...] notes"
  log "poll=${POLL}s settle=${SETTLE}s model=$MODEL"
  trap 'log "cwatch stopped"; rm -f "$PIDFILE"; exit 0' INT TERM
  while true; do
    pass
    sleep "$POLL"
  done
}

# ------------------------------------------------------------------ commands --
case "${1:-start}" in
  start)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "cwatch already running (pid $(cat "$PIDFILE"))"
      exit 0
    fi
    nohup bash "$0" _run >>"$LOG" 2>&1 &
    echo $! >"$PIDFILE"
    echo "cwatch started (pid $(cat "$PIDFILE"))  ·  log: ${LOG#"$ROOT"/}"
    ;;
  _run)
    echo $$ >"$PIDFILE"
    loop
    ;;
  stop)
    if [ -f "$PIDFILE" ]; then
      kill "$(cat "$PIDFILE")" 2>/dev/null && echo "cwatch stopped"
      rm -f "$PIDFILE"
    else
      echo "cwatch is not running"
    fi
    ;;
  status)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "cwatch running (pid $(cat "$PIDFILE"))"
    else
      echo "cwatch not running"
    fi
    echo "outstanding notes:"
    found=0
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      while IFS= read -r mk; do
        [ -n "$mk" ] || continue
        echo "  ${f#"$ROOT"/}: $mk"
        found=1
      done < <(markers_in "$f")
    done < <(scan_files)
    (( found )) || echo "  (none)"
    ;;
  once)
    [ "${2:-}" = "-n" ] && DRY_RUN=1
    pass
    ;;
  log)
    tail -f "$LOG"
    ;;
  reset)
    rm -f "$ATTEMPTS"/*
    echo "attempt counters cleared"
    ;;
  *)
    sed -n '3,16p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
