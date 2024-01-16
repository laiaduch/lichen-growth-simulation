# This is a failed DLA implementation for lichen growth

import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Window configuration
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Open DLA Lichen Growth")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Algorithm parameters
seed_position = (width // 2, height // 2)
particle_radius = 1
max_particles = 5000

# Array to save the positions
particles = [seed_position]

def draw_particles():
    for particle in particles:
        pygame.draw.circle(window, white, particle, particle_radius)

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if len(particles) < max_particles:
            # Generate a new random particle
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(particle_radius * 2, particle_radius * 4)
            new_particle = (
                int(seed_position[0] + distance * math.cos(angle)),
                int(seed_position[1] + distance * math.sin(angle))
            )

            # Verify if the new particle is in contact with an existent cluster
            for existing_particle in particles:
                if math.dist(new_particle, existing_particle) < particle_radius * 2:
                    particles.append(new_particle)
                    break  # Loop exit when the particle is aggregated

        window.fill(black)
        draw_particles()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()