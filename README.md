# App Store 版本信息获取工具

这是一个功能完整的 App Store 版本信息获取工具集，支持自动版本检查、批量获取版本信息、智能更新发布日期，并生成包含所有版本详细信息的汇总报告。

## 🚀 主要功能

- **🔍 智能版本检查**: 自动检测并更新过时的历史文件
- **📱 批量版本获取**: 获取指定数量的历史版本信息
- **📅 自动日期更新**: 智能更新版本发布日期
- **📊 完整汇总报告**: 包含所有版本的详细信息
- **📈 包体趋势图**: 自动生成包体大小随时间变化的趋势图
- **🔄 增量更新**: 支持版本信息的增量更新，不覆盖现有数据
- **⚡ 完全自动化**: 无需手动维护，脚本自动处理所有流程

## 工具列表

### 1. 自动版本检查与汇总工具 ⭐ **推荐使用**

**文件**: `auto_fetch_popular_apps.py`

**功能**: 自动获取热门应用的最新版本信息，包含智能版本检查、自动更新和完整汇总功能

**使用方法**:
```bash
# 获取所有热门应用的最新10个版本（自动检查一致性）
python3 auto_fetch_popular_apps.py

# 获取所有热门应用的最新N个版本
python3 auto_fetch_popular_apps.py --count 20

# 获取指定应用的最新版本
python3 auto_fetch_popular_apps.py --app 抖音 --count 5

# 仅检查版本一致性（不获取新数据）
python3 auto_fetch_popular_apps.py --check-only

# 仅绘制包体趋势图（不获取新数据）
python3 auto_fetch_popular_apps.py --plot-only
```

**参数**:
- `--count N`: 获取每个应用的最新版本数量（默认: 10）
- `--app <应用名称>`: 指定应用名称（快手/抖音/微信/小红书/支付宝/淘宝）
- `--check-only`: 仅检查版本一致性，不获取新数据
- `--plot-only`: 仅绘制包体趋势图，不获取新数据

**智能特性**:
- 🔍 **自动版本检查**: 每次运行自动检查历史文件是否包含最新版本
- 🔄 **自动更新**: 发现过时数据时自动删除并重新获取
- 📊 **完整汇总**: 生成包含所有版本详细信息的汇总报告
- 📈 **包体趋势图**: 自动生成包体大小随时间变化的趋势图
- 💾 **增量更新**: 支持版本信息的增量更新，不覆盖现有数据
- 🎯 **热门应用**: 内置6个热门中文应用，一键获取所有信息

**输出文件**:
- `version_output/app_{app_id}_latest.json`: 每个应用的完整版本信息
- `version_output/popular_apps_summary.json`: 所有应用的汇总报告
- `graph_output/package_size_trends.png`: 包体大小趋势图

**汇总报告结构**:
```json
{
  "fetch_time": "2025-08-15 12:50:09",
  "results": {
    "抖音": {
      "app_id": "1142110895",
      "version_count": 10,
      "latest_version": "35.4.0",
      "latest_size": "518M",
      "latest_release_date": "2025-08-12",
      "last_updated": "2025-08-15 12:50:09",
      "all_versions": [
        {
          "short_version": "35.4.0",
          "bundle_version": "354013",
          "app_ext_vrs_id": "876956752",
          "download_url": "...",
          "md5": "...",
          "uncompressed_size": 939970560,
          "download_size": 517516847,
          "appstore_display_size": "518M",
          "release_date": "2025-08-12"
        }
        // ... 还有9个版本的详细信息
      ]
    }
  }
}
```

**📈 包体趋势图功能**:
- **双图表设计**: 上图显示包体大小随时间变化趋势，下图显示最新版本大小对比
- **数据转换**: 自动将 `download_size` (字节) 转换为 MB 单位
- **时间轴**: 横坐标为发布日期，支持时间排序和趋势分析
- **品牌色彩**: 每个应用使用其知名品牌色彩，确保视觉识别度
- **可视化**: 每个应用用不同颜色表示，包含数据点标记
- **高质量输出**: 300 DPI 高分辨率PNG格式，适合报告和展示
- **自动生成**: 每次运行汇总后自动生成，也可单独使用 `--plot-only` 参数

