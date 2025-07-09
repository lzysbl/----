import pygame
import random

class BattleSystem:
    """战斗系统类，处理更复杂的战斗逻辑"""
    
    @staticmethod
    def calculate_damage(attacker_power, defender_level=1):
        """计算伤害值，加入随机性"""
        base_damage = attacker_power
        variance = random.randint(-5, 5)
        return max(1, base_damage + variance)
    
    @staticmethod
    def calculate_critical_hit():
        """计算是否暴击（10%几率）"""
        return random.random() < 0.1
    
    @staticmethod
    def battle_result(player, enemy):
        """执行一次战斗回合"""
        results = []
        
        # 玩家攻击
        player_damage = BattleSystem.calculate_damage(player.attack_power)
        is_critical = BattleSystem.calculate_critical_hit()
        
        if is_critical:
            player_damage *= 2
            results.append("玩家暴击！")
        else:
            results.append("玩家攻击")
        
        enemy.hp -= player_damage
        
        # 敌人反击（如果还活着）
        if enemy.is_alive():
            enemy_damage = BattleSystem.calculate_damage(enemy.attack_power)
            
            # 计算玩家的有效防御力
            player_defense = player.get_effective_defense() if hasattr(player, 'get_effective_defense') else 0
            final_damage = max(1, enemy_damage - player_defense)
            
            player.hp -= final_damage
            
            if player_defense > 0:
                results.append(f"敌人反击，护盾减少{player_defense}点伤害")
            else:
                results.append("敌人反击")
        
        return results
