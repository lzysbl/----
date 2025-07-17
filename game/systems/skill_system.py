import pygame
import random

class SkillSystem:
    """技能系统"""
    
    @staticmethod
    def get_available_skills():
        """获取可用技能列表"""
        return {
            "fireball": {
                "name": "火球术",
                "description": "发射火球攻击敌人",
                "damage": 50,
                "cost": 20,  # 魔法消耗
                "cooldown": 3000,  # 冷却时间(毫秒)
                "range": 100
            },
            "heal": {
                "name": "治疗术",
                "description": "恢复生命值",
                "heal": 50,
                "cost": 15,
                "cooldown": 5000,
                "range": 0
            },
            "shield": {
                "name": "护盾术",
                "description": "提供临时防护",
                "defense": 10,
                "cost": 25,
                "cooldown": 8000,
                "duration": 10000  # 持续时间
            }
        }
    
    @staticmethod
    def cast_skill(player, skill_name, target_pos=None):
        """释放技能"""
        skills = SkillSystem.get_available_skills()
        if skill_name not in skills:
            return False
            
        skill = skills[skill_name]
        current_time = pygame.time.get_ticks()
        
        # 检查魔法值
        if player.mp < skill["cost"]:
            return False
            
        # 检查冷却时间
        if hasattr(player, 'skill_cooldowns'):
            if skill_name in player.skill_cooldowns:
                if current_time - player.skill_cooldowns[skill_name] < skill["cooldown"]:
                    return False
        else:
            player.skill_cooldowns = {}
            
        # 消耗魔法值
        player.mp -= skill["cost"]
        player.skill_cooldowns[skill_name] = current_time
        
        # 执行技能效果
        if skill_name == "fireball":
            return SkillSystem._cast_fireball(player, skill, target_pos)
        elif skill_name == "heal":
            return SkillSystem._cast_heal(player, skill)
        elif skill_name == "shield":
            return SkillSystem._cast_shield(player, skill)
            
        return True
    
    @staticmethod
    def _cast_fireball(player, skill, target_pos):
        """火球术效果"""
        # 创建火球投射物
        if hasattr(player, 'projectiles'):
            player.projectiles.append({
                "type": "fireball",
                "x": player.x,
                "y": player.y,
                "target_x": target_pos[0] if target_pos else player.x + 50,
                "target_y": target_pos[1] if target_pos else player.y,
                "damage": skill["damage"],
                "speed": 5
            })
        return True
    
    @staticmethod
    def _cast_heal(player, skill):
        """治疗术效果"""
        heal_amount = min(skill["heal"], player.max_hp - player.hp)
        player.hp += heal_amount
        return True
    
    @staticmethod
    def _cast_shield(player, skill):
        """护盾术效果"""
        current_time = pygame.time.get_ticks()
        if not hasattr(player, 'buffs'):
            player.buffs = {}
        player.buffs['shield'] = {
            "defense": skill["defense"],
            "end_time": current_time + skill["duration"]
        }
        return True
