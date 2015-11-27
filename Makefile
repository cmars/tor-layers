
REPO := $(shell cd ..; pwd)

all: $(REPO)/trusty/tor-relay $(JUJU_REPOSITORY)/trusty/tor-hidden

$(REPO)/trusty/%:
	JUJU_REPOSITORY=$(REPO) charm build $*

clean:
	$(RM) -r $(REPO)/trusty/tor-relay
	$(RM) -r $(REPO)/trusty/tor-hidden

.PHONY: all clean

