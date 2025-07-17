#!/usr/bin/env python3
"""
快速功能验证脚本
"""
import pygame
import sys
import os

# 确保可以导入游戏模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_enhanced import Game

def main():
    print("====== 功能验证 ======")
    print("1. 血瓶叠加显示")
    print("2. 装备图标显示")
    print("3. 安全物品生成")
    print("====================")
    
    # 初始化游戏
    game = Game()
    
    # 测试血瓶叠加
    print("\n添加5个血瓶...")
    for _ in range(5):
        game.player.inventory.append("血瓶")
    print(f"血瓶数量: {game.player.inventory.count('血瓶')}")
    
    # 测试装备添加
    print("\n添加装备...")
    game.player.inventory.append("装备_sword_1")
    game.player.inventory.append("装备_armor_1")
    game.player.inventory.append("装备_ring_1")
    
    print(f"最终背包内容: {game.player.inventory}")
    print(f"背包大小: {len(game.player.inventory)}")
    
    print("\n启动游戏...")
    print("操作说明:")
    print("- 按TAB键打开/关闭背包")
    print("- 背包打开时，血瓶会显示为 Po x数量")
    print("- 装备会显示为 ⚔🛡💍 等图标")
    print("- 按ESC键退出游戏")
    print("- 在游戏中可以看到敌人掉落的装备和血瓶")
    
    # 游戏主循环
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        # 更新游戏
        game.update()
        
        # 绘制游戏
        game.draw()
        
        # 限制帧率
        clock.tick(60)
    
    pygame.quit()
    print("验证完成！")

if __name__ == "__main__":
    main()
