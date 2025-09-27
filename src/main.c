#include "../lvgl/lvgl.h"
#include "../lv_drivers/display/fbdev.h"
#include "../lv_drivers/indev/evdev.h"

#include "app.h"
#include "libs/mylib/mylib.h"

#include <unistd.h>
#include <pthread.h>
#include <stdio.h>

#include <sys/time.h>

#define SCREEN_WIDTH 480
#define SCREEN_HEIGHT 854
#define DISP_BUF_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT)

int main(void)
{
    // initialize mylib
    mylib_init();

    // invoke function defined in libmylib.so
    printf("call mylib_add(2, 3) = %d\n", mylib_add(2, 3));

    /*LittlevGL init*/
    lv_init();

    /*Linux frame buffer device init*/
    fbdev_init();

    /*A small buffer for LittlevGL to draw the screen's content*/
    static lv_color_t buf[DISP_BUF_SIZE];

    /*Initialize a descriptor for the buffer*/
    static lv_disp_draw_buf_t disp_buf;
    lv_disp_draw_buf_init(&disp_buf, buf, NULL, DISP_BUF_SIZE);

    /*Initialize and register a display driver*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.draw_buf = &disp_buf;
    disp_drv.flush_cb = fbdev_flush;
    disp_drv.hor_res  = SCREEN_WIDTH;
    disp_drv.ver_res  = SCREEN_HEIGHT;
    lv_disp_drv_register(&disp_drv);

    /* Initialize a input device*/
    evdev_init();
    static lv_indev_drv_t indev_drv_1;
    lv_indev_drv_init(&indev_drv_1); /*Basic initialization*/
    indev_drv_1.type = LV_INDEV_TYPE_POINTER;

    /*This function will be called periodically (by the library) to get the mouse position and state*/
    indev_drv_1.read_cb = evdev_read;
    lv_indev_drv_register(&indev_drv_1);

    // run hello world demo
    // you can foud this function in app.c
    create_hello_world_ui();

    /*Handle LitlevGL tasks (tickless mode)*/
    // ReSharper disable once CppDFAEndlessLoop
    while(1) {
        lv_timer_handler();
        usleep(5000);
    }

    return 0;
}

/*Set in lv_conf.h as `LV_TICK_CUSTOM_SYS_TIME_EXPR`*/
#if defined(LV_TICK_CUSTOM) && LV_TICK_CUSTOM
uint32_t custom_tick_get(void)
{
    static uint64_t start_ms = 0;
    if(start_ms == 0) {
        struct timeval tv_start;
        gettimeofday(&tv_start, NULL);
        start_ms = (tv_start.tv_sec * 1000000 + tv_start.tv_usec) / 1000;
    }

    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    const uint64_t now_ms = (tv_now.tv_sec * 1000000 + tv_now.tv_usec) / 1000;

    const uint32_t time_ms = now_ms - start_ms;
    return time_ms;
}
#endif
