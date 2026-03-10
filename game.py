import pgzrun
import random

class Player:
    def __init__(self):
        self.animation_counter = 0
        self.x = 32*2
        self.y = 32*7
        self.image = 'playertmp'
        self.idle_images = ['playertmp', 'playertmp_2']
        self.move_images = ['playermove', 'playermove_2']
        self.moving = False
        self.move_target_x = self.x
        self.move_target_y = self.y
        self.move_speed = 2
        self.move_cooldown = 0
        self.cooldown_time = 0.2
        self.rat_enemy = Actor('enemy1tmp')
        self.rat_idle_images = ['enemy1tmp', 'enemy1tmp_2']
        self.rat_enemy.x = 32*random.randint(5, 8)
        self.rat_enemy.y = 32*random.randint(5, 8)
        self.rat_enemy2 = Actor('enemy1tmp')
        self.rat_enemy2.x = 32*random.randint(5, 8) 
        self.rat_enemy2.y = 32*random.randint(5, 8)
        self.elf_enemy = Actor('enemy2tmp')
        self.elf_idle_images = ['enemy2tmp', 'enemy2tmp_2']
        self.elf_enemy.x = 32*random.randint(5, 8)
        self.elf_enemy.y = 32*random.randint(5, 8)
        self.elf_enemy2 = Actor('enemy2tmp')
        self.elf_enemy2.x = 32*random.randint(5, 8)
        self.elf_enemy2.y = 32*random.randint(5, 8)
        self.mage_idle_images = ['bosstmp', 'bosstmp_2']
        self.mage_enemy = Actor('bosstmp')
        self.mage_enemy.x = 32*random.randint(5, 8)
        self.mage_enemy.y = 32*random.randint(5, 8)

    def move(self):
        if self.move_cooldown > 0:
            return
        if not self.moving:
            if keyboard.right and self.x + 32 < WIDTH:
                self.move_target_x = self.x + 32
                self.moving = True
            elif keyboard.left and self.x - 32 >= 0:
                self.move_target_x = self.x - 32
                self.moving = True
            elif keyboard.up and self.y - 32 >= 0:
                self.move_target_y = self.y - 32
                self.moving = True
            elif keyboard.down and self.y + 32 < HEIGHT:
                self.move_target_y = self.y + 32
                self.moving = True

    def update(self,dt):
        self.move_cooldown = max(0, self.move_cooldown - dt)
        if self.moving:
            if self.x < self.move_target_x:
                self.x += self.move_speed
                if self.x >= self.move_target_x:
                    self.x = self.move_target_x
                    self.finish_move()
            elif self.x > self.move_target_x:
                self.x -= self.move_speed
                if self.x <= self.move_target_x:
                    self.x = self.move_target_x
                    self.finish_move()
            elif self.y < self.move_target_y:
                self.y += self.move_speed
                if self.y >= self.move_target_y:
                    self.y = self.move_target_y
                    self.finish_move()
            elif self.y > self.move_target_y:
                self.y -= self.move_speed
                if self.y <= self.move_target_y:
                    self.y = self.move_target_y
                    self.finish_move()
        self.move()

    def finish_move(self):
        self.moving = False
        self.move_cooldown = self.cooldown_time

    def draw(self):
        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.animation_counter = 0
            images = self.move_images if self.moving else self.idle_images
            current_index = images.index(self.image) if self.image in images else 0
            self.image = images[(current_index + 1) % len(images)]
        screen.blit(self.image, (self.x, self.y))

class Game:
    def __init__(self):
        self.music_play = True
        self.music_pos = 0
        self.volume = 0.05
        music.set_volume(self.volume)
        music.play('music')
        self.state = 'menu'

game = Game()
player = Player()


WIDTH = 800
HEIGHT = 608

buttons = [
    {'rect': Rect(300, 200, 200, 50), 'text': 'Rozpocznij gre', 'action': 'start'},
    {'rect': Rect(300, 270, 200, 50), 'text': 'Przelacz muzyke', 'action': 'toggle_music'},
    {'rect': Rect(300, 340, 200, 50), 'text': 'Wyjscie', 'action': 'exit'},
    {'rect': Rect(300, 410, 200, 50), 'text': 'Jak grac', 'action': 'tutorial'},
    {'rect': Rect(300, 400, 200, 50), 'text': 'Powrot do main menu', 'action': 'powrot'},
]

def draw():
    screen.fill((128, 0, 0))
    if game.state == 'menu':
        for button in buttons:
            screen.draw.rect(button['rect'], (255, 255, 255))
            screen.draw.text(button['text'], center=button['rect'].center, fontsize=30, color=(0, 0, 0))

    if game.state == 'playing':
        for x in range(0, WIDTH, 32):
            for y in range(0, HEIGHT, 32):
                screen.draw.rect(Rect(x, y, 32, 32), (0,0,0))
        player.draw()
        
def toggle_music():
    if game.music_play:
        game.music_play = False
        game.music_pos = music.get_pos() / 1000
        music.pause()
    else:
        game.music_play = True
        music.unpause()

def update(dt):
    if game.state == 'playing':
        player.update(dt)

def on_key_down(key):
    if key == keys.SPACE:
        toggle_music()

def on_mouse_down(pos):
    if game.state == 'menu':
        for button in buttons:
            if button['rect'].collidepoint(pos):
                if button['action'] == 'start':
                    game.state = 'playing'
                elif button['action'] == 'toggle_music':
                    toggle_music()
                elif button['action'] == 'exit':
                    exit()
                elif button['action'] == 'tutorial':
                    game.state = 'tutorial'
    if game.state == 'tutorial':
        if button['rect'].collidepoint(pos):
            if button['action'] == 'powrot':
                game.state = 'menu'
pgzrun.go()


"""




Gra zawiera zarówno muzykę w tle, jak i efekty dźwiękowe

Gra zawiera kilku przeciwników, którzy stwarzają zagrożenie dla głównego bohatera

Przeciwnicy poruszają w świecie gry

Klasa gracza powinna zawierać funkcje ruchu i możliwość odgrywania animacji

Obrazki głównego bohatera oraz przeciwników powinny być animowane podczas ruchu, ORAZ w momencie, kiedy się nie ruszają (dodaj animację spoczynku, może ona przedstawiać postacie, które się rozciągają, rozglądają, wiercą itd.)

Podczas definiowania zmiennych, klas i funkcji używaj jasnych i krótkich nazw w języku angielskim. Możesz skorzystać ze stylu prezentowanego w PEP8

Gra powinna zawierać proste, łatwe do zrozumienia mechanizmy oraz być pozbawiona błędów




Uwagi:
Roguelike oznacza tutaj grę z widokiem z góry, 
w której wszystkie obiekty i postacie są umieszczone w komórkach świata gry opartego na siatce. 
Ruch postaci między komórkami powinien być płynny i animowany.


Wyjątek: MOŻESZ użyć klasy Rect z PyGame.

Roguelike 

zrobione :

menu główne, z następującymi przyciskami:
Rozpocznij grę
Przełącz muzykę Wyłączoną/Włączoną
Wyjście
"""