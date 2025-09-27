#
# Makefile for libraries
#

# Get all library directories
LIB_DIRS := $(wildcard */)

# Default target - build all libraries
all: $(LIB_DIRS)

# Build each library
$(LIB_DIRS):
	@if [ -f $@/Makefile ]; then \
		echo "Building library $@..."; \
		$(MAKE) -C $@ || exit 1; \
	else \
		echo "Warning: No Makefile found in $@"; \
	fi

# Clean all libraries
clean:
	@for lib in $(LIB_DIRS); do \
		if [ -f $$lib/Makefile ]; then \
			echo "Cleaning library $$lib..."; \
			$(MAKE) -C $$lib clean || true; \
		fi \
	done

.PHONY: all $(LIB_DIRS) clean