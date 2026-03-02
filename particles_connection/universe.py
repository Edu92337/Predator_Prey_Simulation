import random, pygame
from particle import Particle

WIDTH =  800
HEIGHT = 800
RADIUS = 200
RADIUS_SQ = RADIUS * RADIUS
V0 = 2

class Universe:
    def __init__(self, window) -> None:
        self.particulas = []
        self.window = window
        # grass is a vector of particle os type grass, which is a tuple of (x, y) coordinates
        self.grass = []
        for _ in range(20):
            self.spawn_grass()

    def add(self, p):
        """Add a particle to the universe."""
        self.particulas.append(p)

    def remove(self, p):
        """Remove a particle from the universe."""
        self.particulas.remove(p)

    def count_prey(self):
        """Count the number of prey particles."""
        return len([p for p in self.particulas if p.state == "prey"])
    def count_predator(self):
        """Count the number of predator particles."""
        return len([p for p in self.particulas if p.state == "predator"])   

    def detect(self):
        n = len(self.particulas)
        parts = self.particulas
        to_remove = set()
        to_add = []
        grass_to_remove = set()
        prey_count = self.count_prey()

        for i in range(n):
            if i in to_remove:
                continue
            p1 = parts[i]
            for j in range(i + 1, n):
                if j in to_remove:
                    continue
                p2 = parts[j]

                p1.localiza_vizinhos(p2)
                p1.detect_colision(p2)

                if p1.is_colliding(p2):
                    if p1.state == "predator" and p2.state == "prey":
                        to_remove.add(j)
                        p1.hunger_increase()
                        p1.eaten_prey += 1

                    elif p1.state == "prey" and p2.state == "predator":
                        to_remove.add(i)
                        p2.hunger_increase()
                        p2.eaten_prey += 1

                    elif p1.state == "predator" and p2.state == "predator":
                        if p1.eaten_prey >= 1 and p2.eaten_prey >= 1:
                            self.create_predator(p1, to_add)
                            p1.eaten_prey = 0
                            self.create_predator(p2, to_add)
                            p2.eaten_prey = 0

                    elif (p1.state == "prey" and p2.state == "prey"
                            and (p1.eaten_prey >= 1 or p2.eaten_prey >= 1)
                    ):
                        self.create_prey(p1, to_add)

                elif p1.state == "predator" and p2.state == "prey" and p1.dist_sq(p2) <= RADIUS_SQ:
                    p1.move_towards(p2)
                    p2.move_away(p1)
                elif p2.state == "predator" and p1.state == "prey" and p2.dist_sq(p1) <= RADIUS_SQ:
                    p2.move_towards(p1)
                    p1.move_away(p2)

            # Hunger decreases each frame; predator dies when it reaches 0.
            if p1.state == "predator":
                p1.hunger_decrease(prey_count)
                if p1.hunger <= 0:
                    to_remove.add(i)
                prey_nearby = any(p.state == "prey" and p1.dist_sq(p) <= RADIUS_SQ for p in parts)
                if not prey_nearby:
                    if p1.eaten_prey >= 1:
                        closest_mate = None
                        closest_mate_dist_sq = float("inf")
                        for p in parts:
                            if p.state == "predator" and p is not p1 and p.eaten_prey >= 1:
                                d = p1.dist_sq(p)
                                if d < closest_mate_dist_sq:
                                    closest_mate_dist_sq = d
                                    closest_mate = p
                        if closest_mate:
                            p1.move_towards(closest_mate)
                        else:
                            p1.wander()
                    else:
                        p1.wander()

            p1.age += 1
            # no loop externo, junto com a lógica de idade
            if p1.state == "prey":
                neighbors = sum(1 for p in parts if p != p1 and p.state == "prey" and p1.dist_sq(p) <= RADIUS_SQ)
                if neighbors > 8 and random.random() < 0.05:
                    to_remove.add(i)
                    
                #move to the closest prey
                no_predator_nearby = not any(p.state == "predator" and p1.dist_sq(p) <= RADIUS_SQ for p in parts)
                no_grass_nearby = not self.grass or min((p1.pos[0]-g[0])**2 + (p1.pos[1]-g[1])**2 for g in self.grass) > RADIUS_SQ
                if no_predator_nearby and no_grass_nearby:
                    closest_prey = None
                    closest_dist_sq = float("inf")
                    for p in parts:
                        if p.state == "prey" and p != p1:
                            dist_sq = p1.dist_sq(p)
                            if dist_sq < closest_dist_sq:
                                closest_dist_sq = dist_sq
                                closest_prey = p
                    if closest_prey and closest_dist_sq <= RADIUS_SQ:
                        p1.flock(closest_prey)
                

                if self.grass:
                    closest_grass = min(self.grass, key=lambda g: (p1.pos[0] - g[0])**2 + (p1.pos[1] - g[1])**2)
                    no_predator_nearby = not any(p.state == "predator" and p1.dist_sq(p) <= RADIUS_SQ for p in parts)
                    if no_predator_nearby:
                        p1.move_towards_grass(closest_grass)
                    dx = p1.pos[0] - closest_grass[0]
                    dy = p1.pos[1] - closest_grass[1]
                    if dx * dx + dy * dy <= (2 * 5) ** 2:
                        grass_to_remove.add(closest_grass)
                        p1.eaten_prey += 1
                        p1.max_age += 150


            if p1.state == "prey" and p1.age >= p1.max_age:
                to_remove.add(i)

        self.particulas = [p for idx, p in enumerate(self.particulas) if idx not in to_remove]
        self.particulas.extend(to_add)
        for g in grass_to_remove:
            if g in self.grass:
                self.grass.remove(g)
        self.create_grass()

    def create_grass(self):
        """Randomly create grass on the field."""
        if random.random() < 0.05:  # 5% chance to create new grass each frame
            self.grass.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    
    def draw_grass(self):
        """Draw grass on the field."""
        for g in self.grass:
            pygame.draw.circle(self.window, "green", g, 3)

    

    def draw_universe(self):
        """Draw all particles and update their positions."""
        for p in self.particulas:
            p.draw_particle()
            p.move()
            self.count_predator()
            self.count_prey()

    def count_neighbors(self, particles):
        """Count the number of neighbors within the configured radius."""
        count = 0
        for p1 in particles:
            for p2 in particles:
                if p1 != p2 and p1.dist_sq(p2) <= RADIUS_SQ:
                    count += 1

        return count
    
    def create_prey(self, reference_particle, to_add):
        """Create a new prey particle near a reference particle."""
        new_prey = Particle(reference_particle.window)
        new_prey.state = "prey"
        to_add.append(new_prey)
        
    def create_predator(self, reference_particle, to_add):
        """Create a new predator particle near a reference particle."""
        new_predator = Particle(reference_particle.window)
        new_predator.state = "predator"
        to_add.append(new_predator)
    
    def spawn_grass(self):
        """Randomly spawn grass on the field."""
        self.grass.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))