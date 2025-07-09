import pygame


def draw_hud(surface, player, font):
    """在屏幕上绘制玩家状态和背包信息"""
    # 绘制生命值条
    hp_ratio = player.hp / player.max_hp
    hp_bar_width = 200
    hp_bar_height = 20
    
    # 绘制血条背景
    pygame.draw.rect(surface, (100, 0, 0), (10, 10, hp_bar_width, hp_bar_height))
    # 绘制血条
    pygame.draw.rect(surface, (255, 0, 0), (10, 10, hp_bar_width * hp_ratio, hp_bar_height))
    # 绘制血条边框
    pygame.draw.rect(surface, (255, 255, 255), (10, 10, hp_bar_width, hp_bar_height), 2)
    
    # 绘制HP文字
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 255, 255))
    surface.blit(hp_text, (220, 12))
    
    # 绘制等级和经验
    level_text = font.render(f"Lv: {player.level}  EXP: {player.exp}/{player.level * 100}", True, (255, 255, 255))
    surface.blit(level_text, (10, 35))
    
    # 绘制金币
    gold_text = font.render(f"Gold: {player.gold}", True, (255, 215, 0))
    surface.blit(gold_text, (10, 55))

    # 绘制背包物品
    inv_str = ", ".join(player.inventory) if player.inventory else "空"
    inv_text = font.render(f"背包: {inv_str}", True, (255, 255, 255))
    surface.blit(inv_text, (10, 75))
    
    # 绘制操作提示
    help_text = font.render("操作: 方向键移动, H键使用血瓶", True, (200, 200, 200))
    surface.blit(help_text, (10, 560))
    
    # 添加输入法提示
    ime_text = font.render("提示: 如无法移动请关闭中文输入法", True, (255, 255, 100))
    surface.blit(ime_text, (10, 580))


def draw_game_info(surface, game_state, font):
    """绘制游戏信息（波次、击杀数等）"""
    # 绘制波次信息
    wave_text = font.render(f"波次: {game_state.wave_number}", True, (255, 255, 255))
    surface.blit(wave_text, (600, 10))
    
    # 绘制击杀数
    kill_text = font.render(f"击杀: {game_state.enemies_killed}", True, (255, 255, 255))
    surface.blit(kill_text, (600, 30))
    
    # 绘制战斗消息
    for i, message in enumerate(game_state.battle_messages[-5:]):  # 最多显示5条消息
        msg_text = font.render(message, True, (255, 255, 0))
        surface.blit(msg_text, (400, 100 + i * 20))
