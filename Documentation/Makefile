# SPDX-License-Identifier: GPL-2.0
# Peios documentation lives in docs/. Retained inputs here serve kernel tooling.
subdir- := devicetree/bindings
srctree ?= .
obj ?= Documentation
TRAIL ?= trail
PYTHON3 ?= python3
BUILDDIR ?= $(abspath $(obj)/output)

ifneq ($(MAKECMDGOALS),cleandocs)
ifeq ($(CONFIG_WARN_MISSING_DOCUMENTS),y)
$(shell cd $(srctree); tools/docs/documentation-file-ref-check --warn)
endif
ifeq ($(CONFIG_WARN_ABI_ERRORS),y)
$(shell $(srctree)/tools/docs/get_abi.py --dir $(srctree)/Documentation/ABI validate)
endif
endif

.PHONY: htmldocs linkcheckdocs htmldocs-redirects mandocs refcheckdocs cleandocs dochelp
htmldocs:
	$(Q)$(TRAIL) build $(abspath $(srctree))/docs --out $(BUILDDIR) --strict

linkcheckdocs: htmldocs
	$(Q)$(PYTHON3) $(srctree)/peios/docs-migration/check_site.py $(BUILDDIR)

htmldocs-redirects: htmldocs
	$(Q)$(PYTHON3) $(srctree)/peios/docs-migration/redirects.py --kernel-root $(srctree) --out $(BUILDDIR)

mandocs:
	$(Q)mkdir -p $(BUILDDIR)/man
	+$(Q)$(MAKE) -C $(srctree)/Documentation/tools/rtla OUTPUT=$(BUILDDIR)/man/ man
	+$(Q)$(MAKE) -C $(srctree)/Documentation/tools/rv OUTPUT=$(BUILDDIR)/man/ man

refcheckdocs:
	$(Q)cd $(srctree); tools/docs/documentation-file-ref-check

cleandocs:
	$(Q)rm -rf $(BUILDDIR)

xmldocs latexdocs pdfdocs epubdocs texinfodocs infodocs:
	@echo 'Peios documentation uses Trail. Use make htmldocs; these Sphinx formats are no longer built.' >&2
	@false

dochelp:
	@echo ' Peios kernel documentation (maintained in docs/):'
	@echo '  htmldocs           - Build the Trail HTML site (TRAIL=path/to/trail)'
	@echo '  linkcheckdocs      - Build and check local links, anchors and assets'
	@echo '  htmldocs-redirects - Build with redirects from former RST page URLs'
	@echo '  mandocs            - Build RTLA and RV manual pages'
	@echo '  refcheckdocs       - Check source references, resolving migrated paths'
	@echo '  cleandocs          - Remove generated documentation output'
	@echo '  BUILDDIR=path      - Override the default Documentation/output'
