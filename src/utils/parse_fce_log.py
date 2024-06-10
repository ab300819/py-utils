#!/usr/bin/env python3

import csv
import json
import re
from datetime import datetime

# 日志内容
test_log = '2024-06-10 00:24:56,760 [Phenix-IJobExecutorService-thread-59897] INFO com.focustech.fce.service.impl.AnalysisRuntimeServiceImpl [00] [] execParam: {"appNameEn":"landing_server","projectNameEn":"mic_en","idc":"TEL","ip":"192.168.4.101","envCode":"prod1","aiHostId":14124,"appId":23454,"famId":23454,"bashParam":"landing-server.jar,1,7030,jdk-17.0.4.1,1.3.1"}'


def parse_row(log):
    # 提取时间
    time_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}'
    time_match = re.search(time_pattern, log)
    log_time = datetime.strptime(time_match.group(), '%Y-%m-%d %H:%M:%S,%f') if time_match else None

    # 提取 JSON 字符串
    json_pattern = r'execParam: ({.*})'
    json_match = re.search(json_pattern, log)
    json_data = json.loads(json_match.group(1)) if json_match else {}

    # 提取所需字段
    appNameEn = json_data.get('appNameEn')
    projectNameEn = json_data.get('projectNameEn')
    idc = json_data.get('idc')
    ip = json_data.get('ip')
    envCode = json_data.get('envCode')
    appId = json_data.get('appId')

    # 准备 CSV 数据
    return [log_time.strftime('%Y-%m-%d %H:%M:%S'), appId, appNameEn, projectNameEn, idc, envCode, ip]


if __name__ == '__main__':
    csv_data = []
    with open('fce-exec-log.log', 'r') as f:
        csv_data.append(parse_row(log))

    # 写入 CSV 文件
    with open("fce-exec-log.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'appId', 'appNameEn', 'projectNameEn', 'idc', 'envCode', 'ip'])
        for row in csv_data:
            writer.writerow(row)
