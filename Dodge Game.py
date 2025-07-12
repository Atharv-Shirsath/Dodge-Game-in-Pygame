import pygame
import random
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Dodge Game")
clock = pygame.time.Clock()


# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# images

time_block_img = pygame.image.load("Untitled.jpg").convert_alpha()

# Game variables
speed_rectangle = 5
speed_character = 10
speed_line_1 = 10
invincible = False
invincible_start_time = 0
invincible_duration = 5000
gun = False
gun_start_time = 0
gun_duration = 5000
time_block = False
time_block_start_time = 0
time_block_duration = 5000

# Character setup
character = pygame.Rect(275, 525, 50, 50)
line = pygame.Rect(0, 600, 600, 1)
line_1 = pygame.Rect(300, 0, 1, 525)


# Functions
def create_rectangles(num):
    rects = []
    for _ in range(num):
        x_pos = random.randint(0, 580)
        y_pos = random.randint(-600, 0)
        rect = pygame.Rect(x_pos, y_pos, 20, 20)
        rects.append(rect)
    return rects


def create_invincible_block(num):
    rects_1 = []
    for _ in range(num):
        x_pos = random.randint(0, 580)
        y_pos = random.randint(-600, 0)
        rect_1 = pygame.Rect(x_pos, y_pos, 20, 20)
        rects_1.append(rect_1)
    return rects_1


def create_gun_block(num):
    rects_2 = []
    for _ in range(num):
        x_pos = random.randint(0, 580)
        y_pos = random.randint(-10000, 0)
        rect_2 = pygame.Rect(x_pos, y_pos, 20, 20)
        rects_2.append(rect_2)
    return rects_2


def create_time_block(num):
    rects_3 = []
    for _ in range(num):
        x_pos = random.randint(0, 580)
        y_pos = random.randint(-15000, 0)
        rect_3 = pygame.Rect(x_pos, y_pos, 20, 20)
        rects_3.append(rect_3)
    return rects_3


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, rect)


# Game state
game_state = "start"  # start, playing, game_over

