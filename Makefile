
REPO := $(shell cd ..; pwd)

CHARMS=tor-relay tor-hidden tor-bridge

all: $(CHARMS:%=$(REPO)/builds/%)

$(REPO)/builds/%:
	JUJU_REPOSITORY=$(REPO) charm build $*

clean:
	$(RM) -r $(CHARMS:%=$(REPO)/builds/%)

.PHONY: all clean

