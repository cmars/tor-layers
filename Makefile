
REPO := $(shell cd ..; pwd)

CHARMS=tor-relay tor-hidden tor-bridge

all: $(CHARMS:%=$(REPO)/xenial/%)

upload: $(CHARMS:%=upload-%)

upload-%:
	charm2 upload $(REPO)/xenial/$* cs:~cmars/xenial/$*

publish: $(CHARMS:%=publish-%)

publish-%:
	charm2 publish cs:~cmars/xenial/$*

$(REPO)/xenial/%:
	JUJU_REPOSITORY=$(REPO) charm build $*

clean:
	$(RM) -r $(CHARMS:%=$(REPO)/xenial/%)

.PHONY: all clean upload publish $(CHARMS:%=upload-%) $(CHARMS:%=publish-%)

