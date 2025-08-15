#!/bin/bash
# AppStore 工具依赖自动安装脚本

echo "🚀 AppStore 版本信息获取工具依赖安装脚本"
echo "=========================================="
echo ""

# 检查 Python 版本
echo "🔍 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [ $? -eq 0 ]; then
    echo "✅ Python 版本: $python_version"
    python_cmd="python3"
elif command -v python &> /dev/null; then
    python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+')
    echo "✅ Python 版本: $python_version"
    python_cmd="python"
else
    echo "❌ 未找到 Python，请先安装 Python 3.6+"
    exit 1
fi

# 检查 pip
echo "🔍 检查 pip..."
if command -v pip3 &> /dev/null; then
    pip_cmd="pip3"
elif command -v pip &> /dev/null; then
    pip_cmd="pip"
else
    echo "❌ 未找到 pip，请先安装 pip"
    exit 1
fi

echo "✅ 使用 $pip_cmd 安装依赖"
echo ""

# 选择安装方式
echo "📋 选择安装方式："
echo "1. 最小安装（仅必需依赖）"
echo "2. 完整安装（包含可选依赖）"
echo "3. 自定义安装"
echo ""
read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "📦 执行最小安装..."
        $pip_cmd install -r requirements-minimal.txt
        ;;
    2)
        echo "📦 执行完整安装..."
        $pip_cmd install -r requirements.txt
        ;;
    3)
        echo "📦 执行自定义安装..."
        echo "请手动选择要安装的依赖："
        echo ""
        read -p "安装 matplotlib? (y/n): " install_matplotlib
        read -p "安装 requests? (y/n): " install_requests
        read -p "安装 tqdm? (y/n): " install_tqdm
        read -p "安装 colorama? (y/n): " install_colorama
        
        if [ "$install_matplotlib" = "y" ]; then
            echo "📦 安装 matplotlib..."
            $pip_cmd install matplotlib
        fi
        
        if [ "$install_requests" = "y" ]; then
            echo "📦 安装 requests..."
            $pip_cmd install requests
        fi
        
        if [ "$install_tqdm" = "y" ]; then
            echo "📦 安装 tqdm..."
            $pip_cmd install tqdm
        fi
        
        if [ "$install_colorama" = "y" ]; then
            echo "📦 安装 colorama..."
            $pip_cmd install colorama
        fi
        ;;
    *)
        echo "❌ 无效选择，退出安装"
        exit 1
        ;;
esac

echo ""
echo "🔍 验证安装..."

# 测试 matplotlib
if $python_cmd -c "import matplotlib.pyplot as plt; print('✅ matplotlib 安装成功')" 2>/dev/null; then
    echo "✅ matplotlib 验证通过"
else
    echo "❌ matplotlib 安装失败或验证失败"
fi

# 测试 requests
if $python_cmd -c "import requests; print('✅ requests 安装成功')" 2>/dev/null; then
    echo "✅ requests 验证通过"
else
    echo "⚠️  requests 未安装或验证失败"
fi

# 测试 tqdm
if $python_cmd -c "import tqdm; print('✅ tqdm 安装成功')" 2>/dev/null; then
    echo "✅ tqdm 验证通过"
else
    echo "⚠️  tqdm 未安装或验证失败"
fi

# 测试 colorama
if $python_cmd -c "import colorama; print('✅ colorama 安装成功')" 2>/dev/null; then
    echo "✅ colorama 验证通过"
else
    echo "⚠️  colorama 未安装或验证失败"
fi

echo ""
echo "🎉 依赖安装完成！"
echo ""
echo "💡 使用提示："
echo "• 运行 'python3 auto_fetch_popular_apps.py --help' 查看使用帮助"
echo "• 运行 'python3 auto_fetch_popular_apps.py --plot-only' 测试绘图功能"
echo "• 查看 README.md 了解详细使用方法"
echo "• 查看 INSTALL.md 了解安装和配置详情"
