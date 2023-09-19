import pygame as pg
import random
import math
from pygame import mixer
pg.init()

screen = pg.display.set_mode((1800,1200))

run=True

# sppeds of the game
playerSpeed=6 
enimesSpeed=6
rocketSpeed=6.5
num_enemies=6 
num_rockets=4

# Background
background=pg.image.load('background.jpg')


# Window logo and game name
pg.display.set_caption("Save the World")
icon = pg.image.load('logo.png')
pg.display.set_icon(icon)

# game music and sounds
mixer.music.load("background_music.mp3")
mixer.music.play(-1)
def explosion():
    explosionSound = mixer.Sound("explosion.wav")
    explosionSound.play()
def rocket_sound():
    rocket_sound=mixer.Sound("rocket_sound.wav")
    rocket_sound.play()

# player image
player = pg.image.load('player.png')


# player movement 
player_x=900
player_y=950
player_update=0
def show_player(x,y):
       screen.blit(player,(x,y))


# enemies image
enemy1 = pg.image.load('enemy1.png')
enemy2= pg.image.load('enemy2.png')
enemy3= pg.image.load('enemy3.png')
enemies=[enemy1,enemy2,enemy3]

# enemy movement


enemy_x=[]
enemy_y=[]
enemy_update=[]
enemy_img=[]
for i in range(num_enemies):
 enemy_img.append(enemies[random.randint(0,2)])
 enemy_x.append(random.randint(0,1672))
 enemy_y.append(random.randint(0,700))
 enemy_update.append(3)

def show_enemy(enemy,x,y):
       screen.blit(enemy,(x,y))

# rocket image
rocket = pg.image.load('rocket.png')

# rocket movment
rocket_x=[]
rocket_y=[]
rocket_update=[]
rocket_status=[]
for i in range(num_rockets):
     rocket_x.append(player_x)
     rocket_y.append(player_y)
     rocket_update.append(-rocketSpeed)
     rocket_status.append(1)

def show_rocket(x,y,i):
       global rocket_status
       rocket_status[i]=0
       screen.blit(rocket,(x+32,y+64))
       
# collision
def isCollision(enemy_x,enemy_y,rocket_x,rocket_y):
    x=(enemy_x-rocket_x)*(enemy_x-rocket_x)
    y=(enemy_y-rocket_y)*(enemy_y-rocket_y)
    distance=math.sqrt(x+y)
    if distance<=75:
         return True
    return False


# score board
score=0
font = pg.font.Font('freesansbold.ttf', 50)

textX = 10
testY = 10

def show_score(x, y):
    score_board = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_board, (x, y))
# gmae over
end=0
def gameOver():
    font_2 = pg.font.Font('freesansbold.ttf', 100)
    lose= font_2.render("GAME OVER !", True, (255, 255, 255))
    screen.blit(lose, (600,500))

# main game
while run :
     if end==1:  
       while run: 
        for event in pg.event.get():
              if event.type ==pg.QUIT:
               run=False 
     screen.blit(background,(0,0))
     for event in pg.event.get():
          if event.type ==pg.QUIT:
               run=False
          if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player_update=-playerSpeed
                if event.key == pg.K_RIGHT:
                     player_update=playerSpeed
                if event.key == pg.K_SPACE:
                     for i in range(num_rockets):
                      if(rocket_status[i]==1):
                          rocket_sound() 
                          rocket_x[i]=player_x
                          rocket_y[i]=player_y
                          show_rocket(rocket_x[i],rocket_y[i],i)
                          break

          if event.type == pg.KEYUP:
                  if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    player_update=0        
     player_x+=player_update 
     if player_x<0:
          player_x=0
     elif player_x>1672:
          player_x=1672    
     for i in range(num_enemies): 
       if enemy_y[i]>825:
           gameOver()
           end=1
           break    
       enemy_x[i]+=enemy_update[i]
       show_enemy(enemy_img[i],enemy_x[i],enemy_y[i])
       if(enemy_x[i]<=0):
          enemy_update[i]=enimesSpeed
          enemy_y[i]+=20
       elif(enemy_x[i]>=1672):
          enemy_update[i]=-enimesSpeed
          enemy_y[i]+=20
       for j in range(num_rockets):   
        if isCollision(enemy_x[i],enemy_y[i],rocket_x[j],rocket_y[j]):
          explosion()
          rocket_status[j]=1
          score+=1
          print(score)
          rocket_y[j]=-1000000
          enemy_img[i]=enemies[random.randint(0,2)]
          enemy_x[i]=random.randint(0,1672)
          enemy_y[i]=random.randint(0,800)

     for i in range(num_rockets):
      if(rocket_y[i]<0):
          rocket_status[i]=1

      if(rocket_status[i]==0):
       show_rocket(rocket_x[i],rocket_y[i],i)        
       rocket_y[i]+=rocket_update[i]    

     show_score(textX,testY)
     show_player(player_x,player_y)  
     pg.display.update()
