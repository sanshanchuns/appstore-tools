# iOS AppStore XML解析器

这个工具用于解析通过特定curl命令获取的iOS AppStore上指定App的下载大小和解压大小信息。

## 功能特性

- 解析iOS AppStore XML文件中的应用信息
- 提取主应用（完整版）的下载大小和解压大小
- 解析增量更新包信息
- 支持查找指定版本的信息
- 导出解析结果到JSON格式

## JSON输出格式

批量获取的版本信息会导出为简化的JSON格式：

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

#### 字段说明

**顶层字段：**
- `app_name` - 应用名称
- `item_id` - App Store ID
- `total_versions` - 版本总数
- `versions` - 版本信息数组（倒序，最新在前）

**版本字段：**
- `short_version` - 短版本号（如 "35.3.0"）
- `bundle_version` - Bundle版本号（如 "353015"）
- `app_ext_vrs_id` - 版本外部标识符
- `download_url` - 下载链接
- `md5` - 文件MD5校验码
- `uncompressed_size` - 解压后大小（字节）
- `download_size` - 下载大小（字节）
- `appstore_display_size` - App Store显示大小（如 "515M"）

## 批量获取App历史版本信息

### 脚本：batch_fetch_versions.py

#### 基本用法

**注意：`--app_id` 参数为必填项，用于指定要获取的App的App Store ID。**

- 获取最新版本：
  ```bash
  python3 batch_fetch_versions.py --app_id 440948110
  ```

- 获取最近N个版本（如最近10个）：
  ```bash
  python3 batch_fetch_versions.py --app_id 440948110 --latest 10
  ```

- 获取指定版本（支持多个ID，用逗号分隔）：
  ```bash
  python3 batch_fetch_versions.py --app_id 440948110 --ids 876862684,876666097,876468641
  ```

- 获取其他App的版本信息（如抖音）：
  ```bash
  python3 batch_fetch_versions.py --app_id 1142110895 --latest 5
  ```

#### 参数说明

- `--app_id` - App Store ID（必填），例如：
  - 快手：`440948110`
  - 抖音：`1142110895`
  - 微信：`414478124`
- `--latest N` - 获取最近N个版本
- `--ids id1,id2,...` - 获取指定版本ID，多个用逗号分隔

#### 输出说明
- 输出JSON文件会自动命名：
  - `app_440948110_latest.json`：最新版本
  - `app_440948110_latest_10.json`：最近10个版本
  - `app_440948110_ids_876862684_876666097.json`：指定ID
- 每次请求的原始XML会保存在 `xml_files/` 目录下，已存在则自动复用
- 结果JSON中的 `versions` 数组为倒序（最新在前）
- 自动生成/更新 `ios_appstore_parsed_{app_id}.json` 文件

#### 依赖
- 需要Python 3
- 依赖库：`requests`（如有网络请求）、`json`（标准库）

#### 示例
```bash
# 获取快手最新版本
python3 batch_fetch_versions.py --app_id 440948110

# 获取快手最近5个版本
python3 batch_fetch_versions.py --app_id 440948110 --latest 5

# 获取抖音指定版本
python3 batch_fetch_versions.py --app_id 1142110895 --ids 876763609,876573499

# 获取微信最近100个版本
python3 batch_fetch_versions.py --app_id 414478124 --latest 100
```

#### 常见App ID参考
- 快手：`440948110`
- 抖音：`1142110895`
- 微信：`414478124`
- 支付宝：`333206289`
- 淘宝：`387682726`
- 拼多多：`1044283059`

## 系统要求

- Python 3.6+
- 标准库：xml.etree.ElementTree, json, sys, typing

## 注意事项

1. XML文件必须是有效的iOS AppStore plist格式
2. 文件大小以字节为单位，脚本会自动格式化为可读格式（KB、MB、GB）
3. 支持查找主应用版本和增量更新包版本
4. 精简版应用信息（thinned-app）如果存在也会被解析
5. `batch_fetch_versions.py` 需要有效的Apple认证信息才能获取XML数据

## 错误处理

- 如果XML文件无法加载，会显示错误信息
- 如果找不到指定版本，会提示"未找到版本信息"
- 如果解析失败，会显示"无法解析XML文件"
- 如果未提供 `--app_id` 参数，会显示帮助信息和用法示例 