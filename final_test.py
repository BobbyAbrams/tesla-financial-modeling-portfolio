#!/usr/bin/env python
"""
最终应用测试
"""
import sys

def run_test():
    print("🚀 Tesla仪表板最终测试")
    print("=" * 60)
    
    all_passed = True
    
    # 测试1: 导入数据处理模块
    print("\n1. 测试数据处理模块...")
    try:
        from deploy.data_processor import tesla_data
        data = tesla_data.data
        print("✅ 数据处理模块导入成功")
        
        # 验证数据
        required = ['regional_data', 'forecast_data', 'traditional_business', 'new_business']
        for key in required:
            if key in data:
                print(f"   ✅ {key}: 可用")
            else:
                print(f"   ❌ {key}: 缺失")
                all_passed = False
    except Exception as e:
        print(f"❌ 数据处理模块错误: {e}")
        all_passed = False
    
    # 测试2: 测试列名访问
    print("\n2. 测试列名访问...")
    try:
        regions = data['regional_data']['地区'].tolist()
        print(f"✅ 地区列访问成功: {len(regions)} 个地区")
        
        years = data['traditional_business']['年份'].tolist()
        print(f"✅ 年份列访问成功: {len(years)} 个年份")
    except Exception as e:
        print(f"❌ 列访问错误: {e}")
        all_passed = False
    
    # 测试3: 导入主应用
    print("\n3. 测试主应用导入...")
    try:
        from app import app
        print("✅ 主应用导入成功")
        
        # 检查必要属性
        required_attrs = ['layout', 'server']
        for attr in required_attrs:
            if hasattr(app, attr):
                print(f"   ✅ 有 {attr} 属性")
            else:
                print(f"   ❌ 缺少 {attr} 属性")
                all_passed = False
    except Exception as e:
        print(f"❌ 主应用导入错误: {e}")
        import traceback
        traceback.print_exc()
        all_passed = False
    
    # 测试4: 测试回调函数
    print("\n4. 测试应用结构...")
    try:
        # 检查是否有回调函数
        import inspect
        import app as app_module
        
        callbacks = [name for name, obj in inspect.getmembers(app_module) 
                    if hasattr(obj, '__name__') and 'callback' in obj.__name__]
        
        if callbacks:
            print(f"✅ 找到 {len(callbacks)} 个回调函数")
        else:
            print("⚠️  未找到回调函数")
    except Exception as e:
        print(f"⚠️  回调函数检查错误: {e}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！应用已完全准备好部署。")
        return True
    else:
        print("❌ 测试失败，请修复问题。")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
