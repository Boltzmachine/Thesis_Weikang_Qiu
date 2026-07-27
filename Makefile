MAIN = Disseration
OUT  = build

.PHONY: all watch view clean distclean cwatch cwatch-stop cwatch-status cwatch-log

all:
	latexmk $(MAIN).tex

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
