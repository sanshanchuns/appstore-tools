import json
import matplotlib.pyplot as plt
import os

# 只用 Arial Unicode MS，macOS自带，支持中英文混排
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def plot_app_download_size(json_file, png_file, app_name):
    if not os.path.exists(json_file):
        print(f"文件不存在: {json_file}")
        return
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    versions = data['versions'][::-1]  # oldest to newest
    x = [v['short_version'] for v in versions]
    y = [v['download_size'] / 1024 / 1024 for v in versions]
    plt.figure(figsize=(16, 6))
    plt.plot(x, y, marker='o', label=app_name)
    plt.xlabel('版本号')
    plt.ylabel('下载大小 (MB)')
    plt.title(f'{app_name} AppStore 下载包大小变化趋势')
    plt.xticks(rotation=60, fontsize=8)
    plt.legend()
    plt.tight_layout()
    plt.savefig(png_file, dpi=200)
    plt.close()
    print(f"已保存图表: {png_file}")

if __name__ == "__main__":
    # 确保 graph_output 目录存在
    graph_output_dir = "graph_output"
    if not os.path.exists(graph_output_dir):
        os.makedirs(graph_output_dir)
    
    # 从 version_output 目录读取文件，保存到 graph_output 目录
    plot_app_download_size(
        'version_output/app_440948110_latest_100.json', 
        os.path.join(graph_output_dir, 'kuaishou_download_size_curve.png'), 
        '快手'
    )
    plot_app_download_size(
        'version_output/app_1142110895_latest_100.json', 
        os.path.join(graph_output_dir, 'douyin_download_size_curve.png'), 
        '抖音'
    ) 