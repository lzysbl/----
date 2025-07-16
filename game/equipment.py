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
            # 武器类
            "iron_sword": Equipment("铁剑", "weapon", {
                "attack": 15,
                "description": "普通的铁制剑，增加攻击力"
            }),
            "steel_sword": Equipment("钢剑", "weapon", {
                "attack": 25,
                "level_requirement": 3,
                "description": "坚固的钢制剑，大幅增加攻击力"
            }),
            "silver_sword": Equipment("银剑", "weapon", {
                "attack": 35,
                "level_requirement": 5,
                "description": "银制长剑，对邪恶生物有额外伤害"
            }),
            "magic_sword": Equipment("魔法剑", "weapon", {
                "attack": 45,
                "mp": 20,
                "level_requirement": 7,
                "description": "蕴含魔法力量的剑，增加攻击力和魔法值"
            }),
            "dragon_sword": Equipment("龙鳞剑", "weapon", {
                "attack": 60,
                "level_requirement": 10,
                "description": "传说中的龙鳞剑，极其锋利"
            }),
            
            # 护甲类
            "leather_armor": Equipment("皮甲", "armor", {
                "defense": 8,
                "hp": 20,
                "description": "轻便的皮制护甲，提供基础防护"
            }),
            "chain_armor": Equipment("锁甲", "armor", {
                "defense": 15,
                "hp": 40,
                "level_requirement": 4,
                "description": "金属链甲，提供更好的防护"
            }),
            "plate_armor": Equipment("板甲", "armor", {
                "defense": 25,
                "hp": 60,
                "level_requirement": 6,
                "description": "重型板甲，提供极佳的防护"
            }),
            "magic_armor": Equipment("魔法护甲", "armor", {
                "defense": 20,
                "hp": 50,
                "mp": 30,
                "level_requirement": 8,
                "description": "魔法护甲，同时提供防护和魔法值"
            }),
            "dragon_armor": Equipment("龙鳞甲", "armor", {
                "defense": 40,
                "hp": 100,
                "level_requirement": 12,
                "description": "传说中的龙鳞甲，防御力极高"
            }),
            
            # 饰品类
            "basic_ring": Equipment("基础戒指", "accessory", {
                "mp": 30,
                "level_requirement": 2,
                "description": "神秘的戒指，增加魔法值"
            }),
            "magic_ring": Equipment("魔法戒指", "accessory", {
                "mp": 50,
                "attack": 5,
                "level_requirement": 4,
                "description": "魔法戒指，增加魔法值和攻击力"
            }),
            "power_ring": Equipment("力量戒指", "accessory", {
                "attack": 10,
                "defense": 5,
                "level_requirement": 5,
                "description": "散发力量的戒指，全面提升属性"
            }),
            "wisdom_ring": Equipment("智慧戒指", "accessory", {
                "mp": 80,
                "level_requirement": 6,
                "description": "智慧戒指，大幅增加魔法值"
            }),
            "health_amulet": Equipment("生命护符", "accessory", {
                "hp": 80,
                "defense": 8,
                "level_requirement": 7,
                "description": "生命护符，增加生命值和防御力"
            }),
            "master_ring": Equipment("大师戒指", "accessory", {
                "attack": 15,
                "defense": 10,
                "mp": 40,
                "level_requirement": 9,
                "description": "大师级戒指，全面提升所有属性"
            }),
            "dragon_amulet": Equipment("龙之护符", "accessory", {
                "attack": 20,
                "defense": 15,
                "hp": 60,
                "mp": 60,
                "level_requirement": 15,
                "description": "传说中的龙之护符，极大提升所有属性"
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
        if random.random() < 0.4:  # 40%概率
            loot.append({"type": "item", "name": "Potion"})
        
        # 装备掉落 - 大幅增加掉落率
        equipment_drop_rate = 0.4 + (enemy_level * 0.1)  # 基础40%，每等级增加10%
        if random.random() < equipment_drop_rate:
            # 根据敌人等级确定可掉落的装备
            available_equipment = []
            
            # 1级装备
            if enemy_level >= 1:
                available_equipment.extend([
                    "iron_sword", "leather_armor", "basic_ring"
                ])
            
            # 3级装备
            if enemy_level >= 3:
                available_equipment.extend([
                    "steel_sword", "chain_armor", "magic_ring"
                ])
            
            # 5级装备
            if enemy_level >= 5:
                available_equipment.extend([
                    "silver_sword", "plate_armor", "power_ring"
                ])
            
            # 7级装备
            if enemy_level >= 7:
                available_equipment.extend([
                    "magic_sword", "magic_armor", "wisdom_ring", "health_amulet"
                ])
            
            # 9级装备
            if enemy_level >= 9:
                available_equipment.extend([
                    "dragon_sword", "dragon_armor", "master_ring"
                ])
            
            # 15级传说装备
            if enemy_level >= 15:
                available_equipment.append("dragon_amulet")
            
            # 随机选择一个装备
            equipment_id = random.choice(available_equipment)
            loot.append({"type": "equipment", "id": equipment_id})
        
        return loot
