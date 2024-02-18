import pygame
import random
import math

# Constants
width = 800
height = 600
background_color = (27, 30, 32)
moving_color = (255, 0, 0)  # New color for moving particle
attached_color = (255, 255, 255)   # Color for attached particles
particle_radius = 1
epsilon = particle_radius / 2
walk_distance = 1  # Adjust as needed
alpha = 1  # Adjust as needed
sigma = 3  # Adjust as needed
tau = 0.6  # Adjust as needed
desired_particles = 600


class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.attached = False  # Added a flag to track attachment


def compute_aggregation_probability(current_particle, neighboring_particles):
    close_particles = [p for p in neighboring_particles if pygame.Vector2(current_particle.position).distance_to(
        p.position) < 2 * particle_radius + epsilon]

    n = len(close_particles)
    return alpha + (1 - alpha) * math.exp(-(sigma * (n - tau)) ** 2)

def generate_new_particle(current_particle, neighboring_particles):
    while True:
        angle = random.uniform(0, 360)
        distance = 2 * particle_radius + epsilon
        new_position = (
            current_particle.position[0] + math.cos(math.radians(angle)) * distance,
            current_particle.position[1] + math.sin(math.radians(angle)) * distance
        )

        if all(pygame.Vector2(new_position).distance_to(p.position) >= distance for p in neighboring_particles):
            return Particle(new_position, pygame.Vector2(0, -1))
def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    particles = [Particle((width / 2, height / 2), pygame.Vector2(0, -1))]
    particle_count = 1

    while particle_count < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current_particle = particles[-1]
        new_particle = generate_new_particle(current_particle, particles)

        current_particle.position = new_particle.position

        if random.random() < compute_aggregation_probability(current_particle, particles):
            particles.append(new_particle)
            particle_count += 1

        screen.fill(background_color)
        for particle in particles:
            if particle.attached:
                pygame.draw.circle(screen, attached_color, (int(particle.position[0]), int(particle.position[1])),
                                   particle_radius)
            else:
                pygame.draw.circle(screen, moving_color, (int(particle.position[0]), int(particle.position[1])),
                                   particle_radius)

        pygame.display.flip()
        pygame.time.delay(10)

        # Check for attachment and update color
        for particle in particles[:-1]:
            if pygame.Vector2(current_particle.position).distance_to(particle.position) < particle_radius * 2 + epsilon:
                current_particle.attached = True

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                waiting = False


if __name__ == "__main__":
    main()
