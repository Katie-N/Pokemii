import pygame
def specialCursor(screen, cursorImage):
    pygame.mouse.set_visible(False)
    cursor_img_rect = cursorImage.get_rect()

    # in your main loop update the position every frame and blit the image    
    cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
    screen.blit(cursorImage, cursor_img_rect) # draw the cursor