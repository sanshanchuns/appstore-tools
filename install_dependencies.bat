@echo off
REM AppStore 工具依赖自动安装脚本 (Windows)

echo 🚀 AppStore 版本信息获取工具依赖安装脚本
echo ==========================================
echo.

REM 检查 Python 版本
echo 🔍 检查 Python 版本...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 已安装
    python_cmd=python
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Python3 已安装
        python_cmd=python3
    ) else (
        echo ❌ 未找到 Python，请先安装 Python 3.6+
        pause
        exit /b 1
    )
)

REM 检查 pip
echo 🔍 检查 pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    pip_cmd=pip
) else (
    pip3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        pip_cmd=pip3
    ) else (
        echo ❌ 未找到 pip，请先安装 pip
        pause
        exit /b 1
    )
)

echo ✅ 使用 %pip_cmd% 安装依赖
echo.

REM 选择安装方式
echo 📋 选择安装方式：
echo 1. 最小安装（仅必需依赖）
echo 2. 完整安装（包含可选依赖）
echo 3. 自定义安装
echo.
set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" (
    echo 📦 执行最小安装...
    %pip_cmd% install -r requirements-minimal.txt
) else if "%choice%"=="2" (
    echo 📦 执行完整安装...
    %pip_cmd% install -r requirements.txt
) else if "%choice%"=="3" (
    echo 📦 执行自定义安装...
    echo 请手动选择要安装的依赖：
    echo.
    set /p install_matplotlib="安装 matplotlib? (y/n): "
    set /p install_requests="安装 requests? (y/n): "
    set /p install_tqdm="安装 tqdm? (y/n): "
    set /p install_colorama="安装 colorama? (y/n): "
    
    if /i "%install_matplotlib%"=="y" (
        echo 📦 安装 matplotlib...
        %pip_cmd% install matplotlib
    )
    
    if /i "%install_requests%"=="y" (
        echo 📦 安装 requests...
        %pip_cmd% install requests
    )
    
    if /i "%install_tqdm%"=="y" (
        echo 📦 安装 tqdm...
        %pip_cmd% install tqdm
    )
    
    if /i "%install_colorama%"=="y" (
        echo 📦 安装 colorama...
        %pip_cmd% install colorama
    )
) else (
    echo ❌ 无效选择，退出安装
    pause
    exit /b 1
)

echo.
echo 🔍 验证安装...

REM 测试 matplotlib
%python_cmd% -c "import matplotlib.pyplot as plt; print('✅ matplotlib 安装成功')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ matplotlib 验证通过
) else (
    echo ❌ matplotlib 安装失败或验证失败
)

REM 测试 requests
%python_cmd% -c "import requests; print('✅ requests 安装成功')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ requests 验证通过
) else (
    echo ⚠️  requests 未安装或验证失败
)

REM 测试 tqdm
%python_cmd% -c "import tqdm; print('✅ tqdm 安装成功')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ tqdm 验证通过
) else (
    echo ⚠️  tqdm 未安装或验证失败
)

REM 测试 colorama
%python_cmd% -c "import colorama; print('✅ colorama 安装成功')" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ colorama 验证通过
) else (
    echo ⚠️  colorama 未安装或验证失败
)

echo.
echo 🎉 依赖安装完成！
echo.
echo 💡 使用提示：
echo • 运行 'python auto_fetch_popular_apps.py --help' 查看使用帮助
echo • 运行 'python auto_fetch_popular_apps.py --plot-only' 测试绘图功能
echo • 查看 README.md 了解详细使用方法
echo • 查看 INSTALL.md 了解安装和配置详情
echo.
pause
