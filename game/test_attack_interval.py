#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试敌人攻击间隔的简单脚本
"""

import pygame
import sys
from enemy import Enemy
from player import Player
from battle import BattleSystem
from game_state import GameState
from font_manager import FontManager

def test_attack_interval():
    """测试敌人攻击间隔"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("攻击间隔测试")
    clock = pygame.time.Clock()
    font = FontManager.get_chinese_font(18)
    
    # 创建测试对象
    player = Player(x=400, y=300)
    enemy = Enemy(x=420, y=300, enemy_type="basic")  # 让敌人贴近玩家
    game_state = GameState()
    
    attack_times = []  # 记录攻击时间
    
    print("开始测试攻击间隔...")
    print("让敌人贴近玩家，观察攻击频率")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # 更新
        player.update()
        enemy.update(player)
        
        # 检查碰撞和攻击
        if player.get_rect().colliderect(enemy.get_rect()):
            if enemy.can_attack():
                current_time = pygame.time.get_ticks()
                attack_times.append(current_time)
                
                # 计算攻击间隔
                if len(attack_times) > 1:
                    interval = attack_times[-1] - attack_times[-2]
                    print(f"攻击间隔: {interval}ms")
                    game_state.add_battle_message(f"攻击！间隔: {interval}ms")
                else:
                    print("首次攻击")
                    game_state.add_battle_message("首次攻击！")
                
                # 执行战斗
                battle_results = BattleSystem.battle_result(player, enemy)
                for result in battle_results:
                    game_state.add_battle_message(result)
                
                # 只保留最近10次攻击记录
                if len(attack_times) > 10:
                    attack_times.pop(0)
        
        # 更新消息
        game_state.update_messages()
        
        # 绘制
        screen.fill((0, 0, 0))
        
        # 绘制对象
        player.draw(screen)
        enemy.draw(screen)
        
        # 绘制信息
        info_text = font.render(f"玩家HP: {player.hp}/{player.max_hp}", True, (255, 255, 255))
        screen.blit(info_text, (10, 10))
        
        enemy_info = font.render(f"敌人HP: {enemy.hp}/{enemy.max_hp}", True, (255, 255, 255))
        screen.blit(enemy_info, (10, 30))
        
        # 绘制攻击间隔信息
        if len(attack_times) > 1:
            last_interval = attack_times[-1] - attack_times[-2]
            interval_text = font.render(f"上次攻击间隔: {last_interval}ms", True, (255, 255, 0))
            screen.blit(interval_text, (10, 50))
        
        # 绘制战斗消息
        for i, message in enumerate(game_state.battle_messages[-8:]):
            msg_text = font.render(message, True, (255, 255, 0))
            screen.blit(msg_text, (10, 100 + i * 20))
        
        # 绘制说明
        help_text = font.render("ESC键退出，观察敌人攻击间隔", True, (200, 200, 200))
        screen.blit(help_text, (10, 550))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    test_attack_interval()
