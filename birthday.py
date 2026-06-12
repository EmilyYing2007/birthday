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
    W     = 100
    SPEED = 6

    CATCH_ZONE_TOP    = 100
    CATCH_ZONE_HEIGHT = 20

    def __init__(self, screen_width, screen_height, sprites):
        self.sw      = screen_width
        self.sh      = screen_height
        self.sprites = sprites  # list of 4 sprites, each with their own height
        self.x       = screen_width // 2 - self.W // 2
        # position based on the tallest sprite so it doesn't jump around
        self.tallest = max(s.get_height() for s in sprites)
        self.y       = screen_height - self.tallest - 10

    def get_sprite(self, score):
        idx = min(score // 2, 4)
        return self.sprites[idx]

    def update(self, keys):
        if keys[pygame.K_LEFT]  and self.x > 0:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT] and self.x + self.W < self.sw:
            self.x += self.SPEED

    def draw(self, surface, score):
        sprite = self.get_sprite(score)
        # anchor to bottom so character feet stay in place as basket fills up
        draw_y = self.y + self.tallest - sprite.get_height()
        surface.blit(sprite, (self.x, draw_y))

    def get_catch_rect(self):
        return pygame.Rect(self.x, self.y + self.CATCH_ZONE_TOP, self.W, self.CATCH_ZONE_HEIGHT)


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    WIDTH, HEIGHT = 480, 640
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catch My Heart 💕")
    clock = pygame.time.Clock()

    BG_COLOR   = (255, 235, 245)
    TEXT_COLOR = (180, 60, 90)

    font_big   = pygame.font.SysFont("Georgia", 36, bold=True)
    font_small = pygame.font.SysFont("Georgia", 22)

    # Load all 4 sprites, scale by width and preserve each one's aspect ratio
    sprites = []
    for i in range(1, 6):
        raw = pygame.image.load(f"aaron{i}.PNG").convert_alpha()
        orig_w, orig_h = raw.get_size()
        scaled_h = int(orig_h * Catcher.W / orig_w)
        sprites.append(pygame.transform.scale(raw, (Catcher.W, scaled_h)))
        print(f"aaron{i}.PNG: original {orig_w}x{orig_h} → scaled {Catcher.W}x{scaled_h}")

    catch_sound = pygame.mixer.Sound("heart.wav")

    heart   = Heart(WIDTH, HEIGHT)
    catcher = Catcher(WIDTH, HEIGHT, sprites)

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

        if catcher.get_catch_rect().colliderect(heart.get_rect()):
            score += 1
            catch_sound.play()
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
        catcher.draw(screen, score)

        score_text  = font_small.render(f"Score: {score}",             True, TEXT_COLOR)
        missed_text = font_small.render(f"Missed: {missed}/{MAX_MISS}", True, TEXT_COLOR)
        screen.blit(score_text,  (12, 12))
        screen.blit(missed_text, (WIDTH - missed_text.get_width() - 12, 12))

        pygame.display.flip()


if __name__ == "__main__":
    main()