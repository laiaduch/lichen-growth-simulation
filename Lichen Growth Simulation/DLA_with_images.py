import pygame
import random
import math

# Constants
width = 800
height = 600
moving_color = (255, 0, 0)  # New color for moving particle
attached_color = (13, 128, 128)  # Color for attached particles

# Parameters
particle_radius = 2
epsilon = particle_radius / 2
walk_distance = 8  # Adjust as needed
alpha = 1  # Adjust as needed
sigma = 3  # Adjust as needed
tau = 0.6  # Adjust as needed
desired_particles = 1000



class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.attached = False  # Added a flag to track attachment


def compute_aggregation_probability(current_particle, neighboring_particles, image):
    close_particles = [p for p in neighboring_particles if pygame.Vector2(current_particle.position).distance_to(
        p.position) < 2 * particle_radius + epsilon]

    n = len(close_particles)
    aggregation_probability = alpha + (1 - alpha) * math.exp(-(sigma * (n - tau)) ** 2)

    # Get grayscale value from the entire image
    pixel_value = image.get_at((int(current_particle.position[0]), int(current_particle.position[1])))
    pixel_value = pixel_value.r / 255.0  # Normalize to a range between 0 and 1

    # Multiply by the grayscale probability
    return aggregation_probability * pixel_value


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    # Load background image and scale it to fit the screen
    background_image = pygame.image.load('./images/L.png')
    background_image = pygame.transform.scale(background_image, (width, height))

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

        # Compute aggregation probability considering the grayscale value of the entire image
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
