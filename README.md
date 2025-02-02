# Satellite Orbit Prediction Tool 卫星轨道预测工具 by SuperPhosphate

If you like this project, please give it a "star"! Thank you for your support!

如果你喜欢这个项目，请点亮“star”！谢谢你的支持！

I am currently still actively learning English and have utilized advanced AI translation technology for the English sections of the project documentation. However, please note that the Chinese version remains the authoritative version for all content. I apologize for any inconvenience this may cause and sincerely thank you for your understanding and cooperation.

我目前仍在学习英文，对于项目文档中的英文部分，我借助了AI翻译技术。但请注意，所有内容均以中文版本为准。对于可能由此带来的任何不便，我深表歉意，并衷心感谢您的理解与配合。

---

## [Overview](#project-introduction) [概述](#项目简介)

### **Project Introduction**

This project is a Python-based satellite trajectory analysis tool that supports quick parsing of satellite orbit information through TLE (Two-Line Element) data. It provides 2D/3D visualization functions, making it suitable for aerospace data analysis, satellite status monitoring, and teaching demonstrations.

---

### **Core Functionalities**

1. **TLE File Management**
   - Automatically scans the working directory to intelligently recognize `.tle`/`.txt` files.
   - Graphical file selection interface (supports Chinese path names).
   - Batch parsing of multiple satellite data.

2. **Orbit Visualization**
   - 2D map projection (supports display of latitude and longitude trajectories).
   - Interactive 3D spatial trajectory display (rotatable/zoomable).
   - 24-hour orbit prediction curves.

3. **Satellite Status Inquiry**
   - Real-time positional coordinates (geocentric coordinate system).
   - Orbit period calculation.
   - Display of sub-satellite point latitude and longitude.

---

### **Technical Highlights**

- **Lightweight Architecture**: Implemented purely in Python, with dependencies only on `Skyfield`, `Matplotlib`, and `Plotly`.
- **Cross-Platform Support**: Compatible with Windows/Linux/macOS systems (expected, as Windows was used for project development).
- **Error Control**: Utilizes SPG4/SDP4 orbit prediction models with kilometer-level accuracy.

---

**Project Scope**: Approximately 300 lines of code, ready-to-use out of the box.

**Data Interface**: Supports NORAD standard TLE format.

**Code Standards**: Modular development with a pylint score of 9.52/10.

---

With this tool, users can complete the entire process of analysis from raw TLE data to visualized trajectories within 5 minutes, significantly lowering the barrier to entry for aerospace data analysis.

---

### **项目简介**

本项目是一个基于Python的卫星轨迹分析工具，支持通过TLE（两行轨道根数）数据快速解析卫星轨道信息，并提供二维/三维可视化功能，适用于航天数据分析、卫星状态监控及教学演示场景。

---

### **核心功能**  

1. **TLE文件管理**  
   - 自动扫描工作目录，智能识别`.tle`/`.txt`文件  
   - 图形化文件选择界面（支持中文路径）  
   - 多卫星数据批量解析  

2. **轨道可视化**  
   - 二维地图投影（支持经纬度轨迹显示）  
   - 三维空间轨迹交互式展示（可旋转/缩放）  
   - 24小时轨道预测曲线  

3. **卫星状态查询**  
   - 实时位置坐标（地心坐标系）  
   - 轨道周期计算  
   - 星下点经纬度显示  

---

### **技术亮点**  

- **轻量化架构**：纯Python实现，依赖库仅需`Skyfield`+`Matplotlib`+`Plotly`  
- **跨平台支持**：兼容Windows/Linux/macOS系统(预期应如此，项目开发使用Windows)  
- **误差控制**：采用SPG4/SDP4轨道预测模型，精度达千米级  

---

**项目规模**：约300行代码，开箱即用  

**数据接口**：支持NORAD标准TLE格式  

**代码规范**：模块化开发，pylint评分9.52/10

---

通过该工具，用户可在5分钟内完成从原始TLE数据到可视化轨迹的全流程分析，大幅降低航天数据分析门槛

---

## 环境要求

### Python Version Python版本

- Python 3.9+

### requirements 依赖库

```text
skyfield~=1.46
numpy~=1.26.0
matplotlib~=3.8.2
plotly~=5.18.0
pytz~=2024.1
cartopy~=0.22.0

```

### Install Requirements 安装依赖

```bash
pip install -r requirements.txt
```

---

## Quick Start 快速开始

### 1. Prepare the TLE file 准备TLE文件

```text
Satellite Name 卫星名称
First line of TLE data (starting with '1 ') 第一行TLE数据（以'1 '开头）
Second line of TLE data (starting with '2 ') 第二行TLE数据（以'2 '开头）
(These groups can be repeated for multiple satellites 可重复多组）
```

Sample File 示例文件 `satellites.tle`:

```tle
ISS (ZARYA)
1 25544U 98067A   24060.48611111  .00020108  00000-0  36573-3 0  9996
2 25544  51.6404 208.9163 0006973 334.1498  72.0548 15.49792978436275
```

### 2. Running the Program 运行程序

Execute the main script:
执行主脚本：

```bash
python satellite_tracker.py
```

---

## Usage Instructions 使用说明

### Step 1 步骤1 - Select TLE File 选择TLE文件

