import urllib.request
import base64
import re

def decode_base64(data):
    # اصلاح پدینگ برای دیکود کردن بدون خطا
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return ""

def encode_base64(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def fetch_configs(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8').strip()
            # اگر محتوا از قبل base64 شده باشد
            if not content.startswith(('vmess://', 'vless://', 'ss://', 'trojan://')):
                decoded = decode_base64(content)
                if decoded:
                    content = decoded
            return content.splitlines()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    # خواندن لینک‌های منبع
    try:
        with open('sources.txt', 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("sources.txt not found!")
        return

    all_configs = []
    seen_identifiers = set()

    for url in urls:
        print(f"Fetching from: {url}")
        configs = fetch_configs(url)
        for config in configs:
            config = config.strip()
            if not config:
                continue
            
            # استخراج آدرس و پورت برای حذف تکراری‌ها
            # این بخش سعی می‌کند کانفیگ‌های کاملاً تکراری را فیلتر کند
            match = re.search(r'@(.*?)(?:\?|#|$)', config)
            if match:
                identifier = match.group(1)
                if identifier in seen_identifiers:
                    continue
                seen_identifiers.add(identifier)
            
            all_configs.append(config)

    # ادغام و ذخیره به صورت Base64 برای سازگاری با تمام کلاینت‌ها
    merged_flat = "\n".join(all_configs)
    merged_base64 = encode_base64(merged_flat)

    with open('sub.txt', 'w') as f:
        f.write(merged_base64)
    
    print(f"Successfully merged {len(all_configs)} configs into sub.txt")

if __name__ == '__main__':
    main()
