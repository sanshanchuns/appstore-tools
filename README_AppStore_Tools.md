# App Store 工具使用指南

这个项目包含三个主要的Python脚本，用于处理App Store数据。

## 工具列表

### 1. 搜索 App ID 工具

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

### 2. 更新版本日期工具

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

### 3. 批量获取版本信息工具

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

### 1. 搜索App ID
```bash
# 搜索App ID
python3 search_app_id_simple.py 抖音
```

### 2. 批量获取版本信息
```bash
# 获取最近100个版本
python3 batch_fetch_versions.py --app_id 1142110895 --latest 100
```

### 3. 更新版本日期
```bash
# 自动获取历史数据并更新版本日期
python3 update_version_dates.py 1142110895 --fetch
```

### 4. 检查更新结果
脚本会自动检查文件状态并显示详细的更新信息。

## 文件结构

```
appstore_parse/
├── search_app_id_simple.py          # 搜索App ID工具
├── update_version_dates.py          # 更新版本日期工具
├── batch_fetch_versions.py          # 批量获取版本信息工具
├── version_input/                   # 历史数据文件目录
│   ├── ios_appstore_history_440948110.json
│   └── ios_appstore_history_1142110895.json
├── version_output/                  # 版本输出文件目录
│   ├── app_440948110_latest_100.json
│   └── app_1142110895_latest_100.json
├── xml_files/                      # XML文件目录
│   ├── app_440948110_*.xml
│   └── app_1142110895_*.xml
└── README_AppStore_Tools.md         # 本说明文档
```

## 注意事项

1. **API 限制**: App Store 搜索 API 可能有请求频率限制
2. **数据时效性**: 历史版本数据可能不是最新的
3. **文件依赖**: 更新版本日期需要对应的历史数据文件存在
4. **网络连接**: 需要稳定的网络连接来访问 App Store API
5. **结果数量**: 搜索工具默认只显示第一个结果，可以通过 `-l` 参数调整
6. **智能检查**: 更新工具会自动检查文件状态，避免不必要的更新
7. **强制更新**: 使用 `--force` 参数可以强制更新所有版本日期
8. **XML文件**: `batch_fetch_versions.py` 需要有效的Apple认证信息才能获取XML数据
9. **文件大小**: 文件大小以字节为单位，脚本会自动格式化为可读格式（KB、MB、GB）

## 故障排除

### 搜索失败
- 检查网络连接
- 确认 App 名称正确
- 尝试使用英文名称搜索
- 检查 `-l` 参数值是否合理（必须大于0）

### 更新失败
- 确认 App ID 正确
- 检查历史数据文件是否存在
- 使用 `--fetch` 参数自动获取历史数据
- 检查版本文件格式是否正确

### 批量获取失败
- 确认 `--app_id` 参数已提供
- 检查Apple认证信息是否有效
- 确认网络连接正常
- 检查XML文件格式是否正确

### 文件不存在
- 使用 `--fetch` 参数自动获取历史数据
- 确认文件路径和权限正确
- 检查网络连接是否正常

## 系统要求

- Python 3.6+
- 标准库：xml.etree.ElementTree, json, sys, typing
- 依赖库：requests（如有网络请求） 