# AppStore 版本信息获取工具安装指南

## 🚀 快速安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd appstore_parse
```

### 2. 安装依赖

```bash
# 安装所有必需依赖
pip install -r requirements.txt

# 或者使用 pip3（如果系统默认使用 Python 3）
pip3 install -r requirements.txt

# 如果遇到权限问题，可以使用用户安装
pip install --user -r requirements.txt
```

### 3. 验证安装

```bash
# 检查 Python 版本（需要 Python 3.6+）
python --version

# 检查 matplotlib 是否安装成功
python -c "import matplotlib.pyplot as plt; print('matplotlib 安装成功')"

# 检查其他依赖
python -c "import requests; print('requests 安装成功')"
```

## 📋 依赖库说明

### 🔴 必需依赖

| 库名 | 版本 | 用途 | 说明 |
|------|------|------|------|
| matplotlib | >=3.5.0 | 数据可视化 | 生成包体趋势图，必需 |

### 🟡 可选依赖

| 库名 | 版本 | 用途 | 说明 |
|------|------|------|------|
| requests | >=2.25.0 | 网络请求 | 用于扩展功能，如直接API调用 |
| tqdm | >=4.62.0 | 进度条 | 提供更好的用户体验 |
| colorama | >=4.4.0 | 终端颜色 | 美化终端输出 |

### 🔵 系统依赖

| 依赖 | 说明 | 安装方法 |
|------|------|----------|
| Python | 3.6+ | 系统自带或官网下载 |
| pip | 包管理器 | 通常随 Python 安装 |
| git | 版本控制 | 系统包管理器安装 |

## 🛠️ 安装方法详解

### 方法 1：使用 pip 安装（推荐）

```bash
# 标准安装
pip install -r requirements.txt

# 指定源安装（国内用户推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 阿里云源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 方法 2：使用 conda 安装

```bash
# 创建新的 conda 环境
conda create -n appstore python=3.8
conda activate appstore

# 安装依赖
conda install matplotlib requests tqdm colorama
```

### 方法 3：手动安装

```bash
# 安装 matplotlib（必需）
pip install matplotlib

# 安装其他可选依赖
pip install requests tqdm colorama
```

## 🔧 环境配置

### 1. 虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv appstore_env

# 激活虚拟环境
# Windows
appstore_env\Scripts\activate
# macOS/Linux
source appstore_env/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 系统级安装

```bash
# 直接安装到系统 Python 环境
sudo pip install -r requirements.txt

# 或者用户级安装
pip install --user -r requirements.txt
```

## 🚨 常见问题解决

### 1. matplotlib 安装失败

```bash
# 安装系统依赖（Ubuntu/Debian）
sudo apt-get install python3-tk

# 安装系统依赖（CentOS/RHEL）
sudo yum install python3-tkinter

# 安装系统依赖（macOS）
brew install python-tk

# 使用 conda 安装
conda install matplotlib
```

### 2. 权限问题

```bash
# 使用用户安装
pip install --user -r requirements.txt

# 或者使用 sudo（不推荐）
sudo pip install -r requirements.txt
```

### 3. 网络问题

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或者配置永久镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 4. Python 版本问题

```bash
# 检查 Python 版本
python --version

# 如果版本过低，升级 Python
# Ubuntu/Debian
sudo apt-get install python3.8

# macOS
brew install python@3.8

# 或者使用 pyenv
pyenv install 3.8.10
pyenv global 3.8.10
```

## ✅ 安装验证

### 1. 基本功能测试

```bash
# 测试 matplotlib 绘图功能
python -c "
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
print('✅ 所有依赖库导入成功')
"

# 测试基本脚本运行
python auto_fetch_popular_apps.py --help
```

### 2. 完整功能测试

```bash
# 测试版本一致性检查
python auto_fetch_popular_apps.py --check-only

# 测试绘图功能
python auto_fetch_popular_apps.py --plot-only
```

## 📱 使用示例

### 1. 获取所有热门应用信息

```bash
python auto_fetch_popular_apps.py
```

### 2. 获取指定应用信息

```bash
python auto_fetch_popular_apps.py --app 抖音 --count 5
```

### 3. 仅检查版本一致性

```bash
python auto_fetch_popular_apps.py --check-only
```

### 4. 仅生成趋势图

```bash
python auto_fetch_popular_apps.py --plot-only
```

## 🔄 更新依赖

```bash
# 更新所有依赖到最新版本
pip install --upgrade -r requirements.txt

# 更新特定依赖
pip install --upgrade matplotlib requests
```

## 📚 更多帮助

- 查看 README.md 了解详细使用方法
- 查看 requirements.txt 了解依赖版本要求
- 如遇问题，请检查 Python 版本和依赖安装状态

## 🎯 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.6 或更高版本
- **内存**: 建议 4GB 以上
- **磁盘空间**: 至少 1GB 可用空间
- **网络**: 稳定的互联网连接（用于访问 App Store API）
