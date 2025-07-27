# EdgeOne优选IP检测与更新工具

这是一个用于检测有效IP地址并自动更新DNS记录的工具集。该工具可以检测指定网段中的可用IP，并将这些IP地址配置到华为云DNS服务中。

## 功能特性

1. **IP地址检测**：并发检测指定网段中的可用IP地址
2. **响应时间排序**：根据响应时间对有效IP进行排序
3. **DNS记录更新**：自动将检测到的有效IP更新到华为云DNS服务
4. **通知推送**：通过Bark服务发送操作结果通知

## 文件说明

- `eo.py`：IP地址检测主程序
- `updatedns.py`：华为云DNS更新程序
- `main.py`：程序入口文件
- `eo.txt`：待检测的IP网段列表（CIDR格式）
- `yes.txt`：检测到的有效IP地址列表
- `requirements.txt`：项目依赖包列表

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. IP地址检测

1. 编辑 `eo.txt` 文件，添加需要检测的IP网段（CIDR格式）：
   ```
   43.174.150.0/24
   43.175.130.0/24
   43.175.132.0/24
   ```

2. 运行IP检测程序：
   ```bash
   python main.py
   ```

3. 程序会生成 `yes.txt` 文件，包含响应时间最快的50个有效IP地址。

### 2. DNS记录更新

1. 配置 `updatedns.py` 中的以下参数：
   - `access_key_id`：华为云账号AccessKey
   - `access_key_secret`：华为云账号AccessKey Secret
   - `device_key`：Bark通知服务的设备key
   - `ZONE_NAME`：域名区域名称
   - `RECORD_NAME`：要更新的记录名称

2. 运行DNS更新程序：
   ```bash
   python updatedns.py
   ```

## 配置说明

请将 `config.py.example` 改名为 `config.py`，并根据实际情况修改其中的参数。

### eo.py 配置

- `INPUT_FILE`：输入文件名（待检测的IP网段列表）
- `OUTPUT_FILE`：输出文件名（检测到的有效IP列表）
- `TIMEOUT`：每个请求的超时时间（秒）
- `MAX_WORKERS`：最大并发请求数
- `TARGET_HOST`：目标主机地址
- `TOTAL`：保留的有效IP数量

### updatedns.py 配置

- `ACCESS_KEY_ID`：华为云账号AccessKey
- `ACCESS_KEY_SECRET`：华为云账号AccessKey Secret
- `ZONE_NAME`：域名区域名称
- `RECORD_NAME`：要更新的记录名称
- `device_key`：Bark通知服务的设备key

## 许可证

[MIT License](LICENSE)