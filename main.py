import pygame

window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

player_x = 400 - 24  # nejdřív 400, pak - 24 aby bylo uprostřed
player_y = 700 - 24
player_image = pygame.transform.scale(  # nejdřív ukázat že je to malý
    pygame.image.load("invaders/player.png"), (48, 48)
)
invader_images = [
    pygame.transform.scale(pygame.image.load("invaders/invader_1.png"), (48, 48)),
    pygame.transform.scale(pygame.image.load("invaders/invader_2.png"), (48, 48)),
    pygame.transform.scale(pygame.image.load("invaders/invader_3.png"), (48, 48)),
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        window.fill((0, 0, 0))
        window.blit(player_image, (player_x, player_y))
        pygame.display.flip()
        clock.tick(60)
