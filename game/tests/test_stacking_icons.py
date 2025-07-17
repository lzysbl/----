#!/usr/bin/env python3
"""
测试血瓶叠加和装备图标功能
"""
import pygame
import sys
import os

# 确保可以导入游戏模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_enhanced import Game

def test_stacking_and_icons():
    # 创建游戏实例
    game = Game()
    
    # 添加多个血瓶到背包
    print("添加多个血瓶...")
    for i in range(5):
        game.player.inventory.append("血瓶")
    
    # 添加一些装备
    print("添加装备...")
    game.player.inventory.append("装备_sword_1")
    game.player.inventory.append("装备_armor_1")
    game.player.inventory.append("装备_ring_1")
    
    print(f"玩家背包内容: {game.player.inventory}")
    print(f"血瓶数量: {game.player.inventory.count('血瓶')}")
    
    # 运行游戏
    print("启动游戏，按TAB键打开背包查看叠加效果...")
    print("按ESC键退出游戏")
    
    # 初始化游戏
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    # 切换背包显示
                    game.inventory_ui.toggle()
                elif game.inventory_ui.is_open:
                    # 如果背包打开，处理背包事件
                    result = game.inventory_ui.handle_event(event, game.player)
                    if result == "close":
                        game.inventory_ui.is_open = False
                    elif result:
                        print(f"操作结果: {result}")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.inventory_ui.is_open:
                    result = game.inventory_ui.handle_mouse_click(event.pos, game.player)
                    if result:
                        print(f"鼠标点击结果: {result}")
        
        # 更新游戏状态
        game.update()
        
        # 绘制游戏画面
        game.draw()
        
        # 显示帧率
        clock.tick(60)
    
    # 退出游戏
    pygame.quit()
    print("测试完成！")

if __name__ == "__main__":
    test_stacking_and_icons()
