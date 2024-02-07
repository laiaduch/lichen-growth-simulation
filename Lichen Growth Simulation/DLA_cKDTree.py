import pygame
import random
import math
from scipy.spatial import cKDTree

# Constants
width = 800
height = 600
background_color = (27, 30, 32)
particle_color = (255, 255, 255)
particle_radius = 1
epsilon = particle_radius / 2
walk_distance = 5
alpha = 0.1  # Adjust as needed
sigma = 0.01  # Adjust as needed
tau = 3  # Adjust as needed
desired_particles = 1000


class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


def compute_aggregation_probability(current_particle, neighboring_particles):
    # Filter particles that are close to the current_particle
    close_particles = [p for p in neighboring_particles if pygame.Vector2(current_particle.position).distance_to(
        p.position) < 2 * particle_radius + epsilon]

    n = len(close_particles)
    return alpha + (1 - alpha) * math.exp(-(sigma * (n - tau)) ** 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    # Initialize with a seed particle
    particles = [Particle((width / 2, height / 2), pygame.Vector2(0, -1))]  # Starting with an upward direction
    particle_positions = [p.position for p in particles]
    kdtree = cKDTree(particle_positions)
    particle_count = 1

    while particle_count < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Move the current particle in a random direction
        current_particle = particles[-1]
        angle = random.uniform(0, 360)
        new_direction = current_particle.direction.rotate(angle)

        # Move the particle
        current_particle.position = (
            current_particle.position[0] + new_direction.x * walk_distance,
            current_particle.position[1] + new_direction.y * walk_distance
        )

        # Use cKDTree to find neighboring particles
        neighboring_indices = kdtree.query_ball_point(current_particle.position, 2 * particle_radius + epsilon)
        neighboring_particles = [particles[i] for i in neighboring_indices]

        # Add new particle to the cluster
        if random.random() < compute_aggregation_probability(current_particle, neighboring_particles):
            # Create a new particle at the current position with a random direction
            new_particle = Particle(current_particle.position, pygame.Vector2(0, -1))

            # Check for aggregation with existing particles
            if any(pygame.Vector2(new_particle.position).distance_to(p.position) < particle_radius * 2 + epsilon for p
                   in neighboring_particles):
                particles.append(new_particle)
                kdtree = cKDTree(particle_positions)  # Update cKDTree with the new particle position
                particle_count += 1

        # Draw particles
        screen.fill(background_color)
        for particle in particles:
            pygame.draw.circle(screen, particle_color, (int(particle.position[0]), int(particle.position[1])),
                               particle_radius)

        pygame.display.flip()
        pygame.time.delay(10)

    # Wait for a key press before quitting
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                waiting = False

if __name__ == "__main__":
    main()
