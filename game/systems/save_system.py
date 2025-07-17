import json
import os
import pygame

class SaveSystem:
    """存档系统"""
    SAVE_FILE = "save_data.json"
    
    @staticmethod
    def save_game(player, game_state):
        """保存游戏数据"""
        save_data = {
            "player": {
                "x": player.x,
                "y": player.y,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "mp": player.mp,
                "max_mp": player.max_mp,
                "level": player.level,
                "exp": player.exp,
                "gold": player.gold,
                "attack_power": player.attack_power,
                "inventory": player.inventory,
                "equipped": getattr(player, 'equipped', {"weapon": None, "armor": None, "accessory": None}),
                "base_defense": getattr(player, 'base_defense', 0)
            },
            "game_state": {
                "wave_number": game_state.wave_number,
                "enemies_killed": game_state.enemies_killed,
                "state": game_state.state
            },
            "timestamp": pygame.time.get_ticks()
        }
        
        try:
            with open(SaveSystem.SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
    
    @staticmethod
    def load_game():
        """加载游戏数据"""
        if not os.path.exists(SaveSystem.SAVE_FILE):
            return None
        
        try:
            with open(SaveSystem.SAVE_FILE, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            return save_data
        except Exception as e:
            print(f"加载失败: {e}")
            return None
    
    @staticmethod
    def apply_save_data(player, game_state, save_data):
        """将存档数据应用到游戏对象"""
        if not save_data:
            return False
        
        try:
            # 恢复玩家数据
            player_data = save_data["player"]
            player.x = player_data["x"]
            player.y = player_data["y"]
            player.hp = player_data["hp"]
            player.max_hp = player_data["max_hp"]
            player.mp = player_data["mp"]
            player.max_mp = player_data["max_mp"]
            player.level = player_data["level"]
            player.exp = player_data["exp"]
            player.gold = player_data["gold"]
            player.attack_power = player_data["attack_power"]
            player.inventory = player_data["inventory"]
            player.equipped = player_data["equipped"]
            player.base_defense = player_data["base_defense"]
            
            # 恢复游戏状态
            state_data = save_data["game_state"]
            game_state.wave_number = state_data["wave_number"]
            game_state.enemies_killed = state_data["enemies_killed"]
            game_state.state = state_data["state"]
            
            return True
        except Exception as e:
            print(f"应用存档数据失败: {e}")
            return False
    
    @staticmethod
    def delete_save():
        """删除存档"""
        try:
            if os.path.exists(SaveSystem.SAVE_FILE):
                os.remove(SaveSystem.SAVE_FILE)
                return True
            return False
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False
    
    @staticmethod
    def has_save():
        """检查是否有存档"""
        return os.path.exists(SaveSystem.SAVE_FILE)

class GameMenu:
    """游戏菜单系统"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.selected_option = 0
        self.menu_state = "main"  # main, pause, game_over
        self.last_render_time = 0
        self.render_interval = 50  # 减少渲染频率，避免闪烁
        
    def draw_main_menu(self):
        """绘制主菜单"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_render_time < self.render_interval:
            return  # 跳过渲染，减少闪烁
        
        self.last_render_time = current_time
        self.screen.fill((0, 0, 0))
        
        # 标题
        title = self.font.render("艾诺迪亚风格 RPG", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 150))
        self.screen.blit(title, title_rect)
        
        # 菜单选项
        options = ["开始游戏", "继续游戏", "退出游戏"]
        if not SaveSystem.has_save():
            options[1] = "继续游戏 (无存档)"
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            if i == 1 and not SaveSystem.has_save():
                color = (100, 100, 100)  # 灰色表示不可选
            
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, 250 + i * 50))
            self.screen.blit(text, text_rect)
        
        # 控制提示
        help_text = self.font.render("使用上下键选择，回车键确认", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(400, 450))
        self.screen.blit(help_text, help_rect)
        
        pygame.display.flip()
    
    def draw_pause_menu(self):
        """绘制暂停菜单"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_render_time < self.render_interval:
            return  # 跳过渲染，减少闪烁
        
        self.last_render_time = current_time
        
        # 半透明背景
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停标题
        title = self.font.render("游戏暂停", True, (255, 255, 255))
        title_rect = title.get_rect(center=(400, 200))
        self.screen.blit(title, title_rect)
        
        # 菜单选项
        options = ["继续游戏", "保存游戏", "返回主菜单"]
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(400, 280 + i * 50))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def handle_input(self, event):
        """处理菜单输入"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 3
            elif event.key == pygame.K_RETURN:
                return self.get_selected_action()
        return None
    
    def get_selected_action(self):
        """获取选中的操作"""
        if self.menu_state == "main":
            if self.selected_option == 0:
                return "start_new_game"
            elif self.selected_option == 1:
                return "continue_game" if SaveSystem.has_save() else None
            elif self.selected_option == 2:
                return "exit_game"
        elif self.menu_state == "pause":
            if self.selected_option == 0:
                return "resume_game"
            elif self.selected_option == 1:
                return "save_game"
            elif self.selected_option == 2:
                return "return_to_main"
        
        return None
