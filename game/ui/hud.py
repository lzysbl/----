import pygame
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from systems.skill_system import SkillSystem


def draw_hud(surface, player, font):
    """在屏幕上绘制玩家状态和背包信息"""
    # 绘制生命值条
    hp_ratio = player.hp / player.max_hp
    hp_bar_width = 200
    hp_bar_height = 20
    
    # 绘制血条背景
    pygame.draw.rect(surface, (100, 0, 0), (10, 10, hp_bar_width, hp_bar_height))
    # 绘制血条
    pygame.draw.rect(surface, (255, 0, 0), (10, 10, hp_bar_width * hp_ratio, hp_bar_height))
    # 绘制血条边框
    pygame.draw.rect(surface, (255, 255, 255), (10, 10, hp_bar_width, hp_bar_height), 2)
    
    # 绘制HP文字
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 255, 255))
    surface.blit(hp_text, (220, 12))
    
    # 绘制魔法值条
    mp_ratio = player.mp / player.max_mp
    mp_bar_y = 35
    
    # 绘制魔法条背景
    pygame.draw.rect(surface, (0, 0, 100), (10, mp_bar_y, hp_bar_width, hp_bar_height))
    # 绘制魔法条
    pygame.draw.rect(surface, (0, 0, 255), (10, mp_bar_y, hp_bar_width * mp_ratio, hp_bar_height))
    # 绘制魔法条边框
    pygame.draw.rect(surface, (255, 255, 255), (10, mp_bar_y, hp_bar_width, hp_bar_height), 2)
    
    # 绘制MP文字
    mp_text = font.render(f"MP: {player.mp}/{player.max_mp}", True, (255, 255, 255))
    surface.blit(mp_text, (220, mp_bar_y + 2))
    
    # 绘制等级和经验
    level_text = font.render(f"等级: {player.level}  经验: {player.exp}/{player.level * 100}", True, (255, 255, 255))
    surface.blit(level_text, (10, 60))
    
    # 绘制金币
    gold_text = font.render(f"金币: {player.gold}", True, (255, 215, 0))
    surface.blit(gold_text, (10, 80))

    # 绘制背包物品 - 只显示消耗品叠加信息
    consumables = {}
    for item in player.inventory:
        if not item.startswith("装备_"):
            consumables[item] = consumables.get(item, 0) + 1
    
    if consumables:
        consumable_strs = []
        for item, count in consumables.items():
            if count > 1:
                consumable_strs.append(f"{item}x{count}")
            else:
                consumable_strs.append(item)
        inv_str = ", ".join(consumable_strs)
    else:
        inv_str = "空"
    
    inv_text = font.render(f"物品: {inv_str}", True, (255, 255, 255))
    surface.blit(inv_text, (10, 100))
    
    # 绘制技能快捷键和冷却时间
    draw_skill_info(surface, player, font)
    
    # 绘制操作提示
    help_text = font.render("操作: WASD移动, H键使用血瓶", True, (200, 200, 200))
    surface.blit(help_text, (10, 520))
    
    # 绘制技能提示
    skill_text = font.render("技能: Q火球术, E治疗术, R护盾术", True, (200, 200, 200))
    surface.blit(skill_text, (10, 540))
    
    # 添加输入法提示
    ime_text = font.render("提示: 如无法移动请关闭中文输入法", True, (255, 255, 100))
    surface.blit(ime_text, (10, 560))

def draw_skill_info(surface, player, font):
    """绘制技能信息"""
    skills = SkillSystem.get_available_skills()
    skill_keys = [("Q", "fireball"), ("E", "heal"), ("R", "shield")]
    current_time = pygame.time.get_ticks()
    
    y_offset = 120
    for i, (key, skill_name) in enumerate(skill_keys):
        skill = skills[skill_name]
        x_pos = 10 + i * 120
        
        # 绘制技能图标背景
        icon_rect = pygame.Rect(x_pos, y_offset, 30, 30)
        
        # 检查冷却状态
        is_on_cooldown = False
        cooldown_remaining = 0
        
        if skill_name in player.skill_cooldowns:
            time_since_cast = current_time - player.skill_cooldowns[skill_name]
            if time_since_cast < skill["cooldown"]:
                is_on_cooldown = True
                cooldown_remaining = skill["cooldown"] - time_since_cast
        
        # 检查魔法值是否足够
        has_enough_mp = player.mp >= skill["cost"]
        
        # 绘制技能图标
        if is_on_cooldown:
            pygame.draw.rect(surface, (100, 100, 100), icon_rect)  # 冷却中为灰色
        elif not has_enough_mp:
            pygame.draw.rect(surface, (100, 0, 0), icon_rect)  # 魔法不足为暗红色
        else:
            if skill_name == "fireball":
                pygame.draw.rect(surface, (255, 100, 0), icon_rect)  # 火球术为橙色
            elif skill_name == "heal":
                pygame.draw.rect(surface, (0, 255, 0), icon_rect)  # 治疗术为绿色
            elif skill_name == "shield":
                pygame.draw.rect(surface, (0, 100, 255), icon_rect)  # 护盾术为蓝色
        
        pygame.draw.rect(surface, (255, 255, 255), icon_rect, 2)  # 边框
        
        # 绘制按键提示
        key_text = font.render(key, True, (255, 255, 255))
        surface.blit(key_text, (x_pos + 10, y_offset + 5))
        
        # 绘制技能名称
        name_text = font.render(skill["name"], True, (255, 255, 255))
        surface.blit(name_text, (x_pos + 35, y_offset))
        
        # 绘制魔法消耗
        cost_text = font.render(f"MP:{skill['cost']}", True, (100, 150, 255))
        surface.blit(cost_text, (x_pos + 35, y_offset + 15))
        
        # 绘制冷却时间
        if is_on_cooldown:
            cooldown_text = font.render(f"{cooldown_remaining//1000 + 1}s", True, (255, 255, 0))
            surface.blit(cooldown_text, (x_pos + 5, y_offset + 35))


def draw_game_info(surface, game_state, font):
    """绘制游戏信息（波次、击杀数等）"""
    # 绘制波次信息
    wave_text = font.render(f"波次: {game_state.wave_number}", True, (255, 255, 255))
    surface.blit(wave_text, (600, 10))
    
    # 绘制击杀数
    kill_text = font.render(f"击杀: {game_state.enemies_killed}", True, (255, 255, 255))
    surface.blit(kill_text, (600, 30))
    
    # 绘制战斗消息
    for i, message in enumerate(game_state.battle_messages[-5:]):  # 最多显示5条消息
        msg_text = font.render(message, True, (255, 255, 0))
        surface.blit(msg_text, (400, 100 + i * 20))
