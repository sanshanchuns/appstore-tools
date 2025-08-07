#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import argparse
import subprocess

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

def get_latest_version_from_history(history_data):
    """从历史数据中获取最新版本号"""
    try:
        # data是一个数组，取第一个元素
        data_item = history_data.get("data", [{}])[0]
        version_history = data_item.get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
        if version_history:
            # 返回第一个版本（通常是最新的）
            return version_history[0].get("versionDisplay")
    except (IndexError, KeyError):
        pass
    return None

def get_latest_version_from_latest_file(latest_data):
    """从latest文件中获取最新版本号"""
    try:
        versions = latest_data.get("versions", [])
        if versions:
            # 返回第一个版本（通常是最新的）
            return versions[0].get("short_version")
    except (IndexError, KeyError):
        pass
    return None

def is_latest_version_has_release_date(latest_data):
    """检查latest文件中的最新版本是否已有release_date"""
    try:
        versions = latest_data.get("versions", [])
        if versions:
            latest_version = versions[0]
            return "release_date" in latest_version and latest_version["release_date"]
    except (IndexError, KeyError):
        pass
    return False

def check_history_file_is_current(app_id):
    """检查history文件是否存在且包含最新版本"""
    history_json_path = f"version_input/ios_appstore_history_{app_id}.json"
    
    if not os.path.exists(history_json_path):
        print(f"📄 History文件不存在: {history_json_path}")
        return False, None
    
    print(f"📄 检查History文件: {history_json_path}")
    history_data = load_json_file(history_json_path)
    if not history_data:
        print("❌ 无法加载History文件")
        return False, None
    
    latest_version = get_latest_version_from_history(history_data)
    if latest_version:
        print(f"✅ History文件包含最新版本: {latest_version}")
        return True, history_data
    else:
        print("❌ History文件中未找到版本信息")
        return False, None

def check_latest_file_needs_update(app_id):
    """检查latest文件是否需要更新"""
    version_file_path = f"version_output/app_{app_id}_latest_100.json"
    
    if not os.path.exists(version_file_path):
        print(f"📄 Latest文件不存在: {version_file_path}")
        return True, None
    
    print(f"📄 检查Latest文件: {version_file_path}")
    latest_data = load_json_file(version_file_path)
    if not latest_data:
        print("❌ 无法加载Latest文件")
        return True, None
    
    # 检查最新版本是否已有release_date
    if is_latest_version_has_release_date(latest_data):
        latest_version = get_latest_version_from_latest_file(latest_data)
        print(f"✅ Latest文件已是最新且包含发布日期: {latest_version}")
        return False, latest_data
    else:
        print("⚠️  Latest文件需要更新发布日期")
        return True, latest_data

