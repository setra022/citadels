from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse


class PongBall(Widget):
    velocity = Vector(2, 4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)  # Ensure ball has a size
        with self.canvas:
            self.color = Color(1, 0, 0, 1)  # Red color
            self.ball = Ellipse(pos=self.pos, size=self.size)

    def move(self):
        # Move the widget
        self.pos = Vector(*self.velocity) + self.pos
        self.ball.pos = self.pos  # Update ellipse position

        # Bounce off top and bottom walls
        if self.top >= self.parent.height or self.y <= 0:
            self.velocity.y *= -1  # Reverse Y direction

        # Bounce off left and right walls
        if self.right >= self.parent.width or self.x <= 0:
            self.velocity.x *= -1  # Reverse X direction


class PongGame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ball = PongBall()
        self.add_widget(self.ball)
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS

    def on_size(self, *args):
        # Place the ball in the center when window is resized
        self.ball.pos = (self.width / 2 - self.ball.width / 2, self.height / 2 - self.ball.height / 2)

    def update(self, dt):
        self.ball.move()


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
