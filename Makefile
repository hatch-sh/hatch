SHELL := /bin/bash
QUIET ?= @
PIP := .venv/bin/pip
PYTHON := .venv/bin/python

python_files := \
	$(wildcard api/**/*.py) \
	$(wildcard *.py) \
	$(wildcard **/*.py)

lint_targets := \
	.build/pylint.made \
	.build/flake8.made

setup_targets := \
	.venv/.installed

setup: $(setup_targets)

install: ; python setup.py install

clean:
	rm -rf .build build dist
	python setup.py clean

distclen: clean;
	rm -rf .venv
	rm /usr/local/bin/easyaws

lint: $(lint_targets)
format: .build/autopep8.made

#
# Rules
#

# Lint python files using pylint
.build/pylint.made: $(python_files)
	$(QUIET).venv/bin/pylint \
		--errors-only \
		--msg-template="{path}({line}): [{msg_id}{obj}] {msg}" \
		$^
	$(call touch, $@)

# Lint python files using flake8
.build/flake8.made: $(python_files)
	$(QUIET).venv/bin/flake8 $^
	$(call touch, $@)

# Format python files using autopep8
.build/autopep8.made: $(python_files)
	$(QUIET).venv/bin/autopep8 --in-place --aggressive --aggressive $^

# Creating the virtual environment
.venv/.made:
	@virtualenv -q --no-site-packages -p python2.7 $(dir $@)
	$(PIP) install pip==9.0.1 setuptools==18.2
	$(call touch, $@)

# Install the dependencies
.venv/.installed: .venv/.made requirements.txt
	$(PIP) install --editable .
	$(call touch, $@)

# This is a target to help you debug the Makefile whenever things
# don't work as you expect. You use it to print the value of a
# variable like so `make print-VARIABLENAME`, e.g.
# `make print-repositories`.
print-%: ; @echo $* is $($*)

#
# Functions
#

# $(call touch, file)
#   Used to touch a file while ensuring that any parent directories are
#   created beforehand.
define touch
	@mkdir -p $(dir $1)
	@touch $1
endef

# $(call print-rule, variable, extra)
#   Used to decorate the output before printing it to stdout.
define print
	@echo -e "[$(shell date +%H:%M:%S)] $(bold_green)$(strip $1)$(reset): $(strip $2)"
endef
