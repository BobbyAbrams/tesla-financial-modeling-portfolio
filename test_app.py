#!/usr/bin/env python
"""
测试应用是否能正常启动
"""

def test_imports():
    """测试所有必要的导入"""
    imports = [
        ('dash', 'Dash'),
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('plotly.express', 'px'),
        ('plotly.graph_objects', 'go'),
    ]
    
    print("测试导入...")
    for module, alias in imports:
        try:
            exec(f"import {module}")
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            return False
    return True

def test_data_processor():
    """测试数据处理模块"""
    print("\n测试数据处理模块...")
    try:
        from deploy.data_processor import tesla_data
        print(f"  ✅ 成功导入 tesla_data")
        
        # 检查数据
        data = tesla_data.data
        print(f"  ✅ 数据加载成功，包含 {len(data)} 个数据集")
        
        # 检查关键数据
        required_keys = ['regional_data', 'total_forecast', 'traditional_business']
        for key in required_keys:
            if key in data:
                print(f"  ✅ 包含 {key}")
            else:
                print(f"  ❌ 缺少 {key}")
                return False
        return True
    except Exception as e:
        print(f"  ❌ 数据处理模块错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app():
    """测试主应用"""
    print("\n测试主应用...")
    try:
        from app import app
        print("  ✅ 成功导入 app")
        
        # 检查是否有server属性
        if hasattr(app, 'server'):
            print("  ✅ app 包含 server 属性")
            return True
        else:
            print("  ❌ app 缺少 server 属性")
            return False
    except Exception as e:
        print(f"  ❌ 应用导入错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Tesla仪表板应用测试")
    print("=" * 50)
    
    success = True
    success = test_imports() and success
    success = test_data_processor() and success
    success = test_app() and success
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 所有测试通过！应用已准备好部署。")
        return 0
    else:
        print("❌ 测试失败，请修复问题。")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
