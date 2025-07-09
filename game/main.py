import pygame
import sys
from map import GameMap
from player import Player
from enemy import Enemy
from item import Item
from hud import draw_hud, draw_game_info
from battle import BattleSystem
from game_state import GameState
from font_manager import FontManager
from skill_system import SkillSystem
from equipment import EquipmentSystem, LootSystem

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def handle_events(player, game_state, game_map):
    """处理系统和用户事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 使用KEYDOWN事件处理所有按键，避免输入法干扰
            if event.key == pygame.K_h:
                # H键使用血瓶
                if "Potion" in player.inventory and player.hp < player.max_hp:
                    heal_amount = min(30, player.max_hp - player.hp)
                    player.hp += heal_amount
                    player.inventory.remove("Potion")
            # 技能快捷键
            elif event.key == pygame.K_q:
                # Q键 - 火球术
                mouse_pos = pygame.mouse.get_pos()
                if SkillSystem.cast_skill(player, "fireball", mouse_pos):
                    game_state.add_battle_message("火球术！")
            elif event.key == pygame.K_e:
                # E键 - 治疗术
                if SkillSystem.cast_skill(player, "heal"):
                    game_state.add_battle_message("治疗术！")
            elif event.key == pygame.K_r:
                # R键 - 护盾术
                if SkillSystem.cast_skill(player, "shield"):
                    game_state.add_battle_message("护盾术！")
            # WASD移动键
            elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                player.handle_keydown_movement(event.key, game_map)

def update_game(player, enemies, items, game_state, game_map):
    """更新玩家、敌人、物品状态并执行碰撞和战斗逻辑"""
    # 物品拾取检测
    for item in items[:]:
        if player.get_rect().colliderect(item.get_rect()):
            player.pick_up(item)
            items.remove(item)
    
    # 更新玩家 - 传入game_map进行墙体碰撞检测
    player.update(game_map)
    
    # 检查波次完成
    if game_state.check_wave_complete(enemies):
        new_enemies = game_state.spawn_new_wave()
        enemies.extend(new_enemies)
        game_state.add_battle_message(f"第 {game_state.wave_number} 波开始！")
    
    # 更新游戏状态
    game_state.update_messages()
    
    # 战斗逻辑
    handle_combat(player, enemies, items, game_state, game_map)

def handle_combat(player, enemies, items, game_state, game_map):
    """处理战斗逻辑"""
    # 处理玩家投射物与敌人的碰撞
    for projectile in player.projectiles[:]:
        for enemy in enemies:
            if enemy.get_rect().collidepoint(projectile["x"], projectile["y"]):
                # 投射物击中敌人
                enemy.hp -= projectile["damage"]
                player.projectiles.remove(projectile)
                game_state.add_battle_message(f"火球术击中敌人，造成{projectile['damage']}点伤害！")
                
                if not enemy.is_alive():
                    # 敌人死亡，生成战利品
                    loot = LootSystem.generate_loot(enemy.level)
                    for loot_item in loot:
                        if loot_item["type"] == "gold":
                            player.gold += loot_item["amount"]
                            game_state.add_battle_message(f"获得 {loot_item['amount']} 金币！")
                        elif loot_item["type"] == "item":
                            player.inventory.append(loot_item["name"])
                            game_state.add_battle_message(f"获得 {loot_item['name']}！")
                        elif loot_item["type"] == "equipment":
                            # 创建装备物品
                            equipment_item = Item(name=f"装备_{loot_item['id']}", x=enemy.x, y=enemy.y)
                            equipment_item.equipment_id = loot_item["id"]
                            items.append(equipment_item)
                            game_state.add_battle_message("掉落装备！")
                    
                    game_state.add_battle_message("敌人被击败！")
                    game_state.enemies_killed += 1
                    player.gain_exp(enemy.exp_reward)
                    enemies.remove(enemy)
                break
    
    # 处理敌人与玩家的近战
    for enemy in enemies:
        enemy.update(player, game_map)  # 传递玩家对象和地图给敌人更新AI
        # 玩家与敌人碰撞检测
        if player.get_rect().colliderect(enemy.get_rect()):
            # 检查攻击冷却，避免连续攻击
            if enemy.can_attack():
                battle_results = BattleSystem.battle_result(player, enemy)
                for result in battle_results:
                    game_state.add_battle_message(result)
                
                if not enemy.is_alive():
                    # 敌人死亡，生成战利品
                    loot = LootSystem.generate_loot(enemy.level)
                    for loot_item in loot:
                        if loot_item["type"] == "gold":
                            player.gold += loot_item["amount"]
                            game_state.add_battle_message(f"获得 {loot_item['amount']} 金币！")
                        elif loot_item["type"] == "item":
                            player.inventory.append(loot_item["name"])
                            game_state.add_battle_message(f"获得 {loot_item['name']}！")
                        elif loot_item["type"] == "equipment":
                            # 创建装备物品
                            equipment_item = Item(name=f"装备_{loot_item['id']}", x=enemy.x, y=enemy.y)
                            equipment_item.equipment_id = loot_item["id"]
                            items.append(equipment_item)
                            game_state.add_battle_message("掉落装备！")
                    
                    game_state.add_battle_message("敌人被击败！")
                    game_state.enemies_killed += 1
                    player.gain_exp(enemy.exp_reward)
                    enemies.remove(enemy)
                    break
                    
                if not player.is_alive():
                    game_state.add_battle_message("玩家被击败，游戏结束")
                    game_state.state = "game_over"
                    pygame.quit()
                    sys.exit()

def render(screen, game_map, player, enemies, items, font, game_state):
    """绘制地图、物品、敌人、玩家和界面数据"""
    screen.fill((0, 0, 0))
    game_map.draw(screen)
    for item in items:
        item.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)
    draw_hud(screen, player, font)
    draw_game_info(screen, game_state, font)
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("艾诺迪亚风格 RPG - 增强版")
    clock = pygame.time.Clock()
    
    # 使用字体管理器获取支持中文的字体
    font = FontManager.get_chinese_font(20)

    # 创建游戏实体
    game_map = GameMap()
    player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)
    enemies = [
        Enemy(x=100, y=100, enemy_type="basic"), 
        Enemy(x=700, y=500, enemy_type="basic")
    ]
    items = [
        Item(name="Gold", x=200, y=200),
        Item(name="Potion", x=400, y=300),
        Item(name="Gold", x=600, y=150),
        Item(name="Potion", x=300, y=450),
        Item(name="Gold", x=500, y=350)
    ]
    game_state = GameState()

    # 游戏主循环
    while True:
        handle_events(player, game_state, game_map)
        update_game(player, enemies, items, game_state, game_map)
        render(screen, game_map, player, enemies, items, font, game_state)
        clock.tick(FPS)

if __name__ == '__main__':
    main()
