import pygame
import os

class FontManager:
    """字体管理器，处理中文字体加载"""
    
    @staticmethod
    def get_chinese_font(size=20):
        """获取支持中文的字体"""
        # Windows系统常见中文字体
        font_names = [
            'microsoftyahei',    # 微软雅黑
            'simsun',           # 宋体
            'simhei',           # 黑体
            'kaiti',            # 楷体
            'dengxian',         # 等线
            'fangsong'          # 仿宋
        ]
        
        for font_name in font_names:
            try:
                font = pygame.font.SysFont(font_name, size)
                # 测试字体是否能正确渲染中文
                test_surface = font.render("测试", True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    print(f"使用字体: {font_name}")
                    return font
            except Exception:
                continue
        
        # 如果系统字体都不可用，尝试加载字体文件
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc",    # 宋体
            "C:/Windows/Fonts/simhei.ttf",    # 黑体
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = pygame.font.Font(font_path, size)
                    print(f"使用字体文件: {font_path}")
                    return font
                except Exception:
                    continue
        
        # 最后使用默认字体
        print("使用默认字体")
        return pygame.font.Font(None, size)
