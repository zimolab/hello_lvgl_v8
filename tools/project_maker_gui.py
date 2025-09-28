#!/usr/bin/env python3

"""
This script is used to create a new project based on the current Hello_lvgl_v8 template in an interactive manner.
GUI version using ttk.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

from project_maker_base import *


class LVGLProjectCreatorGUI:
    def __init__(self, root):

        self.notebook = None
        self.log_text = None
        self.strip_entry = None
        self.ar_entry = None
        self.ld_entry = None
        self.cpp_entry = None
        self.cc_entry = None
        self.separate_frame = None
        self.toolchain_path_entry = None
        self.toolchain_prefix_entry = None
        self.prefix_frame = None
        self.sysroot_entry = None
        self.start_script_entry = None
        self.work_dir_entry = None
        self.bin_name_entry = None
        self.project_basedir_entry = None
        self.project_name_entry = None

        self.root = root
        self.root.title("LVGL v8 Project Creator")
        self.root.geometry("800x700")

        self.init_config = ProjectConfig()
        self.cur_config = ProjectConfig()

        self.project_name_var = tk.StringVar(value=self.init_config.project_name)
        self.project_basedir_var = tk.StringVar(value=self.init_config.project_basedir)
        self.bin_name_var = tk.StringVar(value=self.init_config.bin_name)
        self.work_dir_var = tk.StringVar(value=self.init_config.work_dir)
        self.start_script_var = tk.StringVar(
            value=self.init_config.start_script_filename
        )
        self.exclude_demos_var = tk.IntVar(
            value=self.init_config.exclude_lvgl_demos_and_examples
        )
        self.add_mylib_var = tk.IntVar(value=self.init_config.add_mylib_demo)
        self.sysroot_var = tk.StringVar(value=self.init_config.sysroot_path)
        self.toolchain_method_var = tk.StringVar(value="prefix")
        self.toolchain_path_var = tk.StringVar(value=self.init_config.toolchain_path)
        self.toolchain_prefix_var = tk.StringVar(
            value=self.init_config.toolchain_prefix
        )
        self.cc_path_var = tk.StringVar(value=self.init_config.cc_path)
        self.cpp_path_var = tk.StringVar(value=self.init_config.cpp_path)
        self.ld_path_var = tk.StringVar(value=self.init_config.ld_path)
        self.ar_path_var = tk.StringVar(value=self.init_config.ar_path)
        self.strip_path_var = tk.StringVar(value=self.init_config.strip_path)

        self.create_widgets()

    # noinspection PyTypeChecker
    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook = notebook

        # Basic settings tab
        basic_frame = ttk.Frame(notebook, padding=10)
        notebook.add(basic_frame, text="Basic Settings")

        # Project name
        ttk.Label(basic_frame, text="Project Name:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.project_name_entry = ttk.Entry(
            basic_frame, textvariable=self.project_name_var, width=50
        )
        self.project_name_entry.grid(
            row=0, column=1, columnspan=2, sticky=tk.W + tk.E, pady=5
        )

        # Project base directory
        ttk.Label(basic_frame, text="Project Base Directory:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.project_basedir_entry = ttk.Entry(
            basic_frame, textvariable=self.project_basedir_var, width=50
        )
        self.project_basedir_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=5)
        ttk.Button(
            basic_frame, text="Browse", command=self.browse_project_directory
        ).grid(row=1, column=2, padx=5, pady=5)

        # Binary name
        ttk.Label(basic_frame, text="Output Binary Name:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.bin_name_entry = ttk.Entry(
            basic_frame, textvariable=self.bin_name_var, width=50
        )
        self.bin_name_entry.grid(
            row=2, column=1, columnspan=2, sticky=tk.W + tk.E, pady=5
        )

        # Working directory
        ttk.Label(basic_frame, text="Working Directory:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.work_dir_entry = ttk.Entry(
            basic_frame, textvariable=self.work_dir_var, width=50
        )
        self.work_dir_entry.grid(
            row=3, column=1, columnspan=2, sticky=tk.W + tk.E, pady=5
        )

        # Start script filename
        ttk.Label(basic_frame, text="Startup Script Filename:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.start_script_entry = ttk.Entry(
            basic_frame, textvariable=self.start_script_var, width=50
        )
        self.start_script_entry.grid(
            row=4, column=1, columnspan=2, sticky=tk.W + tk.E, pady=5
        )

        # Exclude LVGL demos and examples
        ttk.Checkbutton(
            basic_frame,
            text="Exclude LVGL demos and examples",
            variable=self.exclude_demos_var,
        ).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Add mylib demo
        ttk.Checkbutton(
            basic_frame,
            text="Add mylib demo (demonstrates custom library integration)",
            variable=self.add_mylib_var,
        ).grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Sysroot path
        ttk.Label(basic_frame, text="Sysroot Path:").grid(
            row=7, column=0, sticky=tk.W, pady=5
        )
        self.sysroot_entry = ttk.Entry(
            basic_frame, textvariable=self.sysroot_var, width=50
        )
        self.sysroot_entry.grid(row=7, column=1, sticky=tk.W + tk.E, pady=5)
        ttk.Button(
            basic_frame,
            text="Browse",
            command=lambda: self.browse_directory(self.sysroot_var),
        ).grid(row=7, column=2, padx=5, pady=5)

        # Toolchain settings tab
        toolchain_frame = ttk.Frame(notebook, padding=10)
        notebook.add(toolchain_frame, text="Toolchain Settings")

        # Toolchain specification method
        ttk.Label(toolchain_frame, text="Toolchain Specification Method:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        ttk.Radiobutton(
            toolchain_frame,
            text="Specify prefix",
            variable=self.toolchain_method_var,
            value="prefix",
        ).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Radiobutton(
            toolchain_frame,
            text="Specify paths separately",
            variable=self.toolchain_method_var,
            value="separate",
        ).grid(row=2, column=0, sticky=tk.W, pady=2)

        # Toolchain prefix frame
        self.prefix_frame = ttk.LabelFrame(
            toolchain_frame, text="Toolchain Prefix", padding=5
        )
        self.prefix_frame.grid(
            row=3, column=0, columnspan=3, sticky=tk.W + tk.E, pady=5
        )

        # Toolchain prefix
        ttk.Label(self.prefix_frame, text="Prefix:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.toolchain_prefix_entry = ttk.Entry(
            self.prefix_frame, textvariable=self.toolchain_prefix_var, width=50
        ).grid(row=0, column=1, sticky=tk.W + tk.E, pady=2)

        # Toolchain path
        ttk.Label(self.prefix_frame, text="Path:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.toolchain_path_entry = ttk.Entry(
            self.prefix_frame, textvariable=self.toolchain_path_var, width=50
        ).grid(row=1, column=1, sticky=tk.W + tk.E, pady=2)
        ttk.Button(
            self.prefix_frame,
            text="Browse",
            command=lambda: self.browse_file_or_directory(
                self.toolchain_path_var,
                title="Select Toolchain Directory",
                filetypes=[],
            ),
        ).grid(row=1, column=2, padx=5, pady=2)

        # Separate paths frame
        self.separate_frame = ttk.LabelFrame(
            toolchain_frame, text="Toolchain Paths", padding=5
        )
        self.separate_frame.grid(
            row=4, column=0, columnspan=3, sticky=tk.W + tk.E, pady=5
        )

        # C Compiler
        ttk.Label(self.separate_frame, text="C Compiler:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )

        self.cc_entry = ttk.Entry(
            self.separate_frame, textvariable=self.cc_path_var, width=50
        )
        self.cc_entry.grid(row=0, column=1, sticky=tk.W + tk.E, pady=2)
        ttk.Button(
            self.separate_frame,
            text="Browse",
            command=lambda: self.browse_file(
                self.cc_path_var,
                title="Select C Compiler",
                filetypes=[("Executable files", "*"), ("All files", "*.*")],
            ),
        ).grid(row=0, column=2, padx=5, pady=2)

        # C++ Compiler
        ttk.Label(self.separate_frame, text="C++ Compiler:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.cpp_entry = ttk.Entry(
            self.separate_frame, textvariable=self.cpp_path_var, width=50
        )
        self.cpp_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=2)
        ttk.Button(
            self.separate_frame,
            text="Browse",
            command=lambda: self.browse_file(
                self.cpp_path_var,
                title="Select C++ Compiler",
                filetypes=[("Executable files", "*"), ("All files", "*.*")],
            ),
        ).grid(row=1, column=2, padx=5, pady=2)

        # Linker
        ttk.Label(self.separate_frame, text="Linker:").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.ld_entry = ttk.Entry(
            self.separate_frame, textvariable=self.ld_path_var, width=50
        )
        self.ld_entry.grid(row=2, column=1, sticky=tk.W + tk.E, pady=2)
        ttk.Button(
            self.separate_frame,
            text="Browse",
            command=lambda: self.browse_file(
                self.ld_path_var,
                title="Select Linker",
                filetypes=[("Executable files", "*"), ("All files", "*.*")],
            ),
        ).grid(row=2, column=2, padx=5, pady=2)

        # Archiver
        ttk.Label(self.separate_frame, text="Archiver:").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.ar_entry = ttk.Entry(
            self.separate_frame, textvariable=self.ar_path_var, width=50
        )
        self.ar_entry.grid(row=3, column=1, sticky=tk.W + tk.E, pady=2)
        ttk.Button(
            self.separate_frame,
            text="Browse",
            command=lambda: self.browse_file(
                self.ar_path_var,
                title="Select Archiver",
                filetypes=[("Executable files", "*"), ("All files", "*.*")],
            ),
        ).grid(row=3, column=2, padx=5, pady=2)

        # Stripper
        ttk.Label(self.separate_frame, text="Stripper:").grid(
            row=4, column=0, sticky=tk.W, pady=2
        )
        self.strip_entry = ttk.Entry(
            self.separate_frame, textvariable=self.strip_path_var, width=50
        )
        self.strip_entry.grid(row=4, column=1, sticky=tk.W + tk.E, pady=2)
        ttk.Button(
            self.separate_frame,
            text="Browse",
            command=lambda: self.browse_file(
                self.strip_path_var,
                title="Select Stripper",
                filetypes=[("Executable files", "*"), ("All files", "*.*")],
            ),
        ).grid(row=4, column=2, padx=5, pady=2)

        # Initially show/hide frames based on selection
        self.update_toolchain_frames()
        self.toolchain_method_var.trace("w", self.on_toolchain_method_changed)

        # Log tab
        log_frame = ttk.Frame(notebook, padding=10)
        notebook.add(log_frame, text="Log")

        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame, text="Create Project", command=self.create_project
        ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(
            button_frame, text="Clear Log", command=self.switch_and_reset_log
        ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_form).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(
            side=tk.RIGHT, padx=5
        )

        # Configure grid weights for responsiveness
        basic_frame.columnconfigure(1, weight=1)
        toolchain_frame.columnconfigure(1, weight=1)
        self.prefix_frame.columnconfigure(1, weight=1)
        self.separate_frame.columnconfigure(1, weight=1)

    def on_toolchain_method_changed(self, *args):
        self.update_toolchain_frames()

    def update_toolchain_frames(self):
        if self.toolchain_method_var.get() == "prefix":
            self.prefix_frame.grid()
            self.separate_frame.grid_remove()
        else:
            self.prefix_frame.grid_remove()
            self.separate_frame.grid()

    def browse_project_directory(self):
        directory = filedialog.askdirectory(initialdir=self.project_basedir_var.get())
        if directory:
            self.project_basedir_var.set(directory)

    def browse_directory(self, var):
        """Browse for a directory and set the variable"""
        directory = filedialog.askdirectory(
            initialdir=(
                var.get()
                if var.get() and var.get() != self.init_config.sysroot_path
                else os.path.expanduser("~")
            )
        )
        if directory:
            var.set(directory)

    @staticmethod
    def browse_file(var, title="Select file", filetypes=None):
        """Browse for a file and set the variable"""
        if filetypes is None:
            filetypes = [("All files", "*.*")]

        filename = filedialog.askopenfilename(
            title=title,
            initialdir=(
                os.path.dirname(var.get())
                if var.get() and var.get() != "$(C_COMPILER)"
                else os.path.expanduser("~")
            ),
            filetypes=filetypes,
        )
        if filename:
            var.set(filename)

    def browse_file_or_directory(self, var, title="Select", filetypes=None):
        """Browse for either a file or directory based on user choice"""
        # choice = messagebox.askquestion(
        #     "Select Type",
        #     "Do you want to select a file or a directory? (yes=file, no=directory)",
        #     icon="question",
        #     type=messagebox.YESNOCANCEL,
        # )
        # if choice == messagebox.YES:
        #     self.browse_file(var, title, filetypes)
        # elif choice == messagebox.NO:
        #     self.browse_directory(var)
        self.browse_directory(var)

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def clear_log_text(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def switch_and_reset_log(self):
        self.notebook.select(2)
        self.clear_log_text()
        self.root.update()

    def reset_form(self):
        self.project_name_var.set(self.init_config.project_name)
        self.project_basedir_var.set(self.init_config.project_basedir)
        self.bin_name_var.set(self.init_config.bin_name)
        self.work_dir_var.set(self.init_config.work_dir)
        self.start_script_var.set(self.init_config.start_script_filename)
        self.exclude_demos_var.set(self.init_config.exclude_lvgl_demos_and_examples)
        self.add_mylib_var.set(self.init_config.add_mylib_demo)
        self.sysroot_var.set(self.init_config.sysroot_path)
        self.toolchain_method_var.set("prefix")
        self.toolchain_prefix_var.set(self.init_config.toolchain_prefix)
        self.cc_path_var.set(self.init_config.cc_path)
        self.cpp_path_var.set(self.init_config.cpp_path)
        self.ld_path_var.set(self.init_config.ld_path)
        self.ar_path_var.set(self.init_config.ar_path)
        self.strip_path_var.set(self.init_config.strip_path)
        self.notebook.select(0)
        self.clear_log_text()

    def create_project(self):
        # Validate required fields
        if not self.project_name_var.get().strip():
            messagebox.showerror("Error", "Project name cannot be empty")
            return

        if not self.project_basedir_var.get().strip():
            messagebox.showerror("Error", "Project base directory cannot be empty")
            return

        if not self.bin_name_var.get().strip():
            messagebox.showerror("Error", "Binary executable name cannot be empty")
            return

        if not self.start_script_var.get().strip():
            messagebox.showerror("Error", "Start script filename cannot be empty")
            return

        # Update config from GUI
        self.cur_config.project_name = self.project_name_var.get().strip()
        self.cur_config.project_basedir = self.project_basedir_var.get().strip()
        self.cur_config.bin_name = self.bin_name_var.get().strip()
        self.cur_config.work_dir = self.work_dir_var.get().strip()
        self.cur_config.start_script_filename = self.start_script_var.get().strip()
        self.cur_config.exclude_lvgl_demos_and_examples = self.exclude_demos_var.get()
        self.cur_config.add_mylib_demo = self.add_mylib_var.get()
        self.cur_config.sysroot_path = self.sysroot_var.get().strip()

        # Update toolchain config
        if self.toolchain_method_var.get() == "prefix":
            self.cur_config.toolchain_path = self.toolchain_path_var.get().strip()
            self.cur_config.toolchain_prefix = self.toolchain_prefix_var.get().strip()
        else:
            self.cur_config.cc_path = self.cc_path_var.get().strip()
            self.cur_config.cpp_path = self.cpp_path_var.get().strip()
            self.cur_config.ld_path = self.ld_path_var.get().strip()
            self.cur_config.ar_path = self.ar_path_var.get().strip()
            self.cur_config.strip_path = self.strip_path_var.get().strip()

        # Update exclude directories based on mylib selection
        exclude_dirs = list(EXCLUDE_DIRS)
        if not self.cur_config.add_mylib_demo:
            exclude_dirs.append("libs/mylib/")

        self.switch_and_reset_log()

        self.log_message("Starting project creation...")
        self.log_message(
            "Project will be created at: " + self.cur_config.get_project_path()
        )

        # Copy template
        success, message = copy_template_to_project_dir(
            self.cur_config,
            exclude_dirs,
            list(EXCLUDE_FIELS),
            log_callback=self.log_message,
            exit_on_error=False,
        )
        if not success:
            messagebox.showerror("Error", message)
            return

        # Fix Makefile
        success, message = fix_makefile(
            self.cur_config, log_callback=self.log_message, exit_on_error=False
        )
        print("debug1")
        if not success:
            messagebox.showerror("Error", message)
            return

        # Fix mylib demo source if needed
        success, message = fix_mylib_demo_src(
            self.cur_config, log_callback=self.log_message, exit_on_error=False
        )
        if not success:
            messagebox.showerror("Error", message)
            return

        self.log_message("Project created successfully!")
        self.log_message(
            "Your project directory is at: {0}".format(
                self.cur_config.get_project_path()
            )
        )

        messagebox.showinfo(
            "Success",
            "Project created successfully!\n\nProject location: {0}".format(
                self.cur_config.get_project_path()
            ),
        )


def main():
    root = tk.Tk()
    app = LVGLProjectCreatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
