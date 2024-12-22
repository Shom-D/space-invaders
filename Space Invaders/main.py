import pgzrun
import random
import time

WIDTH, HEIGHT, TITLE = 900,800,'Space Invaders'
spaceship = Actor('spaceship')
spaceship.y = HEIGHT-100
cooldown = 0.4
last_shot_time = time.time()
bullets = []
enemy_movement = 1 if random.randint(0,1) else -1
print(enemy_movement)
level = 0
max_level = 5
enemies = []
spaceship_speed = 2.6


def create_enemies(level):
    global enemies
    enemies = []
    for y in range(level,0,-1):
        enemies.append(create_row(y))

def create_row(y):
    enemy_row = []
    for x in range(6):
        enemy = Actor('enemy')
        enemy.x= 150+x*120
        enemy.y = 40 +y*70
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
        spaceship.x+= spaceship_speed
    if keyboard.a:
        spaceship.x-= spaceship_speed

    if keyboard.space and cooldown<time.time()-last_shot_time:
        create_bullet(spaceship.pos)
        last_shot_time=time.time()

    for bullet in bullets:
        for enemy_row in enemies:
            if len(enemy_row):
                #print(f"Checking row {enemies.index(enemy_row)}")
                for enemy in enemy_row:
                    #print(f"Checking enemy {enemy_row.index(enemy)} of row {enemies.index(enemy_row)}")
                    if bullet.colliderect(enemy) and bullet in bullets:
                        print(f"Bullet {bullets.index(bullet)} colliding with enemy {enemy_row.index(enemy)} of row {enemies.index(enemy_row)}")
                        bullets.remove(bullet)
                        enemy_row.remove(enemy)
                        enemy.pos = (0,0)
                        break
            else:
                enemies.remove(enemy_row)
        continue

    move_bullets()

    move_enemies()

    if not len(enemies):
        next_level()

def move_bullets():
    global bullets
    for bullet in bullets:
        bullet.y -= 6
        if bullet.y<0:
            bullets.remove(bullet)
            

def move_enemies():
    global enemies
    boundary_check()
    for enemy_row in enemies:
        for enemy in enemy_row:
            enemy.x += enemy_movement + enemy_movement*0.2*(level+1)
    
def boundary_check():
    global enemy_movement
    x_locations = []
    for enemy_row in enemies:
        if enemy_row:
            if enemy_movement== -1:
                x_locations.append(enemy_row[0].x)
            else:
                x_locations.append(enemy_row[-1].x)
    if len(x_locations):
        if min(x_locations)<=20 or max(x_locations)>=WIDTH-20:
            move_vertically()


def move_vertically():
    global enemy_movement, enemies
    enemy_movement *=-1
    for enemy_row in enemies:
        for enemy in enemy_row:
            enemy.y += 35
    
def next_level():
    global bullets,level
    level+=1
    create_enemies(level)
    bullets.clear()

def draw():
    global level
    screen.clear()
    screen.blit('background',(0,0))
    spaceship.draw()
    for bullet in bullets:
        bullet.draw()
    for enemy_row in enemies:
        for enemy in enemy_row:
            enemy.draw()
    
    

pgzrun.go()