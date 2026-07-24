MAIN = Disseration
OUT  = build

.PHONY: all watch view clean distclean

all:
	latexmk $(MAIN).tex

watch:
	latexmk -pvc $(MAIN).tex

view: all
	open $(OUT)/$(MAIN).pdf

clean:
	latexmk -c

distclean:
	latexmk -C
	rm -rf $(OUT)
