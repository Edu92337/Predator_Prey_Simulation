import pygame, particle, universe, random

WIDTH =  800
HEIGHT = 800
PREY0 = random.randint(50, 100)
PREDATOR0 = random.randint(10, 15)

def display_counts(window, uni):
    """Display the counts of prey and predators on the screen."""
    pygame.display.set_caption(f"Prey: {uni.count_prey()}  Predators: {uni.count_predator()}")

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    uni = universe.Universe(window)
    for i in range(PREY0):
        p = particle.Particle(window)
        p.state = "prey"
        uni.add(p)
    for i in range(PREDATOR0):
        p = particle.Particle(window)
        p.state = "predator"
        uni.add(p)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display_counts(window, uni)
        window.fill("black")
        uni.draw_universe()
        uni.draw_grass()
        uni.detect()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
