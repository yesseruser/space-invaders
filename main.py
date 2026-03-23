import pygame

# 1. hráč
# 2. pohyb hráče
# 3. invadeři
# 4. pohyb invaderů
# 5. střílení
# 6. game over / victory

window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

movement_speed = 8

player_x = 400 - 24  # nejdřív 400, pak - 24 aby bylo uprostřed obrazovky (po scale)
player_y = 700 - 24
player_velocity_x = 0
player_image = pygame.transform.scale(  # nejdřív ukázat že je to malý
    pygame.image.load("invaders/player.png"), (48, 48)
)

invader_images = [
    pygame.transform.scale(pygame.image.load("invaders/invader_1.png"), (48, 48)),
    pygame.transform.scale(pygame.image.load("invaders/invader_2.png"), (48, 48)),
    pygame.transform.scale(pygame.image.load("invaders/invader_3.png"), (48, 48)),
]

invaders = []
# [health, x, y]

invader_block_x = 8
invader_block_y = 16

invader_velocity_x = 4

invader_count_x = 6
invader_count_y = 3

game_over_invader_y = player_y - 24

is_game_won = False
is_game_over = False

bullets = []
# [x, y]
bullet_speed = 12


def generate_invaders():
    for y in range(invader_count_y):
        for x in range(invader_count_x):
            invaders.append([3 - y, x * (48 + 8), y * (48 + 8)])  # 8 na rozestupy


def get_invader_block_size():
    max_x = 0
    max_y = 0
    for invader in invaders:
        if invader[1] > max_x:
            max_x = invader[1]
        if invader[2] > max_y:
            max_y = invader[2]
    return (max_x + 48, max_y + 48)


# Uvnitř = 0
# Vlevo = 1
# Vpravo = 2
# Nahoře = 3
# Dole = 4
def is_out_of_screen(x, y, size):
    if x < 0:
        return 1
    if x + size > 800:
        return 2
    if y < 0:
        return 3
    if y + size > 800:
        return 4
    return 0


generate_invaders()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_RIGHT:
                player_velocity_x = movement_speed
            if event.key == pygame.K_LEFT:
                player_velocity_x = -movement_speed
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + 24, player_y])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_velocity_x = 0

    if not is_game_over:
        # Hráč
        player_x += player_velocity_x
        direction = is_out_of_screen(player_x, player_y, 48)
        if direction == 1:
            player_x = 0
        elif direction == 2:
            player_x = 800 - 48

        # Invadeři
        invader_block_x += invader_velocity_x
        direction = is_out_of_screen(
            invader_block_x - 8, invader_block_y, get_invader_block_size()[0] + 16
        )
        # 8 a 16 (= 8 + 8) abychom měli odestup od okraje obrazovky (jako při spawnu)
        if direction == 1 or direction == 2:
            invader_block_y += 24
            invader_velocity_x = -invader_velocity_x

        if invader_block_y + get_invader_block_size()[1] - 24 >= game_over_invader_y:
            is_game_over = True

    window.fill((0, 0, 0))

    window.blit(player_image, (player_x, player_y))

    for invader in invaders:
        window.blit(
            invader_images[invader[0] - 1],
            (invader_block_x + invader[1], invader_block_y + invader[2]),
        )

    # Kulky
    for bullet in bullets:
        pygame.draw.line(
            window,
            (255, 255, 0),
            (bullet[0], bullet[1]),
            (bullet[0], bullet[1] - 24),
            4,
        )
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    pygame.draw.line(
        window, (255, 255, 255), (0, game_over_invader_y), (800, game_over_invader_y), 4
    )

    pygame.display.flip()
    clock.tick(60)
