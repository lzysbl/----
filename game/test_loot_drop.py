#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试装备掉落系统
"""

from equipment import LootSystem

def test_loot_drop():
    """测试装备掉落率"""
    print("=== 装备掉落测试 ===")
    
    # 测试不同等级的敌人
    for enemy_level in [1, 2, 3, 4, 5]:
        print(f"\n敌人等级 {enemy_level}:")
        
        equipment_count = 0
        potion_count = 0
        total_tests = 100
        
        for i in range(total_tests):
            loot = LootSystem.generate_loot(enemy_level)
            
            for item in loot:
                if item["type"] == "equipment":
                    equipment_count += 1
                elif item["type"] == "item" and item["name"] == "Potion":
                    potion_count += 1
        
        equipment_rate = (equipment_count / total_tests) * 100
        potion_rate = (potion_count / total_tests) * 100
        
        print(f"  装备掉落率: {equipment_rate:.1f}%")
        print(f"  血瓶掉落率: {potion_rate:.1f}%")
        print(f"  装备掉落次数: {equipment_count}/100")
        print(f"  血瓶掉落次数: {potion_count}/100")
        
        # 显示掉落的装备类型
        equipment_types = {}
        for i in range(50):  # 生成50次来看装备类型分布
            loot = LootSystem.generate_loot(enemy_level)
            for item in loot:
                if item["type"] == "equipment":
                    equipment_id = item["id"]
                    equipment_types[equipment_id] = equipment_types.get(equipment_id, 0) + 1
        
        if equipment_types:
            print("  装备类型分布:")
            for eq_id, count in equipment_types.items():
                print(f"    {eq_id}: {count}次")

if __name__ == "__main__":
    test_loot_drop()
