import random, os, pgzrun
from pygame import Rect, mixer

TILE = 32
FIELD_WIDTH = 800
FIELD_HEIGHT = 608
HUD_HEIGHT = 4 * TILE

WIDTH = FIELD_WIDTH
HEIGHT = FIELD_HEIGHT + HUD_HEIGHT

BASE_DIR = os.path.dirname(__file__)
BATTLE_SOUNDS = {}


def play_battle_sound(enemy_type):
    sound_name = "magic" if enemy_type == "boss" else "explosion"
    BATTLE_SOUNDS[sound_name].set_volume(0.1)
    BATTLE_SOUNDS[sound_name].play()

class Character:
    def __init__(self, x, y, idle, move, speed=2):
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.idle_images, self.move_images = idle, move
        self.image = idle[0]
        self.moving = False
        self.animation_counter = 0
        self.move_target_x, self.move_target_y = x, y
        self.move_speed = speed
        self.cooldown_time = 0.2
        self.move_cooldown = 0

    def _move_towards(self, dt):
        self.move_cooldown = max(0, self.move_cooldown - dt)
        if not self.moving:
            return
        for attr, target in [("x", "move_target_x"), ("y", "move_target_y")]:
            curr = getattr(self, attr)
            targ = getattr(self, target)
            if curr < targ:
                setattr(self, attr, min(curr + self.move_speed, targ))
            elif curr > targ:
                setattr(self, attr, max(curr - self.move_speed, targ))
        if self.x == self.move_target_x and self.y == self.move_target_y:
            self.finish_move()

    def _animate(self):
        self.animation_counter += 1
        if self.animation_counter >= 5:
            self.animation_counter = 0
            imgs = self.move_images if self.moving else self.idle_images
            idx = imgs.index(self.image) if self.image in imgs else 0
            self.image = imgs[(idx + 1) % len(imgs)]

    def finish_move(self):
        self.moving = False
        self.move_cooldown = self.cooldown_time

    def draw(self, offset=0):
        self._animate()
        screen.blit(self.image, (self.x, self.y + offset))


