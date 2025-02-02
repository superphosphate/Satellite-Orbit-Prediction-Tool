# -*- coding: utf-8 -*-
"""
author: ZengFanyu
email: 3024826049@qq.com
date: 2025/01/29

update:
V0.2.1
- fix 3D
V0.2.0
- finish file select logic
  -> automatically read .tle and .txt file in working path
V0.1.0
- create file, and finish 2D&3D paint logic
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from cartopy import crs
from skyfield.api import load, EarthSatellite
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class TLEFileSelector:

    @staticmethod
    def load_tle_from_directory():
        """从工作目录中读取文件"""
        # 获取当前工作目录
        cwd = os.getcwd()

        # 查找所有.tle文件
        tle_files = [file for file in os.listdir(cwd) if file.lower().endswith(('.tle', '.txt'))]

        if not tle_files:
            print("当前目录未找到TLE文件")
            return None

        # 显示文件列表
        print("找到以下TLE文件：")
        for i, filename in enumerate(tle_files, 1):
            print(f"{i}. {filename}")

        # 用户选择文件
        while True:
            try:
                choice = int(input("请选择要打开的文件编号 (输入0退出): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(tle_files):
                    selected_file = tle_files[choice - 1]
                    break
                print("输入编号无效，请重新输入")
            except ValueError:
                print("请输入有效数字")
        return selected_file


class SatelliteTracker:
    def __init__(self, tle_file_content):
        self.satellites = self._parse_tle(tle_file_content)
        self.selected_satellite = self.satellites[0]
        self.ts = load.timescale()
        self.geocentric = None
        self.subpoint = None

    @staticmethod
    def _parse_tle(tle_file_content):
        """解析TLE数据并处理格式问题"""
        satellites = []
        lines = [line.strip() for line in tle_file_content.strip().split('\n') if line.strip()]

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

    def select_satellite(self):
        """选择第一个卫星"""
        self.selected_satellite = self.satellites[0]

    def list_satellites(self):
        """列出所有卫星的名称"""
        for i, sat in enumerate(self.satellites, 1):
            print(f"{i}. {sat.name}")

    def select_satellite_by_user(self):
        """用户选择一个卫星"""
        self.list_satellites()
        while True:
            try:
                choice = int(input("请选择要跟踪的卫星编号 (输入0退出): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(self.satellites):
                    self.selected_satellite = self.satellites[choice - 1]
                    print(f"已选择卫星: {self.selected_satellite.name}")
                    break
                print("输入编号无效，请重新输入")
            except ValueError:
                print("请输入有效数字")

    @staticmethod
    def generate_times(hours=24, start_time=None):
        """生成时间序列（每5分钟采样一次）"""
        start = start_time or datetime.now(timezone.utc)
        end = start + timedelta(hours=hours)
        delta = timedelta(minutes=5)  # 时间采样速度
        time_points_list = []
        current_time = start
        while current_time <= end:
            time_points_list.append(current_time)
            current_time += delta
        return time_points_list

    def calculate_positions(self, now_time):
        """计算卫星位置"""
        time_array = self.ts.utc(now_time)
        self.geocentric = self.selected_satellite.at(time_array)
        self.subpoint = self.geocentric.subpoint()

    def plot_2d_track(self):
        """绘制二维轨迹图"""
        if not self.subpoint:
            raise ValueError("Please calculate positions first")

        plt.figure(figsize=(12, 6))
        ax = plt.axes(projection=crs.PlateCarree())
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

        plt.title(f"{self.selected_satellite.name} 24-hour track prediction")
        plt.legend()
        plt.show()

    def plot_3d_orbit(self):
        """绘制带经纬线的三维轨道图"""
        if not self.geocentric:
            raise ValueError("请先计算卫星位置")

        # 获取卫星位置数据
        position = self.geocentric.position.km
        earth_radius = 6378.1  # 与地球模型一致的半径

        # 创建地球表面
        theta = np.linspace(0, 2 * np.pi, 100)
        phi = np.linspace(0, np.pi, 50)
        x_earth = earth_radius * np.outer(np.cos(theta), np.sin(phi)).T
        y_earth = earth_radius * np.outer(np.sin(theta), np.sin(phi)).T
        z_earth = earth_radius * np.outer(np.ones(100), np.cos(phi)).T

        # 创建图形对象
        figure = go.Figure()

        # 添加地球表面
        figure.add_trace(go.Surface(
            x=x_earth, y=y_earth, z=z_earth,
            colorscale=[[0, 'rgb(100, 150, 200)'], [1, 'rgb(100, 150, 200)']],
            showscale=False,
            opacity=0.3,
            name="Earth"
        ))

        # 添加经纬线系统（核心新增部分）
        # =================================================================
        # 生成经线系统（每隔30度）
        for lon in np.arange(-180, 180, 30):
            lambda_rad = np.deg2rad(lon)
            phi_range = np.linspace(-89.9, 89.9, 100)  # 避免极点闭合
            phi_rad = np.deg2rad(phi_range)

            x = earth_radius * np.cos(phi_rad) * np.cos(lambda_rad)
            y = earth_radius * np.cos(phi_rad) * np.sin(lambda_rad)
            z = earth_radius * np.sin(phi_rad)

            figure.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line=dict(color='rgba(150, 150, 150, 0.5)', width=1),
                hoverinfo='none',
                showlegend=False
            ))

        # 生成纬线系统（每隔30度，排除极点）
        for lat in np.arange(-80, 90, 30):
            phi_rad = np.deg2rad(lat)
            lambda_range = np.linspace(-180, 180, 100)
            lambda_rad = np.deg2rad(lambda_range)

            x = earth_radius * np.cos(phi_rad) * np.cos(lambda_rad)
            y = earth_radius * np.cos(phi_rad) * np.sin(lambda_rad)
            z = earth_radius * np.sin(phi_rad) * np.ones_like(lambda_rad)

            figure.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines',
                line={'color': 'rgba(150, 150, 150, 0.5)', 'width': 1},
                hoverinfo='none',
                showlegend=False
            ))
        # =================================================================

        # 添加卫星轨道
        figure.add_trace(go.Scatter3d(
            x=position[0], y=position[1], z=position[2],
            mode='lines',
            line={'color': 'red', 'width': 4},
            name=f'{self.selected_satellite.name} Orbit'
        ))

        # 设置布局参数
        figure.update_layout(
            title=f'{self.selected_satellite.name}三维轨道可视化（含经纬网）',
            scene={
                'xaxis': {"visible": True},
                'yaxis': {"visible": True},
                'zaxis': {"visible": True},
                'aspectmode': 'manual',
                'aspectratio': {"x": 1, "y": 1, "z": 1},
                'camera': {
                    "eye": {"x": 1.5, "y": 1.5, "z": 0.8}
                }
            },
            width=1200,
            height=800
        )
        return figure


if __name__ == "__main__":
    file_name = TLEFileSelector.load_tle_from_directory()

    if file_name:
        print(f"{file_name}内检测到卫星：")  # 打印文件名前100字符

        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'r') as f:
            tle_content = f.read()

        # 创建跟踪器实例
        tracker = SatelliteTracker(tle_content)

        # 用户选择卫星
        tracker.select_satellite_by_user()
        if tracker.selected_satellite is None:
            print("未选择卫星，程序退出")
            sys.exit()

        # 生成时间序列并计算位置
        time_points = tracker.generate_times(hours=24)
        tracker.calculate_positions(time_points)

        # 绘制图表
        tracker.plot_2d_track()
        fig = tracker.plot_3d_orbit()
        fig.show()
    else:
        print("未选择文件")
