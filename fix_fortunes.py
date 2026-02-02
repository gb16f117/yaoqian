#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# 读取app.py文件
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义函数：给签文content字段中的逗号后添加\n（如果还没有的话）
def add_newlines_to_content(text):
    # 找到所有content字段的值
    pattern = r'"content": "([^"]*)"'

    def replace_content(match):
        content_str = match.group(1)
        # 如果字符串中还没有\n，则在每个逗号后添加\n
        if '\\n' not in content_str and '，' in content_str:
            new_content = content_str.replace('，', '，\\n')
            return f'"content": "{new_content}"'
        else:
            return match.group(0)

    return re.sub(pattern, replace_content, text)

# 处理content
new_content = add_newlines_to_content(content)

# 同样处理interpretation字段（可选，如果需要的话）
# 这里只处理content

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 已完成！所有签文content字段中的逗号后已添加换行符\\n")
