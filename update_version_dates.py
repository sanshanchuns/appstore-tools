#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import argparse

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载文件 {file_path} 时出错: {e}")
        return None

def save_json_file(file_path, data):
    """保存JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"文件已保存到: {file_path}")
    except Exception as e:
        print(f"保存文件 {file_path} 时出错: {e}")

def show_common_apps():
    """显示常见App的ID列表"""
    print("\n📱 常见App的ID列表:")
    print("=" * 50)
    print("快手 (Kuaishou)          : 440948110")
    print("抖音 (TikTok)            : 1142110895")
    print("微信 (WeChat)            : 414478124")
    print("QQ                      : 444934666")
    print("支付宝 (Alipay)          : 333206289")
    print("淘宝 (Taobao)            : 387682726")
    print("京东 (JD)                : 414245813")
    print("美团 (Meituan)           : 423084029")
    print("滴滴出行 (DiDi)          : 564499420")
    print("微博 (Weibo)             : 350962117")
    print("今日头条 (Toutiao)       : 529092160")
    print("百度 (Baidu)             : 382201985")
    print("网易云音乐 (NetEase)     : 590338362")
    print("QQ音乐 (QQ Music)        : 414603431")
    print("爱奇艺 (iQiyi)           : 393765873")
    print("腾讯视频 (Tencent Video) : 458318329")
    print("优酷 (Youku)             : 336141475")
    print("=" * 50)
    print("💡 提示: 你也可以使用其他App的ID")

def update_version_dates(app_id):
    """更新版本文件中的发布日期"""
    
    # 根据app_id构建文件路径
    history_json_path = f"version_input/ios_appstore_history_{app_id}.json"
    version_file_path = f"version_output/app_{app_id}_latest_100.json"
    
    print(f"App ID: {app_id}")
    print(f"历史数据文件: {history_json_path}")
    print(f"版本文件: {version_file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(history_json_path):
        print(f"文件不存在: {history_json_path}")
        return False
    
    if not os.path.exists(version_file_path):
        print(f"文件不存在: {version_file_path}")
        return False
    
    # 加载历史数据文件
    print(f"正在加载历史数据文件: {history_json_path}")
    history_data = load_json_file(history_json_path)
    if not history_data:
        return False
    
    # 加载版本文件
    print(f"正在加载版本文件: {version_file_path}")
    version_data = load_json_file(version_file_path)
    if not version_data:
        return False
    
    # 从嵌套结构中提取versionHistory
    # 根据文件结构，versionHistory在 data[0].attributes.platformAttributes.ios.versionHistory
    try:
        version_history = history_data.get("data", [{}])[0].get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
    except (IndexError, KeyError):
        print("无法找到versionHistory字段")
        return False
    
    if not version_history:
        print("未找到versionHistory数据")
        return False
    
    print(f"找到 {len(version_history)} 个版本历史记录")
    
    # 创建版本号到发布日期的映射
    version_to_date = {}
    for item in version_history:
        version_display = item.get("versionDisplay")
        release_date = item.get("releaseDate")
        if version_display and release_date:
            version_to_date[version_display] = release_date
    
    print(f"创建了 {len(version_to_date)} 个版本号到日期的映射")
    
    # 更新版本文件中的每个版本
    updated_count = 0
    for version in version_data.get("versions", []):
        short_version = version.get("short_version")
        if short_version in version_to_date:
            version["release_date"] = version_to_date[short_version]
            updated_count += 1
            print(f"已更新版本 {short_version} 的发布日期: {version_to_date[short_version]}")
        else:
            print(f"未找到版本 {short_version} 的发布日期")
    
    print(f"总共更新了 {updated_count} 个版本的发布日期")
    
    # 保存更新后的文件
    save_json_file(version_file_path, version_data)
    return True

def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description='更新版本文件中的发布日期',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 update_version_dates.py 440948110    # 更新快手的版本日期
  python3 update_version_dates.py 1142110895   # 更新抖音的版本日期
        """
    )
    parser.add_argument('app_id', nargs='?', help='App ID (例如: 440948110)')
    
    args = parser.parse_args()
    
    # 如果没有传入参数，显示帮助和常见App列表
    if args.app_id is None:
        parser.print_help()
        show_common_apps()
        sys.exit(0)
    
    # 调用更新函数
    success = update_version_dates(args.app_id)
    
    if success:
        print("更新完成！")
        sys.exit(0)
    else:
        print("更新失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 