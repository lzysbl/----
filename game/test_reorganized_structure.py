#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试重新组织后的代码结构
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有关键模块的导入"""
    try:
        print("测试核心模块导入...")
        from core.game_enhanced import Game
        from core.game_state import GameState
        from core.battle import BattleSystem
        print("✓ 核心模块导入成功")
        
        print("测试实体模块导入...")
        from entities.player import Player
        from entities.enemy import Enemy
        from entities.enemy_spawner import EnemySpawner
        from entities.item import Item
        print("✓ 实体模块导入成功")
        
        print("测试系统模块导入...")
        from systems.equipment import EquipmentSystem
        from systems.inventory import InventoryUI
        from systems.skill_system import SkillSystem
        from systems.save_system import SaveSystem
        print("✓ 系统模块导入成功")
        
        print("测试UI模块导入...")
        from ui.hud import draw_hud
        from ui.font_manager import FontManager
        print("✓ UI模块导入成功")
        
        print("测试工具模块导入...")
        from utils.map import GameMap
        print("✓ 工具模块导入成功")
        
        print("\n🎉 所有模块导入测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def test_game_creation():
    """测试游戏对象创建"""
    try:
        print("\n测试游戏对象创建...")
        from core.game_enhanced import Game
        game = Game()
        print("✓ 游戏对象创建成功")
        
        print("测试玩家对象创建...")
        from entities.player import Player
        player = Player(100, 100)
        print(f"✓ 玩家对象创建成功，位置: ({player.x}, {player.y})")
        
        print("测试地图对象创建...")
        from utils.map import GameMap
        game_map = GameMap()
        print("✓ 地图对象创建成功")
        
        print("测试装备系统...")
        from systems.equipment import EquipmentSystem
        equipment_list = EquipmentSystem.get_all_equipment()
        print(f"✓ 装备系统正常，共 {len(equipment_list)} 种装备")
        
        return True
        
    except Exception as e:
        print(f"❌ 对象创建测试失败: {e}")
        return False

def main():
    """主函数"""
    print("="*50)
    print("测试重新组织后的代码结构")
    print("="*50)
    
    # 测试导入
    import_success = test_imports()
    
    if import_success:
        # 测试对象创建
        creation_success = test_game_creation()
        
        if creation_success:
            print("\n🎉 代码结构重组成功！所有测试通过！")
            print("\n文件夹结构:")
            print("├── core/         # 核心游戏逻辑")
            print("├── entities/     # 游戏实体")
            print("├── systems/      # 游戏系统")
            print("├── ui/           # 用户界面")
            print("├── utils/        # 工具模块")
            print("├── tests/        # 测试文件")
            print("└── launcher.py   # 启动器")
            
            print("\n使用方式:")
            print("python launcher.py  # 启动游戏")
            print("python launcher.py 选择对应的测试选项")
            
        else:
            print("\n❌ 对象创建测试失败")
    else:
        print("\n❌ 导入测试失败")

if __name__ == "__main__":
    main()
