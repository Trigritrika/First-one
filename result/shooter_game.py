#Создай собственный Шутер!
from pygame import *
from random import randint
#создай окно игры
window = display.set_mode((1000, 600))
display.set_caption("шутер")
background = transform.scale(image.load("galaxy.jpg"), (1000,1000))
#musica
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
#shit
font.init()
font2 = font.SysFont('Arial',36)
font1 = font.SysFont("Arial", 80)
#cartinochki
img_back = "galaxy.png"
img_hero = "blackhole.png"
img_bullet = 'spiral.png'
img_enemy = 'star.png'
win_width = 1000
win_height = 600
score = 0
lost = 0
max_lost = 5
goal = 20
win = font1.render("YOU WON!", True, (255,255,255))
lose = font1.render("YOU LOSE!", True, (180,0,0))
#MegaClass (tipo Parent)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#classniy player
class Player(GameSprite):
    def update(self):
        
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 995:
            self.rect.x += self.speed
        
#FIRE!!!!FIRE!!!!
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 10, 10, -10)
        bullets.add(bullet)
#enemy class(Plohoi)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 100)
            self.rect.y = 0
            lost = lost+1
#OMG
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    

#player
#player = Player('rocket.png', 5, 420, 4)

#e = (xz)^2
ship = Player(img_hero,5,win_height - 100,100,100,10)

monsters = sprite.Group()
for i in range(1,7):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40,80,80,randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()      
#надо
finish = False
game = True

display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
#цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
    
    if not finish:
        window.blit(background,(0, 0))

        text = font2.render('Счёт:'+ str(score),1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Propusheno:' + str(lost),1,(255,255,255))

        window.blit(text, (10,20))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:

            score = score+1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (300, 200))

        if score >= goal:
            finish = True
            window.blit(win, (300,200))

        text = font2.render('Счёт:'+ str(score),1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('Propusheno:' + str(lost),1,(255,255,255))
        window.blit(text_lose, (10,50))
    
        display.update()
    else:
        finish = False
        score = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

     

        

       
    time.delay(25)
