import pygame
import random
import math

# Constants
width = 800
height = 600
background_color = (27, 30, 32)
moving_color = (255, 0, 0)  # New color for moving particle
attached_color = (255, 255, 255)   # Color for attached particles

# Parameters
particle_radius = 2
epsilon = particle_radius / 2
walk_distance = 8  # Adjust as needed
alpha = 1  # Adjust as needed
sigma = 3  # Adjust as needed
tau = 0.6  # Adjust as needed
desired_particles = 1000
d = 1

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
        angle = random.uniform(0, 360)
        new_direction = current_particle.direction.rotate(angle)

        # Find the particles fixed at a distance of 2*r+epsilon
        close_attached_particles = [p for p in particles if
                                    p.attached and pygame.Vector2(current_particle.position).distance_to(
                                        p.position) < 2 * particle_radius + epsilon]

        # If there are any fixed particles nearby, pick a random one and update the position
        if close_attached_particles:
            random_attached_particle = random.choice(close_attached_particles)
            current_particle.position = (
                random_attached_particle.position[0] + new_direction.x * walk_distance,
                random_attached_particle.position[1] + new_direction.y * walk_distance
            )

        if random.random() < compute_aggregation_probability(current_particle, particles):
            new_particle = Particle(current_particle.position, pygame.Vector2(0, -1))
            particles.append(new_particle)
            particle_count += 1

            current_particle.attached = True


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


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                waiting = False


if __name__ == "__main__":
    main()