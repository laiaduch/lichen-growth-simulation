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
sigma = 0.3  # Adjust as needed
tau = 1  # Adjust as needed

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


def compute_aggregation_probability(current_particle, neighboring_particles, image):
    # Check if the position is within the image bounds
    if 0 <= int(current_particle.position[0]) < width and 0 <= int(current_particle.position[1]) < height:
        # Get grayscale value from the entire image
        pixel_value = image.get_at((int(current_particle.position[0]), int(current_particle.position[1])))
        pixel_value = pixel_value.r / 255.0  # Normalize to a range between 0 and 1

        close_particles = [p for p in neighboring_particles if pygame.Vector2(current_particle.position).distance_to(
            p.position) < 2 * particle_radius + epsilon]

        n = len(close_particles)
        aggregation_probability = alpha + (1 - alpha) * math.exp(-sigma * ((n - tau) ** 2))

        # Multiply by the grayscale probability
        return aggregation_probability * pixel_value
    else:
        return 0  # Return 0 probability if position is out of bounds


def find_seed_position(image):
    max_probability = 0
    seed_position = None

    for _ in range(1000):  # Try 1000 random positions
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        current_particle = Particle((x, y), pygame.Vector2(0, -1))
        current_probability = compute_aggregation_probability(current_particle, [], image)

        if current_probability > max_probability:
            max_probability = current_probability
            seed_position = (x, y)

    return seed_position


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    # Load background image and scale it to fit the screen
    background_image = pygame.image.load('./images/gradient.png')
    background_image = pygame.transform.scale(background_image, (width, height))

    # Find the seed position with the highest probability
    seed_position = find_seed_position(background_image)
    particles = [Particle(seed_position, pygame.Vector2(0, -1))]
    particle_count = 1

    while particle_count < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current_particle = particles[-1]
        angle = random.uniform(0, 360)
        new_direction = current_particle.direction.rotate(angle)

        random_attached_particle = random.choice(particles)
        new_position = (random_attached_particle.position[0] + new_direction.x * walk_distance,
                        random_attached_particle.position[1] + new_direction.y * walk_distance)

        # Check if the particle is too far from the attached particle
        distance_to_attached = pygame.Vector2(new_position).distance_to(random_attached_particle.position)
        if distance_to_attached > kill_distance:
            particles.pop(-1)  # Remove the particle from the list
            break  # Skip this iteration and get a new random direction

        #current_particle.position = new_position
        current_particle.position = (new_position[0] + init_distance, new_position[1] + init_distance)


        if random.random() < compute_aggregation_probability(current_particle, particles, background_image):
            new_particle = Particle(current_particle.position, pygame.Vector2(0, -1))
            particles.append(new_particle)
            particle_count += 1

            current_particle.attached = True

        # Draw the background image
        screen.blit(background_image, (0, 0))

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
