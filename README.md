# Satellite Orbit Prediction Tool

If you like this project, please give it a "star"! Thank you for your support!

I am currently still actively learning English and have utilized advanced AI translation technology for the English sections of the project documentation. However, please note that the Chinese version remains the authoritative version for all content. I apologize for any inconvenience this may cause and sincerely thank you for your understanding and cooperation.

[中文说明文档](README-zh.md)

---

## Overview

### **Project Introduction**

This project is a Python-based satellite trajectory analysis tool that supports quick parsing of satellite orbit information through TLE (Two-Line Element) data. It provides 2D/3D visualization functions, making it suitable for aerospace data analysis, satellite status monitoring, and teaching demonstrations.

---

### **Core Functionalities**

1. **TLE File Management**
   - Automatically scans the working directory to intelligently recognize `.tle`/`.txt` files.
   - Graphical file selection interface (supports Chinese path names).
   - Batch parsing of multiple satellite data.
   - Update your TLE data from a website, and generate timestamp automatically (in [GUI](gui.py)).

2. **Orbit Visualization**
   - 2D map projection (supports display of latitude and longitude trajectories).
   - Interactive 3D spatial trajectory display (rotatable/zoomable).
   - 24-hour orbit prediction curves.

3. **Satellite Status Inquiry**
   - Real-time positional coordinates (geocentric coordinate system).
   - Orbit period calculation.
   - Display of sub-satellite point latitude and longitude.

4. **GUI enable**
   - operate in a `tkinter` GUI

---

### **Technical Highlights**

- **Lightweight Architecture**: Implemented purely in Python, with dependencies only on `Skyfield`, `Matplotlib`, and `Plotly`.
- **Cross-Platform Support**: Compatible with Windows/Linux/macOS systems (expected, as Windows was used for project development).
- **Error Control**: Utilizes SPG4/SDP4 orbit prediction models with kilometer-level accuracy.

---

**Project Scope**: Approximately 300 lines of code, ready-to-use out of the box.

**Data Interface**: Supports NORAD standard TLE format.

**Code Standards**: Modular development with pylint scores of 9.67/10 (main.py) and 9.68/10 (gui.py).

---

With this tool, users can complete the entire process of analysis from raw TLE data to visualized trajectories within 5 minutes, significantly lowering the barrier to entry for aerospace data analysis.

---

### Install Requirements

```bash
# if use venv
# python -m venv myenv
pip install -r requirements.txt
```

---

## Quick Start

### 1. Prepare the TLE file

```text
Satellite Name
First line of TLE data (starting with '1 ')
Second line of TLE data (starting with '2 ') 
(These groups can be repeated for multiple satellites）
```

Sample File `satellites.tle`:

```tle
ISS (ZARYA)
1 25544U 98067A   24060.48611111  .00020108  00000-0  36573-3 0  9996
2 25544  51.6404 208.9163 0006973 334.1498  72.0548 15.49792978436275
```

### 2. Running the Program

Execute the main script:

```bash
python satellite_tracker.py
```

---

## Usage Instructions

### Step 1 - Select TLE File

The program automatically scans the working directory and lists all .tle/.txt files:
程序自动扫描工作目录并列出所有.tle/.txt文件：

```text
找到以下TLE文件：
1. iss.tle
2. gps_sats.txt
输入文件编号选择 (输入0退出): 1
```

### Step 2 - Select Satellite

After parsing the file, the program lists all satellites, just input the index:

```text
1. ISS (ZARYA)
2. GPS BIIF-1 (PRN 25)
请选择卫星编号: 1
已选择卫星: ISS (ZARYA)
```

### Step 3 - Generate Trajectory

The program will automatically:

1. Generate a UTC time series (starting from the current time for 24 hours)
2. Calculate satellite positions
3. Display the following visualization results

---

## Visualization Output

### 2D Trajectory Map

Features 特征:

- Uses PlateCarree projection
- Red trajectory lines mark the satellite path
- Green/blue dots mark the start and end points
- Automatically loads a global basemap and coastlines(TODO)

### 3D Orbit Diagram

Features：

- Semi-transparent Earth model (radius of 6378.1 km)
- Red trajectory lines + yellow markers display the orbit
- Interactive rotation/zoom capabilities
- Equal-scale coordinate system display

---

## Code Structure

### Main Class Descriptions

#### `TLEFileSelector`

- `load_tle_from_directory()`: Automatically scans the working directory to obtain a list of TLE files.

#### `SatelliteTracker`

Core functionality class:

- Initializes by parsing TLE content
- `select_satellite_by_user()`: Interactive satellite selection
- `calculate_positions()`: Calculates orbital positions
- `plot_2d_track()`: Generates a 2D map
- `plot_3d_orbit()`: Generates a 3D view

### Key Methods

```python
def generate_times(hours=24, start_time=None):
    """Generates a UTC time series (default is current time) 生成UTC时间序列（默认当前时间）"""

def _parse_tle(content):
    """Validates and parses the TLE format (automatically skips empty lines) TLE格式校验与解析（自动跳过空行）"""
```

---

## Notes

1. **Timezone Handling**
   - All time calculations are performed using UTC time
   - Local time conversion needs to be done manually

2. **File Requirements**
   - Ensure the TLE file is encoded in UTF-8
   - Each set of TLE must contain 3 lines (name line + two data lines)

3. **Graphic Dependencies**
   - The 2D map requires Cartopy's map data cache (first run may be slower)
   - 3D visualization requires a browser with WebGL support

4. **Common Errors**
   - `ValueError: TLE文件格式错误`: means `ValueError: Incorrect TLE file format` Check the number of lines and format of the file
   - `KeyError: 选择编号`: means `KeyError: Invalid selection number` Input must be a valid number

---

## Example Workflow

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

## Update Log

### V0.3.1

- Added missing type annotations to the code in this commit, to improve maintainability

### V0.3.0

- add GUI: you can download TLE in GUI
- fix README: now it's README.md and README-zh.md

### V0.2.1

- Draw longitude and latitude lines on the Earth in the 3D view as a simple substitute for the Earth's basemap.

### V0.2.0

- Added automatic file scanning functionality
- Support for .txt extensions
- Optimized TLE format validation
- Fixed weird trajectory lines in the 3D view by using a method to increase the time sampling rate

### V0.1.0

- Implemented basic orbital calculations
- Completed basic 2D/3D visualization functionality

---

## TODO

- Complete the Earth's basemap drawing in the 3D view
- Select and display multiple satellites simultaneously
- ...

---

[author] [SuperPhosphate](https://github.com/superphosphate)  
[email] <3024826049@qq.com>  
