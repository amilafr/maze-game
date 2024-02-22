# import module
from pygame import * # import semua objek yg ada di pygame


'''Bikin window game'''

# bikin jendela game
window_width = 700
window_height = 500
window = display.set_mode((window_width, window_height))

# ngasih warna background
window.fill((184, 194, 198))

# background pake image
bg_image = image.load('Images/Backgrounds/galaxy_1.jpg') # nge-load gambar
bg_image = transform.scale(bg_image, (window_width, window_height)) # ubah ukuran gambar biar pas sama backgroundnya

# ngasih caption  
display.set_caption('Game Pacman')


'''Objek Kotak Biasa'''

# class untuk Rectangle
class Rectangle(sprite.Sprite): # turunan dari class sprite
    
    #constructor
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.rect = Rect(x, y, width, height) # bikin kotaknya
        self.fill_color = color # ngisi warnanya
    
    # fungsi untuk nampilin si rectangle
    def display(self):
        draw.rect(window, self.fill_color, self.rect)


class Circle(sprite.Sprite):
    def __init__(self, radius, x, y, color):
        super().__init__()
        # self.circle = Circle(x, y, width, height) # bikin kotaknya
        self.center = (x, y)
        self.radius = radius
        self.fill_color = color # ngisi warnanya

    def display(self):
        draw.circle(window, self.fill_color, self.center, self.radius)

'''Buat sprite dari image'''

# parent class buat sprites --> buat semua gambar
class GameSprite(sprite.Sprite):
   
   #class constructor
   def __init__(self, picture, x, y, width, height):
       # Calling the class constructor (Sprite):
       sprite.Sprite.__init__(self)
       # each sprite must store an image property
       picture = image.load(picture)
       self.image = transform.scale(picture, (width, height))
  
       # ngatur posisi awal karakter
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
   
   # nampilin karakter
   def display(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

# buat geraknya karakter --> buat karakter yang bisa gerak
class Player(GameSprite):
   
   #karakternya bisa dikontrol pake tombol di keyboard (panah atas, bawah, kiri, kanan)
    def __init__(self, picture, x, y, width, height, x_speed, y_speed):
       # Calling the class constructor (Sprite):
       GameSprite.__init__(self, picture, x, y, width, height)
  
       self.x_speed = x_speed
       self.y_speed = y_speed

    # untuk update posisi --> gerak
    def update(self):
        # self.rect.x += self.x_speed
        # self.rect.y += self.y_speed
    
        #horizontal movement first
        if player1.rect.x <= window_width-80 and player1.x_speed > 0 or player1.rect.x >= 0 and player1.x_speed < 0:
            self.rect.x += self.x_speed
        
        #ada dinding/rintangan
        platforms_touched = sprite.spritecollide(self, walls, False) # dinding disentuh gak
        # ngecek kanan-kiri sentuh
        if self.x_speed > 0: # player gerak ke kanan, the character's right edge appears right up to the left edge of the wall
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) #if several walls were touched at once, then the right edge is the minimum possible
        elif self.x_speed < 0: # player gerak ke kiri, then put the character's left edge right up to the right edge of the wall
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) #if several walls have been touched, then the left edge is the maximum
        
        # vertical movement
        if player1.rect.y <= window_height-80 and player1.y_speed > 0 or player1.rect.y >= 0 and player1.y_speed < 0:
            self.rect.y += self.y_speed
        
        # nyentuh dinding
        platforms_touched = sprite.spritecollide(self, walls, False)
        
        if self.y_speed > 0: # going down
            for p in platforms_touched:
                #We're checking which of the platforms is the highest from the ones below, aligning with it, and then take it as our support:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0: #going up
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) #aligning the upper edge along the lower edges of the walls that were touched
    
    # nembak / shoot --> bikin objek bullet
    def shoot(self):
        bullet = Bullet(picture='images-maze/bullet.png', x=self.rect.right, y=self.rect.centery, width=15, height=20, speed=15)
        bullets.add(bullet)
    

# class enemy / musuh
class Enemy(GameSprite):
    side = 'left' # menentukan sekarang gerak ke kanan atau kiri

    # constructor
    def __init__(self, picture, x, y, width, height, speed):
        GameSprite.__init__(self, picture, x, y, width, height)
        self.speed = speed # untuk geraknya musuh

    # untuk gerak kanan - kiri
    def update(self): # bisanya update
        # dia gerak ke kanan kalo udah natap tembok
        if self.rect.x <= 390 : # jarak x wall + width wall
            self.side = 'right'
        # gerak ke kiri kalo udah sampe edge
        if self.rect.x >= window_width - 85:
            self.side = 'left'
        
        # untuk gerak sesuai side
        if self.side == 'left': # side kiri --> gerak ke kiri
            self.rect.x -= self.speed
        else: # side kanan --> gerak ke kanan
            self.rect.x += self.speed
                
