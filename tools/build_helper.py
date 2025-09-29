import json
import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, filedialog

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

_MAKE_TARGETS = ["all", "app", "libs", "clean", "clean-app", "clean-libs", "clean-all"]


class ProjectBuilder:
    def __init__(self, root):
        self.output_text = None
        self.command_text = None
        self.make_target_var = None
        self.extra_make_entry = None
        self.ldflags_entry = None
        self.cflags_entry = None
        self.library_var = None
        self.libraries_listbox = None
        self.libpath_var = None
        self.libpaths_listbox = None
        self.include_path_var = None
        self.includes_listbox = None
        self.startup_workdir_entry = None
        self.startup_workdir_var = None
        self.startup_filename_entry = None
        self.startup_filename_var = None
        self.exclude_demos_var = None
        self.output_bin_var = None
        self.workdir_entry = None
        self.workdir_var = None
        self.sysroot_entry = None
        self.sysroot_var = None
        self.toolchain_prefix_var = None
        self.toolchain_path_entry = None
        self.toolchain_path_var = None

        self.root = root
        self.root.title("构建助手")
        self.root.geometry("900x700")

        # 配置数据
        self.config = {
            "TOOLCHAIN_DIR": "",
            "TOOLCHAIN_PRE": "",
            "PKG_CONFIG_BIN": "",
            "EXCLUDE_DEMOS_AND_EXAMPLES": "1",
            "SYSROOT_DIR": "",
            "BIN": "app",
            "START_SCRIPT_FILENAME": "start.sh",
            "WORK_DIR": r"$${SCRIPT_PATH}",
            "EXTRA_INCLUDE_PATHS": [],
            "EXTRA_LIB_PATHS": [],
            "EXTRA_LIB_LINKED": [],
            "EXTRA_CFLAGS": "",
            "EXTRA_LDFLAGS": "",
            "make_extra_args": "",
        }

        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 创建各个配置页面
        self.create_toolchain_tab()
        self.create_project_tab()
        self.create_includes_tab()
        self.create_libraries_tab()
        self.create_flags_tab()
        self.create_build_tab()

        # 加载默认配置
        self.load_default_config()

    def create_toolchain_tab(self):
        """创建工具链配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="工具链")

        # 工具链路径
        ttk.Label(frame, text="工具链路径:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.toolchain_path_var = tk.StringVar(value=self.config["TOOLCHAIN_DIR"])
        self.toolchain_path_entry = ttk.Entry(
            frame, textvariable=self.toolchain_path_var, width=50
        )
        self.toolchain_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(frame, text="浏览", command=self.browse_toolchain_path).grid(
            row=0, column=2, padx=5, pady=5
        )

        # 工具链前缀
        ttk.Label(frame, text="工具链前缀 (例如：arm-none-gnueabihf-):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.toolchain_prefix_var = tk.StringVar(value=self.config["TOOLCHAIN_PRE"])
        ttk.Entry(frame, textvariable=self.toolchain_prefix_var, width=50).grid(
            row=1, column=1, padx=5, pady=5, sticky="we"
        )

        # 系统根目录
        ttk.Label(frame, text="目标系统根路径:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.sysroot_var = tk.StringVar(value=self.config["SYSROOT_DIR"])
        self.sysroot_entry = ttk.Entry(frame, textvariable=self.sysroot_var, width=50)
        self.sysroot_entry.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(frame, text="浏览", command=self.browse_sysroot).grid(
            row=2, column=2, padx=5, pady=5
        )

        frame.columnconfigure(1, weight=1)

    def create_project_tab(self):
        """创建项目配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="项目")

        # 工作目录
        ttk.Label(frame, text="工作目录:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.workdir_var = tk.StringVar(value=os.getcwd())
        self.workdir_entry = ttk.Entry(frame, textvariable=self.workdir_var, width=50)
        self.workdir_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(frame, text="选择目录", command=self.browse_workdir).grid(
            row=0, column=2, padx=5, pady=5
        )

        # 输出文件名
        ttk.Label(frame, text="目标可执行文件名:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.output_bin_var = tk.StringVar(value=self.config["BIN"])
        ttk.Entry(frame, textvariable=self.output_bin_var, width=50).grid(
            row=1, column=1, padx=5, pady=5, sticky="we"
        )

        # 排除示例和演示
        ttk.Label(frame, text="排除lvgl自带的示例:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.exclude_demos_var = tk.StringVar(
            value=self.config["EXCLUDE_DEMOS_AND_EXAMPLES"]
        )
        exclude_frame = ttk.Frame(frame)
        exclude_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(
            exclude_frame, text="是", variable=self.exclude_demos_var, value="1"
        ).pack(side="left")
        ttk.Radiobutton(
            exclude_frame, text="否", variable=self.exclude_demos_var, value="0"
        ).pack(side="left")

        # LVGL目录
        ttk.Label(frame, text="目标可执行文件启动脚本名称:").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.startup_filename_var = tk.StringVar(
            value=self.config["START_SCRIPT_FILENAME"]
        )
        self.startup_filename_entry = ttk.Entry(
            frame, textvariable=self.startup_filename_var, width=50
        )
        self.startup_filename_entry.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(frame, text="目标可执行文件工作目录:").grid(
            row=4, column=0, sticky="w", padx=5, pady=5
        )
        self.startup_workdir_var = tk.StringVar(value=self.config["WORK_DIR"])
        self.startup_workdir_entry = ttk.Entry(
            frame, textvariable=self.startup_workdir_var, width=50
        )
        self.startup_workdir_entry.grid(row=4, column=1, padx=5, pady=5, sticky="we")

        frame.columnconfigure(1, weight=1)

    def create_includes_tab(self):
        """创建头文件路径配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="头文件")

        # 头文件路径列表
        ttk.Label(frame, text="头文件搜索路径:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )

        # 列表框架
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # 头文件路径列表框
        self.includes_listbox = tk.Listbox(list_frame, height=8)
        self.includes_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.includes_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.includes_listbox.config(yscrollcommand=scrollbar.set)

        # 添加/移除按钮
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=5)

        self.include_path_var = tk.StringVar()
        ttk.Entry(button_frame, textvariable=self.include_path_var, width=40).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="添加路径", command=self.add_include_path).pack(
            side="left", padx=5
        )
        ttk.Button(
            button_frame, text="移除选中", command=self.remove_include_path
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="浏览目录", command=self.browse_include_path
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="清除所有", command=self.clear_include_paths
        ).pack(side="left", padx=5)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

    def create_libraries_tab(self):
        """创建库文件配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="库文件")

        # 创建左右两个框架
        left_frame = ttk.LabelFrame(frame, text="库搜索路径")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        right_frame = ttk.LabelFrame(frame, text="链接到目标的库")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 库搜索路径列表
        self.libpaths_listbox = tk.Listbox(left_frame, height=8)
        self.libpaths_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        libpath_buttons = ttk.Frame(left_frame)
        libpath_buttons.pack(fill="x", padx=5, pady=5)

        self.libpath_var = tk.StringVar()
        ttk.Entry(libpath_buttons, textvariable=self.libpath_var).pack(
            side="left", fill="x", expand=True, padx=5
        )
        ttk.Button(libpath_buttons, text="添加", command=self.add_library_path).pack(
            side="left", padx=5
        )
        ttk.Button(libpath_buttons, text="移除", command=self.remove_library_path).pack(
            side="left", padx=5
        )
        ttk.Button(libpath_buttons, text="浏览", command=self.browse_library_path).pack(
            side="left", padx=5
        )

        # 链接库列表
        self.libraries_listbox = tk.Listbox(right_frame, height=8)
        self.libraries_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        library_buttons = ttk.Frame(right_frame)
        library_buttons.pack(fill="x", padx=5, pady=5)

        self.library_var = tk.StringVar()
        ttk.Entry(library_buttons, textvariable=self.library_var).pack(
            side="left", fill="x", expand=True, padx=5
        )
        ttk.Button(library_buttons, text="添加", command=self.add_library).pack(
            side="left", padx=5
        )
        ttk.Button(library_buttons, text="移除", command=self.remove_library).pack(
            side="left", padx=5
        )
        ttk.Button(library_buttons, text="浏览", command=self.browse_library_file).pack(
            side="left", padx=5
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

    def create_flags_tab(self):
        """创建编译标志配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="构建选项")

        # CFLAGS
        ttk.Label(frame, text="额外的CFLAGS:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.cflags_entry = tk.Text(frame, width=60, height=7)
        self.cflags_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # LDFLAGS
        ttk.Label(frame, text="额外LDFLAGS:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.ldflags_entry = tk.Text(frame, width=60, height=7)
        self.ldflags_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # 额外参数
        ttk.Label(frame, text="额外的make参数:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.extra_make_entry = tk.Text(frame, width=60, height=7)
        self.extra_make_entry.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        frame.columnconfigure(1, weight=1)

    def create_build_tab(self):
        """创建构建控制标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="构建")

        # 构建控制框架
        control_frame = ttk.Frame(frame)
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Makefile目标选择
        ttk.Label(control_frame, text="Makefile目标:").pack(side="left", padx=5)
        self.make_target_var = tk.StringVar(value=_MAKE_TARGETS[0])
        target_combo = ttk.Combobox(
            control_frame,
            textvariable=self.make_target_var,
            values=_MAKE_TARGETS,
        )
        target_combo.pack(side="left", padx=5)

        # 按钮框架
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side="left", padx=20)

        ttk.Button(button_frame, text="生成命令", command=self.generate_command).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="构建目标", command=self.execute_build).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="清理所有", command=self.clean_project).pack(
            side="left", padx=5
        )

        # 配置管理按钮
        config_frame = ttk.Frame(control_frame)
        config_frame.pack(side="right", padx=5)

        ttk.Button(config_frame, text="保存配置", command=self.save_config).pack(
            side="left", padx=5
        )
        ttk.Button(config_frame, text="加载配置", command=self.load_config).pack(
            side="left", padx=5
        )

        control_frame.columnconfigure(1, weight=1)

        # 命令预览
        ttk.Label(frame, text="生成的make命令:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.command_text = tk.Text(frame, height=8, width=80)
        self.command_text.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.command_text.yview
        )
        scrollbar.grid(row=2, column=2, sticky="ns")
        self.command_text.config(yscrollcommand=scrollbar.set)

        # 输出区域
        ttk.Label(frame, text="编译输出:").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )

        self.output_text = tk.Text(frame, height=12, width=80, bg="black", fg="white")
        self.output_text.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
        )

        output_scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.output_text.yview
        )
        output_scrollbar.grid(row=4, column=2, sticky="ns")
        self.output_text.config(yscrollcommand=output_scrollbar.set)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(4, weight=1)

    def browse_toolchain_path(self):
        """浏览选择工具链路径"""
        path = filedialog.askdirectory(title="选择工具链目录", parent=self.root)
        if path:
            self.toolchain_path_var.set(path)

    def browse_sysroot(self):
        """浏览选择系统根目录"""
        path = filedialog.askdirectory(title="选择目标系统根目录", parent=self.root)
        if path:
            self.sysroot_var.set(path)

    def browse_workdir(self):
        """浏览选择工作目录"""
        path = filedialog.askdirectory(title="选择工作目录", parent=self.root)
        if path:
            self.workdir_var.set(path)

    def browse_include_path(self):
        """浏览选择头文件路径"""
        path = filedialog.askdirectory(title="选择头文件目录")
        if not path:
            return
        path = Path(path).absolute().as_posix()
        if path in self.config["EXTRA_INCLUDE_PATHS"]:
            tk.messagebox.showwarning(
                "注意", "该路径已添加到列表中！", parent=self.root
            )
            return
        self.config["EXTRA_INCLUDE_PATHS"].append(path)
        self.includes_listbox.insert(tk.END, path)

    def browse_library_path(self):
        """浏览选择库文件路径"""
        path = filedialog.askdirectory(title="选择库文件搜索路径").strip()
        if not path:
            return
        path = Path(path).absolute().as_posix()
        if path in self.config["EXTRA_LIB_PATHS"]:
            tk.messagebox.showwarning(
                "注意", "该路径已添加到列表中！", parent=self.root
            )
            return
        self.config["EXTRA_LIB_PATHS"].append(path)
        self.libpaths_listbox.insert(tk.END, path)

    def browse_library_file(self):
        """浏览选择库文件"""
        path = filedialog.askopenfilename(
            parent=self.root,
            title="选择库文件",
            filetypes=[("静态库", "*.a"), ("动态库", "*.so"), ("全部", "*")],
        ).strip()
        if not path:
            return
        path = Path(path).absolute().as_posix()
        if path in self.config["EXTRA_LIB_LINKED"]:
            tk.messagebox.showwarning(
                "注意", "该链接库已添加到列表中！", parent=self.root
            )
            return
        self.config["EXTRA_LIB_LINKED"].append(path)
        self.libraries_listbox.insert(tk.END, path)

    def add_include_path(self):
        """添加头文件路径"""
        path = self.include_path_var.get().strip()
        if not path:
            tk.messagebox.showwarning("注意", "请填写头文件路径", parent=self.root)
            return
        # path = Path(path).absolute().as_posix()
        if path not in self.config["EXTRA_INCLUDE_PATHS"]:
            self.config["EXTRA_INCLUDE_PATHS"].append(path)
            self.includes_listbox.insert(tk.END, path)
            self.include_path_var.set("")
        else:
            tk.messagebox.showwarning(
                "注意", "该路径已添加到列表中！", parent=self.root
            )
            self.include_path_var.set("")

    def remove_include_path(self):
        """移除选中的头文件路径"""
        selection = self.includes_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning(
                "注意", "请先选择要移除的项目！", parent=self.root
            )
            return
        self.includes_listbox: tk.Listbox
        index = selection[0]
        cur_path = self.includes_listbox.get(index)
        if cur_path in self.config["EXTRA_INCLUDE_PATHS"]:
            self.config["EXTRA_INCLUDE_PATHS"].remove(cur_path)
        self.includes_listbox.delete(index)

    def clear_include_paths(self):
        """清空头文件路径"""
        ret = tk.messagebox.askquestion(
            "确认",
            "确定要清空头文件路径列表吗？",
            parent=self.root,
            icon="warning",
        )
        if ret == "yes":
            self.config["EXTRA_INCLUDE_PATHS"] = []
            self.includes_listbox.delete(0, tk.END)

    def add_library_path(self):
        """添加库搜索路径"""
        path = self.libpath_var.get().strip()
        if not path:
            tk.messagebox.showwarning("注意", "请填写库搜索路径", parent=self.root)
            return
        # path = Path(path).absolute().as_posix()
        if path in self.config["EXTRA_LIB_PATHS"]:
            tk.messagebox.showwarning(
                "注意", "该路径已添加到列表中！", parent=self.root
            )
            return

        self.config["EXTRA_LIB_PATHS"].append(path)
        self.libpaths_listbox.insert(tk.END, path)
        self.libpath_var.set("")

    def remove_library_path(self):
        """移除选中的库搜索路径"""
        selection = self.libpaths_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning(
                "注意", "请先选择要移除的项目！", parent=self.root
            )
            return
        self.libpaths_listbox: tk.Listbox
        index = selection[0]
        cur_path = self.libpaths_listbox.get(index)
        if cur_path in self.config["EXTRA_LIB_PATHS"]:
            self.config["EXTRA_LIB_PATHS"].remove(cur_path)
        self.libpaths_listbox.delete(index)

    def add_library(self):
        """添加链接库"""
        lib = self.library_var.get().strip()
        if not lib:
            tk.messagebox.showwarning("注意", "请填写链接库名称", parent=self.root)
            return

        if lib in self.config["EXTRA_LIB_LINKED"]:
            tk.messagebox.showwarning(
                "注意", "该链接库已添加到列表中！", parent=self.root
            )
            return
        self.config["EXTRA_LIB_LINKED"].append(lib)
        self.libraries_listbox.insert(tk.END, lib)
        self.library_var.set("")

    def remove_library(self):
        """移除选中的链接库"""
        selection = self.libraries_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning(
                "注意", "请先选择要移除的项目！", parent=self.root
            )
            return
        self.libraries_listbox: tk.Listbox
        index = selection[0]
        cur_lib = self.libraries_listbox.get(index)
        if cur_lib in self.config["EXTRA_LIB_LINKED"]:
            self.config["EXTRA_LIB_LINKED"].remove(cur_lib)
        self.libraries_listbox.delete(index)

    def generate_command(self, target=None):
        """生成make命令"""
        # 更新配置
        self.update_config()

        # 构建命令
        cmd_parts = ["make"]

        pwd = self.workdir_var.get().strip()
        if pwd:
            cmd_parts.append(f"--directory={pwd}")

        # 添加目标
        if not target:
            target = self.make_target_var.get().strip()
        if target:
            cmd_parts.append(target)

        if target.startswith("clean"):
            command = " ".join(cmd_parts)
            # 显示命令
            self.command_text.delete(1.0, tk.END)
            self.command_text.insert(1.0, command)
            return self.command_text.get(1.0, tk.END)

        def _to_include_options(paths):
            return " ".join([f"-I{path.strip()}" for path in paths if path.strip()])

        def _to_lib_path_options(paths):
            return " ".join([f"-L{path.strip()}" for path in paths if path.strip()])

        def _to_lib_options(libs):
            result = []
            for lib in libs:
                lib = lib.strip()
                if not lib:
                    continue
                if lib.startswith("-l"):
                    result.append(lib)
                    continue
                lib_filename = Path(lib).absolute().name
                if lib_filename.startswith("lib"):
                    if lib_filename.endswith(".a"):
                        result.append(f"-l{lib_filename[3:-2]}")
                    elif lib_filename.endswith(".so"):
                        result.append(f"-l{lib_filename[3:-3]}")
                    else:
                        result.append(f"-l:{lib_filename}")
                else:
                    result.append(f"-l:{lib_filename}")
            return " ".join(result)

        for varname, value in self.config.items():
            if isinstance(value, str):
                value = value.strip()

            if not value:
                continue

            if varname.startswith("make_"):
                continue

            if varname == "EXTRA_INCLUDE_PATHS":
                cmd_parts.append(f'"EXTRA_INCLUDE_PATHS={_to_include_options(value)}"')
                continue

            if varname == "EXTRA_LIB_PATHS":
                cmd_parts.append(f'"EXTRA_LIB_PATHS={_to_lib_path_options(value)}"')
                continue

            if varname == "EXTRA_LIB_LINKED":
                cmd_parts.append(f'"EXTRA_LIB_LINKED={_to_lib_options(value)}"')
                continue
            cmd_parts.append(f'"{varname}={value}"')

        # 添加额外参数
        extra_args = self.extra_make_entry.get(1.0, tk.END).strip()
        if extra_args:
            cmd_parts.append(extra_args)

        command = " ".join(cmd_parts)

        # 显示命令
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(1.0, command)
        self.command_text.get(1.0, tk.END)

        return command

    def execute_build(self, target=None):
        """执行编译"""
        command = self.generate_command(target=target)

        try:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"执行命令: {command}\n")
            self.output_text.insert(tk.END, "=" * 50 + "\n")

            # 执行命令
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            # 实时输出
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self.output_text.insert(tk.END, output)
                    self.output_text.see(tk.END)
                    self.root.update()
            process.wait()
            if process.returncode == 0:
                self.output_text.insert(tk.END, "\n编译成功!\n")
            else:
                self.output_text.insert(
                    tk.END, f"\n编译失败! 退出码: {process.returncode}\n"
                )
        except Exception as e:
            messagebox.showerror("错误", f"执行命令时出错: {str(e)}", parent=self.root)

    def clean_project(self):
        """清理项目"""
        self.execute_build(target="clean-all")

    def save_config(self):
        """保存配置到文件"""
        self.update_config()

        filename = filedialog.asksaveasfilename(
            title="保存配置",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not filename:
            return
        try:
            with open(filename, "w") as f:
                json.dump(self.config, f, indent=2)
            messagebox.showinfo("成功", "配置保存成功!", parent=self.root)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置时出错: {str(e)}", parent=self.root)

    def load_config(self):
        """从文件加载配置"""
        filename = filedialog.askopenfilename(
            title="加载配置",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            parent=self.root,
        )
        if not filename:
            return

        try:
            with open(filename, "r") as f:
                self.config = json.load(f)
            self.apply_config()
            messagebox.showinfo("成功", "配置加载成功!", parent=self.root)
        except Exception as e:
            messagebox.showerror("错误", f"加载配置时出错: {str(e)}", parent=self.root)

    def update_config(self):
        """更新配置数据"""

        lib_paths = [
            path.strip()
            for path in self.libpaths_listbox.get(0, tk.END)
            if path.strip()
        ]
        libs = [
            lib.strip() for lib in self.libraries_listbox.get(0, tk.END) if lib.strip()
        ]
        include_paths = [
            path.strip()
            for path in self.includes_listbox.get(0, tk.END)
            if path.strip()
        ]

        self.config.update(
            {
                "TOOLCHAIN_DIR": self.toolchain_path_var.get().strip(),
                "TOOLCHAIN_PRE": self.toolchain_prefix_var.get().strip(),
                # "PKG_CONFIG_BIN": self.pkg_config_bin_var.get().strip(),
                "SYSROOT_DIR": self.sysroot_var.get().strip(),
                "BIN": self.output_bin_var.get().strip(),
                "START_SCRIPT_FILENAME": self.startup_filename_var.get().strip(),
                "WORK_DIR": self.startup_workdir_entry.get().strip(),
                "EXCLUDE_DEMOS_AND_EXAMPLES": self.exclude_demos_var.get().strip(),
                "EXTRA_CFLAGS": self.cflags_entry.get(1.0, tk.END).strip(),
                "EXTRA_LDFLAGS": self.ldflags_entry.get(1.0, tk.END).strip(),
                "EXTRA_INCLUDE_PATHS": include_paths,
                "EXTRA_LIB_PATHS": lib_paths,
                "EXTRA_LIB_LINKED": libs,
                "make_extra_args": self.extra_make_entry.get(1.0, tk.END).strip(),
            }
        )

    def apply_config(self):
        """应用配置到界面"""
        self.toolchain_path_var.set(self.config.get("TOOLCHAIN_DIR", "").strip())
        self.toolchain_prefix_var.set(self.config.get("TOOLCHAIN_PRE", "").strip())
        self.sysroot_var.set(self.config.get("SYSROOT_DIR", "").strip())
        self.output_bin_var.set(self.config.get("BIN", "app.bin").strip())
        self.exclude_demos_var.set(
            self.config.get("EXCLUDE_DEMOS_AND_EXAMPLES", "1").strip()
        )
        self.startup_filename_var.set(
            self.config.get("START_SCRIPT_FILENAME", "".strip())
        )
        self.startup_workdir_var.set(self.config.get("WORK_DIR", "").strip())
        self.cflags_entry.delete(1.0, tk.END)
        self.cflags_entry.insert(1.0, self.config.get("EXTRA_CFLAGS", "").strip())
        self.ldflags_entry.delete(1.0, tk.END)
        self.ldflags_entry.insert(1.0, self.config.get("EXTRA_LDFLAGS", "").strip())

        self.extra_make_entry.delete(1.0, tk.END)
        self.extra_make_entry.insert(
            1.0, self.config.get("make_extra_args", "").strip()
        )

        # 更新列表
        self.includes_listbox.delete(0, tk.END)
        inserted = []
        for path in self.config.get("EXTRA_INCLUDE_PATHS", []):
            path = path.strip()
            if not path:
                continue
            if path in inserted:
                continue
            inserted.append(path)
            self.includes_listbox.insert(tk.END, path)

        inserted.clear()
        self.libpaths_listbox.delete(0, tk.END)
        for path in self.config.get("EXTRA_LIB_PATHS", []):
            path = path.strip()
            if not path:
                continue
            if path in inserted:
                continue
            inserted.append(path)
            self.libpaths_listbox.insert(tk.END, path)

        inserted.clear()
        self.libraries_listbox.delete(0, tk.END)
        for lib in self.config.get("EXTRA_LIB_LINKED", []):
            lib = lib.strip()
            if not lib:
                continue
            if lib in inserted:
                continue
            inserted.append(lib)
            self.libraries_listbox.insert(tk.END, lib)
        inserted.clear()
        self.root.update()

    def load_default_config(self):
        """加载默认配置"""
        # 这里可以设置一些默认值
        pass


def main():
    root = tk.Tk()
    app = ProjectBuilder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