def fetch_app_history(app_id):
    """获取App的历史版本数据"""
    print(f"🔄 正在获取App ID {app_id} 的历史版本数据...")
    
    # 构建curl命令
    curl_command = [
        'curl',
        '-H', 'Host: amp-api-edge.apps.apple.com',
        '-H', 'X-Apple-Tz: 28800',
        '-H', 'Authorization: Bearer eyJraWQiOiJGNDdEWk4xOEYwIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJBUzI4UjdHMTdNIiwiaWF0IjoxNzU0NTczMTExLCJleHAiOjE3NTcxNjUxMTEsImRzaWQiOiIxNjU4NTc0NDcwIiwibWlkIjoiMGNDeW16ak1TNUo3YlcvMW8vSGJvZUw4V21JPSJ9.dWWr2mx9tITYt14uS-G6JFCAvVhWoVL5K1xdVu95e2oeszC1pB0GblODoDSlRZz7LEKzDXlQ5mJrq7pG7zNlbw',
        '-H', 'X-Apple-Store-Front: 143465-19,29 t:apps3',
        '-H', 'Accept: */*',
        '-H', 'X-Apple-I-MD-RINFO: 50660608',
        '-H', 'Accept-Language: zh-Hans-CN',
        '-H', 'X-Apple-Client-Application: com.apple.AppStore',
        '-H', 'X-Apple-I-MD-M: 0cCymzjMS5J7bW/1o/HboeL8WmJ+F+3UlvX6wrvF5T4eFm5ZIVtJHs5DY+ktlxMPT3zNRkpD72jxrBPs',
        '-H', 'X-Apple-I-TimeZone: GMT+8',
        '-H', 'X-Apple-I-MD: AAAABQAAABBHRnUWJRg/0neCWQO4ueFAAAAAAw==',
        '-H', 'X-Apple-I-Client-Time: 2025-08-07T13:27:49Z',
        '-H', 'X-Apple-ADSID: 000620-05-128b6733-47c6-4bf8-9dfc-efde2924bf3a',
        '-H', 'User-Agent: AppStore/3.0 iOS/14.2 model/iPhone10,3 hwp/t8015 build/18B92 (6; dt:159) AMS/1',
        '-H', 'X-DSID: 1658574470',
        '-H', 'Cookie: X-Dsid=1658574470; xt-b-ts-1658574470=1754573110022; itspod=59; pldfltcid=d7b308d236bd453ea2233f23e27705f1059; tv-pldfltcid=d7b308d236bd453ea2233f23e27705f1059; mz_at0-1658574470=AwQAAAGfAAIjqAAAAABolKk29fzw30Uz4c+z7FLVJrhDR+8JMjI=; xp_ab=1#fNPb5Km+-2+xSb5Dsb01#of2rI6Z+-2+EcaH_Qo01#d5VBr6w+-2+NQRqfVj00#Zh4zkDd+-2+IstHuDt01#QVJEGsa+-2+ulL46Uv01; mz_at_ssl-1658574470=AwUAAAGfAAIjqAAAAABolKk2GnXNL+j6HMBx/js7AeuhH/bAo04=; isPpuOptOut=1; vrep=CIat75YGEgQIAxAAEgQIChAAEgQIDRAAEgQIARAAEgQIDBAAEgQICxAAEgQIDhAAEgQIEhAAEgQIBBAAEgQIBRAAEgQIAhAAEgQIBhAAEgQIDxAAEgQIEBAAEgQICRAAEgQIExAAEgQICBAAEgQIBxAAEgQIERAA; wosid-lite=bCC1t1gvDi1bRIFnxx2YiM',
        '-H', 'X-Apple-I-Locale: zh_CN',
        '--compressed',
        f'https://amp-api-edge.apps.apple.com/v1/catalog/cn/apps/{app_id}?platform=iphone&additionalPlatforms=appletv%2Cipad%2Cmac%2Cwatch&extend=versionHistory&l=zh-Hans-CN'
    ]
    
    try:
        # 执行curl命令
        result = subprocess.run(curl_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 解析JSON响应
            data = json.loads(result.stdout)
            
            # 检查是否包含versionHistory
            data_item = data.get("data", [{}])[0]
            version_history = data_item.get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
            
            if version_history:
                print(f"✅ 成功获取到 {len(version_history)} 个版本历史记录")
                return data
            else:
                print("❌ 响应中未找到versionHistory数据")
                return None
                
        else:
            print(f"❌ 请求失败: {result.stderr}")
            print(f"返回码: {result.returncode}")
            return None
            
    except json.JSONDecodeError as e:
        print(f"❌ 响应不是有效的JSON格式: {e}")
        print(f"响应内容: {result.stdout[:200]}...")
        return None
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return None

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

def update_version_dates(app_id, fetch_history=False, force_update=False):
    """更新版本文件中的发布日期"""
    
    print(f"🔍 开始处理App ID: {app_id}")
    print("=" * 60)
    
    # 检查history文件是否需要更新
    history_is_current, history_data = check_history_file_is_current(app_id)
    
    # 如果需要获取历史数据且history文件不是最新的
    if fetch_history and not history_is_current:
        print(f"📥 History文件需要更新，正在获取最新数据...")
        
        # 确保目录存在
        os.makedirs("version_input", exist_ok=True)
        
        # 获取历史数据
        history_data = fetch_app_history(app_id)
        if history_data:
            # 保存历史数据文件
            history_json_path = f"version_input/ios_appstore_history_{app_id}.json"
            save_json_file(history_json_path, history_data)
        else:
            print("❌ 获取历史数据失败")
            return False
    elif not history_is_current:
        print("❌ History文件不存在或不是最新的")
        print("💡 提示: 使用 --fetch 参数可以自动获取历史数据")
        return False
    
    # 检查latest文件是否需要更新
    latest_needs_update, latest_data = check_latest_file_needs_update(app_id)
    
    if not latest_needs_update and not force_update:
        print("✅ 所有文件都是最新的，无需更新")
        return True
    
    if not latest_data:
        print("❌ 无法加载Latest文件")
        return False
    
    # 从嵌套结构中提取versionHistory
    try:
        # data是一个数组，取第一个元素
        data_item = history_data.get("data", [{}])[0]
        version_history = data_item.get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
    except (IndexError, KeyError):
        print("❌ 无法找到versionHistory字段")
        return False
    
    if not version_history:
        print("❌ 未找到versionHistory数据")
        return False
    
    print(f"✅ 找到 {len(version_history)} 个版本历史记录")
    
    # 创建版本号到发布日期的映射
    version_to_date = {}
    for item in version_history:
        version_display = item.get("versionDisplay")
        release_date = item.get("releaseDate")
        if version_display and release_date:
            version_to_date[version_display] = release_date
    
    print(f"✅ 创建了 {len(version_to_date)} 个版本号到日期的映射")
    
    # 更新版本文件中的每个版本
    updated_count = 0
    for version in latest_data.get("versions", []):
        short_version = version.get("short_version")
        if short_version in version_to_date:
            # 检查是否已经有release_date且不是强制更新
            if "release_date" in version and version["release_date"] and not force_update:
                print(f"⏭️  跳过版本 {short_version} (已有发布日期: {version['release_date']})")
                continue
            
            version["release_date"] = version_to_date[short_version]
            updated_count += 1
            print(f"✅ 已更新版本 {short_version} 的发布日期: {version_to_date[short_version]}")
        else:
            print(f"⚠️  未找到版本 {short_version} 的发布日期")
    
    print(f"✅ 总共更新了 {updated_count} 个版本的发布日期")
    
    # 保存更新后的文件
    version_file_path = f"version_output/app_{app_id}_latest_100.json"
    save_json_file(version_file_path, latest_data)
    return True

def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description='更新版本文件中的发布日期',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 update_version_dates.py 440948110                    # 更新快手的版本日期
  python3 update_version_dates.py 1142110895 --fetch          # 获取历史数据并更新抖音的版本日期
  python3 update_version_dates.py 414478124 -f                # 获取历史数据并更新微信的版本日期
  python3 update_version_dates.py 440948110 --force           # 强制更新所有版本日期
        """
    )
    parser.add_argument('app_id', nargs='?', help='App ID (例如: 440948110)')
    parser.add_argument('-f', '--fetch', action='store_true', 
                       help='如果历史数据文件不存在或不是最新的，自动获取历史数据')
    parser.add_argument('--force', action='store_true',
                       help='强制更新所有版本日期，即使已有发布日期')
    
    args = parser.parse_args()
    
    # 如果没有传入参数，显示帮助和常见App列表
    if args.app_id is None:
        parser.print_help()
        show_common_apps()
        sys.exit(0)
    
    # 调用更新函数
    success = update_version_dates(args.app_id, args.fetch, args.force)
    
    if success:
        print("🎉 处理完成！")
        sys.exit(0)
    else:
        print("❌ 处理失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 