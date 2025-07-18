import pygame
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.map import GameMap
from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item
from ui.hud import draw_hud, draw_game_info
from core.battle import BattleSystem
from core.game_state import GameState
from ui.font_manager import FontManager
from systems.skill_system import SkillSystem
from systems.equipment import EquipmentSystem, LootSystem
from systems.save_system import SaveSystem, GameMenu
from systems.inventory import InventoryUI
from entities.enemy_spawner import EnemySpawner

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class Game:
    """主游戏类"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("艾诺迪亚风格 RPG - 完整版")
        self.clock = pygame.time.Clock()
        self.font = FontManager.get_chinese_font(20)
        self.game_state_mode = "menu"  # menu, playing, paused
        self.menu = GameMenu(self.screen, self.font)
        
        # 游戏实体
        self.game_map = None
        self.player = None
        self.enemies = []
        self.items = []
        self.game_state = None
        self.inventory_ui = None
        
    def initialize_game(self, load_save=False):
        """初始化游戏"""
        self.game_map = GameMap()
        self.player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)
        
        # 使用智能生成系统生成敌人
        self.enemies = EnemySpawner.spawn_enemies(self.game_map, count=2, player_pos=(self.player.x, self.player.y))
        
        # 生成物品到安全位置
        self.items = []
        item_types = ["Gold", "血瓶", "Gold", "血瓶", "Gold"]
        for item_type in item_types:
            item = Item.create_safe_item(item_type, self.game_map, self.items)
            self.items.append(item)
        
        # 给玩家一些初始装备用于测试
        if not load_save:
            self.player.inventory.extend([
                "装备_iron_sword", 
                "装备_leather_armor", 
                "装备_magic_ring",
                "血瓶", 
                "血瓶"
            ])
        
        self.game_state = GameState()
        
        # 创建背包界面
        self.inventory_ui = InventoryUI(self.screen, self.font)
        
        if load_save:
            save_data = SaveSystem.load_game()
            if save_data:
                SaveSystem.apply_save_data(self.player, self.game_state, save_data)
                # 清理物品和敌人，重新生成
                self.items.clear()
                self.enemies.clear()
                
    def handle_menu_events(self):
        """处理菜单事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            action = self.menu.handle_input(event)
            if action:
                self.process_menu_action(action)
    
    def process_menu_action(self, action):
        """处理菜单操作"""
        if action == "start_new_game":
            self.initialize_game(load_save=False)
            self.game_state_mode = "playing"
        elif action == "continue_game":
            self.initialize_game(load_save=True)
            self.game_state_mode = "playing"
        elif action == "exit_game":
            pygame.quit()
            sys.exit()
        elif action == "resume_game":
            self.game_state_mode = "playing"
        elif action == "save_game":
            if SaveSystem.save_game(self.player, self.game_state):
                self.game_state.add_battle_message("游戏已保存！")
            else:
                self.game_state.add_battle_message("保存失败！")
            self.game_state_mode = "playing"
        elif action == "return_to_main":
            self.game_state_mode = "menu"
            self.menu.menu_state = "main"
            self.menu.selected_option = 0

    def handle_game_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC键暂停游戏
                    self.game_state_mode = "paused"
                    self.menu.menu_state = "pause"
                    self.menu.selected_option = 0
                elif event.key == pygame.K_TAB:
                    # TAB键打开背包
                    self.inventory_ui.toggle()
                    if self.inventory_ui.is_open:
                        self.game_state.add_battle_message("背包已打开")
                    else:
                        self.game_state.add_battle_message("背包已关闭")
                # 背包打开时优先处理背包输入
                elif self.inventory_ui.is_open:
                    result = self.inventory_ui.handle_input(event, self.player)
                    if result and result != "close":
                        self.game_state.add_battle_message(result)
                # 技能快捷键
                elif event.key == pygame.K_q:
                    # Q键 - 火球术
                    mouse_pos = pygame.mouse.get_pos()
                    if SkillSystem.cast_skill(self.player, "fireball", mouse_pos):
                        self.game_state.add_battle_message("火球术！")
                elif event.key == pygame.K_e:
                    # E键 - 治疗术
                    if SkillSystem.cast_skill(self.player, "heal"):
                        self.game_state.add_battle_message("治疗术！")
                elif event.key == pygame.K_r:
                    # R键 - 护盾术
                    if SkillSystem.cast_skill(self.player, "shield"):
                        self.game_state.add_battle_message("护盾术！")
                # 保存游戏
                elif event.key == pygame.K_F5:
                    if SaveSystem.save_game(self.player, self.game_state):
                        self.game_state.add_battle_message("游戏已保存！")
                    else:
                        self.game_state.add_battle_message("保存失败！")
                # WASD移动
                elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    self.player.handle_keydown_movement(event.key, self.game_map)
        
            # 处理鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.inventory_ui.is_open:  # 左键点击且背包未打开
                    # 普通攻击
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_player_attack(mouse_pos)
                elif self.inventory_ui.is_open:
                    # 背包打开时处理背包鼠标事件
                    result = self.inventory_ui.handle_input(event, self.player)
                    if result and result != "close":
                        self.game_state.add_battle_message(result)
        
            # 处理背包鼠标事件
            elif self.inventory_ui.is_open:
                result = self.inventory_ui.handle_input(event, self.player)
                if result and result != "close":
                    self.game_state.add_battle_message(result)

    def update_game(self):
        """更新游戏状态"""
        # 物品拾取检测
        for item in self.items[:]:
            if self.player.get_rect().colliderect(item.get_rect()):
                result = self.player.pick_up(item)
                if result and isinstance(result, str):
                    self.game_state.add_battle_message(result)
                self.items.remove(item)
        
        # 更新玩家 - 传入game_map进行墙体碰撞检测
        self.player.update(self.game_map)
        
        # 处理玩家特殊输入（如使用物品）
        special_input_result = self.player.handle_special_input()
        if special_input_result:
            self.game_state.add_battle_message(special_input_result)
        
        # 检查波次完成
        if self.game_state.check_wave_complete(self.enemies):
            new_enemies = self.game_state.spawn_new_wave(self.game_map, (self.player.x, self.player.y))
            self.enemies.extend(new_enemies)
            self.game_state.add_battle_message(f"第 {self.game_state.wave_number} 波开始！")
        
        # 更新游戏状态
        self.game_state.update_messages()
        
        # 战斗逻辑
        self.handle_combat()

    def handle_combat(self):
        """处理战斗逻辑"""
        # 处理玩家投射物与敌人的碰撞
        for projectile in self.player.projectiles[:]:
            for enemy in self.enemies:
                if enemy.get_rect().collidepoint(projectile["x"], projectile["y"]):
                    # 投射物击中敌人
                    enemy.hp -= projectile["damage"]
                    self.player.projectiles.remove(projectile)
                    self.game_state.add_battle_message(f"火球术击中敌人，造成{projectile['damage']}点伤害！")
                    
                    if not enemy.is_alive():
                        self.handle_enemy_death(enemy)
                    break
        
        # 处理敌人AI更新和攻击
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.game_map)  # 传入game_map进行墙体碰撞检测
            
            # 检查敌人是否可以攻击玩家（近距离攻击，不是碰撞攻击）
            distance = enemy.distance_to_player(self.player)
            if distance <= 40 and enemy.can_attack():  # 近距离攻击
                # 敌人攻击玩家
                damage = enemy.attack_damage
                self.player.hp -= damage
                self.game_state.add_battle_message(f"敌人攻击你，造成{damage}点伤害！")
                enemy.last_attack_time = pygame.time.get_ticks()
                
                # 检查玩家是否死亡
                if not self.player.is_alive():
                    self.game_state.add_battle_message("玩家被击败，游戏结束")
                    self.game_state.state = "game_over"
                    self.game_state_mode = "menu"
                    self.menu.menu_state = "main"

    def handle_enemy_death(self, enemy):
        """处理敌人死亡"""
        # 生成战利品
        loot = LootSystem.generate_loot(enemy.level)
        for loot_item in loot:
            if loot_item["type"] == "gold":
                self.player.gold += loot_item["amount"]
                self.game_state.add_battle_message(f"获得 {loot_item['amount']} 金币！")
            elif loot_item["type"] == "item":
                self.player.inventory.append(loot_item["name"])
                self.game_state.add_battle_message(f"获得 {loot_item['name']}！")
            elif loot_item["type"] == "equipment":
                # 创建装备物品
                equipment_item = Item(name=f"装备_{loot_item['id']}", x=enemy.x, y=enemy.y)
                equipment_item.equipment_id = loot_item["id"]
                self.items.append(equipment_item)
                self.game_state.add_battle_message("掉落装备！")
        
        self.game_state.add_battle_message("敌人被击败！")
        self.game_state.enemies_killed += 1
        self.player.gain_exp(enemy.exp_reward)
        self.enemies.remove(enemy)

    def render(self):
        """渲染游戏画面"""
        if self.game_state_mode == "menu":
            self.menu.draw_main_menu()
        elif self.game_state_mode == "paused":
            # 先绘制游戏画面
            self.render_game()
            # 再绘制暂停菜单
            self.menu.draw_pause_menu()
        elif self.game_state_mode == "playing":
            self.render_game()
    
    def render_game(self):
        """渲染游戏画面"""
        self.screen.fill((0, 0, 0))
        self.game_map.draw(self.screen)
        
        for item in self.items:
            item.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        self.player.draw(self.screen)
        draw_hud(self.screen, self.player, self.font)
        draw_game_info(self.screen, self.game_state, self.font)
        
        # 绘制背包界面（如果打开）
        self.inventory_ui.draw(self.player)
        
        # 只在游戏模式下调用display.flip()
        if self.game_state_mode == "playing":
            pygame.display.flip()

    def run(self):
        """运行游戏主循环"""
        while True:
            if self.game_state_mode == "menu":
                self.handle_menu_events()
            elif self.game_state_mode == "paused":
                self.handle_menu_events()
            elif self.game_state_mode == "playing":
                self.handle_game_events()
                self.update_game()
            
            self.render()
            self.clock.tick(FPS)

    def handle_player_attack(self, mouse_pos):
        """处理玩家普通攻击"""
        # 检查攻击距离
        attack_range = 50
        player_center = (self.player.x, self.player.y)
        
        # 检查鼠标点击位置是否在攻击范围内
        distance = ((mouse_pos[0] - player_center[0]) ** 2 + (mouse_pos[1] - player_center[1]) ** 2) ** 0.5
        if distance > attack_range:
            self.game_state.add_battle_message("目标太远了！")
            return
        
        # 检查是否击中敌人
        for enemy in self.enemies[:]:
            enemy_rect = enemy.get_rect()
            if enemy_rect.collidepoint(mouse_pos):
                # 计算攻击伤害
                base_damage = getattr(self.player, 'attack_power', 20)
                equipment_bonus = getattr(self.player, 'attack', 0) - 20  # 装备加成
                total_damage = base_damage + equipment_bonus
                
                # 攻击敌人
                enemy.hp -= total_damage
                self.game_state.add_battle_message(f"攻击敌人，造成{total_damage}点伤害！")
                
                # 检查敌人是否死亡
                if not enemy.is_alive():
                    self.handle_enemy_death(enemy)
                return
        
        # 没有击中敌人
        self.game_state.add_battle_message("攻击落空！")

if __name__ == '__main__':
    game = Game()
    game.run()
