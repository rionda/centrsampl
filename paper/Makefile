LATEX = pdflatex
MAINFILE = centrsampl-nostyle
UPLOADURI = ssh.cs.brown.edu:public_html/

.PHONY: all archive check clean osx pdf upload view

all : archive

$(MAINFILE).aux: *.tex
	$(LATEX) $(MAINFILE).tex
	$(LATEX) $(MAINFILE).tex

$(MAINFILE).blg: *.bib $(MAINFILE).aux
	$(LATEX) $(MAINFILE).tex
	bibtex --min-crossrefs=20 $(MAINFILE)
	$(LATEX) $(MAINFILE).tex
	$(LATEX) $(MAINFILE).tex

$(MAINFILE).pdf: *.tex *.bib figures/*eps
	$(LATEX) $(MAINFILE).tex
	bibtex --min-crossrefs=20 $(MAINFILE)
	$(LATEX) $(MAINFILE).tex
	$(LATEX) $(MAINFILE).tex

$(MAINFILE).tar.bz2: *tex $(MAINFILE).pdf
	env COPYFILE_DISABLE=1 tar cjvfh $(MAINFILE).tar.bz2 *.tex *.bib *.pdf $(wildcard *.bst) $(wildcard *.cls) $(wildcard *.clo) $(wildcard *.eps) $(wildcard *.svg) Makefile

archive: $(MAINFILE).tar.bz2

check: *.tex
	$(LATEX) $(MAINFILE).tex | grep -s -e "multiply" -e "undefined"

clean:
	-/bin/rm -f $(MAINFILE).pdf $(MAINFILE).tar.bz2 *.dvi *.aux *.ps *~
	-/bin/rm -f *.log *.lot *.lof *.toc *.blg *.bbl *.out 

pdf: $(MAINFILE).pdf

osx: pdf
	open $(MAINFILE).pdf

upload: pdf
	scp $(MAINFILE).pdf $(UPLOADURI)

view: pdf
	acroread  -geometry 1000x1000 $(MAINFILE).pdf