### 2. 搜索 App ID 工具

**文件**: `search_app_id_simple.py`

**功能**: 通过 App Store 搜索 API 获取应用的 ID

**使用方法**:
```bash
python3 search_app_id_simple.py <App名称> [-l <数量>]
```

**参数**:
- `app_name`: 要搜索的App名称（必需）
- `-l, --limit`: 显示结果数量（可选，默认: 1）

**示例**:
```bash
# 默认只显示第一个结果
python3 search_app_id_simple.py 抖音

# 显示前3个结果
python3 search_app_id_simple.py 抖音 -l 3

# 显示前5个结果
python3 search_app_id_simple.py 微信 --limit 5

# 显示帮助信息
python3 search_app_id_simple.py --help
```

**输出示例**:
```
🔍 正在搜索: 抖音
📝 搜索关键词: %E6%8A%96%E9%9F%B3
📊 显示结果数量: 1
============================================================
✅ 找到 228 个结果，显示前 1 个:
------------------------------------------------------------
1. 抖音
   📱 App ID: 1142110895
   👨‍💻 开发者: Beijing Douyin Technology Co., Ltd.

🎯 推荐使用: 抖音 (ID: 1142110895)

💡 你可以使用以下命令更新版本日期:
python3 update_version_dates.py 1142110895
```

### 3. 更新版本日期工具

**文件**: `update_version_dates.py`

**功能**: 更新版本文件中的发布日期，支持智能检查和自动获取历史数据

**使用方法**:
```bash
python3 update_version_dates.py <App_ID> [选项]
```

**参数**:
- `app_id`: App ID（必需，例如: 440948110）
- `-f, --fetch`: 如果历史数据文件不存在或不是最新的，自动获取历史数据
- `--force`: 强制更新所有版本日期，即使已有发布日期

**示例**:
```bash
# 基本使用（需要历史数据文件已存在）
python3 update_version_dates.py 440948110

# 自动获取历史数据并更新
python3 update_version_dates.py 1142110895 --fetch

# 强制更新所有版本日期
python3 update_version_dates.py 440948110 --force

# 显示帮助和常见App列表
python3 update_version_dates.py
```

**智能检查功能**:
- 🔍 **History文件检查**: 自动检查 `version_input/ios_appstore_history_xxx.json` 是否存在且包含最新版本
- 📊 **Latest文件检查**: 检查 `version_output/app_xxx_latest_100.json` 是否需要更新发布日期
- ⏭️ **跳过已更新**: 如果版本已有发布日期且不是强制更新，会自动跳过
- 📥 **自动获取**: 使用 `--fetch` 参数可以自动从App Store API获取历史数据

**输出示例**:
```
🔍 开始处理App ID: 440948110
============================================================
📄 检查History文件: version_input/ios_appstore_history_440948110.json
✅ History文件包含最新版本: 13.6.60
📄 检查Latest文件: version_output/app_440948110_latest_100.json
✅ Latest文件已是最新且包含发布日期: 13.6.60
✅ 所有文件都是最新的，无需更新
🎉 处理完成！
```

### 4. 批量获取版本信息工具

**文件**: `batch_fetch_versions.py`

**功能**: 批量获取App的历史版本信息，包括下载大小、解压大小等详细信息

**使用方法**:
```bash
python3 batch_fetch_versions.py --app_id <App_ID> [选项]
```

**参数**:
- `--app_id`: App Store ID（必填），例如：440948110
- `--latest N`: 获取最近N个版本
- `--ids id1,id2,...`: 获取指定版本ID，多个用逗号分隔

**示例**:
```bash
# 获取最新版本
python3 batch_fetch_versions.py --app_id 440948110

# 获取最近10个版本
python3 batch_fetch_versions.py --app_id 440948110 --latest 10

# 获取指定版本（支持多个ID，用逗号分隔）
python3 batch_fetch_versions.py --app_id 440948110 --ids 876862684,876666097,876468641

# 获取其他App的版本信息（如抖音）
python3 batch_fetch_versions.py --app_id 1142110895 --latest 5
```

**输出说明**:
- 输出JSON文件会自动命名：
  - `app_440948110_latest.json`：最新版本
  - `app_440948110_latest_10.json`：最近10个版本
  - `app_440948110_ids_876862684_876666097.json`：指定ID
