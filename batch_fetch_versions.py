#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量获取快手不同版本信息的脚本
使用softwareVersionExternalIdentifier来获取不同版本
"""

import subprocess
import json
import os
import time
from typing import List, Dict
import argparse
import re
import xml.etree.ElementTree as ET

class iOSAppStoreParser:
    def __init__(self, xml_file: str):
        try:
            self.tree = ET.parse(xml_file)
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            print(f"XML解析错误: {e}")
            print(f"XML文件: {xml_file}")
            # 尝试读取文件内容的前几行来调试
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"XML文件内容前500字符: {content[:500]}")
            except Exception as read_error:
                print(f"无法读取XML文件: {read_error}")
            raise
    
    def find_version_info(self) -> Dict:
        """查找版本信息"""
        app_info = self.parse_app_info()
        thinned_app = self.parse_thinned_app_info()
        
        return {
            'app_info': app_info,
            'thinned_app': thinned_app
        }
    
    def parse_app_info(self) -> Dict:
        """解析应用信息"""
        app_info = {}
        
        # 根据XML结构，根元素是 <plist>，其第一个子元素是 <dict>
        # 我们需要访问 self.root[0] 来获取主要的dict元素
        main_dict = self.root[0]
        
        for i, child in enumerate(main_dict):
            if child.tag == 'key' and child.text == 'songList':
                song_list_idx = list(main_dict).index(child)
                if song_list_idx + 1 < len(main_dict):
                    song_list = main_dict[song_list_idx + 1]
                    if song_list.tag == 'array' and len(song_list) > 0:
                        first_song = song_list[0]
                        if first_song.tag == 'dict':
                            for i, elem in enumerate(first_song):
                                if elem.tag == 'key' and elem.text == 'metadata':
                                    if i + 1 < len(first_song):
                                        metadata = first_song[i + 1]
                                        if metadata.tag == 'dict':
                                            for j, meta_elem in enumerate(metadata):
                                                if meta_elem.tag == 'key':
                                                    key_name = meta_elem.text
                                                    if j + 1 < len(metadata):
                                                        value_elem = metadata[j + 1]
                                                        if key_name == 'bundleDisplayName':
                                                            app_info['app_name'] = value_elem.text
                                                        elif key_name == 'bundleVersion':
                                                            app_info['bundle_version'] = value_elem.text
                                                        elif key_name == 'bundleShortVersionString':
                                                            app_info['short_version'] = value_elem.text
                                                        elif key_name == 'itemId':
                                                            app_info['item_id'] = value_elem.text
                                                        elif key_name == 'softwareVersionExternalIdentifier':
                                                            app_info['software_version_external_identifier'] = value_elem.text
                                                        elif key_name == 'softwareVersionExternalIdentifiers':
                                                            if value_elem.tag == 'array':
                                                                app_info['software_version_external_identifiers'] = [e.text for e in value_elem if e.text]
                                    break
                break
        return app_info
    
    def parse_thinned_app_info(self) -> Dict:
        """解析thinned-app信息"""
        thinned_app_info = {}
        
        # 根据XML结构，根元素是 <plist>，其第一个子元素是 <dict>
        main_dict = self.root[0]
        
        for child in main_dict:
            if child.tag == 'key' and child.text == 'songList':
                song_list_idx = list(main_dict).index(child)
                if song_list_idx + 1 < len(main_dict):
                    song_list = main_dict[song_list_idx + 1]
                    if song_list.tag == 'array':
                        for song in song_list:
                            if song.tag == 'dict':
                                for i, elem in enumerate(song):
                                    if elem.tag == 'key' and elem.text == 'thinned-app':
                                        if i + 1 < len(song):
                                            thinned_app = song[i + 1]
                                            if thinned_app.tag == 'dict':
                                                for j, thinned_elem in enumerate(thinned_app):
                                                    if thinned_elem.tag == 'key':
                                                        key_name = thinned_elem.text
                                                        if j + 1 < len(thinned_app):
                                                            value_elem = thinned_app[j + 1]
                                                            if key_name == 'variantId':
                                                                thinned_app_info['variant_id'] = value_elem.text
                                                            elif key_name == 'URL':
                                                                thinned_app_info['download_url'] = value_elem.text
                                                            elif key_name == 'uncompressedSize':
                                                                thinned_app_info['uncompressed_size'] = int(value_elem.text)
                                                            elif key_name == 'md5':
                                                                thinned_app_info['md5'] = value_elem.text
                                                            elif key_name == 'asset-info':
                                                                if value_elem.tag == 'dict':
                                                                    for k, asset_elem in enumerate(value_elem):
                                                                        if asset_elem.tag == 'key' and asset_elem.text == 'file-size':
                                                                            if k + 1 < len(value_elem):
                                                                                file_size_elem = value_elem[k + 1]
                                                                                thinned_app_info['download_size'] = int(file_size_elem.text)
                                                                                thinned_app_info['appstore_display_size'] = self.format_appstore_size(int(file_size_elem.text))
                                        break
                                break
                break
        return thinned_app_info
    
    def format_appstore_size(self, size_bytes: int) -> str:
        """格式化AppStore显示大小（1000进制）"""
        return f"{round(size_bytes / (1000 * 1000))}M"

class BatchVersionFetcher:
    def __init__(self, app_id: str = "440948110"):
        self.app_id = app_id
        self.salable_adam_id = app_id
    
    def update_ios_appstore_parsed_json(self):
        """
        自动更新 ios_appstore_parsed.json，如果本地不是最新则覆盖。
        """
        # 确保 version_input 目录存在
        version_input_dir = "version_input"
        if not os.path.exists(version_input_dir):
            os.makedirs(version_input_dir)
            
        temp_xml = 'latest_temp.xml'
        try:
            # 直接调用fetch_app_xml.sh，只传app_id获取最新版本
            result = subprocess.run(['bash', 'fetch_app_xml.sh', self.app_id],
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"获取最新XML失败: {result.stderr}")
                return False
            
            # 检查返回的内容是否为空或无效
            if not result.stdout.strip():
                print("获取最新XML返回空内容")
                return False
            
            # 检查返回的内容是否包含错误
            if 'failureType' in result.stdout and '1010' in result.stdout:
                print(f"警告: Apple接口返回错误 (failureType: 1010)，可能接口已过期或需要更新认证信息")
                print("跳过自动更新，使用本地JSON文件")
                return True
            
            with open(temp_xml, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            # 2. 解析出software_version_external_identifier
            parser = iOSAppStoreParser(temp_xml)
            latest_info = parser.find_version_info()
            latest_id = latest_info['app_info']['software_version_external_identifier']
            # 3. 读取本地json
            json_filename = os.path.join(version_input_dir, f'ios_appstore_parsed_{self.app_id}.json')
            if os.path.exists(json_filename):
                with open(json_filename, 'r', encoding='utf-8') as f:
                    local_id = json.load(f)['app_info']['software_version_external_identifier']
            else:
                local_id = None
            # 4. 判断是否需要更新
            if latest_id != local_id:
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(latest_info, f, ensure_ascii=False, indent=2)
                print(f"已更新 {json_filename}")
            else:
                print(f"本地 {json_filename} 已是最新")
        except Exception as e:
            print(f"更新过程中出错: {e}")
            print("跳过自动更新，使用本地JSON文件")
            return True
        finally:
            if os.path.exists(temp_xml):
                os.remove(temp_xml)
    
    def fetch_single_version(self, app_ext_vrs_id: str) -> Dict:
        """
        获取单个版本的信息
        
        Args:
            app_ext_vrs_id: 版本的appExtVrsId
            
        Returns:
            Dict: 版本信息
        """
        # 创建xml_files目录
        xml_dir = "xml_files"
        if not os.path.exists(xml_dir):
            os.makedirs(xml_dir)
        
        # 生成XML文件名
        xml_file = os.path.join(xml_dir, f"app_{self.app_id}_{app_ext_vrs_id}.xml")
        
        # 检查XML文件是否已存在
        if os.path.exists(xml_file):
            print(f"版本 {app_ext_vrs_id} 的XML文件已存在，直接读取...")
        else:
            print(f"版本 {app_ext_vrs_id} 的XML文件不存在，正在获取...")
            try:
                # 直接调用fetch_app_xml.sh，传app_id和版本id
                result = subprocess.run(['bash', 'fetch_app_xml.sh', self.app_id, app_ext_vrs_id], 
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    print(f"获取版本 {app_ext_vrs_id} 失败: {result.stderr}")
                    return None
                
                # 检查返回的内容是否为空或无效
                if not result.stdout.strip():
                    print(f"获取版本 {app_ext_vrs_id} 返回空内容")
                    return None
                
                # 检查返回的内容是否包含错误
                if 'failureType' in result.stdout and '1010' in result.stdout:
                    print(f"警告: Apple接口返回错误 (failureType: 1010)，可能接口已过期或需要更新认证信息")
                    print(f"无法获取版本 {app_ext_vrs_id} 的信息")
                    return None
                
                # 保存XML到xml_files目录
                with open(xml_file, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                    
            except subprocess.TimeoutExpired:
                print(f"获取版本 {app_ext_vrs_id} 超时")
                return None
            except Exception as e:
                print(f"获取版本 {app_ext_vrs_id} 出错: {e}")
                return None
        
        # 解析XML（无论是新获取的还是已存在的）
        try:
            parser = iOSAppStoreParser(xml_file)
            version_info = parser.find_version_info()
            
            if version_info and version_info.get('app_info'):
                app_info = version_info.get('app_info', {})
                
                # 检查返回的版本ID是否与请求的版本ID匹配
                returned_version_id = app_info.get('software_version_external_identifier')
                if returned_version_id != app_ext_vrs_id:
                    print(f"版本 {app_ext_vrs_id} 不存在，返回的是版本 {returned_version_id} 的数据")
                    # 删除无效的XML文件
                    if os.path.exists(xml_file):
                        os.remove(xml_file)
                        print(f"已删除无效的XML文件: {xml_file}")
                    return None
                
                # 合并app_info和thinned_app为一个对象
                app_info = app_info.copy()
                thinned_app = version_info.get('thinned_app', {}).copy()
                
                # 将app_ext_vrs_id添加到合并后的对象中
                app_info['app_ext_vrs_id'] = app_ext_vrs_id
                
                # 移除不需要的字段（保留app_name和item_id用于顶层保存）
                for field in ['software_version_external_identifiers', 'software_version_external_identifier']:
                    if field in app_info:
                        del app_info[field]
                
                # 移除variant_id（无意义字段）
                if 'variant_id' in thinned_app:
                    del thinned_app['variant_id']
                
                # 合并两个字典
                merged_version_data = {**app_info, **thinned_app}
                
                print(f"成功解析版本 {app_ext_vrs_id} 信息")
                return merged_version_data
            else:
                print(f"版本 {app_ext_vrs_id} 解析失败")
                # 尝试读取XML文件内容来调试
                try:
                    with open(xml_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"XML文件内容前1000字符: {content[:1000]}")
                except Exception as read_error:
                    print(f"无法读取XML文件: {read_error}")
                # 如果解析失败，删除无效的XML文件
                if os.path.exists(xml_file):
                    os.remove(xml_file)
                    print(f"已删除无效的XML文件: {xml_file}")
                return None
                
        except Exception as e:
            print(f"解析版本 {app_ext_vrs_id} 出错: {e}")
            # 尝试读取XML文件内容来调试
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"XML文件内容前1000字符: {content[:1000]}")
            except Exception as read_error:
                print(f"无法读取XML文件: {read_error}")
            # 如果解析出错，删除无效的XML文件
            if os.path.exists(xml_file):
                os.remove(xml_file)
                print(f"已删除无效的XML文件: {xml_file}")
            return None
    
    def fetch_multiple_versions(self, app_ext_vrs_ids: List[str]) -> List[Dict]:
        """
        批量获取多个版本的信息
        
        Args:
            app_ext_vrs_ids: 版本ID列表
            
        Returns:
            List[Dict]: 版本信息列表
        """
        versions_data = []
        total = len(app_ext_vrs_ids)
        
        for i, app_ext_vrs_id in enumerate(app_ext_vrs_ids, 1):
            print(f"进度: {i}/{total}")
            version_data = self.fetch_single_version(app_ext_vrs_id)
            if version_data:
                versions_data.append(version_data)
        
        return versions_data
    
    def save_to_json(self, versions_data: List[Dict], output_file: str = "versions.json"):
        """
        保存版本信息到JSON文件
        
        Args:
            versions_data: 版本信息列表
            output_file: 输出文件路径
        """
        if not versions_data:
            print("没有版本数据可保存")
            return
        
        # 从第一个版本获取app_name和item_id（所有版本都一样）
        first_version = versions_data[0]
        app_name = first_version.get('app_name', '')
        item_id = first_version.get('item_id', '')
        
        # 从所有版本的app_info中移除app_name和item_id（避免重复）
        for version in versions_data:
            if 'app_name' in version:
                del version['app_name']
            if 'item_id' in version:
                del version['item_id']
        
        # 倒排versions数组，最新的版本放在第一位
        versions_data.reverse()
        
        output_data = {
            'app_name': app_name,
            'item_id': item_id,
            'total_versions': len(versions_data),
            'versions': versions_data
        }
        
        # 确保 version_output 目录存在
        version_output_dir = "version_output"
        if not os.path.exists(version_output_dir):
            os.makedirs(version_output_dir)

        with open(os.path.join(version_output_dir, output_file), 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n版本信息已保存到: {os.path.join(version_output_dir, output_file)}")
        print(f"总共获取了 {len(versions_data)} 个版本的信息")

    def generate_ios_appstore_parsed_json(self):
        """
        自动生成一个新的 ios_appstore_parsed_{app_id}.json 文件
        通过curl命令获取最新版本的XML，解析后生成JSON
        """
        # 确保 version_input 目录存在
        version_input_dir = "version_input"
        if not os.path.exists(version_input_dir):
            os.makedirs(version_input_dir)
            
        temp_xml = f'latest_{self.app_id}.xml'
        
        # 直接调用fetch_app_xml.sh，只传app_id（获取最新版本）
        try:
            result = subprocess.run(['bash', 'fetch_app_xml.sh', self.app_id], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"获取最新XML失败: {result.stderr}")
                return False
            
            # 检查返回的内容是否包含错误
            if 'failureType' in result.stdout and '1010' in result.stdout:
                print(f"警告: Apple接口返回错误 (failureType: 1010)，可能接口已过期或需要更新认证信息")
                print(f"无法为App ID {self.app_id} 生成JSON文件")
                return False
            
            # 保存XML到临时文件
            with open(temp_xml, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            # 解析XML生成JSON
            try:
                parser = iOSAppStoreParser(temp_xml)
                latest_info = parser.find_version_info()
                
                if latest_info and latest_info.get('app_info'):
                    # 保存为JSON文件
                    json_filename = os.path.join(version_input_dir, f'ios_appstore_parsed_{self.app_id}.json')
                    with open(json_filename, 'w', encoding='utf-8') as f:
                        json.dump(latest_info, f, ensure_ascii=False, indent=2)
                    print(f"已生成 {json_filename}")
                    return True
                else:
                    print(f"解析XML失败，无法生成JSON文件")
                    print(f"解析结果: {latest_info}")
                    return False
                    
            except Exception as e:
                print(f"解析XML出错: {e}")
                return False
                
        except Exception as e:
            print(f"生成JSON文件过程中出错: {e}")
            return False
        finally:
            # 清理临时文件
            if os.path.exists(temp_xml):
                os.remove(temp_xml)

def main():
    parser = argparse.ArgumentParser(description="App Store版本信息批量获取工具")
    parser.add_argument('--app_id', type=str, required=True, help='App Store ID，必填')
    parser.add_argument('--latest', type=int, help='获取最近N个版本')
    parser.add_argument('--ids', type=str, help='获取指定版本ID，多个用逗号分隔')
    import sys
    if len(sys.argv) == 1:
        parser.print_help()
        print("""
