#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试扩展装备系统
验证新增装备和掉落系统
"""

from equipment import EquipmentSystem, LootSystem

def test_expanded_equipment():
    """测试扩展装备系统"""
    print("=== 扩展装备系统测试 ===")
    
    # 获取所有装备
    equipment_system = EquipmentSystem()
    all_equipment = equipment_system.get_all_equipment()
    
    print(f"总装备数量: {len(all_equipment)}")
    print()
    
    # 按类型分组显示装备
    weapon_count = 0
    armor_count = 0
    accessory_count = 0
    
    print("=== 武器类装备 ===")
    for eq_id, equipment in all_equipment.items():
        if equipment.type == "weapon":
            weapon_count += 1
            print(f"{weapon_count}. {equipment.name} (等级{equipment.level_requirement})")
            print(f"   攻击力: +{equipment.stats.get('attack', 0)}")
            if 'mp' in equipment.stats:
                print(f"   魔法值: +{equipment.stats['mp']}")
            print(f"   描述: {equipment.description}")
            print()
    
    print("=== 护甲类装备 ===")
    for eq_id, equipment in all_equipment.items():
        if equipment.type == "armor":
            armor_count += 1
            print(f"{armor_count}. {equipment.name} (等级{equipment.level_requirement})")
            print(f"   防御力: +{equipment.stats.get('defense', 0)}")
            print(f"   生命值: +{equipment.stats.get('hp', 0)}")
            if 'mp' in equipment.stats:
                print(f"   魔法值: +{equipment.stats['mp']}")
            print(f"   描述: {equipment.description}")
            print()
    
    print("=== 饰品类装备 ===")
    for eq_id, equipment in all_equipment.items():
        if equipment.type == "accessory":
            accessory_count += 1
            print(f"{accessory_count}. {equipment.name} (等级{equipment.level_requirement})")
            stats_info = []
            if 'attack' in equipment.stats:
                stats_info.append(f"攻击力: +{equipment.stats['attack']}")
            if 'defense' in equipment.stats:
                stats_info.append(f"防御力: +{equipment.stats['defense']}")
            if 'hp' in equipment.stats:
                stats_info.append(f"生命值: +{equipment.stats['hp']}")
            if 'mp' in equipment.stats:
                stats_info.append(f"魔法值: +{equipment.stats['mp']}")
            print(f"   {', '.join(stats_info)}")
            print(f"   描述: {equipment.description}")
            print()
    
    print("=== 装备统计 ===")
    print(f"武器: {weapon_count}种")
    print(f"护甲: {armor_count}种")
    print(f"饰品: {accessory_count}种")
    print(f"总计: {weapon_count + armor_count + accessory_count}种")
    print()
    
    # 测试掉落系统
    print("=== 掉落系统测试 ===")
    for enemy_level in range(1, 16, 2):  # 测试1,3,5,7,9,11,13,15级
        print(f"\\n{enemy_level}级敌人掉落测试:")
        
        equipment_drops = {}
        total_tests = 100
        
        for i in range(total_tests):
            loot = LootSystem.generate_loot(enemy_level)
            for item in loot:
                if item["type"] == "equipment":
                    equipment_id = item["id"]
                    if equipment_id in all_equipment:
                        equipment_name = all_equipment[equipment_id].name
                        equipment_drops[equipment_name] = equipment_drops.get(equipment_name, 0) + 1
                    else:
                        print(f"  ⚠️  未知装备ID: {equipment_id}")
        
        if equipment_drops:
            print("  掉落装备分布:")
            for equipment_name, count in sorted(equipment_drops.items(), key=lambda x: x[1], reverse=True):
                print(f"    {equipment_name}: {count}次")
        else:
            print("  没有装备掉落")
    
    print("\\n=== 魔法戒指识别测试 ===")
    magic_ring = all_equipment.get("magic_ring")
    if magic_ring:
        print(f"✓ 魔法戒指识别成功: {magic_ring.name}")
        print(f"  类型: {magic_ring.type}")
        print(f"  等级要求: {magic_ring.level_requirement}")
        print(f"  属性: {magic_ring.stats}")
        print(f"  描述: {magic_ring.description}")
    else:
        print("✗ 魔法戒指识别失败")
    
    print("\\n✓ 扩展装备系统测试完成")

if __name__ == "__main__":
    test_expanded_equipment()