- 每次请求的原始XML会保存在 `xml_files/` 目录下，已存在则自动复用
- 结果JSON中的 `versions` 数组为倒序（最新在前）
- 自动生成/更新 `ios_appstore_parsed_{app_id}.json` 文件

**JSON输出格式**:
```json
{
  "app_name": "抖音",
  "item_id": "1142110895",
  "total_versions": 1,
  "versions": [
    {
      "short_version": "35.3.0",
      "bundle_version": "353015",
      "app_ext_vrs_id": "876763609",
      "download_url": "https://iosapps.itunes.apple.com/...",
      "md5": "d21056609b5faa949d6d41116334e4ee",
      "uncompressed_size": 935434240,
      "download_size": 515289507,
      "appstore_display_size": "515M"
    }
  ]
}
```

**字段说明**:
- **顶层字段**:
  - `app_name` - 应用名称
  - `item_id` - App Store ID
  - `total_versions` - 版本总数
  - `versions` - 版本信息数组（倒序，最新在前）

- **版本字段**:
  - `short_version` - 短版本号（如 "35.3.0"）
  - `bundle_version` - Bundle版本号（如 "353015"）
  - `app_ext_vrs_id` - 版本外部标识符
  - `download_url` - 下载链接
  - `md5` - 文件MD5校验码
  - `uncompressed_size` - 解压后大小（字节）
  - `download_size` - 下载大小（字节）
  - `appstore_display_size` - App Store显示大小（如 "515M"）

## 常见App ID列表

| App名称 | App ID | 说明 |
|---------|--------|------|
| 快手 (Kuaishou) | 440948110 | 短视频平台 |
| 抖音 (TikTok) | 1142110895 | 短视频平台 |
| 微信 (WeChat) | 414478124 | 社交应用 |
| QQ | 444934666 | 社交应用 |
| 支付宝 (Alipay) | 333206289 | 支付应用 |
| 淘宝 (Taobao) | 387682726 | 电商平台 |
| 京东 (JD) | 414245813 | 电商平台 |
| 美团 (Meituan) | 423084029 | 生活服务 |
| 滴滴出行 (DiDi) | 564499420 | 出行服务 |
| 微博 (Weibo) | 350962117 | 社交媒体 |
| 今日头条 (Toutiao) | 529092160 | 新闻资讯 |
| 百度 (Baidu) | 382201985 | 搜索引擎 |
| 网易云音乐 (NetEase) | 590338362 | 音乐应用 |
| QQ音乐 (QQ Music) | 414603431 | 音乐应用 |
| 爱奇艺 (iQiyi) | 393765873 | 视频平台 |
| 腾讯视频 (Tencent Video) | 458318329 | 视频平台 |
| 优酷 (Youku) | 336141475 | 视频平台 |
| 拼多多 | 1044283059 | 电商平台 |

## 工作流程

### 🚀 推荐流程（一键获取所有热门应用）

```bash
# 获取所有热门应用的最新10个版本（推荐）
python3 auto_fetch_popular_apps.py

# 获取所有热门应用的最新20个版本
python3 auto_fetch_popular_apps.py --count 20

# 仅检查版本一致性
python3 auto_fetch_popular_apps.py --check-only
```

**优势**: 
- ✅ 完全自动化，无需手动维护
- ✅ 自动检查版本一致性
- ✅ 自动更新过时数据
- ✅ 生成完整汇总报告
- ✅ 支持增量更新

### 📱 传统流程（单个应用处理）

#### 1. 搜索App ID
```bash
# 搜索App ID
python3 search_app_id_simple.py 抖音
```

#### 2. 批量获取版本信息
```bash
# 获取最近100个版本
python3 batch_fetch_versions.py --app_id 1142110895 --latest 100
```

#### 3. 更新版本日期
```bash
# 自动获取历史数据并更新版本日期
python3 update_version_dates.py 1142110895 --fetch
```

#### 4. 检查更新结果
脚本会自动检查文件状态并显示详细的更新信息。

### 🔍 版本一致性检查流程

