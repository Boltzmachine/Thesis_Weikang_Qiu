$pdf_mode = 1;                 # pdflatex
$bibtex_use = 2;               # run bibtex, and clean .bbl on `latexmk -C`
$out_dir = 'build';
$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
@default_files = ('Disseration.tex');

# Also remove these on `latexmk -c`
$clean_ext = 'synctex.gz bbl run.xml brf';
