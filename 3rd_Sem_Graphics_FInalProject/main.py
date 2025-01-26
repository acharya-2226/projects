import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 60, 30
ZOMBIE_SIZE = 50  # Scale up by 3 times
POWERUP_SIZE = 30  # Scale up by 3 times
LANES = [100, 200, 300, 400, 500]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# Load background image
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load car images
car_images = [pygame.transform.scale(pygame.image.load(f'car{i}.png'), (CAR_WIDTH, CAR_HEIGHT)) for i in range(1, 7)]

# Load zombie image
zombie_image = pygame.transform.scale(pygame.image.load('zombie.png'), (ZOMBIE_SIZE, ZOMBIE_SIZE))

# Load power-up image
powerup_image = pygame.transform.scale(pygame.image.load('powerup.png'), (POWERUP_SIZE, POWERUP_SIZE))

# Create game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Crossing Zombie")

# Clock to control frame rate
clock = pygame.time.Clock()

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = zombie_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, speed):
        super().__init__()
        self.image = random.choice(car_images)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = lane
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = powerup_image.copy()
        if type == "health":
            self.image.fill(CYAN, special_flags=pygame.BLEND_ADD)
        elif type == "speed":
            self.image.fill(YELLOW, special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()

def check_collisions(zombie, vehicles, powerups):
    if pygame.sprite.spritecollide(zombie, vehicles, False):
        return True
    for powerup in powerups:
        if pygame.sprite.collide_rect(zombie, powerup):
            powerup.kill()
            return powerup.type
    return None

def display_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def main():
    zombie = Zombie()
    all_sprites = pygame.sprite.Group(zombie)
    vehicles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    score = 0
    level = 1
    vehicle_spawn_rate = 0.02
    powerup_spawn_rate = 0.01

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        zombie.update(keys)

        # Add vehicles and power-ups dynamically
        if random.random() < vehicle_spawn_rate:
            lane = random.choice(LANES)
            speed = random.randint(3 + level, 6 + level)
            vehicle = Vehicle(lane, speed)
            vehicles.add(vehicle)
            all_sprites.add(vehicle)

        if random.random() < powerup_spawn_rate:
            x = random.randint(0, WIDTH - POWERUP_SIZE)
            powerup = PowerUp(x, 0, random.choice(["health", "speed"]))
            powerups.add(powerup)
            all_sprites.add(powerup)

        # Update vehicles and power-ups
        vehicles.update()
        powerups.update()

        # Check collisions
        collision_result = check_collisions(zombie, vehicles, powerups)
        if collision_result == True:
            display_text("Game Over!", 64, RED, WIDTH // 2 - 150, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
        elif collision_result == "health":
            score += 10
        elif collision_result == "speed":
            zombie.speed += 2

        # Increase difficulty with score
        if score // 50 > level - 1:
            level += 1
            vehicle_spawn_rate += 0.005

        # Draw all sprites
        all_sprites.draw(screen)

        # Display score and level
        display_text(f"Score: {score}", 36, BLACK, 10, 10)
        display_text(f"Level: {level}", 36, BLACK, 10, 50)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
