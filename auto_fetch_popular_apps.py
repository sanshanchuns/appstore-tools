#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动获取热门应用最新版本信息的脚本
直接复用现有的batch_fetch_versions.py和update_version_dates.py
增强版：自动检测并更新过时的历史文件
"""

import subprocess
import json
import os
import time
import argparse
import sys
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 颜色分析功能已简化，直接使用默认颜色

class PopularAppsFetcher:
    def __init__(self):
        # 热门应用ID映射
        self.popular_apps = {
            "快手": "440948110",
            "抖音": "1142110895", 
            "微信": "414478124",
            "小红书": "741292507",
            "支付宝": "333206289",
            "淘宝": "387682726",
            "拼多多": "1044283059"
        }
        
        # 确保目录存在
        os.makedirs("version_input", exist_ok=True)
        os.makedirs("version_output", exist_ok=True)
        os.makedirs("graph_output", exist_ok=True)
    
    def get_latest_version_from_xml(self, app_id: str) -> str:
        """从App Store获取最新版本号"""
        try:
            # 直接调用batch_fetch_versions.py获取最新版本，不依赖现有文件
            cmd = ['python3', 'batch_fetch_versions.py', '--app_id', app_id, '--latest', '1']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # 从输出中提取版本号
                try:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if '版本号:' in line:
                            version = line.split('版本号:')[1].strip()
                            print(f"📱 从App Store获取到最新版本: {version}")
                            return version
                except:
                    pass
            
            # 如果无法从输出获取，尝试从现有的latest.json文件读取
            latest_file = f"version_output/app_{app_id}_latest.json"
            if os.path.exists(latest_file):
                try:
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if data and 'versions' in data and len(data['versions']) > 0:
                        version = data['versions'][0].get('short_version')
                        print(f"📱 从现有latest文件获取到最新版本: {version}")
                        return version
                except Exception as e:
                    print(f"❌ 读取现有latest文件失败: {e}")
            
            return None
            
        except Exception as e:
            print(f"❌ 获取最新版本号失败: {e}")
            return None
    
    def check_version_consistency(self, app_id: str) -> bool:
        """检查历史文件中的版本是否与最新版本一致"""
        history_file = f"version_input/ios_appstore_history_{app_id}.json"
        
        # 如果历史文件不存在，需要更新
        if not os.path.exists(history_file):
            print(f"📄 历史文件不存在: {history_file}")
            return False
        
        try:
            # 获取历史文件中的版本信息
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            data_item = history_data.get("data", [{}])[0]
            version_history = data_item.get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
            
            if not version_history:
                print(f"⚠️  历史文件中没有版本信息")
                return False
            
            # 获取历史文件中的最新版本和版本数量
            history_latest_version = version_history[0].get("versionDisplay")
            history_latest_date = version_history[0].get("releaseDate")
            history_version_count = len(version_history)
            
            print(f"📋 历史文件显示: 最新版本 {history_latest_version} ({history_latest_date}), 共 {history_version_count} 个版本")
            
            # 获取实际最新版本
            actual_latest_version = self.get_latest_version_from_xml(app_id)
            
            if not actual_latest_version:
                print(f"⚠️  无法获取实际最新版本，假设历史文件是最新的")
                return True
            
            print(f"📱 实际最新版本: {actual_latest_version}")
            
            # 检查版本是否一致
            if history_latest_version == actual_latest_version:
                print(f"✅ 版本一致，历史文件是最新的")
                return True
            else:
                print(f"⚠️  版本不一致！历史文件: {history_latest_version}, 实际: {actual_latest_version}")
                return False
                
        except Exception as e:
            print(f"❌ 检查版本一致性失败: {e}")
            return False
    
    def auto_update_history_if_needed(self, app_id: str) -> bool:
        """如果历史文件过时，自动更新"""
        print(f"🔍 检查App ID {app_id} 的版本一致性...")
        
        if not self.check_version_consistency(app_id):
            print(f"🔄 检测到历史文件过时，正在自动更新...")
            
            # 删除过时的历史文件
            history_file = f"version_input/ios_appstore_history_{app_id}.json"
            if os.path.exists(history_file):
                os.remove(history_file)
                print(f"🗑️  已删除过时的历史文件: {history_file}")
            
            # 重新获取最新数据
            try:
                cmd = ['python3', 'update_version_dates.py', app_id, '--fetch']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"✅ 历史文件自动更新成功")
                    return True
                else:
                    print(f"❌ 历史文件自动更新失败: {result.stderr}")
                    return False
                    
            except Exception as e:
                print(f"❌ 历史文件自动更新出错: {e}")
                return False
        else:
            print(f"✅ 历史文件是最新的，无需更新")
            return True
    
    def get_version_dates_from_history(self, app_id: str) -> dict:
        """从历史文件中获取版本号到发布日期的映射"""
        history_file = f"version_input/ios_appstore_history_{app_id}.json"
        
        if not os.path.exists(history_file):
            print(f"⚠️  历史文件不存在: {history_file}")
            return {}
        
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            # 创建版本号到发布日期的映射
            version_to_date = {}
            try:
                data_item = history_data.get("data", [{}])[0]
                version_history = data_item.get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
                
                for item in version_history:
                    version_display = item.get("versionDisplay")
                    release_date = item.get("releaseDate")
                    if version_display and release_date:
                        version_to_date[version_display] = release_date
                
                print(f"✅ 从历史文件获取到 {len(version_to_date)} 个版本的发布日期")
                return version_to_date
                
            except (IndexError, KeyError) as e:
                print(f"❌ 解析历史文件失败: {e}")
                return {}
                
        except Exception as e:
            print(f"❌ 读取历史文件失败: {e}")
            return {}
    
    def infer_release_date_for_new_version(self, version_to_date: dict, new_version: str) -> str:
        """对于不在历史数据中的新版本，尝试推断发布日期"""
        if not version_to_date:
            return "未知"
        
        # 按版本号排序，获取最新版本的发布日期
        sorted_versions = sorted(version_to_date.keys(), key=lambda x: [int(i) for i in x.split('.')], reverse=True)
        
        if sorted_versions:
            latest_known_version = sorted_versions[0]
            latest_known_date = version_to_date[latest_known_version]
            
            # 如果新版本号明显大于已知版本，尝试推断发布日期
            try:
                new_version_parts = [int(i) for i in new_version.split('.')]
                latest_known_parts = [int(i) for i in latest_known_version.split('.')]
                
                # 如果主版本号相同，次版本号增加，可能是最近发布的
                if (len(new_version_parts) >= 2 and len(latest_known_parts) >= 2 and 
                    new_version_parts[0] == latest_known_parts[0] and 
                    new_version_parts[1] > latest_known_parts[1]):
                    
                    # 尝试推断发布日期：通常在已知版本发布后几天到一周
                    from datetime import datetime, timedelta
                    try:
                        latest_date = datetime.strptime(latest_known_date, "%Y-%m-%d")
                        # 假设新版本在已知版本后3-7天发布
                        inferred_date = latest_date + timedelta(days=7)
                        inferred_date_str = inferred_date.strftime("%Y-%m-%d")
                        print(f"💡 版本 {new_version} 不在历史数据中，基于版本号推断发布日期为: {inferred_date_str}")
                        return inferred_date_str
                    except:
                        pass
                
                print(f"💡 版本 {new_version} 不在历史数据中，推断发布日期为: {latest_known_date}")
                return latest_known_date
            except:
                print(f"💡 版本 {new_version} 不在历史数据中，推断发布日期为: {latest_known_date}")
                return latest_known_date
        
        return "未知"
    
    def merge_release_dates(self, app_id: str, version_count: int):
        """将发布日期信息合并到版本文件中，只处理versionHistory中存在的版本"""
        output_file = f"version_output/app_{app_id}_latest_{version_count}.json"
        
        if not os.path.exists(output_file):
            print(f"❌ 版本文件不存在: {output_file}")
            return False
        
        try:
            # 读取版本文件
            with open(output_file, 'r', encoding='utf-8') as f:
                version_data = json.load(f)
            
            # 获取版本号到发布日期的映射
            version_to_date = self.get_version_dates_from_history(app_id)
            
            if not version_to_date:
                print(f"⚠️  无法获取发布日期信息，跳过合并")
                return False
            
            # 只保留在versionHistory中存在的版本
            valid_versions = []
            ignored_count = 0
            
            for version in version_data.get('versions', []):
                short_version = version.get('short_version')
                if short_version in version_to_date:
                    # 版本在versionHistory中存在，添加发布日期
                    version['release_date'] = version_to_date[short_version]
                    valid_versions.append(version)
                else:
                    # 版本不在versionHistory中，忽略
                    ignored_count += 1
                    print(f"⚠️  忽略版本 {short_version}（不在versionHistory中）")
            
            # 更新版本数据
            version_data['versions'] = valid_versions
            version_data['total_versions'] = len(valid_versions)
            
            # 保存更新后的文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 成功处理 {len(valid_versions)} 个有效版本，忽略 {ignored_count} 个无效版本")
            return True
            
        except Exception as e:
            print(f"❌ 合并发布日期信息失败: {e}")
            return False
    
    def find_best_matching_date(self, target_version: str, version_to_date: dict) -> str:
        """智能匹配版本号，找到最合适的发布日期"""
        if not target_version or not version_to_date:
            return None
        
        # 1. 精确匹配
        if target_version in version_to_date:
            return version_to_date[target_version]
        
        # 2. 尝试主版本号匹配（如 8.0.x 匹配 8.0.62）
        target_parts = target_version.split('.')
        if len(target_parts) >= 2:
            major_minor = f"{target_parts[0]}.{target_parts[1]}"
            
            # 找到所有匹配主版本号的版本
            matching_versions = []
            for version, date in version_to_date.items():
                if version.startswith(major_minor):
                    matching_versions.append((version, date))
            
            if matching_versions:
                # 按版本号排序，找到最接近的版本
                matching_versions.sort(key=lambda x: [int(i) for i in x[0].split('.')], reverse=True)
                
                # 尝试找到最合适的匹配
                target_num = int(target_parts[2]) if len(target_parts) > 2 else 0
                
                for version, date in matching_versions:
                    version_parts = version.split('.')
                    if len(version_parts) > 2:
                        version_num = int(version_parts[2])
                        # 如果版本号差异在合理范围内，使用该日期
                        if abs(target_num - version_num) <= 10:  # 允许10个版本的差异
                            print(f"💡 版本 {target_version} 智能匹配到 {version} 的发布日期: {date}")
                            return date
                
                # 如果没找到合适的，使用主版本号下最新的版本日期
                closest_version, closest_date = matching_versions[0]
                print(f"💡 版本 {target_version} 使用主版本号 {major_minor} 的最新日期: {closest_date}")
                return closest_date
        
        # 3. 如果还是找不到，尝试推断日期
        return self.infer_release_date_for_new_version(version_to_date, target_version)
    
    def merge_to_latest_file(self, app_id: str, version_count: int):
        """将新获取的版本信息合并到统一的latest.json文件中，只保留versionHistory中的版本"""
        temp_file = f"version_output/app_{app_id}_latest_{version_count}.json"
        latest_file = f"version_output/app_{app_id}_latest.json"
        
        if not os.path.exists(temp_file):
            print(f"❌ 临时版本文件不存在: {temp_file}")
            return False
        
        try:
            # 读取新获取的版本信息
            with open(temp_file, 'r', encoding='utf-8') as f:
                new_versions_data = json.load(f)
            
            # 获取versionHistory中的有效版本
            version_to_date = self.get_version_dates_from_history(app_id)
            if not version_to_date:
                print(f"⚠️  无法获取versionHistory信息，跳过合并")
                return False
            
            # 过滤出有效的版本（在versionHistory中存在）
            valid_new_versions = []
            for version in new_versions_data.get('versions', []):
                short_version = version.get('short_version')
                if short_version in version_to_date:
                    valid_new_versions.append(version)
            
            print(f"📊 新获取版本中，{len(valid_new_versions)} 个在versionHistory中，{len(new_versions_data.get('versions', [])) - len(valid_new_versions)} 个被忽略")
            
            # 读取现有的latest文件（如果存在）
            existing_versions = []
            existing_last_updated = None
            if os.path.exists(latest_file):
                with open(latest_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_versions = existing_data.get('versions', [])
                    existing_last_updated = existing_data.get('last_updated')
                    print(f"📁 现有latest文件包含 {len(existing_versions)} 个版本")
            
            # 过滤现有版本，只保留在versionHistory中的版本
            valid_existing_versions = []
            for version in existing_versions:
                short_version = version.get('short_version')
                if short_version in version_to_date:
                    valid_existing_versions.append(version)
            
            print(f"📊 现有版本中，{len(valid_existing_versions)} 个在versionHistory中，{len(existing_versions) - len(valid_existing_versions)} 个被过滤")
            
            # 创建版本ID到版本的映射，用于去重与变更检测
            existing_version_map = {}
            for version in valid_existing_versions:
                version_id = version.get('app_ext_vrs_id')
                if version_id:
                    existing_version_map[version_id] = version

            new_version_map = {}
            for version in valid_new_versions:
                version_id = version.get('app_ext_vrs_id')
                if version_id:
                    new_version_map[version_id] = version

            # 计算真正新增与变更的版本
            existing_ids = set(existing_version_map.keys())
            new_ids = set(new_version_map.keys())
            actually_new_ids = new_ids - existing_ids

            # 仅比较稳定字段，避免临时URL变动导致误判
            keys_to_compare = {
                'short_version', 'bundle_version', 'download_size', 'uncompressed_size',
                'appstore_display_size', 'md5', 'release_date'
            }

            changed_ids = set()
            for vid in (new_ids & existing_ids):
                old_v = existing_version_map.get(vid, {})
                new_v = new_version_map.get(vid, {})
                # 提取对比的子集
                old_sub = {k: old_v.get(k) for k in keys_to_compare}
                new_sub = {k: new_v.get(k) for k in keys_to_compare}
                if old_sub != new_sub:
                    changed_ids.add(vid)

            # 合并：以现有版本为基础，新增或覆盖变更的版本
            version_map = dict(existing_version_map)
            for vid, v in new_version_map.items():
                version_map[vid] = v
            
            # 转换为列表并按版本号排序（最新的在前）
            all_versions = list(version_map.values())
            all_versions.sort(key=lambda x: x.get('short_version', ''), reverse=True)
            
            # 判断是否需要更新last_updated
            # 当有新版本或版本信息发生变化时，总是更新时间戳
            should_update_timestamp = False
            if len(actually_new_ids) > 0:  # 有新增版本
                should_update_timestamp = True
                print(f"🆕 检测到 {len(actually_new_ids)} 个新版本，将更新时间戳")
            elif len(changed_ids) > 0:  # 有版本信息变更
                should_update_timestamp = True
                print(f"🔄 检测到 {len(changed_ids)} 个版本信息变更，将更新时间戳")
            elif len(all_versions) != len(valid_existing_versions):  # 版本数量发生变化
                should_update_timestamp = True
                print(f"📊 版本数量发生变化（{len(valid_existing_versions)} -> {len(all_versions)}），将更新时间戳")
            else:
                print(f"✅ 版本信息无变化，保持原有时间戳")
            
            # 准备输出数据
            output_data = {
                'app_name': new_versions_data.get('app_name', ''),
                'item_id': new_versions_data.get('item_id', ''),
                'total_versions': len(all_versions),
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S') if should_update_timestamp else existing_last_updated,
                'versions': all_versions
            }
            
            # 保存到latest文件
            with open(latest_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            if should_update_timestamp:
                print(f"✅ 成功合并到latest文件，总共 {len(all_versions)} 个有效版本（真正新增 {len(actually_new_ids)} 个，变更 {len(changed_ids)} 个），时间戳已更新")
            else:
                print(f"✅ 成功合并到latest文件，总共 {len(all_versions)} 个有效版本（无变化），时间戳未更新")
            
            # 删除临时文件
            os.remove(temp_file)
            print(f"🗑️  已删除临时文件: {temp_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ 合并到latest文件失败: {e}")
            return False
    
    def fetch_app_versions(self, app_name: str, app_id: str, version_count: int = 10):
        """获取指定应用的最新版本信息"""
        print(f"\n📱 开始获取 {app_name} (ID: {app_id}) 的最新 {version_count} 个版本...")
        print("=" * 60)
        
        try:
            # 调用batch_fetch_versions.py获取版本信息
            cmd = ['python3', 'batch_fetch_versions.py', '--app_id', app_id, '--latest', str(version_count)]
            print(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {app_name} 版本信息获取成功")
                return True
            else:
                print(f"❌ {app_name} 版本信息获取失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ {app_name} 获取超时")
            return False
        except Exception as e:
            print(f"❌ {app_name} 获取出错: {e}")
            return False
    
    def update_version_dates(self, app_name: str, app_id: str):
        """更新版本发布日期"""
        print(f"📅 正在更新 {app_name} 的版本发布日期...")
        
        try:
            # 调用update_version_dates.py更新发布日期
            cmd = ['python3', 'update_version_dates.py', app_id, '--fetch']
            print(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ {app_name} 发布日期更新成功")
                return True
            else:
                print(f"❌ {app_name} 发布日期更新失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ {app_name} 更新超时")
            return False
        except Exception as e:
            print(f"❌ {app_name} 更新出错: {e}")
            return False
    
    def process_single_app(self, app_name: str, app_id: str, version_count: int = 10):
        """处理单个应用：获取版本信息并更新发布日期"""
        print(f"\n🔄 处理应用: {app_name}")
        print("-" * 40)
        
        # 1. 检查版本一致性，如果过时则更新历史文件
        print(f"🔍 正在检查 {app_name} 的版本一致性...")
        if not self.check_version_consistency(app_id):
            print(f"🔄 检测到历史文件过时，正在更新...")
            self.auto_update_history_if_needed(app_id)
        
        # 2. 获取版本信息
        if not self.fetch_app_versions(app_name, app_id, version_count):
            return False
        
        # 3. 更新发布日期（获取历史数据）
        print(f"📅 正在更新 {app_name} 的版本发布日期...")
        if not self.update_version_dates(app_name, app_id):
            print(f"⚠️  {app_name} 发布日期更新失败，但版本信息已获取")
        
        # 4. 合并发布日期信息到版本文件（同时过滤无效版本）
        print(f"🔗 正在合并发布日期信息并过滤无效版本...")
        if self.merge_release_dates(app_id, version_count):
            print(f"✅ {app_name} 发布日期信息合并成功")
        else:
            print(f"⚠️  {app_name} 发布日期信息合并失败")
        
        # 5. 合并到统一的latest文件
        print(f"📁 正在合并到统一的latest文件...")
        if self.merge_to_latest_file(app_id, version_count):
            print(f"✅ {app_name} 已合并到latest文件")
        else:
            print(f"❌ {app_name} 合并到latest文件失败")
        
        return True
    
    def generate_summary(self):
        """生成汇总信息到popular_apps_summary.json"""
        print(f"\n📊 正在生成汇总信息...")
        
        all_results = {}
        
        for app_name, app_id in self.popular_apps.items():
            latest_file = f"version_output/app_{app_id}_latest.json"
            
            if os.path.exists(latest_file):
                try:
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    versions = data.get('versions', [])
                    if versions:
                        latest_version = versions[0]
                        all_results[app_name] = {
                            'app_id': app_id,
                            'version_count': len(versions),
                            'latest_version': latest_version.get('short_version', 'N/A'),
                            'latest_size': latest_version.get('appstore_display_size', 'N/A'),
                            'latest_release_date': latest_version.get('release_date', 'N/A'),
                            'last_updated': data.get('last_updated', 'N/A'),
                            'all_versions': versions  # 添加所有版本的详细信息
                        }
                    else:
                        all_results[app_name] = {
                            'app_id': app_id,
                            'version_count': 0,
                            'latest_version': 'N/A',
                            'latest_size': 'N/A',
                            'latest_release_date': 'N/A',
                            'last_updated': 'N/A'
                        }
                except Exception as e:
                    print(f"❌ 读取 {app_name} 的latest文件失败: {e}")
                    all_results[app_name] = {
                        'app_id': app_id,
                        'version_count': 0,
                        'latest_version': 'N/A',
                        'latest_size': 'N/A',
                        'latest_release_date': 'N/A',
                        'last_updated': 'N/A',
                        'all_versions': []
                    }
            else:
                all_results[app_name] = {
                    'app_id': app_id,
                    'version_count': 0,
                    'latest_version': 'N/A',
                    'latest_size': 'N/A',
                    'latest_release_date': 'N/A',
                    'last_updated': 'N/A',
                    'all_versions': []
                }
        
        # 保存汇总结果
        summary_file = "version_output/popular_apps_summary.json"
        
        # 检查是否需要更新summary的last_updated
        should_update_summary = False
        existing_summary_data = {}
        
        # 如果summary文件存在，读取现有数据
        if os.path.exists(summary_file):
            try:
                with open(summary_file, 'r', encoding='utf-8') as f:
                    existing_summary_data = json.load(f)
            except:
                pass
        
        # 检查是否有应用数据发生变化
        if existing_summary_data:
            existing_results = existing_summary_data.get('results', {})
            for app_name, result in all_results.items():
                existing_result = existing_results.get(app_name, {})
                # 检查版本数量、最新版本、发布日期是否有变化
                if (result.get('version_count', 0) != existing_result.get('version_count', 0) or
                    result.get('latest_version', 'N/A') != existing_result.get('latest_version', 'N/A') or
                    result.get('latest_release_date', 'N/A') != existing_result.get('latest_release_date', 'N/A')):
                    should_update_summary = True
                    print(f"🔍 检测到 {app_name} 数据变化，将更新summary时间戳")
                    break
        else:
            # 如果summary文件不存在，需要更新
            should_update_summary = True
            print(f"🔍 首次生成summary，将设置时间戳")
        
        # 准备summary数据（移除 fetch_time 字段）
        summary_data = {
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S') if should_update_summary else existing_summary_data.get('last_updated', 'N/A'),
            'results': all_results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        if should_update_summary:
            print(f"💾 汇总信息已更新并保存到: {summary_file}")
        else:
            print(f"💾 汇总信息无变化，保存到: {summary_file}")
        
        # 打印汇总信息
        print("\n📊 热门应用版本信息汇总")
        print("=" * 80)
        print(f"{'应用名称':<12} {'最新版本':<12} {'大小':<8} {'发布日期':<12} {'版本数':<8} {'更新时间':<20}")
        print("-" * 80)
        
        for app_name, result in all_results.items():
            print(f"{app_name:<12} {result['latest_version']:<12} {result['latest_size']:<8} {result['latest_release_date']:<12} {result['version_count']:<8} {result['last_updated']:<20}")
        
        print(f"\n💾 汇总信息已保存到: {summary_file}")
        
        # 绘制包体趋势图
        print(f"\n📈 正在绘制包体趋势图...")
        self.plot_package_size_trends()
        
        return all_results
    
    def plot_package_size_trends(self):
        """根据summary绘制包体趋势图"""
        try:
            summary_file = "version_output/popular_apps_summary.json"
            
            if not os.path.exists(summary_file):
                print(f"❌ 汇总文件不存在: {summary_file}")
                return
            
            # 读取汇总数据
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary_data = json.load(f)
            
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图形和子图
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
            fig.suptitle('热门应用包体大小趋势图', fontsize=16, fontweight='bold')
            
            # 获取应用颜色
            app_colors = self.get_app_colors()
            
            # 数据收集
            all_data = {}
            latest_sizes = {}
            
            for app_name, app_data in summary_data.get('results', {}).items():
                if 'all_versions' not in app_data:
                    continue
                
                versions = app_data['all_versions']
                app_data_points = []
                
                for version in versions:
                    release_date = version.get('release_date')
                    download_size = version.get('download_size')
                    
                    if release_date and download_size:
                        try:
                            # 转换日期格式
                            date_obj = datetime.strptime(release_date, '%Y-%m-%d')
                            # 转换大小为MB
                            size_mb = download_size / (1024 * 1024)
                            
                            app_data_points.append((date_obj, size_mb))
                        except (ValueError, TypeError):
                            continue
                
                if app_data_points:
                    # 按日期排序
                    app_data_points.sort(key=lambda x: x[0])
                    all_data[app_name] = app_data_points
                    
                    # 记录最新版本的大小
                    if app_data_points:
                        latest_sizes[app_name] = app_data_points[-1][1]
            
            # 绘制趋势线图
            ax1.set_title('包体大小随时间变化趋势', fontsize=14, fontweight='bold')
            ax1.set_xlabel('发布日期', fontsize=12)
            ax1.set_ylabel('包体大小 (MB)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            
            for app_name, data_points in all_data.items():
                if data_points:
                    dates = [point[0] for point in data_points]
                    sizes = [point[1] for point in data_points]
                    
                    ax1.plot(dates, sizes, 
                            marker='o', 
                            linewidth=2, 
                            markersize=6,
                            color=app_colors.get(app_name, '#000000'),
                            label=app_name,
                            alpha=0.8)
            
            # 设置x轴日期格式
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            ax1.tick_params(axis='x', rotation=45)
            
            # 添加图例
            ax1.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
            
            # 绘制最新版本大小对比柱状图
            ax2.set_title('最新版本包体大小对比', fontsize=14, fontweight='bold')
            ax2.set_xlabel('应用名称', fontsize=12)
            ax2.set_ylabel('包体大小 (MB)', fontsize=12)
            ax2.grid(True, alpha=0.3)
            
            if latest_sizes:
                apps = list(latest_sizes.keys())
                sizes = list(latest_sizes.values())
                colors_list = [app_colors.get(app, '#000000') for app in apps]
                
                bars = ax2.bar(apps, sizes, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1)
                
                # 在柱状图上添加数值标签
                for bar, size in zip(bars, sizes):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{size:.1f}MB', ha='center', va='bottom', fontsize=10, fontweight='bold')
                
                ax2.tick_params(axis='x', rotation=45)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图片
            output_file = "graph_output/package_size_trends.png"
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"📊 包体趋势图已保存到: {output_file}")
            
            # 显示图片
            plt.show()
            
        except Exception as e:
            print(f"❌ 绘制包体趋势图失败: {e}")
            import traceback
            traceback.print_exc()
    
    def get_app_colors(self):
        """获取应用的颜色配置"""
        return self.get_default_colors()
    
    def get_default_color(self, app_name):
        """获取应用的默认颜色"""
        default_colors = {
            "快手": "#FF6B6B",      # 快手红
            "抖音": "#000000",      # 抖音黑
            "微信": "#07C160",      # 微信绿
            "小红书": "#FF2442",    # 小红书红
            "支付宝": "#1677FF",    # 支付宝蓝
            "淘宝": "#FF6A00",      # 淘宝橙
            "拼多多": "#E02E24"     # 拼多多红
        }
        return default_colors.get(app_name, "#666666")
    
    def get_default_colors(self):
        """获取所有应用的默认颜色"""
        return {app_name: self.get_default_color(app_name) for app_name in self.popular_apps.keys()}
    
    def fetch_all_popular_apps(self, version_count: int = 10):
        """获取所有热门应用的最新版本信息"""
        print(f"🚀 开始获取热门应用的最新 {version_count} 个版本信息")
        print("=" * 80)
        
        for app_name, app_id in self.popular_apps.items():
            try:
                success = self.process_single_app(app_name, app_id, version_count)
                
                if success:
                    print(f"✅ {app_name} 处理完成")
                else:
                    print(f"❌ {app_name} 处理失败")
                
            except Exception as e:
                print(f"❌ {app_name} 处理出错: {e}")
            
            print("-" * 60)
        
        # 生成汇总信息
        self.generate_summary()
        print("🎉 所有热门应用处理完成！")

def main():
    parser = argparse.ArgumentParser(
        description='自动获取热门应用最新版本信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 auto_fetch_popular_apps.py                    # 获取所有热门应用的最新10个版本
  python3 auto_fetch_popular_apps.py --count 20         # 获取所有热门应用的最新20个版本
  python3 auto_fetch_popular_apps.py --app 快手         # 只获取快手的版本信息
  python3 auto_fetch_popular_apps.py --app 抖音 --count 5  # 只获取抖音的最新5个版本
  python3 auto_fetch_popular_apps.py --check-only       # 仅检查版本一致性，不获取新数据
  python3 auto_fetch_popular_apps.py --plot-only        # 仅绘制包体趋势图，不获取新数据
        """
    )
    
    parser.add_argument('--count', type=int, default=10, 
                       help='获取每个应用的最新版本数量 (默认: 10)')
    parser.add_argument('--app', type=str, 
                       help='指定应用名称 (快手/抖音/微信/小红书/支付宝/淘宝)')
    parser.add_argument('--check-only', action='store_true',
                       help='仅检查版本一致性，不获取新数据')
    parser.add_argument('--plot-only', action='store_true',
                       help='仅绘制包体趋势图，不获取新数据')
    
    args = parser.parse_args()
    
    fetcher = PopularAppsFetcher()
    
    if args.check_only:
        # 仅检查版本一致性
        print("🔍 开始检查所有应用的版本一致性...")
        for app_name, app_id in fetcher.popular_apps.items():
            print(f"\n📱 检查 {app_name} (ID: {app_id})...")
            fetcher.auto_update_history_if_needed(app_id)
        print("\n✅ 版本一致性检查完成！")
        return
    
    if args.plot_only:
        # 仅绘制包体趋势图
        print("📈 开始绘制包体趋势图...")
        fetcher.plot_package_size_trends()
        return
    
    if args.app:
        # 获取指定应用
        if args.app not in fetcher.popular_apps:
            print(f"❌ 不支持的应用名称: {args.app}")
            print(f"支持的应用: {', '.join(fetcher.popular_apps.keys())}")
            sys.exit(1)
        
        app_id = fetcher.popular_apps[args.app]
        success = fetcher.process_single_app(args.app, app_id, args.count)
        
        if not success:
            print(f"❌ 获取 {args.app} 的版本信息失败")
            sys.exit(1)
        
        # 生成汇总信息
        fetcher.generate_summary()
    else:
        # 获取所有热门应用
        fetcher.fetch_all_popular_apps(args.count)

if __name__ == "__main__":
    main()