```bash
# 检查所有应用的版本一致性
python3 auto_fetch_popular_apps.py --check-only

# 检查指定应用的版本一致性
python3 auto_fetch_popular_apps.py --app 抖音 --count 5

### 📈 包体趋势图生成流程

```bash
# 生成所有应用的包体趋势图
python3 auto_fetch_popular_apps.py --plot-only

# 获取数据并自动生成趋势图
python3 auto_fetch_popular_apps.py --count 10

# 查看生成的趋势图
open graph_output/package_size_trends.png
```
```

## 文件结构

```
appstore_parse/
├── auto_fetch_popular_apps.py      # ⭐ 自动版本检查与汇总工具（推荐）
├── search_app_id_simple.py         # 搜索App ID工具
├── update_version_dates.py         # 更新版本日期工具
├── batch_fetch_versions.py         # 批量获取版本信息工具
├── fetch_app_xml.sh               # 获取App XML的Shell脚本
├── requirements.txt                # 完整依赖库列表
├── requirements-minimal.txt        # 最小依赖库列表（仅必需）
├── install_dependencies.sh        # 依赖安装脚本（macOS/Linux）
├── install_dependencies.bat       # 依赖安装脚本（Windows）
├── INSTALL.md                     # 详细安装指南
├── app_colors_config.json         # 应用品牌色彩配置
├── version_input/                  # 历史数据文件目录
│   ├── ios_appstore_history_440948110.json
│   └── ios_appstore_history_1142110895.json
├── version_output/                 # 版本输出文件目录
│   ├── app_440948110_latest.json  # 快手完整版本信息
│   ├── app_1142110895_latest.json # 抖音完整版本信息
│   ├── app_414478124_latest.json  # 微信完整版本信息
│   ├── app_741292507_latest.json  # 小红书完整版本信息
│   ├── app_333206289_latest.json  # 支付宝完整版本信息
│   ├── app_387682726_latest.json  # 淘宝完整版本信息
│   └── popular_apps_summary.json  # 所有应用汇总报告
├── graph_output/                   # 图形输出目录
│   └── package_size_trends.png    # 包体大小趋势图
├── xml_files/                     # XML文件目录（临时文件）
│   ├── app_440948110_*.xml
│   └── app_1142110895_*.xml
└── README.md                      # 本说明文档
```

## 注意事项

### 🔧 技术注意事项

1. **API 限制**: App Store 搜索 API 可能有请求频率限制
2. **数据时效性**: 历史版本数据可能不是最新的
3. **文件依赖**: 更新版本日期需要对应的历史数据文件存在
4. **网络连接**: 需要稳定的网络连接来访问 App Store API
5. **结果数量**: 搜索工具默认只显示第一个结果，可以通过 `-l` 参数调整
6. **智能检查**: 更新工具会自动检查文件状态，避免不必要的更新
7. **强制更新**: 使用 `--force` 参数可以强制更新所有版本日期
8. **XML文件**: `batch_fetch_versions.py` 需要有效的Apple认证信息才能获取XML数据
9. **文件大小**: 文件大小以字节为单位，脚本会自动格式化为可读格式（KB、MB、GB）

### 🚀 新功能特性

10. **自动版本检查**: `auto_fetch_popular_apps.py` 会自动检查版本一致性，无需手动维护
11. **增量更新**: 支持版本信息的增量更新，不会覆盖现有的完整数据
12. **完整汇总**: 汇总报告包含所有版本的详细信息，不仅仅是摘要
13. **热门应用内置**: 内置6个热门中文应用，无需手动配置
14. **临时文件管理**: 自动清理临时文件，保持目录整洁
15. **版本一致性**: 确保 `version_count` 与实际包含的版本数量一致

## 故障排除

### 🚀 自动版本检查工具故障

#### 版本一致性检查失败
- 确认网络连接正常
- 检查 `fetch_app_xml.sh` 脚本权限是否正确
- 验证Apple认证信息是否有效
- 使用 `--check-only` 参数单独检查版本一致性

#### 汇总生成失败
- 确认 `version_output/` 目录存在且有写入权限
- 检查各个应用的 `latest.json` 文件是否完整
- 验证JSON文件格式是否正确

