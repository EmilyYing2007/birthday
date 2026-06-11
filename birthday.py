import pygame
import random
import sys

def quit_game():
    pygame.quit()
    sys.exit()

def draw_heart(surface, color, cx, cy, size=20):
    r = size // 2
    pygame.draw.circle(surface, color, (cx - r // 2, cy - r // 4), r // 2)
    pygame.draw.circle(surface, color, (cx + r // 2, cy - r // 4), r // 2)
    points = [
        (cx - r, cy - r // 4),
        (cx + r, cy - r // 4),
        (cx,     cy + r),
    ]
    pygame.draw.polygon(surface, color, points)


class Heart:
    SIZE = 22

    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.reset()

    def reset(self):
        self.x     = random.randint(self.SIZE, self.width - self.SIZE)
        self.y     = -self.SIZE
        self.speed = random.uniform(2.5, 4.5)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        draw_heart(surface, (255, 80, 120), self.x, int(self.y), self.SIZE)

    def is_off_screen(self):
        return self.y > self.height + self.SIZE

    def get_rect(self):
        s = self.SIZE
        return pygame.Rect(self.x - s, self.y - s, s * 2, s * 2)


class Catcher:
    W     = 90
    H     = 18
    SPEED = 6

    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.x  = screen_width  // 2 - self.W // 2
        self.y  = screen_height - 60

    def update(self, keys):
        if keys[pygame.K_LEFT]  and self.x > 0:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT] and self.x + self.W < self.sw:
            self.x += self.SPEED

    def draw(self, surface):
        r = self.get_rect()
        pygame.draw.ellipse(surface, (255, 140, 170), r)
        pygame.draw.ellipse(surface, (255, 80, 120),  r, 3)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.W, self.H)


def main():
    pygame.init()

    WIDTH, HEIGHT = 480, 640
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catch My Heart")
    clock = pygame.time.Clock()

    BG_COLOR   = (255, 235, 245)
    TEXT_COLOR = (180, 60, 90)

    font_big   = pygame.font.SysFont("Georgia", 36, bold=True)
    font_small = pygame.font.SysFont("Georgia", 22)

    heart   = Heart(WIDTH, HEIGHT)
    catcher = Catcher(WIDTH, HEIGHT)

    score    = 0
    missed   = 0
    MAX_MISS = 5

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_game()

        keys = pygame.key.get_pressed()
        catcher.update(keys)
        heart.update()

        if catcher.get_rect().colliderect(heart.get_rect()):
            score += 1
            heart.reset()

        if heart.is_off_screen():
            missed += 1
            heart.reset()

        # Game over screen
        if missed >= MAX_MISS:
            screen.fill(BG_COLOR)
            m1 = font_big.render("Game Over!", True, TEXT_COLOR)
            m2 = font_small.render(f"You caught {score} hearts!", True, TEXT_COLOR)
            m3 = font_small.render("Press ESC to quit", True, TEXT_COLOR)
            screen.blit(m1, m1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            screen.blit(m2, m2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
            screen.blit(m3, m3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
            pygame.display.flip()
            clock.tick(60)
            continue

        # Draw
        screen.fill(BG_COLOR)
        heart.draw(screen)
        catcher.draw(screen)

        score_text  = font_small.render(f"Score: {score}",        True, TEXT_COLOR)
        missed_text = font_small.render(f"Missed: {missed}/{MAX_MISS}", True, TEXT_COLOR)
        screen.blit(score_text,  (12, 12))
        screen.blit(missed_text, (WIDTH - missed_text.get_width() - 12, 12))

        pygame.display.flip()


if __name__ == "__main__":
    main()