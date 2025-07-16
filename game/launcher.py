#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
艾诺迪亚风格RPG游戏启动脚本
"""

import sys
import os

def check_dependencies():
    """检查依赖包"""
    try:
        import pygame
        print(f"✓ pygame {pygame.version.ver} 已安装")
        return True
    except ImportError:
        print("✗ pygame 未安装")
        print("请运行: pip install pygame")
        return False

def main():
    """主函数"""
    print("="*50)
    print("艾诺迪亚风格RPG游戏")
    print("="*50)
    
    # 检查依赖
    if not check_dependencies():
        input("按任意键退出...")
        sys.exit(1)
    
    print("\n选择游戏版本:")
    print("1. 增强版游戏 (推荐) - 包含菜单、存档、完整功能")
    print("2. 标准版游戏 - 基础游戏循环")
    print("3. 按键测试 - 测试输入法兼容性")
    print("4. WASD移动测试 - 测试新的移动控制")
    print("5. 墙体碰撞测试 - 测试墙体碰撞功能")
    print("6. 敌人行为测试 - 测试敌人AI行为")
    print("7. 攻击间隔测试 - 测试敌人攻击间隔")
    print("8. 完整功能测试 - 测试背包系统和敌人生成")
    print("9. 装备替换测试 - 测试装备替换不丢失")
    print("10. 装备掉落测试 - 测试装备掉落到背包")
    print("11. 扩展装备测试 - 测试新增装备和掉落系统")
    print("12. 背包新功能测试 - 测试点击选中、丢弃、摧毁功能")
    print("13. 性能测试 - 数据结构查找性能对比")
    
    try:
        choice = input("\n请选择 (1-13, 默认1): ").strip()
        if not choice:
            choice = "1"
        
        if choice == "1":
            print("\n启动增强版游戏...")
            import game_enhanced
            game_enhanced.Game().run()
        elif choice == "2":
            print("\n启动标准版游戏...")
            import main
            main.main()
        elif choice == "3":
            print("\n启动按键测试...")
            import test_h_key
            test_h_key.main()
        elif choice == "4":
            print("\n启动WASD移动测试...")
            import test_wasd_movement
            test_wasd_movement.test_wasd_movement()
        elif choice == "5":
            print("\n启动墙体碰撞测试...")
            import test_wall_collision
            test_wall_collision.test_wall_collision()
        elif choice == "6":
            print("\n启动敌人行为测试...")
            import test_enemy_behavior
            test_enemy_behavior.test_enemy_behavior()
        elif choice == "7":
            print("\n启动攻击间隔测试...")
            import test_attack_interval
            test_attack_interval.test_attack_interval()
        elif choice == "8":
            print("\n启动完整功能测试...")
            import test_full_features
            test_full_features.test_full_features()
        elif choice == "9":
            print("\n启动装备替换测试...")
            import test_equipment_fix
            test_equipment_fix.test_equipment_replacement()
        elif choice == "10":
            print("\n启动装备掉落测试...")
            import test_drop_to_inventory
            test_drop_to_inventory.test_equipment_drop_to_inventory()
        elif choice == "11":
            print("\n启动扩展装备测试...")
            import test_expanded_equipment
            test_expanded_equipment.test_expanded_equipment()
        elif choice == "12":
            print("\n启动背包新功能测试...")
            import test_inventory_new_features
            test_inventory_new_features.test_inventory_new_features()
        elif choice == "13":
            print("\n启动性能测试...")
            sys.path.append('..')
            import main as perf_test
            perf_test.main()
        else:
            print("无效选择，启动增强版游戏...")
            import game_enhanced
            game_enhanced.Game().run()
            
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"\n错误: {e}")
        input("按任意键退出...")

if __name__ == "__main__":
    main()
