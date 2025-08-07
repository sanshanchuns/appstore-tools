#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS AppStore XML解析器 - 精简版本
用于解析通过curl命令获取的iOS AppStore上指定App的精简版应用信息
"""

import xml.etree.ElementTree as ET
import json
import sys
from typing import Dict, List, Optional, Tuple

class iOSAppStoreParser:
    def __init__(self, xml_file_path: str):
        """
        初始化解析器
        
        Args:
            xml_file_path: XML文件路径
        """
        self.xml_file_path = xml_file_path
        self.tree = None
        self.root = None
        
    def load_xml(self) -> bool:
        """
        加载XML文件
        
        Returns:
            bool: 加载是否成功
        """
        try:
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
            
            # 如果根元素是plist，则取第一个dict子元素作为实际根元素
            if self.root.tag == 'plist' and len(self.root) > 0:
                self.root = self.root[0]
            
            return True
        except Exception as e:
            print(f"加载XML文件失败: {e}")
            return False
    
    def debug_print_all_keys(self, elem, path='root'):
        """
        递归打印所有dict/array中的key路径，便于定位字段
        """
        if elem.tag == 'dict':
            children = list(elem)
            i = 0
            while i < len(children):
                if children[i].tag == 'key':
                    key_name = children[i].text
                    print(f"{path} -> {key_name}")
                    if i + 1 < len(children):
                        self.debug_print_all_keys(children[i + 1], path + f' -> {key_name}')
                    i += 2
                else:
                    i += 1
        elif elem.tag == 'array':
            for idx, child in enumerate(elem):
                self.debug_print_all_keys(child, path + f'[{idx}]')

    def parse_app_info(self) -> Dict:
        """
        解析应用基本信息
        
        Returns:
            Dict: 应用信息字典
        """
        app_info = {}
        for child in self.root:
            if child.tag == 'key' and child.text == 'songList':
                song_list_idx = list(self.root).index(child)
                if song_list_idx + 1 < len(self.root):
                    song_list = self.root[song_list_idx + 1]
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
                                                                app_info['software_version_external_identifiers'] = [v.text for v in value_elem if v.tag == 'integer']
        return app_info
    
    def parse_package_info(self, package_elem) -> Dict:
        """
        解析包信息
        
        Args:
            package_elem: 包元素
            
        Returns:
            Dict: 包信息
        """
        package_info = {}
        
        for i, elem in enumerate(package_elem):
            if elem.tag == 'key':
                key_name = elem.text
                if i + 1 < len(package_elem):
                    value_elem = package_elem[i + 1]
                    
                    if key_name == 'URL':
                        package_info['download_url'] = value_elem.text
                    elif key_name == 'uncompressedSize':
                        package_info['uncompressed_size'] = int(value_elem.text)
                    elif key_name == 'priorVersionBundleVersion':
                        package_info['prior_version_bundle'] = value_elem.text
                    elif key_name == 'priorVersionBundleShortVersionString':
                        package_info['prior_version_short'] = value_elem.text
                    elif key_name == 'md5':
                        package_info['md5'] = value_elem.text
                    elif key_name == 'variantId':
                        package_info['variant_id'] = value_elem.text
                    elif key_name == 'asset-info':
                        if value_elem.tag == 'dict':
                            for j, asset_elem in enumerate(value_elem):
                                if asset_elem.tag == 'key' and asset_elem.text == 'file-size':
                                    if j + 1 < len(value_elem):
                                        file_size_elem = value_elem[j + 1]
                                        package_info['download_size'] = int(file_size_elem.text)
        
        return package_info
    
    def parse_thinned_app_info(self) -> Dict:
        """
        解析精简版应用信息
        
        Returns:
            Dict: 精简版应用信息
        """
        thinned_app_info = {}
        # 查找songList中的thinned-app
        for child in self.root:
            if child.tag == 'key' and child.text == 'songList':
                song_list_idx = list(self.root).index(child)
                if song_list_idx + 1 < len(self.root):
                    song_list = self.root[song_list_idx + 1]
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
        # 添加AppStore显示大小（1000进制，取整数）
        if 'download_size' in thinned_app_info:
            appstore_display_size = int(int(thinned_app_info['download_size']) / 1_000_000)
            thinned_app_info['appstore_display_size'] = f"{appstore_display_size}M"
        return thinned_app_info
    
    def format_size(self, size_bytes: int) -> str:
        """
        格式化文件大小显示
        
        Args:
            size_bytes: 字节数
            
        Returns:
            str: 格式化后的大小字符串
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    
    def find_version_info(self, target_version: str = None) -> Dict:
        """
        查找指定版本的信息
        
        Args:
            target_version: 目标版本号，如果为None则显示所有版本
            
        Returns:
            Dict: 版本信息
        """
        if not self.load_xml():
            return {}
        
        result = {
            'app_info': self.parse_app_info(),
            'thinned_app': self.parse_thinned_app_info()
        }
        
        return result
    
    def find_specific_version(self, target_version: str) -> Dict:
        """
        查找指定版本的信息
        
        Args:
            target_version: 目标版本号（可以是短版本号或Bundle版本号）
            
        Returns:
            Dict: 指定版本的信息
        """
        info = self.find_version_info()
        
        if not info:
            return {}
        
        # 检查精简版应用版本
        app_info = info.get('app_info', {})
        thinned_app = info.get('thinned_app', {})
        
        if (app_info.get('short_version') == target_version or 
            app_info.get('bundle_version') == target_version):
            return {
                'type': 'thinned_app',
                'version': target_version,
                'download_size': thinned_app.get('download_size'),
                'uncompressed_size': thinned_app.get('uncompressed_size'),
                'md5': thinned_app.get('md5'),
                'download_url': thinned_app.get('download_url'),
                'variant_id': thinned_app.get('variant_id')
            }
        
        return {}
    
    def print_version_info(self, target_version: str = None):
        """
        打印版本信息
        
        Args:
            target_version: 目标版本号，如果为None则显示所有版本
        """
        if target_version:
            # 查找指定版本
            version_info = self.find_specific_version(target_version)
            if version_info:
                print(f"找到版本 {target_version} 的信息:")
                print(f"类型: {version_info['type']}")
                print(f"设备变体: {version_info.get('variant_id', 'N/A')}")
                print(f"下载大小: {self.format_size(version_info.get('download_size', 0))}")
                print(f"解压大小: {self.format_size(version_info.get('uncompressed_size', 0))}")
                print(f"MD5: {version_info.get('md5', 'N/A')}")
            else:
                print(f"未找到版本 {target_version} 的信息")
            return
        
        info = self.find_version_info(target_version)
        
        if not info:
            print("无法解析XML文件")
            return
        
        print("=" * 80)
        print("iOS AppStore 精简版应用信息解析结果")
        print("=" * 80)
        
        # 应用基本信息
        app_info = info.get('app_info', {})
        if app_info:
            print(f"应用名称: {app_info.get('app_name', 'N/A')}")
            print(f"Bundle版本: {app_info.get('bundle_version', 'N/A')}")
            print(f"短版本号: {app_info.get('short_version', 'N/A')}")
            print(f"应用ID: {app_info.get('item_id', 'N/A')}")
            print()
        
        # 精简版应用信息
        thinned_app = info.get('thinned_app', {})
        if thinned_app:
            print("精简版应用:")
            print(f"  设备变体: {thinned_app.get('variant_id', 'N/A')}")
            print(f"  AppStore显示大小: {thinned_app.get('appstore_display_size', 'N/A')}")
            print(f"  下载大小: {self.format_size(thinned_app.get('download_size', 0))}")
            print(f"  解压大小: {self.format_size(thinned_app.get('uncompressed_size', 0))}")
            print(f"  MD5: {thinned_app.get('md5', 'N/A')}")
            print()
        else:
            print("未找到精简版应用信息")
    
    def export_to_json(self, output_file: str = None):
        """
        导出解析结果到JSON文件
        
        Args:
            output_file: 输出文件路径，如果为None则使用默认路径
        """
        if output_file is None:
            output_file = "ios_appstore_parsed.json"
        
        info = self.find_version_info()
        if info:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                print(f"解析结果已导出到: {output_file}")
            except Exception as e:
                print(f"导出JSON文件失败: {e}")
        else:
            print("无法解析XML文件")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python parse_ios_appstore_clean.py <xml_file_path> [target_version] [output_json_file]")
        print("示例: python parse_ios_appstore_clean.py test.xml")
        print("示例: python parse_ios_appstore_clean.py test.xml 13.6.50")
        print("示例: python parse_ios_appstore_clean.py test.xml 13.6.50 output.json")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    target_version = sys.argv[2] if len(sys.argv) > 2 else None
    output_json = sys.argv[3] if len(sys.argv) > 3 else None
    
    parser = iOSAppStoreParser(xml_file)
    
    # 打印解析结果
    parser.print_version_info(target_version)
    
    # 导出到JSON文件
    if output_json:
        parser.export_to_json(output_json)
    elif not target_version:  # 只有在不指定版本时才导出完整JSON
        parser.export_to_json()

if __name__ == "__main__":
    main() 