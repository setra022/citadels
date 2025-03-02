from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window


class PongBall(Widget):
    velocity = Vector(4, 4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)  # Set ball size
        with self.canvas:
            self.color = Color(1, 0, 0, 1)  # Red ball
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
            
            # 🔹 Push the ball slightly away to prevent multiple collisions
            if ball.velocity.x > 0:
                ball.x = self.right + 1  # Move ball right (if hitting left paddle)
            else:
                ball.x = self.x - ball.width - 1  # Move ball left (if hitting right paddle)

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

        # Track pressed keys
        self.pressed_keys = set()
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS

    def on_size(self, *args):
        # Place the ball in the center
        self.ball.pos = (self.width / 2 - self.ball.width / 2, self.height / 2 - self.ball.height / 2)
        
        # Position paddles on the left and right
        self.paddle_left.pos = (10, self.height / 2 - self.paddle_left.height / 2)
        self.paddle_right.pos = (self.width - 20, self.height / 2 - self.paddle_right.height / 2)

    def on_key_down(self, window, key, *args):
        self.pressed_keys.add(key)

    def on_key_up(self, window, key, *args):
        self.pressed_keys.discard(key)

    def move_paddles(self, dt):
        step = 10  # Paddle movement speed

        # Move Player 1 (Left Paddle) - Z (up) & S (down)
        if 122 in self.pressed_keys:  # 'z' key
            self.paddle_left.y = min(self.height - self.paddle_left.height, self.paddle_left.y + step)
        if 115 in self.pressed_keys:  # 's' key
            self.paddle_left.y = max(0, self.paddle_left.y - step)

        # Move Player 2 (Right Paddle) - Up & Down arrows
        if 273 in self.pressed_keys:  # Up arrow
            self.paddle_right.y = min(self.height - self.paddle_right.height, self.paddle_right.y + step)
        if 274 in self.pressed_keys:  # Down arrow
            self.paddle_right.y = max(0, self.paddle_right.y - step)

    def update(self, dt):
        self.ball.move()

        # Move paddles
        self.move_paddles(dt)

        # Check for paddle collisions
        self.paddle_left.bounce_ball(self.ball)
        self.paddle_right.bounce_ball(self.ball)


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
