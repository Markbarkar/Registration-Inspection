import requests

proxy_url = "http://abc4841381_82v3-zone-star-region-US:AAAAaaaa9527@na.9dc1b25972c51e1b.abcproxy.vip:4950"

proxies = {
    "http": proxy_url,
    "https": proxy_url,  # 对 HTTPS，一般也用 http://user:pass@host:port（HTTP CONNECT）
}

# 简单请求示例
try:
    r = requests.get("https://httpbin.org/get", proxies=proxies, timeout=10)
    print("status:", r.status_code)
    print(r.text)
except requests.exceptions.RequestException as e:
    print("请求错误：", e)
