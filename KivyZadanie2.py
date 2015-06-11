from kivy.uix.button import Button

__author__ = 'Crejzer'
#!/usr/bin/kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty,NumericProperty, ReferenceListProperty, Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.vector import Vector

#przeszkoda ktora nalezy unikac w naszej grze
class Przeszkoda(Widget):

    #klasa wykrywajaca kolizje z electronem
    def koniecgry(self, electron):
        if electron.y >= self.y - 30:
            electron.canvas.clear()


#Klasa obslugujaca elektron
class Electron(Widget):

    #wspolrzedne electronu
    wspolrzedna_x = NumericProperty(0)
    wspolrzedna_y = NumericProperty(0)
    polorzenie = ReferenceListProperty(wspolrzedna_x, wspolrzedna_y)

    #metoda aktualizujaca pozycje
    def move(self):
        self.pos = Vector(*self.polorzenie) + self.pos

    #metda sprawdzajaca czy nastapila kolizja z przeszkoda
    def koniecgry(self, przeszkoda):
        if self.collide_widget(przeszkoda):
            self.canvas.clear()


#pierwsze okno naszej aplikacji (Menu)
class Menu(Screen):

    #stringi uzywane do stworzenia menu
    nazwaGry = StringProperty("ElectronParty");
    opis = StringProperty("Pomoz elektornowi dojsc na impreze!")
    start = StringProperty("Start Game")

class Level1(Screen):
    #stringi uzywane do stworzenia levelu
    nextLevel = StringProperty("Next Level")
    level1 = StringProperty("Level 1")
    opis1 = StringProperty("Nie pozwol aby elektron wpadl na szare pole lub biale pole!")
    restart = StringProperty("Restart")

    #metody dodajace do przycisku mozliwosc resetowania poziomu
    #niestety nie dziala
    """
    def rysuj (self):
        self.electron.canvas.draw()

    def resetet(self):
        self.reset.bind(on_press=self.rysuj)
    """

    #wlaczanie zegara do wykrywania kolizji
    def start(self):
        Clock.schedule_interval(self.update, 1.0/60.0)

    #wylaczanie zegara
    def stop(self):
        Clock.unschedule(self.update)

    #przemieszczanie sie obiektu za kursorem
    def on_touch_move(self, touch):
        #wlaczam zegar aby sprawdzic kolizje
        self.start()
        #self.resetet()
        if touch.y:
            self.electron.y = touch.y - 30/2
        if touch.x:
            self.electron.x = touch.x - 30/2

    #wylaczam zegar aby mozliwe bylo przemieszczanie sie miedzy levelami
    def on_touch_up(self, touch):
        self.stop()

    #sprawdzanie czy nie nastapila kolizja
    def update(self, dt):
        self.electron.koniecgry(self.button1)
        self.przeszkoda.koniecgry(self.electron)


#nastepny level
class Level2(Screen):
    autor = StringProperty("Wykonal Krystian Kedron")
    dopiska = StringProperty("Wiecej leveli wkrotce :)")

#klasa do oblugiwania ekranow
class ScreenManager(ScreenManager):
    pass

#uruchamiania naszej aplikacji przez plik .kv poniewaz tam obslugiwane jest przelaczanie sie miedzy levelami
game = Builder.load_file("electronParty.kv")

#Klasa uruchamiajasa nasza gre
class ElectronPartyApp(App):
    def build(self):
        return game;

#uruchamianie naszej gry
if __name__ == '__main__':
    ElectronPartyApp().run()

