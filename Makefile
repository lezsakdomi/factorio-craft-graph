GRAPH_NAME=graph
OUTPUT_NAME=data

PREFERRED_FORMAT=svg
PREFERRED_FILE=$(GRAPH_NAME).$(PREFERRED_FORMAT)
DOT_TOOL=dot

DOWNLOAD_FACTORIO=1
FACTORIO_DIR=$(if $(DOWNLOAD_FACTORIO),factorio,.)

.PHONY: all
all: $(PREFERRED_FILE)

$(GRAPH_NAME).%: $(OUTPUT_NAME).dot
	$(DOT_TOOL) -T$* <$< >$@

$(OUTPUT_NAME).html: $(OUTPUT_NAME).md
	markdown $< >$@

.SECONDARY: $(OUTPUT_NAME).dot
$(OUTPUT_NAME).%: generate-dot.py $(FACTORIO_DIR)
	python3 generate-dot.py --factorio $(FACTORIO_DIR) -f $* >$@

.PHONY: clean clean-$(GRAPH_NAME) clean-$(OUTPUT_NAME)
clean: clean-$(GRAPH_NAME) clean-$(OUTPUT_NAME)
	-rm factorio.tar.xz
	-rm -r factorio

clean-$(GRAPH_NAME):
	-rm $(GRAPH_NAME).*

clean-$(OUTPUT_NAME):
	-rm $(OUTPUT_NAME).*

.PHONY: open
open: $(PREFERRED_FILE)
	xdg-open $<

#.PHONY: open-in-firefox open-in-vim
open-in-%: $(PREFERRED_FILE)
	$* $<

.SECONDARY: factorio
factorio: factorio.tar.xz
	tar -xJf $<

.INTERMEDIATE: factorio.tar.xz
# Download factorio
factorio.tar.xz:
	wget https://www.factorio.com/get-download/latest/demo/linux64 -Ofactorio.tar.xz
