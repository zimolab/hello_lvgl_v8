//
// Created by zimolab on 2025/9/25.
//

#include "../lvgl/lvgl.h"

#include "app.h"

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

/**
 * @brief 取随即颜色
 */
inline static lv_color_t random_color()
{
    srand((unsigned int)time(NULL));
    uint32_t color_value = ((uint32_t)rand()) % 0xffffff; // 生成随机颜色值
    return lv_color_hex(color_value);                     // 使用十六进制颜色值
}

/**
 * @brief 按钮事件回调函数
 * @param e 事件指针
 */
static void btn_event_cb(lv_event_t * e)
{
    lv_event_code_t event_code = lv_event_get_code(e);   // 获取事件代码
    lv_obj_t * target          = lv_event_get_target(e); // 获取触发事件的对象
    static int count           = 0;                      // 计数器

    if(event_code == LV_EVENT_CLICKED) {
        /* 当按钮被点击时，改变标签的文本 */
        lv_obj_t * label = (lv_obj_t *)lv_event_get_user_data(e); // 获取用户数据（标签指针）
        char * msg       = malloc(100);
        sprintf(msg, "Hello LVGL! %d", count++);
        lv_label_set_text(label, msg);
        /* 可以添加其他效果，比如改变按钮颜色 */
        lv_obj_set_style_bg_color(target, random_color(), LV_STATE_DEFAULT); // 使用随机颜色
        free(msg);
    }
}

/**
 * @brief 创建Hello World界面
 */
void create_hello_world_ui(void)
{
    /* 获取当前活动屏幕 */
    lv_obj_t * scr = lv_scr_act();

    /* 1. 创建一个按钮 */
    lv_obj_t * btn = lv_btn_create(scr);       // 在屏幕上创建一个按钮
    lv_obj_set_size(btn, 150, 150);            // 设置按钮大小（宽度150像素，高度150像素）
    lv_obj_align(btn, LV_ALIGN_CENTER, 0, 30); // 将按钮在屏幕上居中对齐，并向下偏移30像素

    /* 2. 为按钮添加标签（初始文本） */
    lv_obj_t * label_btn = lv_label_create(btn);
    lv_label_set_text(label_btn, "Click Me!");
    lv_obj_center(label_btn); // 将标签在按钮内居中对齐

    /* 3. 创建一个用于显示信息的标签 */
    lv_obj_t * label_info = lv_label_create(scr);
    lv_label_set_text(label_info, "Welcome to LVGL!");
    lv_obj_align(label_info, LV_ALIGN_CENTER, 0, -105);               // 在屏幕居中位置向上偏移105像素
    lv_obj_set_style_text_align(label_info, LV_TEXT_ALIGN_CENTER, 0); // 设置文本居中对齐

    /* 4. 为按钮添加事件回调函数，并将信息标签作为用户数据传入 */
    lv_obj_add_event_cb(btn, btn_event_cb, LV_EVENT_CLICKED,
                        label_info); // 为按钮的点击事件添加回调函数
}
