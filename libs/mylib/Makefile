#
# Makefile for mylib
#

# Library name
LIB_NAME = mylib

OBJ_DIR = $(shell pwd)

# Source files
SRCS = mylib.c
OBJS = $(SRCS:%.c=$(OBJ_DIR)/%.o)

# Compiler flags
CFLAGS ?= -O2 -fPIC -I.

# Build targets
all: $(OBJ_DIR)/lib$(LIB_NAME).so $(OBJ_DIR)/lib$(LIB_NAME).a

# Shared library
$(OBJ_DIR)/lib$(LIB_NAME).so: $(OBJS)
	@mkdir -p $(dir $@)
	@$(CC) -shared -o $@ $(OBJS)
	@echo "CC $<"
	@echo "Built shared library: $@"
	@echo "Installing shared library to $(TARGET_SHARED_LIBS_DIR)"
	@cp $@ $(TARGET_SHARED_LIBS_DIR)
	@echo ""

# Static library
$(OBJ_DIR)/lib$(LIB_NAME).a: $(OBJS)
	@mkdir -p $(dir $@)
	@$(AR) rcs $@ $(OBJS)
	@echo "AR $<"
	@echo "Built static library: $@"
	@echo ""

# Compile objects
$(OBJ_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) -c -o $@ $<
	@echo "CC $<"
	@echo ""

# Clean
clean:
	rm -f $(OBJ_DIR)/*.o
	rm -f $(OBJ_DIR)/*.a
	rm -f $(OBJ_DIR)/*.so
	rm -f $(TARGET_SHARED_LIBS_DIR)/lib$(LIB_NAME).so

.PHONY: all clean