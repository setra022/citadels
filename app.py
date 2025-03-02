from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse


class PongBall(Widget):
    velocity = Vector(4, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(1, 0, 0, 1)  # Red color
            self.ball = Ellipse(pos=self.pos, size=(50, 50))

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.ball.pos = self.pos  # Update position


class PongGame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ball = PongBall()
        self.add_widget(self.ball)

    def update(self, dt):
        print(f"Ball position: {self.ball.pos}, size: {self.ball.size}")
        self.ball.move()


class PongApp(App):
    def build(self):
        game = PongGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # Run the game loop
        return game


if __name__ == '__main__':
    PongApp().run()
