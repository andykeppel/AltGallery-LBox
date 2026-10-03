# AltGallery-LBox

[![Update source](https://github.com/andykeppel/AltGallery-LBox/actions/workflows/update.yml/badge.svg)](https://github.com/andykeppel/AltGallery-LBox/actions/workflows/update.yml)

将 [AltGallery](https://github.com/bebound/AltGallery) 应用源转换为 LBox 使用的兼容格式。

## 添加到 LBox

在 LBox 的添加源入口粘贴以下地址：

```text
https://raw.githubusercontent.com/andykeppel/AltGallery-LBox/main/altgallery-lbox.json
```

## 自动更新

- 上游：https://raw.githubusercontent.com/bebound/AltGallery/master/all-apps.json
- GitHub Actions 每 6 小时运行一次，计划时间为北京时间 02:17、08:17、14:17、20:17；实际执行可能延迟。
- 也可以进入 Actions → Update AltGallery LBox source → Run workflow 手动更新。
- 仅在内容发生变化时提交；获取或校验失败时保留上一份源。
- GitHub 可能暂停连续 60 天无仓库活动的公开仓库定时工作流；如停止更新，在 Actions 中重新启用。

## 转换规则

保留应用名称、图标、介绍、截图、下载链接、原始 versions 列表及其他上游数据，以上游 versions[0] 为首选版本，补齐每个应用的：

| LBox 顶层字段 | 上游字段 |
| --- | --- |
| version | versions[0].version |
| versionDate | versions[0].date |
| downloadURL | versions[0].downloadURL |
| size | versions[0].size |
| versionDescription | versions[0].localizedDescription |

同时同步 minOSVersion、maxOSVersion、buildVersion（上游提供时）。

本项目仅转换源格式，不托管 IPA，也不改写为代理下载地址。能否安装、运行仍取决于应用自身要求及客户端支持。转换不会解决 GitHub 网络访问或 VPN 并行问题。

## 本地运行

仅需 Python 3.10+，无第三方依赖：

```sh
python convert.py
# 使用已下载的上游 JSON 校验
python convert.py --input all-apps.json --output altgallery-lbox.json
```

应用数据与资源归上游项目及各应用作者所有。本仓库为独立兼容转换，不代表 AltGallery 官方。
