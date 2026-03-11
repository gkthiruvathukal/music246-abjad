LILYPOND ?= lilypond
PYTHON   ?= python3

SRC_DIR  := src
BUILD_DIR := build

SOURCES := $(wildcard $(SRC_DIR)/*.ly)
PDFS    := $(patsubst $(SRC_DIR)/%.ly,$(BUILD_DIR)/%.pdf,$(SOURCES))
MIDIS   := $(patsubst $(SRC_DIR)/%.ly,$(BUILD_DIR)/%.midi,$(SOURCES))

ABJAD_CMD := $(PYTHON) -m modus_operandi_abjad

.PHONY: all clean abjad abjad-ly abjad-pdf abjad-midi abjad-wav install jazz-rhythms jazz-rhythms-ly jazz-rhythms-pdf

all: $(PDFS)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# LilyPond produces both .pdf and .midi from a single invocation.
# We use the .pdf as the primary target and the .midi comes along for free.
$(BUILD_DIR)/%.pdf $(BUILD_DIR)/%.midi: $(SRC_DIR)/%.ly | $(BUILD_DIR)
	$(LILYPOND) -o $(BUILD_DIR)/$* $<

# --- Python / Abjad targets ---
install:
	$(PYTHON) -m pip install -e .

ABJAD_CMD := $(PYTHON) -m modus_operandi_abjad
abjad:
	$(ABJAD_CMD) -o $(BUILD_DIR)

abjad-ly:
	$(ABJAD_CMD) -o $(BUILD_DIR) --ly

abjad-pdf:
	$(ABJAD_CMD) -o $(BUILD_DIR) --pdf

abjad-midi:
	$(ABJAD_CMD) -o $(BUILD_DIR) --midi

abjad-wav:
	./midi2wav.sh $(BUILD_DIR)/modus-operandi-abjad.midi $(BUILD_DIR)/modus-operandi-abjad.wav

JAZZ_RHYTHMS_CMD := $(PYTHON) -m jazz_rhythm.cli

jazz-rhythms:
	$(JAZZ_RHYTHMS_CMD) -o $(BUILD_DIR)

jazz-rhythms-ly:
	$(JAZZ_RHYTHMS_CMD) -o $(BUILD_DIR) --ly

jazz-rhythms-pdf:
	$(JAZZ_RHYTHMS_CMD) -o $(BUILD_DIR) --pdf

clean:
	rm -rf $(BUILD_DIR)
