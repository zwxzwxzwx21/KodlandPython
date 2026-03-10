import pgzrun

class Game:
    def __init__(self):
        self.music_play = True
        self.music_pos = 0
        self.volume = 0.05
        music.set_volume(self.volume)
        music.play('music')

game = Game()

WIDTH = 800
HEIGHT = 600

def draw():
    screen.fill((128, 0, 0))

def toggle_music():
    if game.music_play:
        game.music_play = False
        game.music_pos = music.get_pos() / 1000
        music.pause()
    else:
        game.music_play = True
        music.unpause()

def on_key_down(key):
    if key == keys.SPACE:
        toggle_music()

pgzrun.go()


"""

Wyjątek: MOŻESZ użyć klasy Rect z PyGame.

Roguelike 

menu główne, z następującymi przyciskami:
Rozpocznij grę
Przełącz muzykę Wyłączoną/Włączoną
Wyjście

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


"""