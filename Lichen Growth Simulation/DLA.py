import pygame
import random
import math

# Constants
width = 800
height = 600
background_color = (57, 60, 62)
particle_color = (255, 255, 255)
particle_radius = 1
epsilon = particle_radius / 2
walk_distance = 5
alpha = 0.1  # Adjust as needed
sigma = 0.01  # Adjust as needed
tau = 3    # Adjust as needed
desired_particles = 500

class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

def compute_aggregation_probability(neighboring_particles):
    n = len(neighboring_particles)
    return alpha + (1 - alpha) * math.exp(-(sigma * (n - tau))**2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    # Initialize with a seed particle
    particles = [Particle((width / 2, height / 2), pygame.Vector2(0, -1))]  # Starting with an upward direction
    particle_count = 1

    while particle_count < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Add new particle to the cluster
        if random.random() < compute_aggregation_probability(particles):
            random_particle = random.choice(particles)

            # Randomly rotate the current direction
            angle = random.uniform(-30, 30)  # Adjust angle as needed
            new_direction = random_particle.direction.rotate(angle)

            # Move the new particle
            new_particle_position = (
                random_particle.position[0] + new_direction.x * (2 * particle_radius + epsilon),
                random_particle.position[1] + new_direction.y * (2 * particle_radius + epsilon)
            )
            new_particle = Particle(new_particle_position, new_direction)

            # Check for aggregation with existing particles
            if any(pygame.Vector2(new_particle.position).distance_to(p.position) < particle_radius * 2 + epsilon for p in particles):
                particles.append(new_particle)
                particle_count += 1

        # Draw particles
        screen.fill(background_color)
        for particle in particles:
            pygame.draw.circle(screen, particle_color, (int(particle.position[0]), int(particle.position[1])), particle_radius)

        pygame.display.flip()
        pygame.time.delay(10)

    pygame.quit()

if __name__ == "__main__":
    main()
