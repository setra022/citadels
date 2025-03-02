from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle


class PongBall(Widget):
    velocity = Vector(3, 4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)  # Ensure ball has a size
        with self.canvas:
            self.color = Color(1, 0, 0, 1)  # Red color
            self.ball = Ellipse(pos=self.pos, size=self.size)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.ball.pos = self.pos  # Update ellipse position

        # Bounce off top and bottom walls
        if self.top >= self.parent.height or self.y <= 0:
            self.velocity.y *= -1  # Reverse Y direction


class PongPaddle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (10, 100)  # Paddle size
        with self.canvas:
            self.color = Color(0, 0, 1, 1)  # Blue paddles
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):  # Check for collision
            ball.velocity.x *= -1  # Reverse ball direction

    def on_pos(self, *args):
        self.rect.pos = self.pos  # Update paddle position


class PongGame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create paddles and ball
        self.ball = PongBall()
        self.paddle_left = PongPaddle()
        self.paddle_right = PongPaddle()

        # Add them to the game
        self.add_widget(self.ball)
        self.add_widget(self.paddle_left)
        self.add_widget(self.paddle_right)

        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS

    def on_size(self, *args):
        # Place the ball in the center
        self.ball.pos = (self.width / 2 - self.ball.width / 2, self.height / 2 - self.ball.height / 2)
        
        # Position paddles on the left and right
        self.paddle_left.pos = (10, self.height / 2 - self.paddle_left.height / 2)
        self.paddle_right.pos = (self.width - 20, self.height / 2 - self.paddle_right.height / 2)

    def update(self, dt):
        self.ball.move()

        # Check for paddle collisions
        self.paddle_left.bounce_ball(self.ball)
        self.paddle_right.bounce_ball(self.ball)


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
