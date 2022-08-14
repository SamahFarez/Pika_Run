
from email.mime import image
from lib2to3.refactor import MultiprocessRefactoringTool
from operator import index
import random
from re import I
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        Player_walk1 = pygame.image.load('graphics/Player/Pokerun.png').convert_alpha()
        Player_walk1 = pygame.transform.scale(Player_walk1, (100, 80)).convert_alpha()
        Player_walk2 = pygame.image.load('graphics/Player/Run2-pika.png').convert_alpha()
        Player_walk2 = pygame.transform.scale(Player_walk2, (100, 80)).convert_alpha()
        Player_walk3 = pygame.image.load('graphics/Player/pika.png').convert_alpha()
        Player_walk3 = pygame.transform.scale(Player_walk3, (100, 80)).convert_alpha()
        
        self.Player_walk = [ Player_walk1, Player_walk2, Player_walk3 ]
        self.Player_index = 0
        self.Player_jump = pygame.image.load('graphics/Player/jump-pika.png').convert_alpha()
        self.Player_jump = pygame.transform.scale(self.Player_jump, (95, 80)).convert_alpha() 
        
        self.image = self.Player_walk [ self.Player_index ]
        self.rect = self.image.get_rect(midbottom = (150,300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('audio/jumpp.wav')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys [ pygame.K_SPACE ] and self.rect.bottom >= 305 : 
            self.gravity = -20
            self.jump_sound.play()
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 305 : self.rect.bottom = 305
    
    def reset_gravity(self):
        self.gravity = 0
        self.rect.bottom = 305
        
    def animate(self):
        if self.rect.bottom < 305 : self.image = self. Player_jump
        else :
            self.Player_index += 0.1
            if self.Player_index >= len(self.Player_walk) : self.Player_index = 0
            self.image = self.Player_walk[int(self.Player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate() 
        if game_active == False :
            self.reset_gravity()    

class Obstacles ( pygame.sprite.Sprite ):
    def __init__(self,type) :
        super().__init__()
        
        if type == 'dragon':
            Drago_surf1 = pygame.image.load('graphics/Fly/Drag.png').convert_alpha()
            Drago_surf1 = pygame.transform.scale(Drago_surf1, (200, 110)).convert_alpha()
            Drago_surf2 = pygame.image.load('graphics/Fly/Drag2.png').convert_alpha()
            Drago_surf2 = pygame.transform.scale(Drago_surf2, (200, 140)).convert_alpha()
            self.frames = [Drago_surf1, Drago_surf2]
            y_pos = 150
        
        elif type == 'bee':
            Bee_surf1 = pygame.image.load('graphics/Fly/Beee.png').convert_alpha()
            Bee_surf1 = pygame.transform.scale(Bee_surf1, (100, 80)).convert_alpha()
            Bee_surf2 = pygame.image.load('graphics/Fly/Beee2.png').convert_alpha()
            Bee_surf2 = pygame.transform.scale(Bee_surf2, (105, 120)).convert_alpha()
            self.frames = [Bee_surf1, Bee_surf2]
            y_pos = 130
            
        elif type == 'ball':
            Ball_surf1 = pygame.image.load('graphics/Fly/pokeball.png').convert_alpha()
            Ball_surf1 = pygame.transform.scale(Ball_surf1, (60, 30)).convert_alpha()
            Ball_surf2 = pygame.image.load('graphics/Fly/pokeball2.png').convert_alpha()
            Ball_surf2 = pygame.transform.scale(Ball_surf2, (30, 45)).convert_alpha()
            self.frames = [Ball_surf1, Ball_surf2]
            y_pos = 200
            
        elif type == 'cat':
            cat_surf1 = pygame.image.load('graphics/ground/cat.png').convert_alpha()
            Cat_surf1 = pygame.transform.scale(cat_surf1, (60, 60)).convert_alpha()
            cat_surf2 = pygame.image.load('graphics/ground/cat2.png').convert_alpha()
            Cat_surf2 = pygame.transform.scale(cat_surf2, (70, 70)).convert_alpha()
            self.frames = [Cat_surf1, Cat_surf2]
            y_pos = 305
        
        else :
            Rock_surf = pygame.image.load('graphics/ground/Rocks.png').convert_alpha()
            Rock_surf = pygame.transform.scale(Rock_surf, (60, 50)).convert_alpha()
            self.frames = [Rock_surf, Rock_surf]
            y_pos = 315
            
            
        self.animate_index = 0
            
        self.image =  self.frames [ self.animate_index ]
        self.rect = self.image.get_rect ( midbottom = ( random.randint (900, 1100 ), y_pos ))
    
    def animate(self):
            self.animate_index += 0.03
            if self.animate_index >= len(self.frames) : self.animate_index = 0
            self.image = self.frames[int(self.animate_index)]
        
    def destroy(self):
        if self.rect.x <= - 250 : self.kill()
    
    def update(self):
        self.animate()
        self.rect.x -= 6 
        self.destroy()
   
#FUNCTIONS
def background():  
    
    ground1.x -= 5
    screen.blit(Ground1, ground1)
    ground2.x -= 5
    screen.blit(Ground2, ground2)
    
    if ground2.x == -800 : 
        ground2.x = 800     
    if ground1.x == -800 : 
        ground1.x = 800  
          
def display_time():
    current_time = int (pygame.time.get_ticks()/1000) - start_time
    score_surf = small_font.render(f'Score:{current_time}', False, 'black').convert_alpha()
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)  
    return current_time 

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacles_group, False ): 
        gameover_sound = pygame.mixer.Sound('audio/fail.wav')
        gameover_sound.set_volume(0.5)
        gameover_sound.play()
        obstacles_group.empty()
        return False
    else :  return True

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pika Run ! ')
clock = pygame.time.Clock()

#FONTS
big_font = pygame.font.Font('font/Pixeltype.ttf', 80)
medium_font = pygame.font.Font('font/Pixeltype.ttf', 50)
small_font = pygame.font.Font('font/Pixeltype.ttf', 35)

#VARS
game_active = False
start_time = 0
score = 0     

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play( loops = -1 )

#GROUPS
#player:
player = pygame.sprite.GroupSingle()
player.add(Player())
#obstacles:
obstacles_group = pygame.sprite.Group()

#SCREEN
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
Ground1 = pygame.image.load('graphics/ground.png').convert()
ground1 = Ground1.get_rect(topleft = (0 , 300 ))
Ground2 = pygame.image.load('graphics/ground.png').convert()
ground2  = Ground2.get_rect(topleft = (800, 300 ))
    
#PAUSE
replayPika_surf = pygame.image.load('graphics/Player/pikapika.png').convert_alpha()
replayPika_surf = pygame.transform.scale(replayPika_surf, (180, 150)).convert_alpha()
gameOver_surf = big_font.render('  !! PIKA RUN !!  ', False, 'Black')
replay_surf = medium_font.render(' > press SPACE to run <', False, 'Black')

#TIMER
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
            if game_active:
                game_active=False
                
            else:
                pygame.quit()
                exit()
                    
        if game_active:
            if event.type == obstacle_timer:
                obstacles_group.add(Obstacles(choice(['dragon', 'ball', 'cat', 'rock', 'rock', 'rock', 'bee']))) 
               
            if int (pygame.time.get_ticks()/1000)%10 == 0 :
                pika = pygame.mixer.Sound('audio/Pika_Pi.mp3')
                pika.set_volume(0.2)
                pika.play()
                 
        else :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE:
                    game_active=True
                    start_time = int (pygame.time.get_ticks()/1000)
                    
    if game_active:
        
        #SCREEN
        screen.blit(sky_surf, (0, 0))
        background()

        # SCORE  
        score = display_time()
        
        # PLAYER:
        player.draw(screen)
        player.update()
        
        #OBSTACLES
        obstacles_group.draw(screen)
        obstacles_group.update()

        #COLLISION
        game_active = collision_sprite()

    else:
        #PAUSE SCREEN
        screen.fill('lightblue')
        screen.blit(gameOver_surf, (250, 50))
        message_score = small_font.render(f'Your Score : {score}', False , 'black ')
        message_rect = message_score.get_rect(center= (400, 115))
        screen.blit(message_score, message_rect)
        screen.blit(replayPika_surf, (300, 150))
        screen.blit(replay_surf, (225, 320))
        player.update()
                                  
    pygame.display.update()
    clock.tick(60)