### 🔍 搜索失败
- 检查网络连接
- 确认 App 名称正确
- 尝试使用英文名称搜索
- 检查 `-l` 参数值是否合理（必须大于0）

### 📅 更新失败
- 确认 App ID 正确
- 检查历史数据文件是否存在
- 使用 `--fetch` 参数自动获取历史数据
- 检查版本文件格式是否正确

### 📱 批量获取失败
- 确认 `--app_id` 参数已提供
- 检查Apple认证信息是否有效
- 确认网络连接正常
- 检查XML文件格式是否正确

### 📁 文件不存在
- 使用 `--fetch` 参数自动获取历史数据
- 确认文件路径和权限正确
- 检查网络连接是否正常

### 🔧 常见问题解决

#### 版本数量不匹配
- 运行 `python3 auto_fetch_popular_apps.py --check-only` 检查版本一致性
- 删除过时的历史文件，让脚本自动重新获取
- 确认 `batch_fetch_versions.py` 正常工作

#### 汇总信息不完整
- 检查所有应用的 `latest.json` 文件是否存在
- 运行完整的获取流程：`python3 auto_fetch_popular_apps.py`
- 验证JSON文件格式和内容完整性

#### 自动更新失败
- 检查网络连接和API访问权限
- 确认 `update_version_dates.py` 脚本正常工作
- 查看错误日志，定位具体问题

## 系统要求

- Python 3.6+
- 标准库：xml.etree.ElementTree, json, sys, typing, subprocess, os, time, argparse
- 依赖库：requests（如有网络请求）

## 🚀 快速开始

### 0. 安装依赖（首次使用）

```bash
# 方法1：使用安装脚本（推荐）
./install_dependencies.sh                    # macOS/Linux
install_dependencies.bat                     # Windows

# 方法2：手动安装
pip install -r requirements.txt              # 完整安装
pip install -r requirements-minimal.txt      # 最小安装（仅必需）

# 方法3：使用国内镜像源（推荐国内用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 1. 一键获取所有热门应用信息（推荐）

```bash
# 获取所有热门应用的最新10个版本
python3 auto_fetch_popular_apps.py
```

### 2. 检查版本一致性

```bash
# 检查所有应用的版本一致性
python3 auto_fetch_popular_apps.py --check-only
```

### 3. 获取指定应用信息

```bash
# 获取抖音的最新5个版本
python3 auto_fetch_popular_apps.py --app 抖音 --count 5
```

### 4. 查看汇总报告

```bash
# 查看生成的汇总报告
cat version_output/popular_apps_summary.json
```

### 5. 生成包体趋势图

```bash
# 生成包体趋势图
python3 auto_fetch_popular_apps.py --plot-only

# 查看生成的趋势图
open graph_output/package_size_trends.png
```

## 📊 输出示例

运行 `python3 auto_fetch_popular_apps.py` 后，您将得到：

- **6个应用的完整版本信息**：每个应用包含指定数量的版本详情
- **统一的汇总报告**：`popular_apps_summary.json` 包含所有应用的摘要和详细信息
- **包体趋势图**：`package_size_trends.png` 显示包体大小随时间的变化趋势
- **自动版本检查**：确保所有数据都是最新的
- **增量更新支持**：不会覆盖现有的完整数据

## 🎯 内置热门应用

| 应用名称 | App ID | 说明 |
|---------|--------|------|
| 快手 | 440948110 | 短视频平台 |
| 抖音 | 1142110895 | 短视频平台 |
| 微信 | 414478124 | 社交应用 |
| 小红书 | 741292507 | 生活方式平台 |
| 支付宝 | 333206289 | 支付应用 |
| 淘宝 | 387682726 | 电商平台 |

## 💡 使用建议

1. **首次使用**: 直接运行 `python3 auto_fetch_popular_apps.py` 获取所有应用信息
2. **定期检查**: 使用 `--check-only` 参数检查版本一致性
3. **增量更新**: 使用 `--count` 参数指定需要的版本数量
4. **数据分析**: 利用生成的汇总报告和趋势图进行版本趋势分析
5. **可视化**: 使用 `--plot-only` 参数快速生成包体趋势图
6. **自动化**: 可以设置定时任务，定期运行版本检查和图表生成 