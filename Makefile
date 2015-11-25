
JUJU_REPOSITORY := $(shell cd ..; pwd)

all: $(JUJU_REPOSITORY)/trusty/tor-relay $(JUJU_REPOSITORY)/trusty/tor-hidden

$(JUJU_REPOSITORY)/trusty/%:
	JUJU_REPOSITORY=$(JUJU_REPOSITORY) charm build $*

clean:
	$(RM) -r $(JUJU_REPOSITORY)/trusty/tor-relay
	$(RM) -r $(JUJU_REPOSITORY)/trusty/tor-hidden

.PHONY: all clean

