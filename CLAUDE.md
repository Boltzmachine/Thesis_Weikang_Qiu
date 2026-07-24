# CLAUDE.md

Yale PhD dissertation (LaTeX). Main document: `Disseration.tex` (note the typo in the
filename — it is intentional, do not "fix" it).

## Build

```
make          # latexmk -> build/Disseration.pdf
make watch    # latexmk -pvc, continuous preview
make view     # build and open the PDF
make clean    # latexmk -c   (aux files)
make distclean# latexmk -C   (everything, incl. build/)
```

- Engine is **pdflatex + bibtex** (`.latexmkrc`), output goes to `build/`.
- Always build the whole document (`Disseration.tex`), never a chapter file alone.
- When checking a change compiles, run `make` and look for `!` / `.tex:LINE:` errors in
  the log; warnings about badboxes and undefined refs on a first pass are normal.

## Layout

- `Disseration.tex` — preamble, title/advisor/date metadata, and the `\include` /
  `\input` list of chapters.
- `macros.tex` — all extra packages and custom commands shared by the chapters
  (`\alg`, `\sail`, `\etal`, `\xhdr`, math operators, algorithm2e config).
  New macros go here, not in a chapter file.
- `abstract.tex`, `acknowledgements.tex`, `Introduction.tex` — front matter and Ch. 1.
- `PHIL/` — one example paper turned into a chapter group. `PHIL/main.tex` sets the order of
  `000intro`, `002preliminaries`, `001related_work`, `003approach`, `004experiments`,
  `005conclusion` (the file numbering does **not** match the reading order — follow
  `main.tex`). Figures live in `PHIL/figures/` and are referenced as
  `figures/xxx.png` thanks to `\graphicspath` in `Disseration.tex`.
- `bibfile.bib` — the single bibliography; style is `plainnat` with `natbib`.
- `yalephd.cls` — the Yale GSAS class file. Treat as vendored: don't edit it; if
  formatting needs to change, do it in the preamble of `Disseration.tex`.

## Conventions

- Citations use natbib: `\citep{key}` for parenthetical, `\citet{key}` inline.
- New references get appended to `bibfile.bib`; keep keys in the existing style and
  don't reformat or reorder unrelated entries.
- Labels are prefixed by kind: `chapter:`, `sec:`, `fig:`, `tab:`, `eq:`.
- `macros.tex` defines review-annotation commands (`\rex`, `\jure`, `\michal`,
  `\update`) that render colored inline notes. Don't leave new ones in final text.
- Adding a chapter: create the `.tex`, then `\include`/`\input` it from
  `Disseration.tex` (or from `PHIL/main.tex` for that group).

## Writing

- Academic prose, third person, past tense for experiments. Match the voice of the
  surrounding chapter rather than imposing a new one.
- Don't silently rewrite passages that were not asked about; edits should be scoped to
  what the user requested.

把https://www.overleaf.com/project/65b48eb2ee466089c846f6eb也加入dissertation，

## General Notes

合并paper时，appendix统一先不放
macro全文统一
如果你要copy一些东西，请不用verbose的输出内容，以免出现错误。尽量使用程序，例如cat来合并bib。但是，你需要保证rewind的时候也能撤销这些。

overleaf的token在@.latex_token