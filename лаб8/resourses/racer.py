import pygame
import random
import time


pygame.init() # initializes all the pygame sub-modules


WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Road Runner Game")

# image loading
image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')
image_coin = pygame.image.load('resources/Coin.png')

image_coin = pygame.transform.scale(image_coin, (50, 50))  # transform image coin by 50x50 pixels

# music loading
pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)
sound_crash = pygame.mixer.Sound('resources/crash.wav')
sound_coin = pygame.mixer.Sound('resources/coin.mp3')

# font and text
font_large = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
image_game_over = font_large.render("Game Over", True, "black")


FPS = 60
clock = pygame.time.Clock()


WHITE = (255, 255, 255)


# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50)) # center of the screen
        self.speed = 5

    def move(self):
        #player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)


# enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = random.randint(5, 10) # random speed between 5 and 10
        self.reset_position()

    def reset_position(self):
        # enemy reset position
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.reset_position()


# coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # coin reset position
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-200, -50)

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > HEIGHT:
            self.reset_position()


# "Game Over" function 
def show_game_over():
    screen.fill("red")
    screen.blit(image_game_over, (WIDTH // 2 - image_game_over.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.mixer.music.stop()

    # wait for player pressed space
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


# score
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# main code
def main():
    # create sprites
    player = Player()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    # create 1 enemy 
    for _ in range(1):
        enemy = Enemy()
        enemies.add(enemy)

    # create coin 
    for _ in range(2):
        coin = Coin()
        coins.add(coin)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, *enemies, *coins)

    score = 0
    coin_count = 0
    speed_increase_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.move() # function move player

        # update sprites 
        for entity in all_sprites:
            entity.move()

        # crach detection
        if pygame.sprite.spritecollideany(player, enemies):
            sound_crash.play()
            show_game_over()
            return

        # coin check
        coins_collected = pygame.sprite.spritecollide(player, coins, True)
        for _ in coins_collected:
            sound_coin.play()
            coin_count += 1
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        # speed facter every 10 sec
        speed_increase_timer += 1
        if speed_increase_timer >= FPS * 10:
            for enemy in enemies:
                enemy.speed += 1
            speed_increase_timer = 0

        # background and all sprites
        screen.blit(image_background, (0, 0))
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # show score and coin count
        draw_text(f"Score: {coin_count * 10}", font_small, WHITE, 10, 10)
        draw_text(f"Coins: {coin_count}", font_small, WHITE, WIDTH - 100, 10)

        
        pygame.display.flip()
        clock.tick(FPS) #sets the FPS

    pygame.quit()


if __name__ == "__main__":
    main()