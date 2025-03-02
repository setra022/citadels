from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = Vector(4, 0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)  # Set a visible size
        with self.canvas:
            self.color = Color(1, 0, 0, 1)  # Red color
            self.ball = Ellipse(pos=self.pos, size=self.size)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.ball.pos = self.pos  # Update position


class PongGame(Widget):
    def update(self, dt):
        print(f"Ball position: {self.ball.pos}, size: {self.ball.size}")
        self.ball.move()

    def on_touch_down(self, touch):
        self.ball.velocity = Vector(4, 0).rotate(45)  # Start the ball movement


class PongApp(App):
    def build(self):
        game = PongGame()
        game.ball = PongBall()
        game.add_widget(game.ball)
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # Run the game loop
        return game


if __name__ == '__main__':
    PongApp().run()
