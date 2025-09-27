# LVGL for frame buffer device

LVGL configured to work with `/dev/fb0` and `/dev/input/event0` on Linux.

This project needs the following dependencies:

- lvgl v8.4
- lv_drivers

Please put the `lvgl` and `lv_drivers`  of the corresponding version (you can download/clone them from the official repositories)
in the root directory of the project.

Please change the path to the compiler and linker in the Makefile according to your system.

The source code will be in the `src` directory by default. The `src/main.c` will be the entry point of the program.

The output binary will be in the `build/bin`.

All object files will be in the `build/obj` directory by default.


To speed up the build process, `examples` and `demos` contained in the `lvgl` library will be excluded from the compilation
by default. If you want to include them, please set the `EXCLUDE_DEMOS_AND_EXAMPLES` variable to `0` in the `Makefile` and
turn on the corresponding options in the `lv_conf.h` file, such as `LV_BUILD_EXAMPLES`, `LV_USE_DEMO_WIDGETS`, etc.

To build the project, run:

```bash
make
```

To clean the project, run:

```bash
make clean
```

To build the application only, run:
```bash
make app
```

To build the thirdparty libraries (in `libs` directory) only, run:
```bash
make libs
```

To clean the thirdparty libraries, run:
```bash
make clean-libs
```

To clean the application, run:
```bash
make clean-app
```

Once the project is built, the output binary can be found in the `build/bin` directory. Besides the application binary, a startup script normaly named `start.sh` will be also generated in the `build/bin` directory, which is used to start the application. And a `libs` 
will be created in the `build/bin` directory, which contains the thirdparty libraries(`*.so`).
So a typical directory structure of the `build/bin` directory may look like this:

```text
build/bin
├── app
├── libs
│   ├── libmylib.so
├── start.sh
```

It is recommended to upload the whole `build/bin` directory to the target device and run the `start.sh` to start the application. The `start.sh` will automatically set the environment to run the application.

Note: this project is made for a rk3506(a arm soc with 3 * A7 cores and 1 * M0 mcu) with a 480x800 LCD screen with a touch panel.
It should also work on other framebuffer-based linux system, but you may need to modify some configurations in the `lv_conf.h`, `lv_drv_conf.h` and `src/main.c`.

---

Thirdparty libraries intergration can be done with a simple `Makefile` file. Refer to the `libs/mylib/Makefile` for more information.
