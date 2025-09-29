#
# Makefile
#
TOOLCHAIN_PATH	=	$(TOOLCHAIN_PATH)
TOOLCHAIN_PREFIX	=	$(TOOLCHAIN_PREFIX)

# make sure the TOOLCHAIN_PATH ends with a slash if it is not empty
ifneq ($(strip $(TOOLCHAIN_PATH)),)
TOOLCHAIN_PATH = $(patsubst %/,%,$(TOOLCHAIN_PATH))/
PKG_CONFIG = $(TOOLCHAIN_PATH)/pkg-config
endif

# setup the toolchain
# ether set the TOOLCHAIN_PATH and TOOLCHAIN_PREFIX variable or 
# set the C_COMPILER, CXX_COMPILER, AR_BIN, LD_BIN, STRIP_BIN, PKG_CONFIG_BIN variables separately
# setup the toolchain
# ether set the TOOLCHAIN_PATH and TOOLCHAIN_PREFIX variable or 
# set the C_COMPILER, CXX_COMPILER, AR_BIN, LD_BIN, STRIP_BIN, PKG_CONFIG_BIN variables separately
ifneq ($(strip $(TOOLCHAIN_PATH))$(strip $(TOOLCHAIN_PREFIX)),)
CC	=	$(strip $(TOOLCHAIN_PATH))$(strip $(TOOLCHAIN_PREFIX))gcc
CXX	=	$(strip $(TOOLCHAIN_PATH))$(strip $(TOOLCHAIN_PREFIX))g++
AR	=	$(strip $(TOOLCHAIN_PATH))$(strip $(TOOLCHAIN_PREFIX))ar
LD	=	$(strip $(TOOLCHAIN_PATH))$(strip $(TOOLCHAIN_PREFIX))ld
STRIP = $(strip $(TOOLCHAIN_PATH))$(strip $(TOOLCHAIN_PREFIX))strip
else
CC	=	$(C_COMPILER)
CXX	=	$(CXX_COMPILER)
AR	=	$(AR_BIN)
LD	=	$(LD_BIN)
STRIP	=	$(STRIP_BIN)
PKG_CONFIG = $(PKG_CONFIG_BIN)
endif

# check if pkg-config is available
ifeq ($(strip $(PKG_CONFIG)),)
$(warning PKG_CONFIG variable is not set)
endif

export	TOOLCHAIN_PATH
export	TOOLCHAIN_PREFIX
export	CC
export	CXX
export	AR
export	LD
export	STRIP
export	PKG_CONFIG

# feature flags
# whether to exclude demos and examples from the build
EXCLUDE_DEMOS_AND_EXAMPLES	?=	1

# directories
LVGL_DIR_NAME	?=	lvgl
LVGL_DIR	?=	${shell pwd}
SRC_DIR	=	$(abspath $(LVGL_DIR)/src)
LIBS_DIRNAME =	libs
LIBS_DIR	=	$(abspath $(LVGL_DIR)/$(LIBS_DIRNAME))
BUILD_DIR	=	$(abspath $(LVGL_DIR)/build)
BUILD_OBJ_DIR	=	$(abspath $(BUILD_DIR)/obj)
BUILD_BIN_DIR	=	$(abspath $(BUILD_DIR)/bin)
TARGET_SHARED_LIBS_DIR	=	$(abspath $(BUILD_BIN_DIR)/libs)

export LIBS_DIRNAME
export BUILD_BIN_DIR
export TARGET_SHARED_LIBS_DIR


# distribution directory
SYSROOT	=	$(SYSROOT_DIR)
export SYSROOT

# output binary name
BIN	?=	app
export BIN

# start.sh configs
START_SCRIPT_FILENAME	?=	start.sh
WORK_DIR	?=	$${SCRIPT_PATH}

export START_SCRIPT_FILENAME
export WORK_DIR


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


# add your own include paths here
INCLUDE_PATHS += -I$(LVGL_DIR) -I$(SRC_DIR) -I$(LIBS_DIR)
EXTRA_INCLUDE_PATHS = $(EXTRA_INCLUDE_PATHS)
# if you set the PKG_CONFIG variable correctly, 
# you can use pkg-config to find the include paths like below(take glib-2.0 as an example):
# INCLUDE_PATHS += $(shell $(PKG_CONFIG) --cflags glib-2.0)
#INCLUDE_PATHS += $(shell $(PKG_CONFIG) --cflags glib-2.0)

# $(info include paths: $(INCLUDE_PATHS))
EXTRA_CFLAGS    =   $(EXTRA_CFLAGS)
# compiler flags
CFLAGS	+=	-O3 -g0 \
			$(WARNINGS) \
			$(INCLUDE_PATHS) \
			$(EXTRA_INCLUDE_PATHS) \
			$(EXTRA_CFLAGS) \
			$(if $(SYSROOT),--sysroot=$(SYSROOT),)


