from platform import platform
import sys
import pygame
from pygame.locals import *
import pickle
from os import path


class Button:
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        #self.clicked = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        # check mouse over and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                action = True
                self.clicked = True
            
            if key[pygame.K_RETURN] and self.clicked == False:
                action = True
                self.clicked = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            


        # draw button 
        screen.blit(self.img, self.rect)

        return action 


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('files/images/blob.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter = -50


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, state):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('files/images/platform.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.move_x, self.move_y = move_x, move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1

        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter = -50


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('files/images/lava.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('files/images/coin.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center  = (x, y)
        self.move_direction = 1
        self.move_counter = 0


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('files/images/exit.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1

        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter = -50


class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('files/images/dirt.png').convert_alpha()
        grass_img = pygame.image.load('files/images/grass.png').convert_alpha()

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)

                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0, 'x')
                    platform_group.add(platform)

                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1, 'y')
                    platform_group.add(platform)
                
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)

                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)


                
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            # pygame.draw.rect(screen, white, tile[1], 2)
            screen.blit(tile[0], tile[1])
            

class Player():
    def __init__(self, x, y):
        self.reset(x, y)


    def update(self, game_over, level):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_tresh = 20


        if game_over == 0:

            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -17
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.counter += 1   
                self.direction = -1
                dx -= 4

            # direction ### direction ### 
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.counter += 1
                self.direction = 1
                dx += 4
            if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT] and not key[pygame.K_a] and not key[pygame.K_d]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.frames_right[0]
                if self.direction == -1:
                    self.image = self.frames_left[0]


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            self.in_air = True
            for tile in map.tile_list:
                # check for collision in x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below (if jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0 
                        self.in_air = False


            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            # check for colisiopn with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
            
            # collision with platforms
            for plat in platform_group:
                # collision in the x
                if plat.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # collision in the y
                if plat.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # if bellow platforom
                    if abs((self.rect.top + dy) - plat.rect.bottom) < col_tresh:
                        self.vel_y = 0
                        dy = plat.rect.bottom - self.rect.top
                    # if above platform
                    elif abs((self.rect.bottom + dy) - plat.rect.top) < col_tresh:
                        self.rect.bottom = plat.rect.top - 1
                        dy = 0
                        self.in_air = False
                        # move sideways with platform
                        if plat.move_x != 0:
                            self.rect.x += plat.move_direction

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy


            # handle animation 
            if self.counter > walk_cooldown:
                self.index += 1
                if self.index >= len(self.frames_right) - 1:
                    self.index = 0
                self.counter = 0

                if self.direction == 1:
                    self.image = self.frames_right[self.index]
                
                if self.direction == -1:
                    self.image = self.frames_left[self.index]

        elif game_over == -1:
            draw_text('GAME OVER!', font, blue, (sw // 2), sh // 2 - 80)
            #game_over_fx.play()
            #game_over_fx.fadeout(1)
            self.image = self.dead_img
            if self.rect.y > 100:
                self.rect.y -= 5    

        #draw player onto screen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, white, self.rect, 2)


        return game_over

    # re-init
    def reset(self, x, y):
        # player animation frames
        self.frames_right = []
        self.frames_left = []
        self.index = 0
        self.counter = 0
        self.dead_img = pygame.image.load('files/images/ghost.png')
        for i in range(1, 5):
            img_right = pygame.image.load(f'files/images/guy{i}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.frames_right.append(img_right)
            self.frames_left.append(img_left)

        # player variables
        self.image = self.frames_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


def draw_text(txt, font, color, x, y):
    img = font.render(txt, font, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

def display_time():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    draw_text(f'Time: {current_time}', score_font, white, sw//2 + 200, 20)
    return current_time


#function to reset level
def reset_level(level):
    player.reset(100, sh - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    #load in level data and create world
    if path.exists(f'files/data/level{level}_data'):
        pickle_in = open(f'files/data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
        #create dummy coin for showing the score
        score_coin = Coin(tile_size // 2, tile_size // 2)
        coin_group.add(score_coin)
        world = World(world_data)
        return world
    
def set_highscore(score):
    with open('scores.txt', 'r') as f:
        high_score = int(f.readlines()[0])
        #print(high_score)

    if score > high_score:
        with open("scratch.txt","w") as f:
            f.write(str(score))
            #print(high_score)
    return high_score



pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

sw = 1000
sh = 1000

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption('Moonwalker')

#define game variables
clock = pygame.time.Clock()
fps = 60
white = (255, 255, 255)
tile_size = 50
game_over = 0
main_menu = True
level = 2
max_level = 7
score = 0

# define fonts
font = pygame.font.SysFont('Bauhaus 93', 70)
score_font = pygame.font.SysFont('Bauhaus 93', 30)

# define colors
white = (255, 255, 255)
blue = (0, 0, 255)

#load images
sun_img = pygame.image.load('files/images/sun.png').convert_alpha()
bg_img = pygame.image.load('files/images/sky.png').convert_alpha()
restart_img = pygame.image.load('files/images/restart_btn.png').convert_alpha()
start_img = pygame.image.load('files/images/start_btn.png').convert_alpha()
exit_img = pygame.image.load('files/images/exit_btn.png').convert_alpha()

# load sounds
coin_fx = pygame.mixer.Sound('files/music/coin.wav')
game_over_fx = pygame.mixer.Sound('files/music/game_over.wav')
jump_fx = pygame.mixer.Sound('files/music/jump.wav')
pygame.mixer.music.load('files/music/music.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0, 5000)
# set volumes
coin_fx.set_volume(0.5)
game_over_fx.set_volume(0.5)
jump_fx.set_volume(0.5)

# instances and groups
player = Player(100, sh - 130)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()


# create dummy coin for score display
score_coin = Coin( tile_size // 2, tile_size//2 + 5)
coin_group.add(score_coin)

# time
start_time = 0


# map creation
if path.exists(f'files/data/level{level}_data'):
    pickle_in = open(f'files/data/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
    map = World(world_data)
    

# create button
restart_button = Button(sw // 2, sh // 2, restart_img)
start_button = Button(sw // 2 - 225, sh // 2, start_img)
exit_button = Button(sw // 2 + 200, sh // 2, exit_img)



run = True
while run:
    # main game loop

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu:

        start_time = int(pygame.time.get_ticks() / 1000)
        if exit_button.draw():
            run = False
        key = pygame.key.get_pressed()
        if start_button.draw() or key[pygame.K_RETURN]:
            main_menu = False
    
    else:
        map.draw()
        #print(map)     
        
        if game_over == 0:
            blob_group.update()
            # update score
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text(f'       {score}', score_font, white, tile_size - 10, 30)
            draw_text(f'Level: {level}', score_font, white, sw//2, 20)
            time = display_time()

        # if player died
        if game_over == -1:
            key = pygame.key.get_pressed()
            if restart_button.draw() or key[pygame.K_RETURN]:
                player.reset(100, sh - 130)
                game_over = 0

        #if player has completed the level
        if game_over == 1:
            #reset game and go to next level
            level += 1
            if level <= max_level:
                #reset level
                world_data = []
                map = reset_level(level)
                
                game_over = 0
                
                
            else:
                draw_text('YOU WIN!', font, blue, sw // 2, sh // 2 - 80)
                draw_text(f'Your Score: {time}', score_font, blue, sw // 2, sh // 2 + 80)
                set_highscore(time)
                draw_text(f'High Score: {set_highscore(time)}', score_font, blue, sw // 2, sh // 2 + 140)

                # restart game
                if restart_button.draw():
                    level = 1
                    #reset level
                    world_data = []
                    map = reset_level(level)
                    game_over = 0
                    score = 0


        blob_group.draw(screen)
        platform_group.draw(screen)
        platform_group.update()
        lava_group.draw(screen)
        lava_group.update()
        exit_group.draw(screen)
        coin_group.draw(screen)



        try:
            game_over = player.update(game_over, level)
        except:
            continue


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
