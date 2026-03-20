SPHINXBUILD   ?= $(shell if [ -x ../.venv/bin/sphinx-build ]; then echo ../.venv/bin/sphinx-build; else echo sphinx-build; fi)
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html latexpdf

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf "$(BUILDDIR)"

html:
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)"

latexpdf:
	$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)"