class Enemy(Character):
    def __init__(self, x, y, etype, power, idle, move):
        super().__init__(x, y, idle, move)
        self.enemy_type = etype
        self.power = power
        self.move_cooldown = random.uniform(0.5, 2.0)
        self.cooldown_time = self.move_cooldown

    def update(self, dt):
        self.move_cooldown = max(0, self.move_cooldown - dt)
        self._move_towards(dt)
        if not self.moving and self.move_cooldown <= 0:
            self.choose_random_move()

    def choose_random_move(self):
        directions = [(TILE, 0), (-TILE, 0), (0, TILE), (0, -TILE)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < FIELD_WIDTH and 0 <= ny < FIELD_HEIGHT:
                if not (nx == player.x and ny == player.y):
                    self.prev_x = self.x
                    self.prev_y = self.y
                    self.move_target_x = nx
                    self.move_target_y = ny
                    self.moving = True
                    break


class Player(Character):
    def __init__(self):
        super().__init__(TILE * 2, TILE * 7, ["playertmp", "playertmp_2"], ["playermove", "playermove_2"])
        self.move_cooldown = 0

    def reset_position(self):
        self.x = TILE * 2
        self.y = TILE * 7
        self.moving = False
        self.move_cooldown = 0
        self.move_target_x = self.x
        self.move_target_y = self.y

    def move(self):
        if self.move_cooldown > 0 or self.moving:
            return
        
        moves = [
            (keyboard.right, self.x + TILE, FIELD_WIDTH, "x"),
            (keyboard.left, self.x - TILE, FIELD_WIDTH, "x"),
            (keyboard.up, self.y - TILE, FIELD_HEIGHT, "y"),
            (keyboard.down, self.y + TILE, FIELD_HEIGHT, "y")
        ]
        for key, new_pos, limit, attr in moves:
            if key and 0 <= new_pos < limit:
                setattr(self, f"move_target_{attr}", new_pos)
                self.moving = True
                return

    def update(self, dt):
        self._move_towards(dt)
        self.move()


class Game:
    def __init__(self):
        for sound_name in ["explosion", "magic"]:
            sound_path = os.path.join(BASE_DIR, "sounds", "SFX", f"{sound_name}.wav")
            BATTLE_SOUNDS[sound_name] = mixer.Sound(sound_path)
        
        self.state = "menu"
        self.player_power = 2
        self.message = ""
        self.battle_active = False
        self.battle_enemy = None
        self.battle_loser = None
        self.battle_timer = 0
        self.blink_timer = 0
        self.blink_visible = True
        self.music_play = True
        self.volume = 0.05
        
        music.play("music")
        music.set_volume(self.volume)

    def reset_battle(self):
        self.battle_active = False
        self.battle_enemy = None
        self.battle_loser = None
        self.battle_timer = 0
        self.blink_timer = 0
        self.blink_visible = True


def build_enemies():
    used = set()
    specs = [
        ("enemy1", 1, ["enemy1tmp", "enemy1tmp_2"], ["enemy1move", "enemy1move_2"]),
        ("enemy1", 1, ["enemy1tmp", "enemy1tmp_2"], ["enemy1move", "enemy1move_2"]),
        ("enemy2", 3, ["enemy2tmp", "enemy2tmp_2"], ["enemy2move", "enemy2move_2"]),
        ("enemy2", 3, ["enemy2tmp", "enemy2tmp_2"], ["enemy2move", "enemy2move_2"]),
        ("boss", 5, ["bosstmp", "bosstmp_2"], ["bossmove", "bossmove_2"]),
    ]
    enemies = []
    for etype, power, idle, move in specs:
        while True:
            x = TILE * random.randint(0, (FIELD_WIDTH // TILE) - 1)
            y = TILE * random.randint(0, (FIELD_HEIGHT // TILE) - 1)
            if (x, y) != (player.x, player.y) and (x, y) not in used:
                used.add((x, y))
                enemies.append(Enemy(x, y, etype, power, idle, move))
                break
    return enemies


def start_battle(enemy):
    game.battle_active = True
    game.battle_enemy = enemy
    game.battle_timer = 1.0
    game.blink_timer = 0.5
    game.blink_visible = True
    
    if game.player_power > enemy.power:
        game.battle_loser = "enemy"
        game.message = "bitwa: wygrywasz"
    elif game.player_power < enemy.power:
        game.battle_loser = "player"
        game.message = "bitwa: przegrywasz"
    else:
        game.battle_loser = None
        game.message = "bitwa: remis"


def resolve_battle():
    enemy = game.battle_enemy
    if game.battle_loser == "enemy" and enemy in enemies:
        enemies.remove(enemy)
        game.player_power += enemy.power
        game.message = f"pokonany {enemy.enemy_type}, moc: {game.player_power}"
        if enemy.enemy_type == "boss":
            game.state = "win"
            game.message = "wygrana: boss pokonany"
    elif game.battle_loser == "player":
        game.state = "lose"
        game.message = "przegrana"
    else:
        game.message = "remis - bez zmian"
    game.reset_battle()


def draw_hud():
    screen.draw.filled_rect(Rect(0, 0, WIDTH, HUD_HEIGHT), (30, 30, 30))
    screen.draw.text(f"moc: {game.player_power}", (20, 15), fontsize=36, color=(255, 255, 255))
    screen.blit(player.idle_images[0], (20, 55))
    
    x = 110
    for enemy in enemies:
        screen.blit(enemy.idle_images[0], (x, 60))
        screen.draw.text(str(enemy.power), (x + 8, 92), fontsize=26, color=(255, 220, 80))
        x += 50
    
    if game.message:
        screen.draw.text(game.message, (400, 15), fontsize=32, color=(255, 255, 255))


def draw_buttons(buttons):
    for button in buttons:
        screen.draw.rect(button["rect"], (255, 255, 255))
        screen.draw.text(button["text"], center=button["rect"].center, fontsize=30, color=(0, 0, 0))


def draw_playing():
    draw_hud()
    for x in range(0, FIELD_WIDTH, TILE):
        for y in range(0, FIELD_HEIGHT, TILE):
            screen.draw.rect(Rect(x, y + HUD_HEIGHT, TILE, TILE), (0, 0, 0))
    
    for enemy in enemies:
        should_hide = (game.battle_active and game.battle_enemy == enemy and 
                      game.battle_loser == "enemy" and game.battle_timer <= 0 and not game.blink_visible)
        should_blink = (game.battle_active and game.battle_enemy == enemy and 
                       game.battle_loser == "enemy" and game.battle_timer <= 0 and game.blink_visible)
        
        if not should_hide:
            if should_blink:
                screen.blit("spritedeath", (enemy.x, enemy.y + HUD_HEIGHT))
            else:
                enemy.draw(HUD_HEIGHT)
    
    if game.battle_active and game.battle_loser == "player" and game.battle_timer <= 0:
        if game.blink_visible:
            screen.blit("spritedeath", (player.x, player.y + HUD_HEIGHT))
    else:
        player.draw(HUD_HEIGHT)


def draw():
    screen.fill((128, 0, 0))
    if game.state == "menu":
        draw_buttons(buttons[:-1])
    elif game.state == "tutorial":
        lines = [
            "zasady:",
            "gracz moc 2",
            "enemy1 moc 1, enemy2 moc 3, boss moc 5",
            "jesli masz wiecej mocy - wygrywasz bitwe",
            "jesli mniej - przegrywasz",
            "jesli tyle samo - remis",
            "cel: pokonaj bossa",
        ]
        for i, line in enumerate(lines):
            screen.draw.text(line, (70, 120 + i * 45), fontsize=36, color=(255, 255, 255))
        draw_buttons([buttons[-1]])
    elif game.state == "playing":
        draw_playing()
    elif game.state in ["win", "lose"]:
        draw_playing()
        txt = "wygrales" if game.state == "win" else "przegrales"
        panel = Rect(120, HUD_HEIGHT + 180, 560, 220)
        screen.draw.filled_rect(panel, (20, 20, 20))
        screen.draw.rect(panel, (255, 255, 255))
        screen.draw.text(txt, center=(panel.centerx, panel.centery - 20), fontsize=54, color=(255, 255, 255))
        screen.draw.text("kliknij aby wrocic do menu", center=(panel.centerx, panel.centery + 45), fontsize=30, color=(220, 220, 220))


def update(dt):
    if game.state != "playing":
        return
    if game.battle_active:
        game.battle_timer -= dt
        if game.battle_timer <= 0:
            game.blink_timer -= dt
            if game.blink_timer > 0:
                game.blink_visible = not game.blink_visible
            else:
                resolve_battle()
        return
    player.update(dt)
    for enemy in enemies:
        enemy.update(dt)
    for enemy in enemies[:]:
        if enemy.x == player.x and enemy.y == player.y:
            play_battle_sound(enemy.enemy_type)
            if game.player_power != enemy.power:
                start_battle(enemy)
            else:
                enemy.x, enemy.y = enemy.prev_x, enemy.prev_y
                game.message = "remis - bez zmian"
            break


def on_key_down(key):
    if key == keys.SPACE:
        game.music_play = not game.music_play
        music.pause() if not game.music_play else music.unpause()


def on_mouse_down(pos):
    if game.state == "menu":
        for btn in buttons[:-1]:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "start":
                    player.reset_position()
                    game.player_power, game.message = 2, "pokonaj bossa"
                    game.reset_battle()
                    game.state = "playing"
                    global enemies
                    enemies = build_enemies()
                elif btn["action"] == "toggle_music":
                    game.music_play = not game.music_play
                    music.pause() if not game.music_play else music.unpause()
                elif btn["action"] == "exit":
                    exit()
                elif btn["action"] == "tutorial":
                    game.state = "tutorial"
    elif game.state == "tutorial" and buttons[-1]["rect"].collidepoint(pos):
        game.state = "menu"
    elif game.state in ["win", "lose"]:
        game.state = "menu"


buttons = [
    {"rect": Rect(300, 200, 200, 50), "text": "Rozpocznij gre", "action": "start"},
    {"rect": Rect(300, 270, 200, 50), "text": "Przelacz muzyke", "action": "toggle_music"},
    {"rect": Rect(300, 340, 200, 50), "text": "Wyjscie", "action": "exit"},
    {"rect": Rect(300, 410, 200, 50), "text": "Jak grac", "action": "tutorial"},
    {"rect": Rect(300, 400, 200, 50), "text": "powrot do main menu", "action": "powrot"},
]

game = Game()
player = Player()
enemies = []
pgzrun.go()
