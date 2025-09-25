#
# Makefile
#

# compilers, please change to your own c/c++ compilers
CC	=	$(C_COMPILER)
CXX	=	$(CXX_COMPILER)

# feature flags
# whether to exclude demos and examples from the build
EXCLUDE_DEMOS_AND_EXAMPLES = 1

# directories
LVGL_DIR_NAME	?=	lvgl
LVGL_DIR	?=	${shell pwd}
SRC_DIR	=	$(LVGL_DIR)/src
BUILD_DIR	=	./build
BUILD_OBJ_DIR	=	$(BUILD_DIR)/obj
BUILD_BIN_DIR	=	$(BUILD_DIR)/bin

# output binary name
BIN = app

# warnings to disabled
WARNINGS	=	-Wall -Wshadow -Wundef -Wmissing-prototypes -Wno-discarded-qualifiers -Wall -Wextra -Wno-unused-function -Wno-error=strict-prototypes \
				-Wpointer-arith -fno-strict-aliasing -Wno-error=cpp -Wuninitialized -Wmaybe-uninitialized -Wno-unused-parameter \
				-Wno-missing-field-initializers -Wtype-limits -Wsizeof-pointer-memaccess -Wno-format-nonliteral -Wno-cast-qual \
				-Wunreachable-code -Wno-switch-default -Wreturn-type -Wmultichar -Wformat-security -Wno-ignored-qualifiers \
				-Wno-error=pedantic -Wno-sign-compare -Wno-error=missing-prototypes -Wdouble-promotion -Wclobbered -Wdeprecated \
				-Wempty-body -Wtype-limits -Wshift-negative-value -Wstack-usage=2048 -Wno-unused-value -Wno-unused-parameter \
				-Wno-missing-field-initializers -Wuninitialized -Wmaybe-uninitialized -Wall -Wextra -Wno-unused-parameter \
				-Wno-missing-field-initializers -Wtype-limits -Wsizeof-pointer-memaccess -Wno-format-nonliteral -Wpointer-arith \
				-Wno-cast-qual -Wmissing-prototypes -Wunreachable-code -Wno-switch-default -Wreturn-type -Wmultichar \
				-Wno-discarded-qualifiers -Wformat-security -Wno-ignored-qualifiers -Wno-sign-compare

# compiler flags
CFLAGS	?=	-O3 -g0 \
			-I$(LVGL_DIR)/ -I$(SRC_DIR) \
			$(WARNINGS)

# linker flags
LDFLAGS	?=	-lm


prefix	?=	/usr
bindir	?=	$(prefix)/bin

# object file ext
OBJEXT ?= .o

# c source files to be compiled
CSRCS	:=	$(shell find $(SRC_DIR) -type f -name '*.c')
#CSRCS +=$(LVGL_DIR)/mouse_cursor_icon.c

# cpp source files to be compiled
CXXSRCS	:=	$(shell find $(SRC_DIR) -type f -name '*.cpp')

# assembly source files to be compiled
ASRCS	:= $(shell find $(SRC_DIR) -type f -name '*.S')

include $(LVGL_DIR)/lvgl_include.mk

# object files 
COBJS	=	$(CSRCS:%.c=$(BUILD_OBJ_DIR)/%$(OBJEXT))
CXXOBJS	=	$(CXXSRCS:%.cpp=$(BUILD_OBJ_DIR)/%$(OBJEXT))
AOBJS	=	$(ASRCS:%.S=$(BUILD_OBJ_DIR)/%$(OBJEXT))


SRCS	=	$(ASRCS) $(CSRCS) $(CXXSRCS)
OBJS	=	$(AOBJS) $(COBJS) $(CXXOBJS)

all: | $(BUILD_OBJ_DIR) $(BUILD_BIN_DIR) $(DIST_DIR)
all: $(BUILD_BIN_DIR)/$(BIN)

$(BUILD_OBJ_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "CC $<"

$(BUILD_OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	@$(CXX) $(CFLAGS) -c $< -o $@
	@echo "CXX $<"

$(BUILD_OBJ_DIR)/%.o: %.S
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "AS $<"

$(BUILD_BIN_DIR)/$(BIN): $(OBJS)
	$(CC) -o $@ $(OBJS) $(LDFLAGS)
	@echo "Build completed. Output binary: $(BUILD_BIN_DIR)/$(BIN)"

$(BUILD_OBJ_DIR):
	@mkdir -p $@

$(BUILD_BIN_DIR):
	@mkdir -p $@

clean: 
	rm -rf $(BUILD_DIR)

# install:
# 	install $(DIST_DIR)/$(BIN) $(DESTDIR)$(bindir)

# uninstall:
# 	$(RM) -r $(addprefix $(DESTDIR)$(bindir)/,$(BIN))

# .PHONY: all clean install uninstall
.PHONY: all clean
