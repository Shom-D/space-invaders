import pgzrun
import random
import time

WIDTH, HEIGHT, TITLE = 900,800,'Space Invaders'
spaceship = Actor('spaceship')
spaceship.y = HEIGHT-120
cooldown = 0.4
last_shot_time = time.time()
bullets = []
level = 2
max_level = 5
enemies = []

def create_enemies(level):
    global enemies
    enemies_per_row = 6
    for y in range(level):
        enemies.append(create_row(y))

def create_row(y):
    enemy_row = []
    for x in range(6):
        enemy = Actor('enemy')
        enemy.x= 150+x*120
        enemy.y = 100 +y*70
        enemy_row.append(enemy)
    return enemy_row

def create_bullet(spaceship_pos):
    global bullets
    bullet = Actor('bullet')
    bullet.pos = spaceship_pos
    bullets.append(bullet)

def update():
    global last_shot_time,level
    if keyboard.d:
        spaceship.x+=2
    if keyboard.a:
        spaceship.x-=2

    if keyboard.space and cooldown<time.time()-last_shot_time:
        create_bullet(spaceship.pos)
        last_shot_time=time.time()

    for bullet in bullets:
        if len(enemies):
            for enemy_row in enemies:
                for enemy in enemy_row:
                    if bullet.colliderect(enemy):
                        bullets.remove(bullet)
                        enemy_row.remove(enemy)
        else:
            level+=1
            print(f"Level incremented to {level}")
            create_enemies()
    
            
 
    move_bullets()


def move_bullets():
    global bullets
    for bullet in bullets:
        bullet.y -= 5
        if bullet.y<0:
            bullets.remove(bullet)
            
def draw():
    global level
    screen.clear()
    spaceship.draw()
    for bullet in bullets:
        bullet.draw()
    for enemy_row in enemies:
        for enemy in enemy_row:
            enemy.draw()
    
    if not len(enemies):
        level+=1
        create_enemies(level)



pgzrun.go()