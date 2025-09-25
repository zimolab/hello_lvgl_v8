# if EXCLUDE_DEMOS_AND_EXAMPLES is not defined, we will exclude demos and examples modules
# which can speed up the build process.
ifneq ($(EXCLUDE_DEMOS_AND_EXAMPLES),1)
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/demos/lv_demos.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/examples/lv_examples.mk
endif
# include the lvgl library modules
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/core/lv_core.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/draw/lv_draw.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/extra/lv_extra.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/font/lv_font.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/hal/lv_hal.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/misc/lv_misc.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/widgets/lv_widgets.mk
# include the lvgl drivers modules
include $(LVGL_DIR)/lv_drivers/lv_drivers.mk