The program automatically scans the working directory and lists all .tle/.txt files:
程序自动扫描工作目录并列出所有.tle/.txt文件：

```text
找到以下TLE文件：
1. iss.tle
2. gps_sats.txt
输入文件编号选择 (输入0退出): 1
```

### Step 2 步骤2 - Select Satellite 选择卫星

After parsing the file, the program lists all satellites, just input the index:
程序解析文件后列出所有卫星：

```text
1. ISS (ZARYA)
2. GPS BIIF-1 (PRN 25)
请选择卫星编号: 1
已选择卫星: ISS (ZARYA)
```

### Step 3 步骤3 - Generate Trajectory 生成轨迹

The program will automatically:
程序将自动：

1. Generate a UTC time series (starting from the current time for 24 hours) 生成UTC时间序列（当前时间起24小时）
2. Calculate satellite positions 计算卫星位置
3. Display the following visualization results 显示以下可视化结果

---

## Visualization Output 可视化输出

### 2D Trajectory Map 二维轨迹地图

Features 特征:

- Uses PlateCarree projection 使用PlateCarree投影
- Red trajectory lines mark the satellite path 红色轨迹线标注卫星路径
- Green/blue dots mark the start and end points 绿色/蓝色圆点标记起止点
- Automatically loads a global basemap and coastlines(TODO) 自动加载全球底图与海岸线( 未完成 )

### 3D Orbit Diagram 三维轨道图

Features 特征：

- Semi-transparent Earth model (radius of 6378.1 km) 半透明地球模型（半径6378.1km）
- Red trajectory lines + yellow markers display the orbit 红色轨迹线+黄色标记点显示轨道
- Interactive rotation/zoom capabilities 可交互旋转/缩放视图
- Equal-scale coordinate system display 等比例坐标系显示

---

## Code Structure 代码结构

### Main Class Descriptions 主要类说明

#### `TLEFileSelector`

- `load_tle_from_directory()`: Automatically scans the working directory to obtain a list of TLE files. 自动扫描工作目录获取TLE文件列表

#### `SatelliteTracker`

Core functionality class:
核心功能类：

- Initializes by parsing TLE content 初始化时解析TLE内容
- `select_satellite_by_user()`: Interactive satellite selection 交互式卫星选择
- `calculate_positions()`: Calculates orbital positions 计算轨道位置
- `plot_2d_track()`: Generates a 2D map 生成二维地图
- `plot_3d_orbit()`: Generates a 3D view 生成三维视图

### Key Methods 关键方法

```python
def generate_times(hours=24, start_time=None):
    """Generates a UTC time series (default is current time) 生成UTC时间序列（默认当前时间）"""

def _parse_tle(content):
    """Validates and parses the TLE format (automatically skips empty lines) TLE格式校验与解析（自动跳过空行）"""
```

---

## Notes 注意事项

1. **Timezone Handling 时区处理**
   - All time calculations are performed using UTC time 所有时间计算均使用UTC时间
   - Local time conversion needs to be done manually 本地时间需自行转换

2. **File Requirements 文件要求**
   - Ensure the TLE file is encoded in UTF-8 确保TLE文件为UTF-8编码
   - Each set of TLE must contain 3 lines (name line + two data lines) 每组TLE必须包含3行（名称行+两数据行）

3. **Graphic Dependencies 图形依赖**
   - The 2D map requires Cartopy's map data cache (first run may be slower) 二维地图需要Cartopy的地图数据缓存（首次运行可能较慢）
   - 3D visualization requires a browser with WebGL support 三维可视化需浏览器支持WebGL

4. **Common Errors 常见错误**
   - `ValueError: TLE文件格式错误`: means `ValueError: Incorrect TLE file format` Check the number of lines and format of the file 检查文件行数与格式
   - `KeyError: 选择编号`: means `KeyError: Invalid selection number` Input must be a valid number 输入必须是有效数字

---

## Example Workflow 示例运行流程

```text
> python satellite_tracker.py

找到以下TLE文件：
1. iss.tle
请选择要打开的文件编号 (输入0退出): 1

1. ISS (ZARYA)
请选择要跟踪的卫星编号: 1

计算轨道数据中...
显示2D轨迹窗口（关闭后继续）...
生成3D可视化页面...
```

---

## Update Log 更新日志

### V0.2.1

- Draw longitude and latitude lines on the Earth in the 3D view as a simple substitute for the Earth's basemap. 为三维视图中的地球绘制经纬线，简单代替地球底图

### V0.2.0

- Added automatic file scanning functionality 新增自动文件扫描功能
- Support for .txt extensions 支持.txt扩展名
- Optimized TLE format validation 优化TLE格式校验
- Fixed weird trajectory lines in the 3D view by using a method to increase the time sampling rate 使用提高时间采样率的方法，修复三维视图中怪异的轨迹连线

### V0.1.0

- Implemented basic orbital calculations 实现基础轨道计算
- Completed basic 2D/3D visualization functionality 完成基本的二维/三维可视化功能

---

## TODO 待更新

- Complete the Earth's basemap drawing in the 3D view 完成三维视图中地球底图绘制工作
- Select and display multiple satellites simultaneously 选择多卫星同步展示
- ...

---

[author] [SuperPhosphate](https://github.com/superphosphate)  
[email] <3024826049@qq.com>  
