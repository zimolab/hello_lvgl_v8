import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import json


class CProjectBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("C项目编译辅助工具 - LVGL项目")
        self.root.geometry("900x700")

        # 配置数据
        self.config = {
            "toolchain_path": "",
            "toolchain_prefix": "",
            "sysroot": "",
            "output_bin": "app.bin",
            "exclude_demos": "1",
            "include_paths": [],
            "library_paths": [],
            "libraries": [],
            "cflags": "",
            "ldflags": "",
            "pkg_config_flags": "",
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
        ttk.Label(frame, text="工具链路径 (TOOLCHAIN_PATH):").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.toolchain_path_var = tk.StringVar()
        self.toolchain_path_entry = ttk.Entry(
            frame, textvariable=self.toolchain_path_var, width=50
        )
        self.toolchain_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(frame, text="浏览", command=self.browse_toolchain_path).grid(
            row=0, column=2, padx=5, pady=5
        )

        # 工具链前缀
        ttk.Label(frame, text="工具链前缀 (TOOLCHAIN_PREFIX):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.toolchain_prefix_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.toolchain_prefix_var, width=50).grid(
            row=1, column=1, padx=5, pady=5, sticky="we"
        )
        ttk.Label(frame, text="如: arm-linux-gnueabihf-").grid(
            row=1, column=2, sticky="w", padx=5, pady=5
        )

        # 系统根目录
        ttk.Label(frame, text="系统根目录 (SYSROOT):").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.sysroot_var = tk.StringVar()
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
        ttk.Label(frame, text="输出文件名 (OUTPUT_BIN):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.output_bin_var = tk.StringVar(value="app.bin")
        ttk.Entry(frame, textvariable=self.output_bin_var, width=50).grid(
            row=1, column=1, padx=5, pady=5, sticky="we"
        )

        # 排除示例和演示
        ttk.Label(frame, text="排除示例和演示:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.exclude_demos_var = tk.StringVar(value="1")
        exclude_frame = ttk.Frame(frame)
        exclude_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(
            exclude_frame, text="是", variable=self.exclude_demos_var, value="1"
        ).pack(side="left")
        ttk.Radiobutton(
            exclude_frame, text="否", variable=self.exclude_demos_var, value="0"
        ).pack(side="left")

        # LVGL目录
        ttk.Label(frame, text="LVGL目录 (LVGL_DIR):").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.lvgl_dir_var = tk.StringVar()
        self.lvgl_dir_entry = ttk.Entry(frame, textvariable=self.lvgl_dir_var, width=50)
        self.lvgl_dir_entry.grid(row=3, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(frame, text="浏览", command=self.browse_lvgl_dir).grid(
            row=3, column=2, padx=5, pady=5
        )

        frame.columnconfigure(1, weight=1)

    def create_includes_tab(self):
        """创建头文件路径配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="头文件")

        # 头文件路径列表
        ttk.Label(frame, text="头文件搜索路径 (INCLUDE_PATHS):").grid(
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

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

    def create_libraries_tab(self):
        """创建库文件配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="库文件")

        # 创建左右两个框架
        left_frame = ttk.LabelFrame(frame, text="库搜索路径 (LIB_PATHS)")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        right_frame = ttk.LabelFrame(frame, text="链接库 (LIB_LINKED)")
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

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

    def create_flags_tab(self):
        """创建编译标志配置标签页"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="编译选项")

        # CFLAGS
        ttk.Label(frame, text="自定义 CFLAGS:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.cflags_var = tk.StringVar()
        cflags_entry = ttk.Entry(frame, textvariable=self.cflags_var, width=60)
        cflags_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # LDFLAGS
        ttk.Label(frame, text="自定义 LDFLAGS:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.ldflags_var = tk.StringVar()
        ldflags_entry = ttk.Entry(frame, textvariable=self.ldflags_var, width=60)
        ldflags_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # pkg-config标志
        ttk.Label(frame, text="pkg-config标志:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.pkg_config_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.pkg_config_var, width=60).grid(
            row=2, column=1, padx=5, pady=5, sticky="we"
        )

        # 额外参数
        ttk.Label(frame, text="额外make参数:").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.extra_args_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.extra_args_var, width=60).grid(
            row=3, column=1, padx=5, pady=5, sticky="we"
        )

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
        self.make_target_var = tk.StringVar(value="all")
        target_combo = ttk.Combobox(
            control_frame,
            textvariable=self.make_target_var,
            values=[
                "all",
                "app",
                "libs",
                "clean",
                "clean-app",
                "clean-libs",
                "clean-all",
            ],
        )
        target_combo.pack(side="left", padx=5)

        # 按钮框架
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side="left", padx=20)

        ttk.Button(button_frame, text="生成命令", command=self.generate_command).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="执行编译", command=self.execute_build).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="清理项目", command=self.clean_project).pack(
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
        path = filedialog.askdirectory(title="选择工具链目录")
        if path:
            self.toolchain_path_var.set(path)

    def browse_sysroot(self):
        """浏览选择系统根目录"""
        path = filedialog.askdirectory(title="选择系统根目录")
        if path:
            self.sysroot_var.set(path)

    def browse_workdir(self):
        """浏览选择工作目录"""
        path = filedialog.askdirectory(title="选择工作目录")
        if path:
            self.workdir_var.set(path)

    def browse_lvgl_dir(self):
        """浏览选择LVGL目录"""
        path = filedialog.askdirectory(title="选择LVGL目录")
        if path:
            self.lvgl_dir_var.set(path)

    def browse_include_path(self):
        """浏览选择头文件路径"""
        path = filedialog.askdirectory(title="选择头文件目录")
        if path:
            self.include_path_var.set(path)

    def browse_library_path(self):
        """浏览选择库文件路径"""
        path = filedialog.askdirectory(title="选择库文件目录")
        if path:
            self.libpath_var.set(path)

    def add_include_path(self):
        """添加头文件路径"""
        path = self.include_path_var.get().strip()
        if path and path not in self.config["include_paths"]:
            self.config["include_paths"].append(path)
            self.includes_listbox.insert(tk.END, path)
            self.include_path_var.set("")

    def remove_include_path(self):
        """移除选中的头文件路径"""
        selection = self.includes_listbox.curselection()
        if selection:
            index = selection[0]
            self.config["include_paths"].pop(index)
            self.includes_listbox.delete(index)

    def add_library_path(self):
        """添加库搜索路径"""
        path = self.libpath_var.get().strip()
        if path and path not in self.config["library_paths"]:
            self.config["library_paths"].append(path)
            self.libpaths_listbox.insert(tk.END, path)
            self.libpath_var.set("")

    def remove_library_path(self):
        """移除选中的库搜索路径"""
        selection = self.libpaths_listbox.curselection()
        if selection:
            index = selection[0]
            self.config["library_paths"].pop(index)
            self.libpaths_listbox.delete(index)

    def add_library(self):
        """添加链接库"""
        lib = self.library_var.get().strip()
        if lib and lib not in self.config["libraries"]:
            self.config["libraries"].append(lib)
            self.libraries_listbox.insert(tk.END, lib)
            self.library_var.set("")

    def remove_library(self):
        """移除选中的链接库"""
        selection = self.libraries_listbox.curselection()
        if selection:
            index = selection[0]
            self.config["libraries"].pop(index)
            self.libraries_listbox.delete(index)

    def generate_command(self):
        """生成make命令"""
        # 更新配置
        self.update_config()

        # 构建命令
        cmd_parts = ["make"]

        # 添加目标
        target = self.make_target_var.get().strip()
        if target:
            cmd_parts.append(target)

        # 添加工具链变量
        if self.config["toolchain_path"]:
            cmd_parts.append(f"TOOLCHAIN_PATH={self.config['toolchain_path']}")

        if self.config["toolchain_prefix"]:
            cmd_parts.append(f"TOOLCHAIN_PREFIX={self.config['toolchain_prefix']}")

        # 添加系统根目录
        if self.config["sysroot"]:
            cmd_parts.append(f"SYSROOT_DIR={self.config['sysroot']}")

        # 添加输出文件名
        if self.config["output_bin"]:
            cmd_parts.append(f"OUTPUT_BIN={self.config['output_bin']}")

        # 添加排除示例标志
        cmd_parts.append(f"EXCLUDE_DEMOS_AND_EXAMPLES={self.config['exclude_demos']}")

        # 添加LVGL目录
        if self.config.get("lvgl_dir"):
            cmd_parts.append(f"LVGL_DIR={self.config['lvgl_dir']}")

        # 添加头文件路径
        if self.config["include_paths"]:
            include_flags = " ".join(
                [f"-I{path}" for path in self.config["include_paths"]]
            )
            cmd_parts.append(f"INCLUDE_PATHS+={include_flags}")

        # 添加库搜索路径
        if self.config["library_paths"]:
            lib_paths = " ".join([f"-L{path}" for path in self.config["library_paths"]])
            cmd_parts.append(f"LIB_PATHS+={lib_paths}")

        # 添加链接库
        if self.config["libraries"]:
            libs = " ".join([f"-l{lib}" for lib in self.config["libraries"]])
            cmd_parts.append(f"LIB_LINKED+={libs}")

        # 添加自定义CFLAGS和LDFLAGS
        if self.config["cflags"]:
            cmd_parts.append(f"CFLAGS+={self.config['cflags']}")

        if self.config["ldflags"]:
            cmd_parts.append(f"LDFLAGS+={self.config['ldflags']}")

        # 添加pkg-config标志
        if self.config["pkg_config_flags"]:
            cmd_parts.append(f"PKG_CONFIG_FLAGS+={self.config['pkg_config_flags']}")

        # 添加额外参数
        extra_args = self.extra_args_var.get().strip()
        if extra_args:
            cmd_parts.append(extra_args)

        command = " ".join(cmd_parts)

        # 显示命令
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(1.0, command)

        return command

    def execute_build(self):
        """执行编译"""
        command = self.generate_command()
        workdir = self.workdir_var.get().strip()

        if not workdir:
            messagebox.showerror("错误", "请设置工作目录")
            return

        if not os.path.exists(workdir):
            messagebox.showerror("错误", f"工作目录不存在: {workdir}")
            return

        try:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"执行命令: {command}\n")
            self.output_text.insert(tk.END, f"工作目录: {workdir}\n")
            self.output_text.insert(tk.END, "=" * 50 + "\n")

            # 执行命令
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=workdir,
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
            messagebox.showerror("错误", f"执行命令时出错: {str(e)}")

    def clean_project(self):
        """清理项目"""
        workdir = self.workdir_var.get().strip()

        if not workdir:
            messagebox.showerror("错误", "请设置工作目录")
            return

        try:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "正在清理项目...\n")

            # 使用clean目标
            clean_command = "make clean"
            process = subprocess.Popen(
                clean_command,
                shell=True,
                cwd=workdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    self.output_text.insert(tk.END, output)
                    self.output_text.see(tk.END)
                    self.root.update()

            process.wait()
            self.output_text.insert(tk.END, "\n清理完成!\n")

        except Exception as e:
            messagebox.showerror("错误", f"清理项目时出错: {str(e)}")

    def save_config(self):
        """保存配置到文件"""
        self.update_config()

        filename = filedialog.asksaveasfilename(
            title="保存配置",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if filename:
            try:
                with open(filename, "w") as f:
                    json.dump(self.config, f, indent=2)
                messagebox.showinfo("成功", "配置保存成功!")
            except Exception as e:
                messagebox.showerror("错误", f"保存配置时出错: {str(e)}")

    def load_config(self):
        """从文件加载配置"""
        filename = filedialog.askopenfilename(
            title="加载配置", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, "r") as f:
                    self.config = json.load(f)
                self.apply_config()
                messagebox.showinfo("成功", "配置加载成功!")
            except Exception as e:
                messagebox.showerror("错误", f"加载配置时出错: {str(e)}")

    def update_config(self):
        """更新配置数据"""
        self.config.update(
            {
                "toolchain_path": self.toolchain_path_var.get().strip(),
                "toolchain_prefix": self.toolchain_prefix_var.get().strip(),
                "sysroot": self.sysroot_var.get().strip(),
                "output_bin": self.output_bin_var.get().strip(),
                "exclude_demos": self.exclude_demos_var.get().strip(),
                "cflags": self.cflags_var.get().strip(),
                "ldflags": self.ldflags_var.get().strip(),
                "pkg_config_flags": self.pkg_config_var.get().strip(),
                "lvgl_dir": self.lvgl_dir_var.get().strip(),
            }
        )

    def apply_config(self):
        """应用配置到界面"""
        self.toolchain_path_var.set(self.config.get("toolchain_path", ""))
        self.toolchain_prefix_var.set(self.config.get("toolchain_prefix", ""))
        self.sysroot_var.set(self.config.get("sysroot", ""))
        self.output_bin_var.set(self.config.get("output_bin", "app.bin"))
        self.exclude_demos_var.set(self.config.get("exclude_demos", "1"))
        self.cflags_var.set(self.config.get("cflags", ""))
        self.ldflags_var.set(self.config.get("ldflags", ""))
        self.pkg_config_var.set(self.config.get("pkg_config_flags", ""))
        self.lvgl_dir_var.set(self.config.get("lvgl_dir", ""))

        # 更新列表
        self.includes_listbox.delete(0, tk.END)
        for path in self.config.get("include_paths", []):
            self.includes_listbox.insert(tk.END, path)

        self.libpaths_listbox.delete(0, tk.END)
        for path in self.config.get("library_paths", []):
            self.libpaths_listbox.insert(tk.END, path)

        self.libraries_listbox.delete(0, tk.END)
        for lib in self.config.get("libraries", []):
            self.libraries_listbox.insert(tk.END, lib)

    def load_default_config(self):
        """加载默认配置"""
        # 这里可以设置一些默认值
        pass


def main():
    root = tk.Tk()
    app = CProjectBuilder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
