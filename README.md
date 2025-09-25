# LVGL for frame buffer device

LVGL configured to work with `/dev/fb0` and `/dev/input/event0` on Linux.

This project needs the following dependencies:

- lvgl v8.4
- lv_drivers

Please put the `lvgl` and `lv_drivers`  of the corresponding version (you can download/clone them from the official repositories)
in the root directory of the project.

Please change the path to the compiler and linker in the Makefile according to your system.

The source code will be in the `src` directory by default. The `src/main.c` will be the entry point of the program.

The output binary will be in the `build/bin` and `dist/`  directories by default.

All object files will be in the `build/obj` directory by default.


To speed up the build process, `examples` and `demos` contained in the `lvgl` library will be excluded from the compilation
by default. If you want to include them, please set the `EXCLUDE_DEMOS_AND_EXAMPLES` variable to `0` in the `Makefile` and
turn on the corresponding options in the `lv_conf.h` file, such as `LV_BUILD_EXAMPLES`, `LV_USE_DEMO_WIDGETS`, etc.

To build the project, run:

```
make
```

To clean the project, run:

```
make clean
```

Note: this project is made for a rk3506(a arm soc with 3 * A7 cores and 1 * M0 mcu) with a 480x800 LCD screen with a touch panel.
It should also work on other framebuffer-based linux system, but you may need to modify some configurations in the `lv_conf.h`, `lv_drv_conf.h` and `src/main.c`.