PY3 := $(shell command -v python3 2> /dev/null)

ifndef PY3
$(error Could not found python3 command installed on this system.)
endif


.PHONY: install
install:
	chmod a+x sentential.py
	ln -sf $(CURDIR)/sentential.py /usr/local/sbin/sentencial
