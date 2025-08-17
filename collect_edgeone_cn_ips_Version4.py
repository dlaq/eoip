import dns.resolver

# 常用中国大陆 DNS 服务器
dns_servers = [
    "114.114.114.114",   # 114DNS
    "223.5.5.5",         # 阿里DNS
    "119.29.29.29",      # 腾讯DNS
    "180.76.76.76",      # 百度DNS
    "202.96.128.68",     # 广东电信
    "218.30.118.6",      # 北京联通
]

domain = "edgeone.ai"
ips = set()

for server in dns_servers:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server]
    try:
        answer = resolver.resolve(domain, 'A', lifetime=3)
        for rdata in answer:
            ips.add(rdata.address)
        print(f"{server}: {', '.join([r.address for r in answer])}")
    except Exception as e:
        print(f"{server}: 查询失败 ({e})")

print("\n中国大陆常见 DNS 解析到的 edgeone.ai IP如下：")
for ip in ips:
    print(ip)