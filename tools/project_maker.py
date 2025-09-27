#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from project_maker_base import *


def prompt(msg, default):
    print("{0} [{1}]: ".format(msg, default), end="")
    value = str(input())
    if not value:
        return default
    return value


def make_project():

    exclude_dirs = [*EXCLUDE_DIRS]
    exclude_files = [*EXCLUDE_FIELS]

    config = ProjectConfig()
    config.project_name = ""
    config.project_basedir = os.path.expanduser("~")

    print("Welcome to the lvgl v8 project maker! Let's create a new project.")
    print("Please enter the following information:")
    config.project_name = prompt("Project name", config.project_name).strip()
    if not config.project_name:
        print("error: project name cannot be empty")
        exit(1)
    config.project_basedir = prompt(
        "Project base directory", config.project_basedir
    ).strip()
    if not config.project_basedir:
        print("error: project base directory cannot be empty")
        exit(1)

    check_project_path(config)

    config.bin_name = prompt(
        "Output binary executable name ", default=config.bin_name
    ).strip()
    if not config.bin_name:
        print("error: binary executable name cannot be empty")
        exit(1)

    config.work_dir = prompt(
        "Working directory of your application ", default=config.work_dir
    ).strip()

    config.start_script_filename = prompt(
        "Start script filename ", default=config.start_script_filename
    ).strip()
    if not config.start_script_filename:
        print("error: start script filename cannot be empty")
        exit(1)

    choice = prompt(
        "Do you want to exclude lvgl demos and examples (1. yes, 0. no)",
        default=str(config.exclude_lvgl_demos_and_examples),
    ).strip()
    choice = int(choice)
    if choice == 0:
        config.exclude_lvgl_demos_and_examples = 0
    else:
        config.exclude_lvgl_demos_and_examples = 1

    choice = prompt(
        "What way do you want to specify the toolchain?(1. specify prefix, 2. specify paths separately)",
        default="1",
    ).strip()
    if choice == "1":
        config.toolchain_prefix = prompt(
            "Toolchain prefix(please input the full path, e.g. /path/to/toolchain/arm-none-eabi-) ",
            default="",
        ).strip()
        if not config.toolchain_prefix:
            print(
                "warning: toolchain prefix not specified, something may go wrong during compilation"
            )
    else:
        config.cc_path = prompt(
            "C compiler(e.g. /path/to/toolchain/bin/arm-none-eabi-gcc) ",
            default=config.cc_path,
        ).strip()
        if not config.cc_path:
            print(
                "warning: C compiler not specified, something may go wrong during compilation"
            )
        config.cpp_path = prompt(
            "C++ compiler(e.g. /path/to/toolchain/bin/arm-none-eabi-g++) ",
            default=config.cpp_path,
        ).strip()
        if not config.cpp_path:
            print(
                "warning: C++ compiler not specified, something may go wrong during compilation"
            )
        config.ld_path = prompt(
            "Linker(e.g. /path/to/toolchain/bin/arm-none-eabi-ld) ",
            default=config.ld_path,
        ).strip()
        if not config.ld_path:
            print("warning: linker not specified")
        config.ar_path = prompt(
            "Archiver(e.g. /path/to/toolchain/bin/arm-none-eabi-ar)",
            default=config.ar_path,
        ).strip()
        if not config.ar_path:
            print("warning: archiver not specified")
        config.strip_path = prompt(
            "Stripper(e.g. /path/to/toolchain/bin/arm-none-eabi-strip)",
            default=config.strip_path,
        ).strip()
        if not config.strip_path:
            print("warning: stripper not specified")
    choice = prompt(
        "Enable mylib demo which demonstrates how to integrate a custom library into your project (1. yes, 0. no)",
        default=str(config.add_mylib_demo),
    ).strip()
    choice = int(choice)
    if choice == 1:
        config.add_mylib_demo = 1
        print(
            "check libs/mylib/Makefile to understand how to integrate thirdparty library into your project"
        )
    else:
        config.add_mylib_demo = 0
        exclude_dirs.append("libs/mylib/")
    config.sysroot_path = prompt(
        "Target sysroot path(normally used in cross-compiling)",
        default=config.sysroot_path,
    ).strip()

    copy_template_to_project_dir(config, exclude_dirs, exclude_files)
    fix_makefile(config)
    fix_mylib_demo_src(config)
    print("Project created successfully!")
    print("Your project directory is: {0}".format(config.get_project_path()))


if __name__ == "__main__":
    make_project()
