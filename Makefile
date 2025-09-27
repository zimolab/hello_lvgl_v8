#
# Makefile
#

# toolchains, please change to your own toolchains
CC	=	$(C_COMPILER)
CXX	=	$(CXX_COMPILER)
AR	=	$(AR_BIN)
LD	=	$(LD_BIN)
STRIP = $(STRIP_BIN)

export CC
export CXX
export AR
export LD
export STRIP

# feature flags
# whether to exclude demos and examples from the build
EXCLUDE_DEMOS_AND_EXAMPLES = 1

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
SYSROOT	= $(SYSROOT_DIR)
ifeq ($(SYSROOT),)
$(warning SYSROOT_DIR is not set, additional libraries and headers may not be found)
else
SYSROOT = $(abspath $(SYSROOT))
endif
SYSROOT_LIB	=	$(if $(SYSROOT),$(SYSROOT)/lib)
SYSROOT_INC	=	$(if $(SYSROOT),$(SYSROOT)/include)
SYSROOT_USR_LIB	=	$(if $(SYSROOT),$(SYSROOT)/usr/lib)
SYSROOT_USR_INC	=	$(if $(SYSROOT),$(SYSROOT)/usr/include)


export SYSROOT
export SYSROOT_LIB
export SYSROOT_INC
export SYSROOT_USR_LIB
export SYSROOT_USR_INC


# output binary name
BIN = app
export BIN

# start.sh configs
START_SCRIPT_FILENAME	=	start.sh
WORK_DIR	=	"~"

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

# compiler flags
CFLAGS	?=	-O3 -g0 \
			-I$(LVGL_DIR)/ -I$(SRC_DIR) \
			$(WARNINGS)

CFLAGS += $(if $(SYSROOT_INC),-I$(SYSROOT_INC))
CFLAGS += $(if $(SYSROOT_USR_INC),-I$(SYSROOT_USR_INC))
CFLAGS += -I$(LIBS_DIR)

# linker flags
LDFLAGS	?=	-L$(LIBS_DIR)
LDFLAGS += $(if $(SYSROOT_LIB),-L$(SYSROOT_LIB))
LDFLAGS += $(if $(SYSROOT_USR_LIB),-L$(SYSROOT_USR_LIB))

LDFLAGS	+=	-lm

# show how to use third-party libraries
LDFLAGS += -L$(LIBS_DIR)/mylib -lmylib

LIBRARIES := $(wildcard $(LIBS_DIR)/*)

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

# Build both libs and app
app: $(BUILD_BIN_DIR)/$(BIN) startup

# Build only libraries
libs: $(TARGET_SHARED_LIBS_DIR)


# Rule to build libraries
$(TARGET_SHARED_LIBS_DIR): $(LIBRARIES)
	@echo "Building libraries..."
	@mkdir -p $@
	$(MAKE) -C $(LIBS_DIR)
	@touch $@


# Compilation rules
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

# Link application
$(BUILD_BIN_DIR)/$(BIN): $(OBJS) | $(BUILD_LIBS_DIR)
	@if [ "$(CC)" = "" ]; then \
		echo "Please specify C compiler using C_COMPILER variable"; \
		exit 1; \
	fi
	@mkdir -p $(BUILD_BIN_DIR)
	@$(CC) -o $@ $(OBJS) $(LDFLAGS) -Wl,-rpath,'$$ORIGIN'
	@echo "Build completed. Output binary: $(BUILD_BIN_DIR)/$(BIN)"


startup:
	@mkdir -p $(BUILD_BIN_DIR)
	@rm -f $(BUILD_BIN_DIR)/$(START_SCRIPT_FILENAME)
	@chmod +x ${LVGL_DIR}/tools/startup_gen.py
	@${LVGL_DIR}/tools/startup_gen.py


# Clean targets
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

.PHONY: all app libs startup clean clean-app clean-libs clean-all
