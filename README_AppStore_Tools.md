# App Store 工具使用指南

这个项目包含了一套用于获取 App Store 应用信息和更新版本日期的工具。

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

**功能**: 从历史版本数据中提取发布日期，并更新到版本文件中

**使用方法**:
```bash
python3 update_version_dates.py [app_id]
```

**参数**:
- `app_id`: App Store 应用 ID（可选）
  - 如果不提供，会显示帮助信息和常见 App ID 列表

**示例**:
```bash
# 更新指定 App 的版本日期
python3 update_version_dates.py 1142110895

# 显示帮助和常见 App 列表
python3 update_version_dates.py
```

## 常见 App ID 列表

| App 名称 | App ID | 开发者 |
|---------|--------|--------|
| 快手 (Kuaishou) | 440948110 | Beijing Kwai Technology Co., Ltd. |
| 抖音 (TikTok) | 1142110895 | Beijing Douyin Technology Co., Ltd. |
| 微信 (WeChat) | 414478124 | WeChat |
| QQ | 444934666 | Tencent Technology (Shenzhen) Company Limited |
| 支付宝 (Alipay) | 333206289 | Alipay (Hangzhou) Technology Co., Ltd. |
| 淘宝 (Taobao) | 387682726 | Taobao (China) Software Co., Ltd. |
| 京东 (JD) | 414245813 | Beijing Jingdong Century Trading Co., Ltd. |
| 美团 (Meituan) | 423084029 | Beijing Sanfast Information Technology Co., Ltd. |
| 滴滴出行 (DiDi) | 564499420 | Beijing Xiaoju Technology Co., Ltd. |
| 微博 (Weibo) | 350962117 | Weibo Corporation |
| 今日头条 (Toutiao) | 529092160 | Beijing ByteDance Technology Co., Ltd. |
| 百度 (Baidu) | 382201985 | Baidu Online Network Technology (Beijing) Co., Ltd. |
| 网易云音乐 (NetEase) | 590338362 | NetEase (Hangzhou) Network Co., Ltd. |
| QQ音乐 (QQ Music) | 414603431 | Tencent Technology (Shenzhen) Company Limited |
| 爱奇艺 (iQiyi) | 393765873 | Beijing Qiyi Century Science & Technology Co., Ltd. |
| 腾讯视频 (Tencent Video) | 458318329 | Tencent Technology (Shenzhen) Company Limited |
| 优酷 (Youku) | 336141475 | Youku Tudou Inc. |

## 工作流程

1. **搜索 App ID**: 使用 `search_app_id_simple.py` 搜索应用名称获取 App ID
   - 可以使用 `-l` 参数控制显示结果数量
   - 默认只显示第一个（最相关）的结果
2. **更新版本日期**: 使用 `update_version_dates.py` 更新版本文件中的发布日期

## 文件结构

```
appstore_parse/
├── search_app_id_simple.py      # App ID 搜索工具
├── update_version_dates.py      # 版本日期更新工具
├── version_input/               # 历史版本数据输入目录
│   └── ios_appstore_history_*.json
├── version_output/              # 版本文件输出目录
│   └── app_*_latest_*.json
└── README_AppStore_Tools.md     # 本说明文档
```

## 注意事项

1. **API 限制**: App Store 搜索 API 可能有请求频率限制
2. **数据时效性**: 历史版本数据可能不是最新的
3. **文件依赖**: 更新版本日期需要对应的历史数据文件存在
4. **网络连接**: 需要稳定的网络连接来访问 App Store API
5. **结果数量**: 搜索工具默认只显示第一个结果，可以通过 `-l` 参数调整

## 故障排除

### 搜索失败
- 检查网络连接
- 确认 App 名称正确
- 尝试使用英文名称搜索
- 检查 `-l` 参数值是否合理（必须大于0）

### 更新失败
- 确认历史数据文件存在
- 检查 App ID 是否正确
- 验证版本文件格式

## 技术细节

### 搜索 API
- **端点**: `https://amp-api-search-edge.apps.apple.com/v1/catalog/cn/search`
- **方法**: GET
- **参数**: 
  - `platform=iphone`: 平台
  - `term`: 搜索关键词（URL编码）
  - `l=zh-Hans-CN`: 语言

### 数据结构
搜索结果的数据结构：
```json
{
  "results": {
    "search": {
      "data": [
        {
          "id": "App ID",
          "attributes": {
            "name": "App 名称",
            "artistName": "开发者"
          }
        }
      ]
    }
  }
}
```

### 版本文件格式
```json
{
  "app_name": "应用名称",
  "item_id": "App ID",
  "total_versions": 99,
  "versions": [
    {
      "short_version": "版本号",
      "bundle_version": "构建号",
      "release_date": "发布日期"
    }
  ]
}
``` 