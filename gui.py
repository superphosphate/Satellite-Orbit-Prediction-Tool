# -*- coding: utf-8 -*-
"""
author: ZengFanyu
email: 3024826049@qq.com
date: 2025/06/05

update:
V0.3.0
- add GUI
- allow users to download TLE files from a website
"""
import os
from datetime import datetime, timedelta, timezone
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import requests
from skyfield.api import load, EarthSatellite
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go
from cartopy import crs

class SatelliteGUI:
    """Gui主类"""
    def __init__(self, self_root):
        self.status_var = None
        self.display_frame = None
        self.hours_var = None
        self.satellite_listbox = None
        self.progress_bar = None
        self.progress_var = tk.DoubleVar()
        self.root = self_root
        self.root.title("卫星轨道预测工具")
        self.root.geometry("1200x800")
        # 数据存储
        self.satellites = []
        self.selected_satellite = None
        self.ts = load.timescale()
        self.geocentric = None
        self.subpoint = None
        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # 左侧控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)
        # 文件操作区域
        file_frame = ttk.LabelFrame(control_frame, text="TLE文件操作")
        file_frame.pack(fill=tk.X, pady=5)
        ttk.Button(file_frame, text="选择本地文件", command=self.load_local_file).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="从网络下载", command=self.show_download_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="扫描当前目录", command=self.scan_directory).pack(fill=tk.X, pady=2)
        # 网络下载进度条
        self.progress_bar = ttk.Progressbar(file_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=2)
        self.progress_bar.pack_forget()  # 初始隐藏
        # 卫星选择区域
        satellite_frame = ttk.LabelFrame(control_frame, text="卫星选择")
        satellite_frame.pack(fill=tk.X, pady=5)
        self.satellite_listbox = tk.Listbox(satellite_frame, height=8)
        self.satellite_listbox.pack(fill=tk.BOTH, expand=True)
        self.satellite_listbox.bind('<<ListboxSelect>>', self.on_satellite_select)
        # 时间设置区域
        time_frame = ttk.LabelFrame(control_frame, text="时间设置")
        time_frame.pack(fill=tk.X, pady=5)
        ttk.Label(time_frame, text="预测时长(小时):").pack()
        self.hours_var = tk.StringVar(value="24")
        ttk.Entry(time_frame, textvariable=self.hours_var, width=10).pack()
        # 操作按钮区域
        button_frame = ttk.LabelFrame(control_frame, text="轨道显示")
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="计算轨道", command=self.calculate_orbit).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="2D轨迹图", command=self.show_2d_plot).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="3D轨道图", command=self.show_3d_plot).pack(fill=tk.X, pady=2)
        # 右侧显示区域
        self.display_frame = ttk.LabelFrame(main_frame, text="轨道显示")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def show_download_dialog(self):
        """显示下载对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("下载TLE文件")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        # 预设网址列表
        urls = [
            ("Starlink卫星","https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"),
            ("NOAA卫星", "https://celestrak.org/NORAD/elements/gp.php?GROUP=noaa&FORMAT=tle"),
            ("GPS卫星", "https://celestrak.org/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=tle"),
            ("国际空间站", "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"),
            ("地球同步轨道", "https://celestrak.org/NORAD/elements/gp.php?GROUP=geo&FORMAT=tle"),
            ("天气卫星", "https://celestrak.org/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle")
        ]
        ttk.Label(dialog, text="选择预设网址或输入自定义网址:").pack(pady=10)
        # 预设网址按钮
        for name, url in urls:
            ttk.Button(dialog, text=name, 
                      command=lambda u=url,
                           n=name: self.download_tle(u, n, dialog)).pack(fill=tk.X, padx=20, pady=2)
        # 自定义网址输入
        ttk.Label(dialog, text="自定义网址:").pack(pady=(20, 5))
        url_entry = ttk.Entry(dialog, width=60)
        url_entry.pack(padx=20, pady=5)
        ttk.Button(dialog, text="下载",
                  command=lambda: self.download_tle(url_entry.get(), "自定义", dialog)).pack(pady=10)
    def download_tle(self, url, name, dialog):
        """下载TLE文件"""
        if not url:
            messagebox.showerror("错误", "请输入有效的网址")
            return
        dialog.destroy()
        self.progress_bar.pack(fill=tk.X, pady=2)
        self.status_var.set(f"正在下载 {name}...")
        def download_thread():
            try:
                response = requests.get(url, stream=True, timeout=10) # timeout
                response.raise_for_status()
                # 保存文件
                filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tle"
                filepath = os.path.join(os.getcwd(), filename)
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                with open(filepath, 'w', encoding='utf-8') as f:
                    for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk.encode('utf-8'))
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda: self.download_complete(filepath, filename))
            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self.download_error("Request timed out"))
            except Exception as e:
                self.root.after(0, lambda: self.download_error(str(e)))
        threading.Thread(target=download_thread, daemon=True).start()
    def download_complete(self, filepath, filename):
        """下载完成处理"""
        self.progress_bar.pack_forget()
        self.status_var.set(f"下载完成: {filename}")
        self.load_tle_file(filepath)
    def download_error(self, error_msg):
        """下载错误处理"""
        self.progress_bar.pack_forget()
        self.status_var.set("下载失败")
        messagebox.showerror("下载错误", f"下载失败: {error_msg}")
    def load_local_file(self):
        """加载本地TLE文件"""
        file_path = filedialog.askopenfilename(
            title="选择TLE文件",
            filetypes=[("TLE文件", "*.tle"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.load_tle_file(file_path)

    def scan_directory(self):
        """扫描当前目录的TLE文件"""
        cwd = os.getcwd()
        tle_files = [f for f in os.listdir(cwd) if f.lower().endswith(('.tle', '.txt'))]
        if not tle_files:
            messagebox.showinfo("信息", "当前目录未找到TLE文件")
            return
        # 创建文件选择对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("选择TLE文件")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        ttk.Label(dialog, text="发现以下TLE文件:").pack(pady=10)
        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        for file in tle_files:
            listbox.insert(tk.END, file)
        def load_selected():
            selection = listbox.curselection()
            if selection:
                selected_file = tle_files[selection[0]]
                file_path = os.path.join(cwd, selected_file)
                self.load_tle_file(file_path)
                dialog.destroy()
        ttk.Button(dialog, text="加载选中文件", command=load_selected).pack(pady=10)
    def load_tle_file(self, file_path):
        """加载TLE文件并解析卫星数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.satellites = self.parse_tle(content)
            self.update_satellite_list()
            self.status_var.set(f"已加载 {len(self.satellites)} 颗卫星")
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败: {str(e)}")
    @staticmethod
    def parse_tle(content):
        """解析TLE数据"""
        satellites = []
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        if len(lines) % 3 != 0:
            raise ValueError("TLE文件格式错误: 行数不是3的倍数")
        for i in range(0, len(lines), 3):
            name_line = lines[i]
            line1 = lines[i + 1]
            line2 = lines[i + 2]
            if not line1.startswith('1 ') or not line2.startswith('2 '):
                raise ValueError(f"无效的TLE行，位于索引 {i}")
            satellites.append(EarthSatellite(line1, line2, name_line))
        return satellites
    def update_satellite_list(self):
        """更新卫星列表显示"""
        self.satellite_listbox.delete(0, tk.END)
        for sat in self.satellites:
            self.satellite_listbox.insert(tk.END, sat.name)
    def on_satellite_select(self, event):
        """卫星选择事件处理"""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_satellite = self.satellites[index]
            self.status_var.set(f"已选择卫星: {self.selected_satellite.name}")
    def calculate_orbit(self):
        """计算卫星轨道"""
        if not self.selected_satellite:
            messagebox.showwarning("警告", "请先选择一颗卫星")
            return
        try:
            hours = float(self.hours_var.get())
            if hours <= 0:
                raise ValueError("时间必须大于0")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的时间数值")
            return
        self.status_var.set("正在计算轨道...")
        # 生成时间序列
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=hours)
        delta = timedelta(minutes=5)
        time_points = []
        current_time = start_time
        while current_time <= end_time:
            time_points.append(current_time)
            current_time += delta
        # 计算位置
        time_array = self.ts.utc(time_points)
        self.geocentric = self.selected_satellite.at(time_array)
        self.subpoint = self.geocentric.subpoint()
        self.status_var.set(f"轨道计算完成 ({len(time_points)} 个点)")
    def show_2d_plot(self):
        """显示2D轨迹图"""
        if not self.subpoint:
            messagebox.showwarning("警告", "请先计算轨道")
            return
        # 清除显示区域
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        # 创建matplotlib图形
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': crs.PlateCarree()})
        ax.set_global()
        ax.stock_img()
        ax.coastlines()
        # 绘制轨迹
        ax.plot(self.subpoint.longitude.degrees,
                self.subpoint.latitude.degrees,
                'r-', transform=crs.Geodetic(),
                linewidth=2, label=self.selected_satellite.name)
        # 标记起终点
        ax.plot(self.subpoint.longitude.degrees[0],
                self.subpoint.latitude.degrees[0],
                'go', transform=crs.Geodetic(),
                markersize=8, label='Start')
        ax.plot(self.subpoint.longitude.degrees[-1],
                self.subpoint.latitude.degrees[-1],
                'bo', transform=crs.Geodetic(),
                markersize=8, label='End')
        ax.legend()
        plt.title(f"{self.selected_satellite.name}")
        # 嵌入到GUI
        canvas = FigureCanvasTkAgg(fig, self.display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def show_3d_plot(self):
        """显示3D轨道图"""
        if not self.geocentric:
            messagebox.showwarning("警告", "请先计算轨道")
            return
        # 创建3D图形
        position = self.geocentric.position.km
        earth_radius = 6378.1
        # 创建地球表面
        theta = np.linspace(0, 2 * np.pi, 50)
        phi = np.linspace(0, np.pi, 25)
        x_earth = earth_radius * np.outer(np.cos(theta), np.sin(phi)).T
        y_earth = earth_radius * np.outer(np.sin(theta), np.sin(phi)).T
        z_earth = earth_radius * np.outer(np.ones(50), np.cos(phi)).T
        fig = go.Figure()
        # 添加地球表面
        fig.add_trace(go.Surface(
            x=x_earth, y=y_earth, z=z_earth,
            colorscale=[[0, 'rgb(100, 150, 200)'], [1, 'rgb(100, 150, 200)']],
            showscale=False,
            opacity=0.3,
            name="地球"
        ))
        # 添加经纬线
        for lon in np.arange(-180, 180, 30):
            lambda_rad = np.deg2rad(lon)
            phi_range = np.linspace(-89.9, 89.9, 50)
            phi_rad = np.deg2rad(phi_range)
            x = earth_radius * np.cos(phi_rad) * np.cos(lambda_rad)
            y = earth_radius * np.cos(phi_rad) * np.sin(lambda_rad)
            z = earth_radius * np.sin(phi_rad)
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line={'color': 'rgba(150, 150, 150, 0.5)', 'width': 1},
                hoverinfo='none',
                showlegend=False
            ))
        for lat in np.arange(-80, 90, 30):
            phi_rad = np.deg2rad(lat)
            lambda_range = np.linspace(-180, 180, 50)
            lambda_rad = np.deg2rad(lambda_range)
            x = earth_radius * np.cos(phi_rad) * np.cos(lambda_rad)
            y = earth_radius * np.cos(phi_rad) * np.sin(lambda_rad)
            z = earth_radius * np.sin(phi_rad) * np.ones_like(lambda_rad)
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line={'color': 'rgba(150, 150, 150, 0.5)', 'width': 1},
                hoverinfo='none',
                showlegend=False
            ))
        # 添加卫星轨道
        fig.add_trace(go.Scatter3d(
            x=position[0], y=position[1], z=position[2],
            mode='lines',
            line={'color': 'red', 'width': 4},
            name=f'{self.selected_satellite.name} 轨道'
        ))
        fig.update_layout(
            title=f'{self.selected_satellite.name} 三维轨道可视化',
            scene={'xaxis': {'visible': True},
                   'yaxis': {'visible': True},
                   'zaxis': {'visible': True},
                   'aspectmode': 'manual', 'aspectratio': {'x': 1, 'y': 1, 'z': 1},
                   'camera': {'eye': {'x': 1.5, 'y': 1.5, 'z': 0.8}}},
            width=800,
            height=600
        )
        # 在浏览器中显示3D图
        fig.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = SatelliteGUI(root)
    root.mainloop()