示例用法：
  python3 batch_fetch_versions.py --app_id 440948110 --latest 1
  python3 batch_fetch_versions.py --app_id 440948110 --latest 100
  python3 batch_fetch_versions.py --app_id 1142110895 --latest 1
  python3 batch_fetch_versions.py --app_id 1142110895 --ids 876763609,876573499
        """)
        return
    args = parser.parse_args()

    # 创建批量获取器
    fetcher = BatchVersionFetcher(args.app_id)
    
    # 自动更新本地JSON文件
    fetcher.update_ios_appstore_parsed_json()

    # 读取所有版本ID
    json_filename = os.path.join("version_input", f'ios_appstore_parsed_{args.app_id}.json')
    if not os.path.exists(json_filename):
        print(f"未找到 {json_filename}，正在自动生成...")
        # 自动生成JSON文件
        fetcher.generate_ios_appstore_parsed_json()
        if not os.path.exists(json_filename):
            print(f"错误: 无法生成 {json_filename}")
            return
        print(f"已生成 {json_filename}")
    
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    version_ids = data['app_info']['software_version_external_identifiers']
    current_version = data['app_info']['software_version_external_identifier']
    app_name = data['app_info']['app_name']
    print(f"App: {app_name}")
    print(f"从JSON文件中读取到 {len(version_ids)} 个版本ID")
    print(f"当前版本ID: {current_version}")

    # 参数优先级：--ids > --latest > 默认最新版本
    if args.ids:
        version_ids = [vid.strip() for vid in args.ids.split(',') if vid.strip()]
        print(f"获取指定版本: {version_ids}")
    elif args.latest:
        version_ids = version_ids[-args.latest:]
        print(f"获取最近的{args.latest}个版本: {version_ids}")
    else:
        version_ids = [version_ids[-1]]
        print(f"获取最新版本: {version_ids}")

    # 批量获取版本信息
    versions_data = fetcher.fetch_multiple_versions(version_ids)

    if versions_data:
        # 保存到JSON文件
        if args.ids:
            out_name = f"app_{args.app_id}_ids_{'_'.join(version_ids)}.json"
        elif args.latest:
            out_name = f"app_{args.app_id}_latest_{args.latest}.json"
        else:
            out_name = f"app_{args.app_id}_latest.json"
        fetcher.save_to_json(versions_data, out_name)

        # 打印统计信息
        print("\n版本信息统计:")
        print("-" * 30)
        for i, version in enumerate(versions_data, 1):
            print(f"版本 {i}:")
            print(f"  版本ID: {version.get('app_ext_vrs_id', 'N/A')}")
            print(f"  版本号: {version.get('short_version', 'N/A')}")
            print(f"  Bundle版本: {version.get('bundle_version', 'N/A')}")
            print(f"  AppStore显示大小: {version.get('appstore_display_size', 'N/A')}")
            print(f"  下载大小: {version.get('download_size', 0) / (1024*1024):.2f} MB")
            print(f"  解压大小: {version.get('uncompressed_size', 0) / (1024*1024):.2f} MB")
            print()
        print(f"测试完成！获取了 {len(versions_data)} 个版本的信息")

if __name__ == "__main__":
    main() 