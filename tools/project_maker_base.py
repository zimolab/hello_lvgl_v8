"""
Common parts of project_maker.py and project_maker_gui.py.
"""

import os
import subprocess


def abs_join(path, *paths):
    return os.path.abspath(os.path.join(path, *paths))


TEMPLATE_DIR = abs_join(os.path.dirname(__file__), "..")
EXCLUDE_DIRS = (
    ".idea/",
    ".vscode/",
    ".git/",
    "build/",
)
EXCLUDE_FIELS = ".vscode-ctags", "build.sh"


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


def check_project_path(config, log_callback=print, exit_on_error=True):
    project_path = config.get_project_path()
    if os.path.commonprefix([project_path, TEMPLATE_DIR]) == TEMPLATE_DIR:
        msg = "project directory cannot be inside the template directory: {0}".format(
            project_path
        )
        log_callback("error: {0}".format(msg))
        if exit_on_error:
            exit(1)
        return False, msg
    if os.path.isdir(project_path) and os.listdir(project_path):
        msg = "project directory already exists and is not empty: {0}".format(
            project_path
        )
        log_callback("error: {0}".format(msg))
        if exit_on_error:
            exit(1)
        return False, msg
    return True, ""


def copy_template_to_project_dir(
    config, exclude_dirs, exclude_files, log_callback=print, exit_on_error=True
):
    # check if project directory is in the template directory
    ret, msg = check_project_path(
        config, log_callback=log_callback, exit_on_error=exit_on_error
    )
    if (not exit_on_error) and (not ret):
        return False, msg

    if not os.path.isdir(config.get_project_path()):
        log_callback(
            "Creating project directory: {0}".format(config.get_project_path())
        )
        os.makedirs(config.get_project_path(), exist_ok=True)

    log_callback("Copying template to project directory...")
    if not check_rsync_available():
        msg = "rsync not available on your system, please install it."
        log_callback("error: {0}".format(msg))
        if exit_on_error:
            exit(1)
        return False, msg

    if not copy_with_rsync(
        TEMPLATE_DIR,
        config.get_project_path(),
        exclude_dirs,
        exclude_files,
    ):
        msg = "failed to copy template to project directory"
        log_callback("error: {0}".format(msg))
        if exit_on_error:
            exit(1)
        return False, msg
    return True, ""


def fix_makefile(config, log_callback=print, exit_on_error=True):
    log_callback("Fixing Makefile...")
    makefile_path = abs_join(config.get_project_path(), "Makefile")
    if not os.path.isfile(makefile_path):
        msg = "Makefile not found in project directory: {0}".format(makefile_path)
        log_callback("error: {0}".format(msg))
        if exit_on_error:
            exit(1)
        return False, msg

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

    log_callback("Makefile fixed!")
    return True, ""


def fix_mylib_demo_src(config, log_callback=print, exit_on_error=True):
    if config.add_mylib_demo:
        return True
    log_callback("Fixing src/app.c...")
    src_path = abs_join(config.get_project_path(), "src/app.c")
    if not os.path.isfile(src_path):
        msg = "app.c not found in project directory: {0}".format(src_path)
        log_callback("error: {0}".format(msg))
        if exit_on_error:
            exit(1)
        return False, msg

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
    log_callback("src/app.c fixed!")
    return True, ""
