#!/usr/bin/env python3

"""
This script is used to create a new project based on  the current Hello_lvgl_v8 template in an interactive manner.
"""

import os
import subprocess


def abs_join(path, *paths):
    return os.path.abspath(os.path.join(path, *paths))


def check_rsync_available():
    """Check if rsync is available on the system."""
    try:
        subprocess.run(["rsync", "--version"], capture_output=True, check=True)
        return True
    except Exception as e:
        print("exception occurred: {0}".format(e))
        return False


def copy_with_rsync(source_dir, dest_dir, exclude_dirs, exclude_files, progress=False):
    if not source_dir.endswith("/"):
        source_dir = source_dir + "/"

    os.makedirs(os.path.dirname(os.path.abspath(dest_dir)), exist_ok=True)

    cmd = ["rsync", "-av"]
    if progress:
        cmd.append("--progress")
    else:
        cmd.append("--quiet")

    for exclude_dir in exclude_dirs:
        cmd.extend(["--exclude", exclude_dir])

    for exclude_file in exclude_files:
        cmd.extend(["--exclude", exclude_file])

    cmd.extend([source_dir, dest_dir])

    try:
        subprocess.run(cmd, check=True, text=True)
        return True
    except Exception as e:
        print("exception occurred: {0}".format(e))
        return False


TEMPLATE_DIR = abs_join(os.path.dirname(__file__), "..")
EXCLUDE_DIRS = (
    ".idea/",
    ".vscode/",
    ".git/",
    "build/",
)
EXCLUDE_FIELS = ".vscode-ctags", "build.sh"


class ProjectConfig(object):

    def __init__(self):
        self.project_basedir = os.path.expanduser("~")
        self.project_name = ""
        self.bin_name = "app"
        self.exclude_lvgl_demos_and_examples = 1
        self.start_script_filename = "start.sh"
        self.work_dir = r"$${SCRIPT_PATH}"
        self.add_mylib_demo = 0
        self.toolchain_prefix = "$(TOOLCHAIN_PREFIX)"
        self.cc_path = "$(C_COMPILER)"
        self.cpp_path = "$(CXX_COMPILER)"
        self.ld_path = "$(LD_BIN)"
        self.ar_path = "$(AR_BIN)"
        self.strip_path = "$(STRIP_BIN)"
        self.sysroot_path = "$(SYSROOT_DIR)"

    def get_project_path(self):
        return abs_join(self.project_basedir, self.project_name)


def fix_exclude_lvgl_demos_and_examples_var(content, config):
    return content.replace(
        "EXCLUDE_DEMOS_AND_EXAMPLES	=	1",
        "EXCLUDE_DEMOS_AND_EXAMPLES	=	{0}".format(
            int(bool(config.exclude_lvgl_demos_and_examples))
        ),
    )


def fix_sysroot_var(content, config):
    return content.replace(
        "SYSROOT	:=	$(SYSROOT_DIR)",
        "SYSROOT	:=	{0}".format(config.sysroot_path),
    )


def fix_bin_var(content, config):
    return content.replace(
        "BIN	=	app",
        "BIN	=	{0}".format(config.bin_name),
    )


def fix_toolchain_var(content, config):
    return content.replace(
        "TOOLCHAIN_PREFIX	:=	$(TOOLCHAIN_PREFIX)",
        "TOOLCHAIN_PREFIX	:=	{0}".format(config.toolchain_prefix),
    )


def fix_toolchain_bin_vars(content, config):
    return (
        content.replace(
            "CC	=	$(C_COMPILER)",
            "CC	=	{0}".format(config.cc_path),
        )
        .replace(
            "CXX	=	$(CXX_COMPILER)",
            "CXX	=	{0}".format(config.cpp_path),
        )
        .replace(
            "AR	=	$(AR_BIN)",
            "AR	=	{0}".format(config.ar_path),
        )
        .replace(
            "LD	=	$(LD_BIN)",
            "LD	=	{0}".format(config.ld_path),
        )
        .replace(
            "STRIP	=	$(STRIP_BIN)",
            "STRIP	=	{0}".format(config.strip_path),
        )
    )


def fix_start_script_var(content, config):
    return content.replace(
        "START_SCRIPT_FILENAME	=	start.sh",
        "START_SCRIPT_FILENAME	=	{0}".format(config.start_script_filename),
    )


def fix_work_dir_var(content, config):
    return content.replace(
        r"WORK_DIR	=	$${SCRIPT_PATH}",
        "WORK_DIR	=	'{0}'".format(config.work_dir),
    )


def fix_mylib_demo_var(content, config):
    if not config.add_mylib_demo:
        return content.replace(
            "LDFLAGS	+=	-L$(LIBS_DIR)/mylib -lmylib",
            "#LDFLAGS	+=	-L$(LIBS_DIR)/mylib -lmylib",
        )
    return content


def check_project_path(config):
    project_path = config.get_project_path()
    if os.path.commonprefix([project_path, TEMPLATE_DIR]) == TEMPLATE_DIR:
        print(
            "error: project directory cannot be inside the template directory: {0}".format(
                project_path
            )
        )
        exit(1)
    if os.path.isdir(project_path) and os.listdir(project_path):
        print(
            "error: project directory already exists and is not empty: {0}".format(
                project_path
            )
        )
        exit(1)


def copy_template_to_project_dir(config, exclude_dirs, exclude_files):
    # check if project directory is in the template directory
    check_project_path(config)
    if not os.path.isdir(config.get_project_path()):
        print("creating project directory: {0}".format(config.get_project_path()))
        os.makedirs(config.get_project_path(), exist_ok=True)

    print("Copying template to project directory...")
    if not check_rsync_available():
        print("rsync not available on your system, please install it.")
        exit(1)

    if not copy_with_rsync(
        TEMPLATE_DIR,
        config.get_project_path(),
        exclude_dirs,
        exclude_files,
    ):
        print("error: failed to copy template to project directory")
        exit(1)


def fix_makefile(config):
    print("Fixing Makefile...")
    makefile_path = abs_join(config.get_project_path(), "Makefile")
    if not os.path.isfile(makefile_path):
        print(
            "error: Makefile not found in project directory: {0}".format(makefile_path)
        )
        exit(1)

    with open(makefile_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = fix_exclude_lvgl_demos_and_examples_var(content, config)
    content = fix_sysroot_var(content, config)
    content = fix_bin_var(content, config)
    content = fix_toolchain_var(content, config)
    content = fix_toolchain_bin_vars(content, config)
    content = fix_start_script_var(content, config)
    content = fix_work_dir_var(content, config)
    content = fix_mylib_demo_var(content, config)

    with open(makefile_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Makefile fixed!")


def fix_mylib_demo_src(config):
    if config.add_mylib_demo:
        return
    print("Fixing src/app.c...")
    src_path = abs_join(config.get_project_path(), "src/app.c")
    if not os.path.isfile(src_path):
        print("error: app.c not found in project directory: {0}".format(src_path))
        exit(1)

    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = (
        content.replace(
            '#include "libs/mylib/mylib.h"', '//#include "libs/mylib/mylib.h"'
        )
        .replace("mylib_init();", "//mylib_init();")
        .replace(
            r'printf("call mylib_add(2, 3) = %d\n", mylib_add(2, 3)',
            r'//printf("call mylib_add(2, 3) = %d\n", mylib_add(2, 3)',
        )
    )
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("src/app.c fixed!")


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
