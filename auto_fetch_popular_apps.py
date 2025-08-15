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
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

class PopularAppsFetcher:
    def __init__(self):
        # 热门应用ID映射
        self.popular_apps = {
            "快手": "440948110",
            "抖音": "1142110895", 
            # "微信": "414478124",
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
        """从现有的latest.json文件获取最新版本号"""
        try:
            # 首先尝试从现有的latest.json文件读取
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
            
            # 如果现有文件不存在或读取失败，尝试从batch_fetch_versions.py获取
            # 但这次我们直接解析输出，不生成临时文件
            cmd = ['python3', 'batch_fetch_versions.py', '--app_id', app_id, '--latest', '1']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                # 从输出中提取版本号
                try:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if '版本号:' in line:
                            version = line.split('版本号:')[1].strip()
                            print(f"📱 从输出获取到最新版本: {version}")
                            return version
                except:
                    pass
            
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
            # 获取历史文件中的最新版本
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            data_item = history_data.get("data", [{}])[0]
            version_history = data_item.get("attributes", {}).get("platformAttributes", {}).get("ios", {}).get("versionHistory", [])
            
            if not version_history:
                print(f"⚠️  历史文件中没有版本信息")
                return False
            
            # 获取历史文件中的最新版本
            history_latest_version = version_history[0].get("versionDisplay")
            history_latest_date = version_history[0].get("releaseDate")
            
            print(f"📋 历史文件显示最新版本: {history_latest_version} ({history_latest_date})")
            
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
        """将发布日期信息合并到版本文件中"""
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
            
            # 合并发布日期信息
            updated_count = 0
            for version in version_data.get('versions', []):
                short_version = version.get('short_version')
                if short_version in version_to_date:
                    version['release_date'] = version_to_date[short_version]
                    updated_count += 1
                else:
                    version['release_date'] = '未知'
            
            # 保存更新后的文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 成功合并 {updated_count} 个版本的发布日期信息")
            return True
            
        except Exception as e:
            print(f"❌ 合并发布日期信息失败: {e}")
            return False
    
    def merge_to_latest_file(self, app_id: str, version_count: int):
        """将新获取的版本信息合并到统一的latest.json文件中"""
        temp_file = f"version_output/app_{app_id}_latest_{version_count}.json"
        latest_file = f"version_output/app_{app_id}_latest.json"
        
        if not os.path.exists(temp_file):
            print(f"❌ 临时版本文件不存在: {temp_file}")
            return False
        
        try:
            # 读取新获取的版本信息
            with open(temp_file, 'r', encoding='utf-8') as f:
                new_versions_data = json.load(f)
            
            # 读取现有的latest文件（如果存在）
            existing_versions = []
            if os.path.exists(latest_file):
                with open(latest_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_versions = existing_data.get('versions', [])
                    print(f"📁 现有latest文件包含 {len(existing_versions)} 个版本")
            
            # 创建版本ID到版本的映射，用于去重
            version_map = {}
            
            # 先添加现有版本
            for version in existing_versions:
                version_id = version.get('app_ext_vrs_id')
                if version_id:
                    version_map[version_id] = version
            
            # 添加新版本（会覆盖旧版本）
            new_count = 0
            for version in new_versions_data.get('versions', []):
                version_id = version.get('app_ext_vrs_id')
                if version_id:
                    version_map[version_id] = version
                    new_count += 1
            
            # 转换为列表并按版本号排序（最新的在前）
            all_versions = list(version_map.values())
            all_versions.sort(key=lambda x: x.get('short_version', ''), reverse=True)
            
            # 准备输出数据
            output_data = {
                'app_name': new_versions_data.get('app_name', ''),
                'item_id': new_versions_data.get('item_id', ''),
                'total_versions': len(all_versions),
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'versions': all_versions
            }
            
            # 保存到latest文件
            with open(latest_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 成功合并到latest文件，总共 {len(all_versions)} 个版本（新增 {new_count} 个）")
            
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
        
        # 1. 自动检查并更新历史文件（如果需要）
        print(f"🔍 正在检查 {app_name} 的版本一致性...")
        self.auto_update_history_if_needed(app_id)
        
        # 2. 获取版本信息
        if not self.fetch_app_versions(app_name, app_id, version_count):
            return False
        
        # 3. 更新发布日期（获取历史数据）
        if not self.update_version_dates(app_name, app_id):
            print(f"⚠️  {app_name} 发布日期更新失败，但版本信息已获取")
        
        # 4. 合并发布日期信息到版本文件
        print(f"🔗 正在合并发布日期信息...")
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
        summary_data = {
            'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': all_results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
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
            
            # 颜色映射
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            app_colors = dict(zip(self.popular_apps.keys(), colors))
            
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
