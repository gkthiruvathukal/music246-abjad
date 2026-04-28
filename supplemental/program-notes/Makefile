PDF := art-song-program-notes.pdf
TEX := art-song-program-notes.tex

.PHONY: all build view clean

all: build

build: $(PDF)

$(PDF): $(TEX)
	latexmk -pdf $(TEX)

view: $(PDF)
	open $(PDF)

clean:
	latexmk -c $(TEX)
