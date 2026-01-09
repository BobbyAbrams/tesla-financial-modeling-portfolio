#!/usr/bin/env python
"""
修复app.py中的列名不匹配问题
"""

import re

# 读取app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 需要修复的列名映射
replacements = [
    ("data\['regional_data'\]\['Region'\]", "data['regional_data']['地区']"),
    ("data\['regional_data'\]\['Region'\]\.tolist\(\)", "data['regional_data']['地区'].tolist()"),
    ("regional_data\['Region'\]", "regional_data['地区']"),
    ("forecast_data\['Region'\]", "forecast_data['地区']"),
    ("\['Region'\]", "['地区']"),
    ("'Region'", "'地区'"),
]

# 应用替换
for old, new in replacements:
    content = re.sub(old, new, content)

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 已修复列名不匹配问题")
print("原始列名 'Region' 已替换为 '地区'")
