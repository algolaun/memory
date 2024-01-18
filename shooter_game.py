#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

win_w = 700
win_h = 500
font.init()
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 40)
lost = 0
max_lost = 10
win = 0
font = font.Font(None,70)
win_1 = font.render('YOU WIN!',True,(255,215,0))
lose_1 = font.render('YOU LOSE',True,(180,0,0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('lazer.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        
        

            
    
life = 3

num_fire = 0
rel_time = False

monsters = sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, win_w - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)


bullets = sprite.Group()

window = display.set_mode((win_w, win_h))
display.set_caption('Shooter Game')
background = transform.scale(image.load('spase1.jpg'),(win_w, win_h))
ship = Player('rocket.png', 80, 430, 65, 65, 7)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
run = True
clock = time.Clock()
FPS = (60)

finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    
    if not finish:
        window.blit(background,(0,0))
        text_lose = font1.render('пропущено' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('счет' + str(win), 1, (255, 255, 255))
        window.blit(text_win,(10,10))
        window.blit(text_lose,(10,30))
        ship.update()
        asteroids.draw(window)

        monsters.update()
        bullets.update()
        ship.reset()
        asteroids.update()
        

        

        colides = sprite.groupcollide(monsters, bullets, True, True)
        for c in colides:
            win = win + 1
            monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
         
        

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose_1, (200, 200))
            







        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('wait, revald...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))   

        if win >= 10:
            finish = True
            window.blit(win_1, (200,200))

            
        bullets.draw(window)
        monsters.draw(window)
        display.update()
        clock.tick(FPS)
    else:
        finish = False
        win = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1,6):
            monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster) 


    

    time.delay(15)
            


