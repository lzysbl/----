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
from inventory import InventoryUI
from enemy_spawner import EnemySpawner

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def handle_events(player, game_state, game_map, inventory_ui):
    """处理系统和用户事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # TAB键打开背包
            if event.key == pygame.K_TAB:
                inventory_ui.toggle()
                if inventory_ui.is_open:
                    game_state.add_battle_message("背包已打开")
                else:
                    game_state.add_battle_message("背包已关闭")
            # 背包打开时优先处理背包输入
            elif inventory_ui.is_open:
                result = inventory_ui.handle_input(event, player)
                if result and result != "close":
                    game_state.add_battle_message(result)
            # 使用KEYDOWN事件处理所有按键，避免输入法干扰
            elif event.key == pygame.K_h:
                # H键使用血瓶
                if "血瓶" in player.inventory and player.hp < player.max_hp:
                    heal_amount = min(30, player.max_hp - player.hp)
                    player.hp += heal_amount
                    player.inventory.remove("血瓶")
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
        
        # 处理鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not inventory_ui.is_open:  # 左键点击且背包未打开
                # 普通攻击
                mouse_pos = pygame.mouse.get_pos()
                handle_player_attack(mouse_pos, player, enemies, game_state)
            elif inventory_ui.is_open:
                # 背包打开时处理背包鼠标事件
                result = inventory_ui.handle_input(event, player)
                if result and result != "close":
                    game_state.add_battle_message(result)
        
        # 处理背包鼠标事件
        elif inventory_ui.is_open:
            result = inventory_ui.handle_input(event, player)
            if result and result != "close":
                game_state.add_battle_message(result)

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
        new_enemies = game_state.spawn_new_wave(game_map, (player.x, player.y))
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
    
    # 处理敌人AI更新和攻击
    for enemy in enemies:
        enemy.update(player, game_map)  # 传递玩家对象和地图给敌人更新AI
        
        # 检查敌人是否可以攻击玩家（近距离攻击，不是碰撞攻击）
        distance = enemy.distance_to_player(player)
        if distance <= 40 and enemy.can_attack():  # 近距离攻击
            # 敌人攻击玩家
            damage = enemy.attack_damage
            player.hp -= damage
            game_state.add_battle_message(f"敌人攻击你，造成{damage}点伤害！")
            enemy.last_attack_time = pygame.time.get_ticks()
            
            # 检查玩家是否死亡
            if not player.is_alive():
                game_state.add_battle_message("玩家被击败，游戏结束")
                game_state.state = "game_over"
                pygame.quit()
                sys.exit()

def render(screen, game_map, player, enemies, items, font, game_state, inventory_ui):
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
    
    # 绘制背包界面（如果打开）
    inventory_ui.draw(player)
    
    pygame.display.flip()

def handle_player_attack(mouse_pos, player, enemies, game_state):
    """处理玩家普通攻击"""
    # 检查攻击距离
    attack_range = 50
    player_center = (player.x, player.y)
    
    # 检查鼠标点击位置是否在攻击范围内
    distance = ((mouse_pos[0] - player_center[0]) ** 2 + (mouse_pos[1] - player_center[1]) ** 2) ** 0.5
    if distance > attack_range:
        game_state.add_battle_message("目标太远了！")
        return
    
    # 检查是否击中敌人
    for enemy in enemies[:]:
        enemy_rect = enemy.get_rect()
        if enemy_rect.collidepoint(mouse_pos):
            # 计算攻击伤害
            base_damage = getattr(player, 'attack_power', 20)
            equipment_bonus = getattr(player, 'attack', 0) - 20  # 装备加成
            total_damage = base_damage + equipment_bonus
            
            # 攻击敌人
            enemy.hp -= total_damage
            game_state.add_battle_message(f"攻击敌人，造成{total_damage}点伤害！")
            
            # 检查敌人是否死亡
            if not enemy.is_alive():
                # 处理敌人死亡逻辑
                from equipment import LootSystem
                loot = LootSystem.generate_loot(enemy.level)
                for loot_item in loot:
                    if loot_item["type"] == "gold":
                        player.gold += loot_item["amount"]
                        game_state.add_battle_message(f"获得 {loot_item['amount']} 金币！")
                    elif loot_item["type"] == "item":
                        player.inventory.append(loot_item["name"])
                        game_state.add_battle_message(f"获得 {loot_item['name']}！")
                
                game_state.add_battle_message("敌人被击败！")
                game_state.enemies_killed += 1
                player.gain_exp(enemy.exp_reward)
                enemies.remove(enemy)
            return
    
    # 没有击中敌人
    game_state.add_battle_message("攻击落空！")

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
    
    # 使用智能生成系统生成敌人
    enemies = EnemySpawner.spawn_enemies(game_map, count=2, player_pos=(player.x, player.y))
    
    # 给玩家一些初始装备用于测试
    player.inventory.extend([
        "装备_iron_sword", 
        "装备_leather_armor", 
        "装备_magic_ring",
        "血瓶", 
        "血瓶"
    ])
    
    items = [
        Item(name="Gold", x=200, y=200),
        Item(name="血瓶", x=400, y=300),
        Item(name="Gold", x=600, y=150),
        Item(name="血瓶", x=300, y=450),
        Item(name="Gold", x=500, y=350)
    ]
    game_state = GameState()
    
    # 创建背包界面
    inventory_ui = InventoryUI(screen, font)

    # 游戏主循环
    while True:
        handle_events(player, game_state, game_map, inventory_ui)
        update_game(player, enemies, items, game_state, game_map)
        render(screen, game_map, player, enemies, items, font, game_state, inventory_ui)
        clock.tick(FPS)

if __name__ == '__main__':
    main()
