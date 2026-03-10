import pgzrun

alien = Actor("alien")
#alien.pos = 100, 56

WIDTH = 800
HEIGHT = 600
music.play('music')
music_pos = 0
music.set_volume(0.05)

def draw():
    screen.fill((128, 0, 0))
    alien.draw()

def on_key_down(key):
    if key == keys.SPACE:
        toggle_music()

def toggle_music():
    if music.is_playing:
        music_pos = music.get_pos() / 1000
        music.stop()
    else:
        music.play('music', start=music_pos)

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