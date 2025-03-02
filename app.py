from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse


class PongBall(Widget):
    velocity = Vector(2, 4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)  # Ensure the ball has a size
        with self.canvas:
            self.color = Color(1, 0, 0, 1)  # Red color
            self.ball = Ellipse(pos=self.pos, size=self.size)

    def move(self):
        # Move the widget
        self.pos = Vector(*self.velocity) + self.pos
        self.ball.pos = self.pos  # Update the ellipse position

        # Check for collision with top and bottom walls
        if self.top >= self.parent.height or self.y <= 0:
            self.velocity.y *= -1  # Reverse direction on Y-axis


class PongGame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ball = PongBall(pos=self.center)  # Start ball in the center
        self.add_widget(self.ball)
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS

    def update(self, dt):
        self.ball.move()


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
