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
from save_system import SaveSystem, GameMenu

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
        
    def initialize_game(self, load_save=False):
        """初始化游戏"""
        self.game_map = GameMap()
        self.player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)
        self.enemies = [
            Enemy(x=100, y=100, enemy_type="basic"), 
            Enemy(x=700, y=500, enemy_type="basic")
        ]
        self.items = [
            Item(name="Gold", x=200, y=200),
            Item(name="Potion", x=400, y=300),
            Item(name="Gold", x=600, y=150),
            Item(name="Potion", x=300, y=450),
            Item(name="Gold", x=500, y=350)
        ]
        self.game_state = GameState()
        
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
                elif event.key == pygame.K_h:
                    # H键使用血瓶
                    if "Potion" in self.player.inventory and self.player.hp < self.player.max_hp:
                        heal_amount = min(30, self.player.max_hp - self.player.hp)
                        self.player.hp += heal_amount
                        self.player.inventory.remove("Potion")
                        self.game_state.add_battle_message("使用血瓶恢复生命！")
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
        
        # 检查波次完成
        if self.game_state.check_wave_complete(self.enemies):
            new_enemies = self.game_state.spawn_new_wave()
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
        
        # 处理敌人与玩家的近战
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.game_map)  # 传入game_map进行墙体碰撞检测
            # 玩家与敌人碰撞检测
            if self.player.get_rect().colliderect(enemy.get_rect()):
                if enemy.can_attack():
                    battle_results = BattleSystem.battle_result(self.player, enemy)
                    for result in battle_results:
                        self.game_state.add_battle_message(result)
                    
                    if not enemy.is_alive():
                        self.handle_enemy_death(enemy)
                        
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

if __name__ == '__main__':
    game = Game()
    game.run()
