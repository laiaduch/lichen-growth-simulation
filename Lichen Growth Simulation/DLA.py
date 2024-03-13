import pygame
import random
import math

# Constants
width = 800
height = 600
background_color = (27, 30, 32)
moving_color = (255, 0, 0)  # New color for moving particle
attached_color = (13, 128, 128)   # Color for attached particles

# Parameters
desired_particles = 1000
particle_radius = 2
epsilon = particle_radius/2
alpha = 10**-4  # Adjust as needed
sigma = 1  # Adjust as needed
tau = 0.5  # Adjust as needed

# Distances
init_distance = 2 * particle_radius + epsilon
walk_distance = 2 * particle_radius
ro = 2 * particle_radius
kill_distance = 3 * ro

class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.attached = False  # Added a flag to track attachment


def compute_aggregation_probability(current_particle, neighboring_particles):
    close_particles = []
    for p in neighboring_particles:
        if pygame.Vector2(current_particle.position).distance_to(p.position) < ro:
            close_particles.append(p)

    n = len(close_particles)
    return alpha + (1 - alpha) * math.exp(-sigma * ((n - tau) ** 2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    particles = [Particle((width // 2, height // 2), pygame.Vector2(0, -1))]
    particle_count = 1

    while particle_count < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Move the particle randomly
        current_particle = particles[-1]
        angle = random.uniform(0, 360)
        new_direction = current_particle.direction.rotate(angle)

        # Calculate the new position for the current particle based on the random direction and walk distance
        random_attached_particle = random.choice(particles)
        new_position = (random_attached_particle.position[0] + new_direction.x * walk_distance,
                        random_attached_particle.position[1] + new_direction.y * walk_distance)

        # Check if the particle is too far from the attached particle
        distance_to_attached = pygame.Vector2(new_position).distance_to(random_attached_particle.position)
        if distance_to_attached > kill_distance:
            particles.pop(-1)  # Remove the particle from the list
            continue  # Skip this iteration and get a new random direction

        current_particle.position = new_position

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
