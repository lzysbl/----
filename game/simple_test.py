import pygame
import sys

# 最简化的游戏版本，专门测试H键问题
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("简化测试版本")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# 玩家变量
player_x = 400
player_y = 300
player_hp = 100
player_max_hp = 100
potions = 3

while True:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            # H键使用血瓶
            if potions > 0 and player_hp < player_max_hp:
                heal = min(30, player_max_hp - player_hp)
                player_hp += heal
                potions -= 1
    
    # 移动处理
    keys = pygame.key.get_pressed()
    speed = 5
    if keys[pygame.K_LEFT] and player_x > 15:
        player_x -= speed
    if keys[pygame.K_RIGHT] and player_x < 785:
        player_x += speed
    if keys[pygame.K_UP] and player_y > 15:
        player_y -= speed
    if keys[pygame.K_DOWN] and player_y < 585:
        player_y += speed
    
    # 绘制
    screen.fill((0, 0, 0))
    # 绘制玩家
    pygame.draw.rect(screen, (0, 255, 0), (player_x-15, player_y-15, 30, 30))
    
    # 绘制状态
    hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, (255, 255, 255))
    potion_text = font.render(f"Potions: {potions}", True, (255, 255, 255))
    help_text = font.render("Arrow keys: Move, H: Use potion", True, (200, 200, 200))
    
    screen.blit(hp_text, (10, 10))
    screen.blit(potion_text, (10, 35))
    screen.blit(help_text, (10, 560))
    
    pygame.display.flip()
    clock.tick(60)