# Main loop
running = True
while running:
    screen.fill("white")
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # screen.blit(sky_resized, (0, 0))

    if game_state == "start":
        draw_text("Dodge Game", font, "black", screen, 300, 200)
        draw_text("Press SPACE to Start", small_font, "black", screen, 300, 300)
        if key[pygame.K_SPACE]:
            character.x, character.y = 275, 525
            line_1.x, line.y = 300, 550
            falling_rects = create_rectangles(10)
            falling_invincible_block = create_invincible_block(1)
            falling_gun_block = create_gun_block(1)
            falling_time_block = create_time_block(1)
            speed_rectangle = 5
            speed_character = 10
            speed_line_1 = 10
            count = 0
            a = True
            i = 0
            invincible = False
            invincible_start_time = 0
            gun = False
            gun_start_time = 0
            time_block = False
            time_block_start_time = 0
            game_state = "playing"

    elif game_state == "playing":
        current_time = pygame.time.get_ticks()
        if invincible and current_time - invincible_start_time > invincible_duration:
            invincible = False
        if gun and current_time - gun_start_time > gun_duration:
            gun = False
        if time_block and current_time - time_block_start_time > time_block_duration:
            time_block = False

        # Character movement
        if key[pygame.K_LEFT]:
            character.x -= speed_character
            line_1.x -= speed_line_1
            if character.x < 0 or line_1.x < 0:
                character.x = 0
                line_1.x = 25
        elif key[pygame.K_RIGHT]:
            character.x += speed_character
            line_1.x += speed_line_1
            if character.x > 550 or line_1.x > 550:
                character.x = 550
                line_1.x = 575

        # Speed scaling
        if count < 400:
            speed_rectangle = speed_rectangle
        elif count < 800:
            speed_rectangle = 7
        elif count < 1200:
            speed_rectangle = 9
        elif count < 1600:
            speed_rectangle = 11
        elif count < 2000:
            speed_rectangle = 13
        elif count < 2400:
            speed_rectangle = 15

        # Update falling rectangles
        for rect in falling_rects:
            if time_block==True:
                rect.y += 3
            else:
                rect.y += speed_rectangle

            if rect.y > 600:
                rect.y = random.randint(-100, 0)
                rect.x = random.randint(0, 580)

            if rect.colliderect(line_1) and gun:
                rect.y = random.randint(-600, 0)
                rect.x = random.randint(0, 580)
                count+=1

            if rect.colliderect(character) and not invincible:
                if invincible and gun:
                    # screen.blit(character_image_invincible_resized, character.topleft)
                    pygame.draw.rect(screen, "red", line_1)
                    if invincible:
                        pygame.draw.rect(screen, "green", character)
                        pygame.draw.rect(screen, "red", line_1)
                    elif gun:
                        pygame.draw.rect(screen, "black", character)
                        pygame.draw.rect(screen, "red", line_1)
                elif gun:
                    pygame.draw.rect(screen, "black", character)
                    pygame.draw.rect(screen, "red", line_1)
                elif invincible:
                    pygame.draw.rect(screen, "green", character)
                elif time_block:
                    pygame.draw.rect(screen, "red", character)
                else:
                    # screen.blit(character_image_resized, character.topleft)
                    pygame.draw.rect(screen, "red", character)

                for r in falling_rects:
                    # screen.blit(enemy_image_resized, r.topleft)+
                    pygame.draw.rect(screen, "blue", r)
                for inv in falling_invincible_block:
                    # screen.blit(ammo_image_resized,inv.topleft)
                    pygame.draw.rect(screen, "green", inv)
                for gun in falling_gun_block:
                    pygame.draw.rect(screen, "black", gun)
                for tim in falling_time_block:
                    screen.blit(time_block_img, tim.topleft)

                draw_text(f"Score: {int(count/4)}", small_font, "black", screen, 80, 30)

                pygame.display.flip()
                pygame.time.wait(1000)
                game_state = "game_over"

            if a and rect.colliderect(line):
                count += 1

        # Invincibility block
        for rect_1 in falling_invincible_block:
            if time_block==True:
                rect_1.y += 3
            else:
                rect_1.y += speed_rectangle
            if rect_1.colliderect(character):
                speed_character = 10
                rect_1.y = -5000
                rect_1.x = random.randint(0, 580)
                if speed_rectangle == 7:
                    rect_1.y = -7000
                if speed_rectangle == 9:
                    rect_1.y = -9000
                if speed_rectangle == 11:
                    rect_1.y = -11000

                invincible = True
                invincible_start_time = pygame.time.get_ticks()

        if rect_1.y > 600:
            rect_1.y = -5000
            rect_1.x = random.randint(0, 580)
            if speed_rectangle == 7:
                rect_1.y = -7000
            if speed_rectangle == 9:
                rect_1.y = -9000
            if speed_rectangle == 11:
                rect_1.y = -11000

        # gun block
        for rect_2 in falling_gun_block:
            if time_block==True:
                rect_2.y += 3
            else:
                rect_2.y += speed_rectangle
            if rect_2.colliderect(character):
                speed_character = 10
                rect_2.y = -10000
                rect_2.x = random.randint(0, 580)
                if speed_rectangle == 7:
                    rect_2.y = -12000
                if speed_rectangle == 9:
                    rect_2.y = -14000
                if speed_rectangle == 11:
                    rect_2.y = -16000

                gun = True
                gun_start_time = pygame.time.get_ticks()

        if rect_2.y > 600:
            rect_2.y = -10000
            rect_2.x = random.randint(0, 580)
            if speed_rectangle == 7:
                rect_2.y = -12000
            if speed_rectangle == 9:
                rect_2.y = -14000
            if speed_rectangle == 11:
                rect_2.y = -16000

        for rect_3 in falling_time_block:
            rect_3.y += speed_rectangle
            if rect_3.colliderect(character):
                speed_character = 10
                rect_3.y = random.randint(-15000,0)
                rect_3.x = random.randint(0, 580)
                if speed_rectangle == 7:
                    rect_3.y = random.randint(-17000,-15000)
                if speed_rectangle == 9:
                    rect_3.y = random.randint(-19000,-17000)
                if speed_rectangle == 11:
                    rect_3.y = random.randint(-21000,-19000)

                time_block = True
                time_block_start_time = pygame.time.get_ticks()

        if rect_3.y > 600:
            rect_3.y = random.randint(-15000,0)
            rect_3.x = random.randint(0, 580)
            if speed_rectangle == 7:
                rect_3.y = random.randint(-17000,-15000)
            if speed_rectangle == 9:
                rect_3.y = random.randint(-19000,-17000)
            if speed_rectangle == 11:
                rect_3.y = random.randint(-21000,-19000)
        # Drawing
        pygame.draw.rect(screen, "red", character)
        if invincible and gun:
            # screen.blit(character_image_invincible_resized, character.topleft)
            pygame.draw.rect(screen, "red", line_1)
            if invincible:
                pygame.draw.rect(screen, "green", character)
                pygame.draw.rect(screen, "red", line_1)
            elif gun:
                pygame.draw.rect(screen, "black", character)
                pygame.draw.rect(screen, "red", line_1)
        elif gun:
            pygame.draw.rect(screen, "black", character)
            pygame.draw.rect(screen, "red", line_1)
        elif invincible:
            pygame.draw.rect(screen, "green", character)
        elif time_block:
            pygame.draw.rect(screen, "red", character)
        else:
            # screen.blit(character_image_resized, character.topleft)
            pygame.draw.rect(screen, "red", character)

        for rect in falling_rects:
            # screen.blit(enemy_image_resized, rect.topleft)
            pygame.draw.rect(screen, "blue", rect)
        for rect_1 in falling_invincible_block:
            # screen.blit(ammo_image_resized,rect_1.topleft)
            pygame.draw.rect(screen, "green", rect_1)
        for rect_2 in falling_gun_block:
            pygame.draw.rect(screen, "black", rect_2)
        for rect_3 in falling_time_block:
            screen.blit(time_block_img, rect_3.topleft)

        draw_text(f"Score: {int(count/4)}", small_font, "black", screen, 80, 30)

    elif game_state == "game_over":
        draw_text("You Died!", font, "red", screen, 300, 200)
        draw_text(f"Score: {int(count/4)}", small_font, "black", screen, 300, 270)
        draw_text(
            "Press R to Restart or ESC to Quit", small_font, "black", screen, 300, 350
        )
        if key[pygame.K_r]:
            game_state = "start"
        elif key[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
