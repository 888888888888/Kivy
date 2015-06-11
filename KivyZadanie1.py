__author__ = 'Crejzer'

#!/usr/bin/kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

#klasa obslugujaca suwaki do odbijania pileczki
class PongPaddle(Widget):
    score = NumericProperty(0)

    #algorytm odbijania pileczki
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            #kat odbicia pileczki
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            #kierunek
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            #aktualizacjia wspolrzednych pileczki
            ball.velocity = vel.x, vel.y + offset

#klasa obslugujaca pileczke
class PongBall(Widget):

    #wspolrzedne pileczki
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    #metoda aktualizujaca pozycje
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    #obiekty na ktorych bedziemy uzywac danych metod (opcjonalne)
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    #metoda wprawiajaca w ruch pileczke
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    #metoda symulujaca ruch pileczki i jej odbijanie
    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    #metoda obslugujaca ruszanie suwakami
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

#klasa uruchamjajaca nasza gre
class PongApp(App):
    def build(self):
        game = PongGame()
        #puszczenie pileczki w ruch
        game.serve_ball()
        #aktualizacja naszej gry, pozycji pileczki, odbijania (60 razy na sekunede )
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()