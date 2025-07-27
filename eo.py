import subprocess
import ipaddress
from pathlib import Path
import concurrent.futures
from config import INPUT_FILE, OUTPUT_FILE, TIMEOUT, MAX_WORKERS, TARGET_HOST, TOTAL


def expand_ips(line):
    """解析IP或CIDR，返回IP列表"""
    try:
        net = ipaddress.ip_network(line.strip(), strict=False)
        return [str(ip) for ip in net.hosts()]
    except ValueError:
        return [line.strip()]  # 单个IP

def check_ip(ip):
    """使用curl尝试绑定IP访问目标站点，并返回响应时间"""
    curl_cmd = [
        "curl",
        "-s",                     # 静默模式
        "-o", "/dev/null",       # 忽略输出
        "-w", "%{http_code}:%{time_total}",    # 输出HTTP状态码和总时间
        "--resolve", f"{TARGET_HOST}:443:{ip}",
        "--max-time", str(TIMEOUT),
        f"https://{TARGET_HOST}"
    ]

    try:
        # 直接在终端运行curl命令
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 2  # 预留少量时间用于命令处理
        )
        output = result.stdout.strip()
        if ":" in output:
            status_code, response_time = output.split(":", 1)
            response_time = float(response_time)
        else:
            status_code = output
            response_time = TIMEOUT + 2
        
        if status_code == "404":
            print(f"[+] {ip} ✅ ({response_time:.3f}s)")
            return (ip, response_time)
        else:
            print(f"[-] {ip} ❌ (HTTP {status_code})")
    except subprocess.TimeoutExpired:
        print(f"[!] {ip} ⏰ 超时")
    except Exception as e:
        print(f"[!] {ip} ⚠️ 错误: {e}")
    return None

def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)
    output_path.write_text("")  # 清空 yes.txt

    all_ips = []
    for line in input_path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        all_ips.extend(expand_ips(line))

    print(f"共加载 {len(all_ips)} 个IP，开始检查...\n")

    valid_ips_with_time = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_ip, ip): ip for ip in all_ips}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_ips_with_time.append(result)

    # 按照响应时间排序，时间越短越靠前
    valid_ips_with_time.sort(key=lambda x: x[1])
    
    # 提取排序后的IP列表
    valid_ips = [ip for ip, _ in valid_ips_with_time]

    # 根据TOTAL配置决定写入多少个IP
    if len(valid_ips) > TOTAL:
        # 如果结果大于TOTAL，只保留前TOTAL个IP
        write_ips = valid_ips[:TOTAL]
        print(f"\n✅ 检测完成，{len(valid_ips)} 个IP可用，已写入速度前 {TOTAL} 个IP到 {OUTPUT_FILE}")
    else:
        # 如果结果小于等于TOTAL，全部写入
        write_ips = valid_ips
        print(f"\n✅ 检测完成，{len(valid_ips)} 个IP可用，已全部写入 {OUTPUT_FILE}")
    
    # 写入有效IP
    output_path.write_text("\n".join(write_ips), encoding='utf-8')

if __name__ == "__main__":
    main()
