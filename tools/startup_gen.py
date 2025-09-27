#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime


def _env(name, default=None):
    return os.environ.get(name, default)


TEMPLATE = os.path.join(os.path.dirname(__file__), "statrup.sh.tpl")

START_SCRIPT_FILENAME = _env("START_SCRIPT_FILENAME", "startup.sh")
BUILD_BIN_DIR = _env("BUILD_BIN_DIR")

GEN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
BIN = _env("BIN")
LIBS_DIRNAME = _env("LIBS_DIRNAME", "libs")
WORK_DIR = _env("WORK_DIR", r"${APP_DIR}")


REPLACES = {
    r"#{GEN_TIME}": GEN_TIME,
    r"#{BIN}": BIN,
    r"#{LIBS_DIRNAME}": LIBS_DIRNAME,
    r"#{WORK_DIR}": WORK_DIR,
}


if __name__ == "__main__":
    print("Genrating startup script file...")

    if not START_SCRIPT_FILENAME:
        print("START_SCRIPT_FILENAME is not set, please set it in environment variable")
        exit(1)

    if not BUILD_BIN_DIR:
        print("BUILD_BIN_DIR is not set, please set it in environment variable")
        exit(1)

    if not os.path.isdir(BUILD_BIN_DIR):
        os.mkdir(BUILD_BIN_DIR)

    if not os.path.isfile(TEMPLATE):
        print("Template file not found: {}".format(TEMPLATE))
        exit(1)

    if not BIN:
        print("BIN is not set, please set it in environment variable")
        exit(1)

    output_file = os.path.join(BUILD_BIN_DIR, START_SCRIPT_FILENAME)
    output_content = ""
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        output_content = f.read()
    for var, value in REPLACES.items():
        output_content = output_content.replace(var, value)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_content)

    print("Startup script file generated successfully")
    subprocess.call(["chmod", "+x", output_file])
