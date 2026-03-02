import random, pygame

WIDTH =  800
HEIGHT = 800
RADIUS = 200
RADIUS_SQ = RADIUS * RADIUS
V0 = 2
FORCE = 0.15


class Particle:
    def __init__(self, window) -> None:
        self.pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        self.vel = [random.randint(-V0, V0), random.randint(-V0, V0)]
        self.window = window
        self.state = "prey"
        self.hunger = 500
        self.eaten_prey = 0
        self.age = 0
        self.max_age = random.randint(600, 1000)
        self.initial_hunger = 500

    def dist_sq(self, p2):
        """Compute squared distance between this particle and another."""
        dx = self.pos[0] - p2.pos[0]
        dy = self.pos[1] - p2.pos[1]
        return dx * dx + dy * dy
    
    def is_colliding(self, p2, r=5):
        """Return True if this particle is physically colliding with another."""
        return self.dist_sq(p2) <= (2 * r) ** 2
    
    def draw_particle(self):
        """Draw the particle circle."""
        color = "blue"
        if self.state == "predator":
            color = "red"
        elif self.state == "normal":
            color = "white"
        else:
            color = "blue"

        pygame.draw.circle(self.window, color, self.pos, 5)

    def draw_line(self, p2):
        """Draw a line between this particle and another."""
        pygame.draw.line(self.window, "white", self.pos, p2.pos)

    def localiza_vizinhos(self, p2, only_predator=False):
        """Connect nearby particles within the configured radius."""
        if self.dist_sq(p2) > RADIUS_SQ:
            return
        
        if only_predator:
            if self.state == "predator" and p2.state == "predator":
                self.draw_line(p2)
        else:
            self.draw_line(p2)

    def move(self):
        """Move the particle and handle wall collisions."""
        if self.state != "normal":
            self.vel[0] *= 0.98
            self.vel[1] *= 0.98
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            if self.pos[0] <= 0 or self.pos[0] >= WIDTH:
                self.pos[0] = max(0, min(WIDTH, self.pos[0]))
                self.vel[0] *= -1
            if self.pos[1] <= 0 or self.pos[1] >= HEIGHT:
                self.pos[1] = max(0, min(HEIGHT, self.pos[1]))
                self.vel[1] *= -1
        else:
            self.vel[0] = 0
            self.vel[1] = 0
        if self.state == "predator" and self.hunger <=0:
            self.state = "normal"
        
            

    def detect_colision(self, p2, r=5):
        """Detect and resolve elastic collision with another particle."""
        dx = self.pos[0] - p2.pos[0]
        dy = self.pos[1] - p2.pos[1]
        min_dist = 2 * r
        dist_sq = dx * dx + dy * dy
        if dist_sq > min_dist * min_dist:
            return

        if dist_sq == 0:
            dx = random.choice((-1, 1))
            dy = random.choice((-1, 1))
            dist_sq = dx * dx + dy * dy

        dist = dist_sq ** 0.5
        nx = dx / dist
        ny = dy / dist

        # Separate overlapping particles
        overlap = min_dist - dist
        if overlap > 0:
            self.pos[0] += nx * (overlap / 2)
            self.pos[1] += ny * (overlap / 2)
            p2.pos[0] -= nx * (overlap / 2)
            p2.pos[1] -= ny * (overlap / 2)

        # Elastic collision response
        rvx = self.vel[0] - p2.vel[0]
        rvy = self.vel[1] - p2.vel[1]
        if rvx * nx + rvy * ny >= 0:
            return

        tx = -ny
        ty = nx

        v1n = self.vel[0] * nx + self.vel[1] * ny
        v1t = self.vel[0] * tx + self.vel[1] * ty
        v2n = p2.vel[0] * nx + p2.vel[1] * ny
        v2t = p2.vel[0] * tx + p2.vel[1] * ty

        self.vel[0] = v2n * nx + v1t * tx
        self.vel[1] = v2n * ny + v1t * ty
        p2.vel[0] = v1n * nx + v2t * tx
        p2.vel[1] = v1n * ny + v2t * ty


    def hunger_decrease(self, prey_count):
        if self.state == "predator":
            rate = 1 if prey_count > 20 else 0.4
            self.hunger -= rate

    def hunger_increase(self):
        if self.state == "predator":
            self.hunger = min(self.hunger + self.initial_hunger, self.initial_hunger * 2)

    def _apply_force(self, dx, dy):
        dist = (dx * dx + dy * dy) ** 0.5
        if dist > 0:
            self.vel[0] += FORCE * dx / dist
            self.vel[1] += FORCE * dy / dist
            speed = (self.vel[0] ** 2 + self.vel[1] ** 2) ** 0.5
            if speed > V0:
                self.vel[0] = V0 * self.vel[0] / speed
                self.vel[1] = V0 * self.vel[1] / speed

    def wander(self):
        if self.state == "predator":
            self._apply_force(random.uniform(-1, 1), random.uniform(-1, 1))

    def flock(self, target):
        if self.state == "prey":
            self._apply_force(target.pos[0] - self.pos[0], target.pos[1] - self.pos[1])

    def move_towards(self, target):
        if self.state == "predator":
            self._apply_force(target.pos[0] - self.pos[0], target.pos[1] - self.pos[1])

    def move_away(self, target):
        if self.state == "prey":
            self._apply_force(self.pos[0] - target.pos[0], self.pos[1] - target.pos[1])

    def move_towards_grass(self, grass_pos):
        if self.state == "prey":
            self._apply_force(grass_pos[0] - self.pos[0], grass_pos[1] - self.pos[1])
        