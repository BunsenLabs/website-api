#
# Make the BunsenLabs Website
# Written by 2ion <dev@2ion.de>
#

SHELL=/bin/bash

# Pandoc site template
TEMPLATE=templates/default.html5

# Determine HTML targets
TARGETS=$(patsubst %.mkd,%.html,$(wildcard src/*.mkd))

# Files to deploy
ASSETS=$(TARGETS) src/js src/img src/css 

# Main navigation and page header
NAVIGATION_HTML=src/global/navigation.html

# CSS include path, relative to pageroot
STYLE=css/plain.css

# Pandoc arguments
ARGV=--email-obfuscation=javascript \
		 --smart \
		 --template=$(TEMPLATE) \
		 -f markdown+footnotes+fenced_code_attributes \
		 -s \
		 -c $(STYLE) \
		 --highlight-style monochrome \
		 --include-before-body=$(NAVIGATION_HTML)

# Checkout directory which will be uploaded
DESTDIR=dst

# Provides page titles
include config/env.mk

checkout: all
	@rsync -au --human-readable $(ASSETS) $(DESTDIR)

all: $(TARGETS) 

%.html: %.mkd $(TEMPLATE)
	$(info -----)
	pandoc $(ARGV) -M pagetitle="$($<.title)" -o $@ $<
	./postproc $@

clean:
	rm -f src/*.html
	rm -fr dst/*

deploy: checkout
	@echo Not implemented.
