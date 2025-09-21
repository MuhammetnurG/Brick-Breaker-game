import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 15
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Game clock
clock = pygame.time.Clock()


class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = BALL_SIZE // 2
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                BALL_SIZE, BALL_SIZE)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Wall collision
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius:
            self.dy *= -1

        # Update rectangle position
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)


class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


def create_bricks():
    bricks = []
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE]

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
            bricks.append(Brick(brick_x, brick_y, colors[row]))

    return bricks


def show_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    score = 0
    lives = 3
    game_active = True
    game_won = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    # Reset game
                    paddle = Paddle()
                    ball = Ball()
                    bricks = create_bricks()
                    score = 0
                    lives = 3
                    game_active = True
                    game_won = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        # Fill the screen
        screen.fill(BLACK)

        # Draw game elements
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()

        # Display score and lives
        show_text(f"Score: {score}", 36, WHITE, 100, 30)
        show_text(f"Lives: {lives}", 36, WHITE, SCREEN_WIDTH - 100, 30)

        if game_active:
            # Move the ball
            ball.move()

            # Paddle collision
            if ball.rect.colliderect(paddle.rect) and ball.dy > 0:
                # Calculate bounce angle based on where ball hits paddle
                relative_x = (ball.x - paddle.x) / PADDLE_WIDTH
                angle = relative_x * 2 - 1  # -1 to 1
                ball.dx = angle * 5
                ball.dy *= -1

            # Brick collision
            brick_hit = False
            for brick in bricks:
                if brick.visible and ball.rect.colliderect(brick.rect):
                    brick.visible = False
                    ball.dy *= -1
                    score += 10
                    brick_hit = True
                    break

            # Check if all bricks are gone
            if all(not brick.visible for brick in bricks):
                game_active = False
                game_won = True

            # Ball out of bounds
            if ball.y > SCREEN_HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_active = False
                else:
                    ball.reset()
        else:
            # Game over or won screen
            if game_won:
                show_text("YOU WIN!", 72, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            else:
                show_text("GAME OVER", 72, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

            show_text("Press SPACE to play again", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()