import pygame
import random

class Equipment:
    """装备类"""
    def __init__(self, name, equipment_type, stats):
        self.name = name
        self.type = equipment_type  # "weapon", "armor", "accessory"
        self.stats = stats  # {"attack": 0, "defense": 0, "hp": 0, "mp": 0}
        self.level_requirement = stats.get("level_requirement", 1)
        self.description = stats.get("description", "")

class EquipmentSystem:
    """装备系统"""
    
    @staticmethod
    def get_all_equipment():
        """获取所有装备"""
        return {
            "iron_sword": Equipment("铁剑", "weapon", {
                "attack": 15,
                "description": "普通的铁制剑，增加攻击力"
            }),
            "steel_sword": Equipment("钢剑", "weapon", {
                "attack": 25,
                "level_requirement": 3,
                "description": "坚固的钢制剑，大幅增加攻击力"
            }),
            "leather_armor": Equipment("皮甲", "armor", {
                "defense": 8,
                "hp": 20,
                "description": "轻便的皮制护甲，提供基础防护"
            }),
            "chain_mail": Equipment("链甲", "armor", {
                "defense": 15,
                "hp": 40,
                "level_requirement": 4,
                "description": "金属链甲，提供更好的防护"
            }),
            "magic_ring": Equipment("魔法戒指", "accessory", {
                "mp": 30,
                "level_requirement": 2,
                "description": "神秘的戒指，增加魔法值"
            }),
            "power_amulet": Equipment("力量护符", "accessory", {
                "attack": 10,
                "defense": 5,
                "level_requirement": 5,
                "description": "散发力量的护符，全面提升属性"
            })
        }
    
    @staticmethod
    def can_equip(player, equipment):
        """检查玩家是否可以装备该装备"""
        return player.level >= equipment.level_requirement
    
    @staticmethod
    def equip_item(player, equipment_id):
        """装备物品"""
        all_equipment = EquipmentSystem.get_all_equipment()
        if equipment_id not in all_equipment:
            return False
            
        equipment = all_equipment[equipment_id]
        
        if not EquipmentSystem.can_equip(player, equipment):
            return False
        
        # 初始化装备槽
        if not hasattr(player, 'equipped'):
            player.equipped = {"weapon": None, "armor": None, "accessory": None}
        
        # 卸下旧装备
        old_equipment = player.equipped.get(equipment.type)
        if old_equipment:
            EquipmentSystem.unequip_item(player, equipment.type)
        
        # 装备新装备
        player.equipped[equipment.type] = equipment_id
        
        # 应用装备加成
        for stat, value in equipment.stats.items():
            if stat == "attack":
                player.attack_power += value
            elif stat == "defense":
                if not hasattr(player, 'base_defense'):
                    player.base_defense = 0
                player.base_defense += value
            elif stat == "hp":
                player.max_hp += value
                player.hp += value
            elif stat == "mp":
                player.max_mp += value
                player.mp += value
        
        return True
    
    @staticmethod
    def unequip_item(player, equipment_type):
        """卸下装备"""
        if not hasattr(player, 'equipped') or player.equipped.get(equipment_type) is None:
            return False
        
        equipment_id = player.equipped[equipment_type]
        all_equipment = EquipmentSystem.get_all_equipment()
        equipment = all_equipment[equipment_id]
        
        # 移除装备加成
        for stat, value in equipment.stats.items():
            if stat == "attack":
                player.attack_power -= value
            elif stat == "defense":
                player.base_defense -= value
            elif stat == "hp":
                player.max_hp -= value
                player.hp = min(player.hp, player.max_hp)
            elif stat == "mp":
                player.max_mp -= value
                player.mp = min(player.mp, player.max_mp)
        
        player.equipped[equipment_type] = None
        return True

class LootSystem:
    """战利品系统"""
    
    @staticmethod
    def generate_loot(enemy_level):
        """根据敌人等级生成战利品"""
        loot = []
        
        # 金币掉落
        gold_amount = random.randint(5, 20) * enemy_level
        loot.append({"type": "gold", "amount": gold_amount})
        
        # 血瓶掉落
        if random.random() < 0.3:  # 30%概率
            loot.append({"type": "item", "name": "Potion"})
        
        # 装备掉落
        if random.random() < 0.1:  # 10%概率
            available_equipment = ["iron_sword", "leather_armor", "magic_ring"]
            if enemy_level >= 3:
                available_equipment.extend(["steel_sword", "chain_mail"])
            if enemy_level >= 5:
                available_equipment.append("power_amulet")
            
            equipment_id = random.choice(available_equipment)
            loot.append({"type": "equipment", "id": equipment_id})
        
        return loot
