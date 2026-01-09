#!/usr/bin/env python
"""
检查应用是否准备好部署到Render
"""

import os
import sys

def check_file_exists(filename, description=""):
    """检查文件是否存在"""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"{status} {filename} {description}")
    return exists

def check_requirements():
    """检查requirements.txt"""
    if not check_file_exists("requirements.txt"):
        return False
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read().strip()
            if content:
                print("  内容:", content[:100] + "..." if len(content) > 100 else content)
                return True
            else:
                print("  ❌ 文件为空")
                return False
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return False

def check_app_structure():
    """检查应用结构"""
    checks = [
        check_file_exists("app.py", "主应用文件"),
        check_file_exists("deploy/data_processor.py", "数据处理模块"),
        check_file_exists("deploy/__init__.py", "包初始化文件"),
    ]
    
    # 检查app.py是否有server变量
    try:
        with open("app.py", "r") as f:
            content = f.read()
            if "server = app.server" in content or "app.server" in content:
                print("✅ app.py包含server变量")
            else:
                print("❌ app.py缺少server变量")
                checks.append(False)
    except Exception as e:
        print(f"❌ 无法检查app.py: {e}")
        checks.append(False)
    
    return all(checks)

def main():
    print("🚀 Tesla仪表板部署准备检查")
    print("=" * 50)
    
    results = []
    
    print("\n📁 文件检查:")
    results.append(check_file_exists("render.yaml", "Render配置"))
    results.append(check_file_exists("runtime.txt", "Python版本配置"))
    results.append(check_file_exists("Procfile", "启动命令配置"))
    results.append(check_requirements())
    
    print("\n🏗️ 应用结构检查:")
    results.append(check_app_structure())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("🎉 所有检查通过！应用已准备好部署到Render。")
        print("\n下一步：")
        print("1. 访问 https://dashboard.render.com")
        print("2. 等待自动部署完成")
        print("3. 检查部署日志")
        return 0
    else:
        print("❌ 检查失败，请修复上述问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