# add your own library paths here
LIB_PATHS += -L$(LIBS_DIR)
EXTRA_LIB_PATHS = $(EXTRA_LIB_PATHS)

# if you set the PKG_CONFIG variable correctly, 
# you can use pkg-config to find the library paths like below(take glib-2.0 as an example):
#LIB_PATHS += $(shell $(PKG_CONFIG) --libs-only-L glib-2.0)

# $(info library paths: $(LIB_PATHS))

# add your own libraries be linked here
LIB_LINKED += -lm
EXTRA_LIB_LINKED = $(EXTRA_LIB_LINKED)
LIB_LINKED	+=	-L$(LIBS_DIR)/mylib -lmylib

# if you set the PKG_CONFIG variable correctly, 
# you can use pkg-config to find the libraries like this(take glib-2.0 as an example):
#LIB_LINKED += $(shell $(PKG_CONFIG) --libs-only-l glib-2.0)

# $(info libraries to be linked: $(LIB_LINKED))

# linker flags
EXTRA_LDFLAGS	=	$(EXTRA_LDFLAGS)
LDFLAGS	+=	$(LIB_PATHS) \
            $(EXTRA_LIB_PATHS) \
            $(LIB_LINKED) \
            $(EXTRA_LIB_LINKED) \
            $(EXTRA_LDFLAGS) \
			$(if $(SYSROOT),--sysroot=$(SYSROOT),)

# libraries under $(LIBS_DIR)
LIBRARIES	:=	$(wildcard $(LIBS_DIR)/*)

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


all: libs app startup

# build application binary only
app: $(BUILD_BIN_DIR)/$(BIN) startup

# build libraries in $(LIBS_DIR) only
libs: $(TARGET_SHARED_LIBS_DIR)


# rules to build libraries
$(TARGET_SHARED_LIBS_DIR): $(LIBRARIES)
	@echo "Building libraries..."
	@mkdir -p $@
	$(MAKE) -C $(LIBS_DIR)
	@touch $@


# rules to build application binary
$(BUILD_OBJ_DIR)/%.o: %.c
	@if [ "$(CC)" = "" ]; then \
		echo "Please specify C compiler using C_COMPILER variable"; \
		exit 1; \
	fi
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "CC $<"

$(BUILD_OBJ_DIR)/%.o: %.cpp
	@if [ "$(CXX)" = "" ]; then \
		echo "Please specify C++ compiler using CXX_COMPILER variable"; \
		exit 1; \
	fi
	@mkdir -p $(dir $@)
	@$(CXX) $(CFLAGS) -c $< -o $@
	@echo "CXX $<"

$(BUILD_OBJ_DIR)/%.o: %.S
	@if [ "$(CC)" = "" ]; then \
		echo "Please specify C compiler using C_COMPILER variable"; \
		exit 1; \
	fi
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "AS $<"

# link
$(BUILD_BIN_DIR)/$(BIN): $(OBJS) | $(BUILD_LIBS_DIR)
	@if [ "$(CC)" = "" ]; then \
		echo "Please specify C compiler using C_COMPILER variable"; \
		exit 1; \
	fi
	@mkdir -p $(BUILD_BIN_DIR)
	$(CC) -o $@ $(OBJS) $(LDFLAGS)
	@echo "Build completed. Output binary: $(BUILD_BIN_DIR)/$(BIN)"


startup:
	@mkdir -p $(BUILD_BIN_DIR)
	@rm -f $(BUILD_BIN_DIR)/$(START_SCRIPT_FILENAME)
	@chmod +x ${LVGL_DIR}/tools/startup_gen.py
	@${LVGL_DIR}/tools/startup_gen.py


new:
	@chmod +x ${LVGL_DIR}/tools/project_maker.py
	@${LVGL_DIR}/tools/project_maker.py

new-gui:
	@chmod +x ${LVGL_DIR}/tools/project_maker_gui.py
	@${LVGL_DIR}/tools/project_maker_gui.py


# clean targets
clean: clean-app clean-libs clean-all

clean-app:
	@echo "Cleaning app build artifacts..."
	@rm -rf $(BUILD_OBJ_DIR) $(BUILD_BIN_DIR)/$(BIN)
	@rm -rf $(BUILD_BIN_DIR)/$(START_SCRIPT_FILENAME)

clean-libs:
	@echo "Cleaning libs build artifacts..."
	@$(MAKE) -C $(LIBS_DIR) clean
	@rm -rf $(TARGET_SHARED_LIBS_DIR)

clean-all: clean-app clean-libs
	@rm -rf $(BUILD_BIN_DIR)
	@rm -rf $(BUILD_OBJ_DIR)

.PHONY: all app libs startup new new-gui clean clean-app clean-libs clean-all
