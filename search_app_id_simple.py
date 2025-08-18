#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import subprocess
import json
import sys
import argparse

def search_app_id_simple(app_name, limit=1):
    """通过App Store搜索API获取App ID（简化版本）"""
    
    # URL编码搜索关键词
    encoded_term = urllib.parse.quote(app_name)
    
    # 使用原始的完整URL，但只提取必要信息
    curl_command = [
        'curl',
        '-H', 'Host: amp-api-search-edge.apps.apple.com',
        '-H', 'Cookie: X-Dsid=1658574470; xt-b-ts-1658574470=1754573110022; itspod=59; pldfltcid=d7b308d236bd453ea2233f23e27705f1059; tv-pldfltcid=d7b308d236bd453ea2233f23e27705f1059; mz_at0-1658574470=AwQAAAGfAAIjqAAAAABolKk29fzw30Uz4c+z7FLVJrhDR+8JMjI=; xp_ab=1#fNPb5Km+-2+xSb5Dsb01#of2rI6Z+-2+EcaH_Qo01#d5VBr6w+-2+NQRqfVj00#Zh4zkDd+-2+IstHuDt01#QVJEGsa+-2+ulL46Uv01; mz_at_ssl-1658574470=AwUAAAGfAAIjqAAAAABolKk2GnXNL+j6HMBx/js7AeuhH/bAo04=; isPpuOptOut=1; vrep=CIat75YGEgQIAxAAEgQIChAAEgQIDRAAEgQIARAAEgQIDBAAEgQICxAAEgQIDhAAEgQIEhAAEgQIBBAAEgQIBRAAEgQIAhAAEgQIBhAAEgQIDxAAEgQIEBAAEgQICRAAEgQIExAAEgQICBAAEgQIBxAAEgQIERAA; wosid-lite=bCC1t1gvDi1bRIFnxx2YiM',
        '-H', 'User-Agent: AppStore/3.0 iOS/14.2 model/iPhone10,3 hwp/t8015 build/18B92 (6; dt:159) AMS/1',
        '-H', 'X-Apple-Store-Front: 143465-19,29 t:apps3',
        '-H', 'X-Apple-iAd-Request-Data: AAAAAAAAAAA=',
        '-H', 'X-DSID: 1658574470',
        '-H', 'X-Apple-Tz: 28800',
        '-H', 'X-Apple-iAd-Env-Name: AAAAAAAAAEQKAlNTEjlodHRwczovL3RyLmlhZHNkay5hcHBsZS5jb20vYWRzZXJ2ZXIvMi42L3Nwb25zb3JlZC9zZWFyY2gaAzIuNg==',
        '-H', 'X-Apple-Client-Application: com.apple.AppStore',
        '-H', 'X-Apple-I-TimeZone: GMT+8',
        '-H', 'X-Apple-I-Client-Time: 2025-08-07T13:26:26Z',
        '-H', 'X-Apple-App-Store-Client-Request-Id: 4FD51B60-3FC3-4E55-9E04-1E0391765C33',
        '-H', 'Authorization: Bearer eyJraWQiOiJGNDdEWk4xOEYwIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJBUzI4UjdHMTdNIiwiaWF0IjoxNzU0NTczMTExLCJleHAiOjE3NTcxNjUxMTEsImRzaWQiOiIxNjU4NTc0NDcwIiwibWlkIjoiMGNDeW16ak1TNUo3YlcvMW8vSGJvZUw4V21JPSJ9.dWWr2mx9tITYt14uS-G6JFCAvVhWoVL5K1xdVu95e2oeszC1pB0GblODoDSlRZz7LEKzDXlQ5mJrq7pG7zNlbw',
        '-H', 'Accept-Language: zh-Hans-CN',
        '-H', 'X-Apple-I-MD-RINFO: 50660608',
        '-H', 'X-Apple-ADSID: 000620-05-128b6733-47c6-4bf8-9dfc-efde2924bf3a',
        '-H', 'Accept: */*',
        '-H', 'X-Apple-I-MD-M: 0cCymzjMS5J7bW/1o/HboeL8WmJ+F+3UlvX6wrvF5T4eFm5ZIVtJHs5DY+ktlxMPT3zNRkpD72jxrBPs',
        '-H', 'X-Apple-I-Locale: zh_CN',
        '-H', 'X-Apple-I-MD: AAAABQAAABCUdZTb0BBB3R90qEqRMGquAAAAAw==',
        '--compressed',
        # 使用原始完整URL
        f'https://amp-api-search-edge.apps.apple.com/v1/catalog/cn/search?platform=iphone&additionalPlatforms=appletv%2Cipad%2Cmac%2Cwatch&extend=editorialBadgeInfo%2CmessagesScreenshots%2CminimumOSVersion%2CrequiredCapabilities%2CscreenshotsByType%2CsupportsFunCamera%2CvideoPreviewsByType&extend%5Beditorial-items%5D=showLabelInSearch&include=apps%2Ctop-apps&include%5Beditorial-items%5D=marketing-items&meta%5Bmarketing-items%5D=metrics&src=hint&limit%5Bads-result%5D=4&bubble%5Bsearch%5D=apps%2Cdevelopers%2Cgroupings%2Ceditorial-items%2Capp-bundles%2Cin-apps&term={encoded_term}&with=spellCheck&l=zh-Hans-CN'
    ]
    
    print(f"🔍 正在搜索: {app_name}")
    print(f"📝 搜索关键词: {encoded_term}")
    print(f"📊 显示结果数量: {limit}")
    print("=" * 60)
    
    try:
        # 执行curl命令
        result = subprocess.run(curl_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 解析JSON响应
            data = json.loads(result.stdout)
            
            # 提取搜索结果 - 修正数据结构路径
            results = data.get('results', {})
            search_result = results.get('search', {})
            apps = search_result.get('data', [])
            
            if apps:
                total_found = len(apps)
                display_count = min(limit, total_found)
                
                print(f"✅ 找到 {total_found} 个结果，显示前 {display_count} 个:")
                print("-" * 60)
                
                # 显示指定数量的结果
                for i, app in enumerate(apps[:limit], 1):
                    attributes = app.get('attributes', {})
                    app_id = app.get('id')
                    name = attributes.get('name', '未知')
                    artist = attributes.get('artistName', '未知')
                    
                    print(f"{i}. {name}")
                    print(f"   📱 App ID: {app_id}")
                    print(f"   👨‍💻 开发者: {artist}")
                    print()
                
                # 返回第一个结果的ID
                if apps:
                    first_app = apps[0]
                    first_app_id = first_app.get('id')
                    first_app_name = first_app.get('attributes', {}).get('name', '未知')
                    print(f"🎯 推荐使用: {first_app_name} (ID: {first_app_id})")
                    return first_app_id
            else:
                print("❌ 未找到相关App")
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

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='通过App Store搜索API获取App ID',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 search_app_id_simple.py 抖音                    # 默认只显示第一个结果
  python3 search_app_id_simple.py 抖音 -l 3              # 显示前3个结果
  python3 search_app_id_simple.py 微信 --limit 5         # 显示前5个结果
        """
    )
    parser.add_argument('app_name', help='要搜索的App名称')
    parser.add_argument('-l', '--limit', type=int, default=1, 
                       help='显示结果数量 (默认: 1)')
    
    args = parser.parse_args()
    
    # 验证参数
    if args.limit < 1:
        print("❌ 错误: 显示数量必须大于0")
        sys.exit(1)
    
    app_id = search_app_id_simple(args.app_name, args.limit)
    
    if app_id:
        print(f"\n💡 你可以使用以下命令更新版本日期:")
        print(f"python3 update_version_dates.py {app_id}")
    else:
        print("\n❌ 无法获取App ID，请检查App名称是否正确")

if __name__ == "__main__":
    main() 