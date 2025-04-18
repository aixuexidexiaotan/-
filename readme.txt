# 存储桶遍历与文件下载工具

## 简介

这是一个用于检测存储桶遍历漏洞并下载存储桶中文件的Python脚本工具。它可以自动发现可公开访问的存储桶中的文件列表，并将这些文件下载到本地指定目录。

## 功能特性

- 检测存储桶遍历漏洞
- 提取存储桶中的文件key列表
- 自动下载文件到本地指定路径
- 多线程并发下载加速
- 下载结果统计报告
- 路径安全处理

## 系统要求

- Python 3.6+
- requests库

## 安装

1. 克隆仓库或下载脚本文件：
   ```bash
   git clone https://github.com/yourusername/bucket-downloader.git
   cd bucket-downloader
   ```

2. 安装依赖：
   ```bash
   pip install requests
   ```

## 使用方法

### 基本用法

仅检测存储桶并列出文件key：
```bash
python bucket_downloader.py -u http://target-bucket-url/
```

### 下载文件到本地

检测并下载所有文件到指定目录：
```bash
python bucket_downloader.py -u http://target-bucket-url/ -d ./downloads
```

### 使用多线程下载

使用10个线程并发下载：
```bash
python bucket_downloader.py -u http://target-bucket-url/ -d ./downloads -t 10
```

### 参数说明

| 参数 | 缩写 | 描述 | 必需 | 默认值 |
|------|------|------|------|--------|
| --url | -u | 目标存储桶URL | 是 | 无 |
| --download | -d | 本地下载路径 | 否 | 仅列出key |
| --threads | -t | 并发下载线程数 | 否 | 5 |

## 输出示例

```
[+] 可访问的存储桶: http://target-bucket-url/
[+] 发现 42 个key
[+] 开始下载文件到: ./downloads
    √ 下载成功: http://target-bucket-url/file1.txt -> ./downloads/file1.txt
    √ 下载成功: http://target-bucket-url/images/photo.jpg -> ./downloads/images/photo.jpg
    × 下载失败: http://target-bucket-url/private.doc - 403 Client Error: Forbidden

[+] 下载完成: 成功 40 个, 失败 2 个
```
## 注意事项

1. 请确保遵守所有适用的法律和法规
2. 仅在获得明确授权的情况下对目标系统进行测试
3. 高并发下载可能会对目标服务器造成压力
4. 确保有足够的磁盘空间存放下载的文件
5. 某些存储桶可能有访问限制或速率限制
