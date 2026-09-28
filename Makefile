MAIN = Disseration
OUT  = build

.PHONY: all watch view clean distclean cwatch cwatch-stop cwatch-status cwatch-log figure-overview figure-motivation figure-brain-loop

all: figures/thesis_overview.pdf figures/language_bottleneck.pdf figures/future_directions/brain_closed_loop.pdf
	latexmk $(MAIN).tex

# Editable TikZ source for the dissertation overview.
figure-overview: figures/thesis_overview.pdf

figures/thesis_overview.pdf: figures/thesis_overview.tex
	mkdir -p $(OUT)/figures
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(OUT)/figures $<
	cp $(OUT)/figures/thesis_overview.pdf $@

# Motivation examples adapted from the original slide assets.
figure-motivation: figures/language_bottleneck.pdf

figures/language_bottleneck.pdf: figures/language_bottleneck.tex figures/introduction/long_prompt_slide.png figures/introduction/composition_vii.png
	mkdir -p $(OUT)/figures
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(OUT)/figures $<
	cp $(OUT)/figures/language_bottleneck.pdf $@

# Editable paper figure for future closed-loop brain intervention.
figure-brain-loop: figures/future_directions/brain_closed_loop.pdf

figures/future_directions/brain_closed_loop.pdf: figures/future_directions/brain_closed_loop.tex
	mkdir -p $(OUT)/figures/future_directions
	pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$(OUT)/figures/future_directions $<
	cp $(OUT)/figures/future_directions/brain_closed_loop.pdf $@

watch:
	latexmk -pvc $(MAIN).tex

view: all
	open $(OUT)/$(MAIN).pdf

# Background watcher: resolves [C: ...] author notes left in the .tex files.
cwatch:
	bash tools/cwatch.sh start

cwatch-stop:
	bash tools/cwatch.sh stop

cwatch-status:
	bash tools/cwatch.sh status

cwatch-log:
	bash tools/cwatch.sh log

clean:
	latexmk -c

distclean:
	latexmk -C
	rm -rf $(OUT)
