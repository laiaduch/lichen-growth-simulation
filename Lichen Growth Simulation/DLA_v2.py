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
alpha = 10**-4 # Adjust as needed
sigma = 0.3 # Adjust as needed
tau = 3  # Adjust as needed

# Distances
init_distance = 2 * particle_radius + epsilon
walk_distance = particle_radius
ro = 2.5 * particle_radius
#ro = 2.5
kill_distance = 10 * ro

class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.attached = False  # Added a flag to track attachment

def init_particle(particles):
    chosen_particle = random.choice(particles)
    angle = random.uniform(0, 2*math.pi)
    new_position = (chosen_particle.position[0] + init_distance * math.cos(angle),
                    chosen_particle.position[1] + init_distance * math.sin(angle))
    angle = random.uniform(0, 2 * math.pi)
    return Particle(new_position, pygame.Vector2(math.cos(angle), math.sin(angle)))

def compute_aggregation_probability(n):
    return alpha + (1 - alpha) * math.exp(-sigma * ((n - tau) ** 2))
    #return 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    particles = [Particle((width // 2, height // 2), pygame.Vector2(0, -1))]
    current_particle = init_particle(particles)
    particle_count = 0

    for i in range(0,10):
        print(i, compute_aggregation_probability(i))


    while particle_count < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Move the particle randomly
        angle = random.uniform(0, 2*math.pi)
        new_direction = pygame.Vector2(math.cos(angle), math.sin(angle))

        # Calculate the new position for the current particle based on the random direction and walk distance
        new_position = (current_particle.position[0] + new_direction.x * walk_distance,
                       current_particle.position[1] + new_direction.y * walk_distance)

        # Check if the particle is too far from any attached particle
        too_far = True
        for p in particles:
            distance_to_attached = pygame.Vector2(new_position).distance_to(p.position)
            if distance_to_attached < kill_distance:
                too_far = False
                break

        if too_far:
            current_particle = init_particle(particles)
            continue  # Skip this iteration and get a new random direction

        current_particle.position = (new_position[0], new_position[1])

        n = 0
        for p in particles:
            if pygame.Vector2(current_particle.position).distance_to(p.position) < ro:
                n += 1

        aggregation_probability = compute_aggregation_probability(n)
        if random.random() < aggregation_probability:
            particles.append(current_particle)
            print(n)
            particle_count += 1
            #current_particle.attached = True
            current_particle = init_particle(particles)


        screen.fill(background_color)

        for particle in particles:
            pygame.draw.circle(screen, attached_color, (int(particle.position[0]), int(particle.position[1])),
                                particle_radius)

        pygame.draw.circle(screen, moving_color, (int(current_particle.position[0]), int(current_particle.position[1])),
                            particle_radius)

        pygame.display.flip()
        #pygame.time.delay(10)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                waiting = False

if __name__ == "__main__":
    main()
