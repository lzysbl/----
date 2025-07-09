import pygame
import sys

# 简化的测试版本
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("测试H键")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    player_hp = 80
    player_max_hp = 100
    inventory = ["Potion", "Potion"]
    last_heal_time = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                # 简化的血瓶使用逻辑
                current_time = pygame.time.get_ticks()
                if current_time - last_heal_time > 2000 and "Potion" in inventory:
                    heal_amount = min(30, player_max_hp - player_hp)
                    if heal_amount > 0:
                        player_hp += heal_amount
                        inventory.remove("Potion")
                        last_heal_time = current_time
        
        # 简化的渲染
        screen.fill((0, 0, 0))
        hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))
        
        inv_text = font.render(f"Potions: {inventory.count('Potion')}", True, (255, 255, 255))
        screen.blit(inv_text, (10, 30))
        
        help_text = font.render("Press H to use potion", True, (255, 255, 255))
        screen.blit(help_text, (10, 50))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
