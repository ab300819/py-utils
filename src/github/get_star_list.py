#!/usr/bin/env python3

import os
import requests
import pandas as pd

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("⚠️ 没有找到 GITHUB_TOKEN 环境变量，请设置后重试")
    exit()

headers = {"Authorization": f"token {token}"}
stars = []
page = 1

print("⏳ 正在获取 GitHub Star 列表...")

while True:
    url = f"https://api.github.com/user/starred?page={page}&per_page=100"
    r = requests.get(url, headers=headers)
    data = r.json()

    if not data:
        break

    for repo in data:
        stars.append({
            "full_name": repo["full_name"],
            "html_url": repo["html_url"],
            "description": repo["description"] or ""
        })

    page += 1

df = pd.DataFrame(stars)

# 保存为 CSV
df.to_csv("github_stars.csv", index=False, encoding="utf-8-sig")

# 保存为 Markdown
md = df.to_markdown(index=False)
with open("github_stars.md", "w", encoding="utf-8") as f:
    f.write(md)

print(f"✅ 完成！共导出 {len(df)} 个 Star 仓库")
print("📄 已生成文件：github_stars.csv、github_stars.md")