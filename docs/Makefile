# Minimal makefile for Sphinx documentation
#

# Disable make's inbuilt rules
.SUFFIXES:

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = $(VENV_ROOT)/bin/sphinx-build
SPHINXPROJ    = LiteXBuildEnvironmentTool
SOURCEDIR     = .
BUILDDIR      = .build
VENV_ROOT     = $(BUILDDIR)/.venv

# Set up a virtualenv
$(VENV_ROOT)/bin/python3:
	virtualenv -p python3 $(VENV_ROOT)

ACTIVATE = source $(VENV_ROOT)/bin/activate

# Put it first so that "make" without argument is like "make help".
#-------------------------------------------
help: $(SPHINXBUILD)
	@$(SPHINXRUN) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help

# Install the requirements into the virtualenv
#-------------------------------------------
$(VENV_ROOT)/requirements.stamp: requirements.txt $(VENV_ROOT)/bin/python3
	$(ACTIVATE); pip install -r requirements.txt
	@touch $(VENV_ROOT)/requirements.stamp

$(SPHINXBUILD): $(VENV_ROOT)/requirements.stamp $(VENV_ROOT)/bin/python3
	@touch $<

distclean:
	rm -rf _build $(VENV_ROOT) .Makefile.d
	mkdir -p _build
	mkdir -p $(VENV_ROOT)

clean:
	rm -rf _doxygen verilog
	@$(ACTIVATE); $(SPHINXRUN) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

SPHINXRUN = $(ACTIVATE); $(VENV_ROOT)/bin/python3 $(VENV_ROOT)/bin/sphinx-build

.PHONY: distclean clean

# Generate targets for all the other sphinx commands.
#-------------------------------------------
SPHINXCMD = $(SPHINXRUN) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
SPHINXSUBCMD = $(SPHINXRUN) -M $$@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.Makefile.d: $(SPHINXBUILD) Makefile
	$(SPHINXRUN) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) \
		| grep "^ " \
		| sed -e's/^ \+//' -e's|^\([^ ]*\) \+.*$$|\1: $(SPHINXBUILD)\n\t$(SPHINXSUBCMD)\n\n.PHONY: \1\n\n|' \
		> .Makefile.d

-include .Makefile.d

api:
	($(ACTIVATE); cd ..; sphinx-apidoc --ext-autodoc --ext-doctest --ext-todo --module-first -f -o docs/api lxbe_tool)


.PHONY: api
