import pygame
import globalSettings
from spriteAnimator import SpriteAnimator  # Make sure this is defined!
import os

def load_and_scale_spritesheet(path: str, frame_width: int, frame_height: int, scale: float = 1.0):
    spritesheet = pygame.image.load(path).convert_alpha()

    if scale != 1.0:
        sheet_width, sheet_height = spritesheet.get_size()
        spritesheet = pygame.transform.scale(
            spritesheet,
            (int(sheet_width * scale), int(sheet_height * scale))
        )
        frame_width = int(frame_width * scale)
        frame_height = int(frame_height * scale)

    return spritesheet, frame_width, frame_height

def load_menu_screen_assets():
    images = {}
    try:
        pic1_path = os.path.join(globalSettings.menu_path, "MiiChannel.png")
        pic2_path = os.path.join(globalSettings.menu_path, "fightMenu.png")
        save_image_path = os.path.join(globalSettings.menu_path, "save.png")
        cursor_image_path = os.path.join(globalSettings.menu_path, "cursor.png")
        
        if os.path.exists(pic1_path):
            images["mii_channel"] = pygame.image.load(pic1_path).convert()
            images["mii_channel"] = pygame.transform.scale(images["mii_channel"], globalSettings.SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic1_path}")

        if os.path.exists(pic2_path):
            images["fight_menu"] = pygame.image.load(pic2_path).convert()
            images["fight_menu"] = pygame.transform.scale(images["fight_menu"], globalSettings.SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic2_path}")
        
        if os.path.exists(save_image_path):
            images["save_button"] = pygame.image.load(save_image_path).convert_alpha()
            images["save_button"] = pygame.transform.scale(images["save_button"], (globalSettings.SAVE_BUTTON_SIZE, globalSettings.SAVE_BUTTON_SIZE))
        else:
            raise FileNotFoundError(f"Image file not found: {save_image_path}")

        if os.path.exists(cursor_image_path):
            images["cursor"] = pygame.image.load(cursor_image_path).convert_alpha()
            images["cursor"] = pygame.transform.scale(images["cursor"], (75,75))
        else:
            raise FileNotFoundError(f"Image file not found: {cursor_image_path}")
        globalSettings.images.update(images)
        globalSettings.menuAssetsLoaded = True
        return images

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        return {}


def load_fight_screen_assets():
    backgroundPicPath = os.path.join(globalSettings.fight_background_path, "blurryWuhu.png")
    fightingMatsPath = os.path.join(globalSettings.fight_background_path, "fightingMats.png")
    images = {}
    if os.path.exists(backgroundPicPath):
        images["blurryWuhu"] = pygame.image.load(backgroundPicPath).convert()
        images["blurryWuhu"] = pygame.transform.scale(images["blurryWuhu"], globalSettings.SCREEN_SIZE)
    else:
        raise FileNotFoundError(f"Image file not found: {backgroundPicPath}")    

    if os.path.exists(fightingMatsPath):
        images["fightingMats"] = pygame.image.load(fightingMatsPath).convert_alpha()
        images["fightingMats"] = pygame.transform.scale(images["fightingMats"], globalSettings.SCREEN_SIZE)
    else:
        raise FileNotFoundError(f"Image file not found: {fightingMatsPath}")
    
    globalSettings.images.update(images)
    print(globalSettings.images)
    
    # --- Static Images ---
    # globalSettings.images["background"] = pygame.image.load("assets/background.png").convert()
    # globalSettings.images["fightingMats"] = pygame.image.load("assets/fightingMats.png").convert_alpha()

    # --- Spritesheets ---
    player_sheet, pw, ph = load_and_scale_spritesheet("assets/miiSprites/levi.png", 512, 512, scale=1.0)
    opponent_sheet, ow, oh = load_and_scale_spritesheet("assets/miiSprites/liam.png", 512, 512, scale=1.0)
    print(player_sheet)
    globalSettings.spritesheets["player"] = player_sheet
    globalSettings.spritesheets["opponent"] = opponent_sheet

    # --- Animators ---
    globalSettings.animators["player"] = SpriteAnimator(player_sheet, pw, ph, num_frames=16, row=0)
    globalSettings.animators["opponent"] = SpriteAnimator(opponent_sheet, ow, oh, num_frames=16, row=0)

    globalSettings.fightScreenAssetsLoaded = True