# class bullet / peluru
class Bullet(GameSprite):
    # constructor
    def __init__(self, picture, x, y, width, height, speed):
        GameSprite.__init__(self, picture, x, y, width, height)
        self.speed = speed

    # buat dia gerak
    def update(self):
        self.rect.x += self.speed
        # kalo sampe edge dia hilang
        if self.rect.x > window_width:
            self.kill() # biar dia hilang

# variabel warna
PINK = (230, 194, 198)

run = True
finish = False

rect1 = Rectangle(color=PINK, x=150, y=150, width=300, height=40)
rect2 = Rectangle(color=PINK, x=350, y=120, width=40, height=320)

walls = sprite.Group()
# nambahin dinding
walls.add(rect1)
walls.add(rect2)
# walls.add(circle1)

circle1 = Circle(color=PINK, radius=50, x=500, y=100)

player1 = Player(picture='images-maze/hero.png', height=80, width=80, x=20, y=380, x_speed=0, y_speed=0)

# rintangan
obs1 = GameSprite(height=200, width=70, picture='images-maze/platform2_v.png', x=100, y=100)

# finish
finish_obj = GameSprite(picture='images-maze/pac-1.png', height=80, width=80, x=window_width-100, y=window_height-100)

# enemy
# enemy = Game

enemy1 = Enemy(picture='images-maze/cyborg.png', height=70, width=70, x=window_width-80, y=200, speed=5)
enemy2 = Enemy(picture='images-maze/cyborg.png', height=70, width=70, x=window_width-80, y=280, speed=5)

# group enemies
enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)

# peluru
bullets = sprite.Group()

while run:
    # the loop is triggered every 0.05 seconds
    time.delay(50)
    
    # mengaktifkan tombol close
    for e in event.get(): # manggil semua event yg ada di pygame
        if e.type == QUIT:
            run = False
        
        # tombol keyboard ditekan --> KEYDOWN
        elif e.type == KEYDOWN:
            if e.key == K_UP: #atas
                player1.y_speed -= 5
            elif e.key == K_DOWN: #bawah
                player1.y_speed += 5
            elif e.key == K_RIGHT: #kanan
                player1.x_speed += 5
            elif e.key == K_LEFT: #kiri
                player1.x_speed -= 5
            # shoot
            elif e.key == K_SPACE:
                player1.shoot()
        
        elif e.type == KEYUP:
           if e.key == K_LEFT:
               player1.x_speed = 0
           elif e.key == K_RIGHT:
               player1.x_speed = 0
           elif e.key == K_UP:
               player1.y_speed = 0
           elif e.key == K_DOWN:
               player1.y_speed = 0

    if not finish:
        # nampilin gambarnya sebagai background
        window.blit(bg_image, (0,0))

        # bikin objek rectangle
        rect1.display()    
        rect2.display()
        # walls.draw(window)

        # circle1.display()

        # enemy_obj.display()
        # enemy_obj.update()

        bullets.update() # buat move nya si bullet
        bullets.draw(window) # buat nampilin semua bullet

        finish_obj.display()

        # obs1.display()
        # sprite1 = GameSprite(picture='Images/Heros/pacman/pac-1.png', height=50, width=50, x=100, y=200) #bikin objek
        # sprite1.display() #nampilin

        player1.display()
        player1.update()

        # kalo musuh kena peluru
        # sprite.groupcollide(enemies, bullets, True, True)
        
        enemies.update()
        enemies.draw(window) # untuk nampilin semua enemies
        
        # bullet nyentuh enemy atau wall
        sprite.groupcollide(enemies, bullets, True, True) # True --> hilang
        # sprite.groupcollide()
        # groupcollide --> group ketemu group
        sprite.groupcollide(bullets, walls, True, False)


        # nyentuh musuh (spritecollide --> 1 objek ketemu group)
        if sprite.spritecollide(player1, enemies, False): # kondisi player1 nyentuh enemy
            finish = True
            img = image.load('images-maze/game-over_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0, 0))

        # nyentuh finish (collide_rect --> klo 1 objek ketemu 1 objek)
        if sprite.collide_rect(player1, finish_obj): # kondisi player1 nyentuh finish
            finish = True
            img = image.load('images-maze/thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (window_width, window_height)), (0, 0))


    display.update()