import pygame
import random
import math
from PIL import Image

# Constants
width = 800
height = 600
background_color = (27, 30, 32)
moving_color = (255, 0, 0)  # New color for moving particle
attached_color = (13, 128, 128)   # Color for attached particles

# Parameters
desired_particles = 500
particle_radius = 2
epsilon = particle_radius/2
alpha = 10**-2 # Adjust as needed
sigma = 0.3 # Adjust as needed
tau = 1.5  # Adjust as needed

# Distances
init_distance = 2 * particle_radius + epsilon
walk_distance = particle_radius
ro = 2.5 * particle_radius
kill_distance = 10 * ro

class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

def init_particle(particles):
    chosen_particle = random.choice(particles)
    angle = random.uniform(0, 2*math.pi)
    new_position = (chosen_particle.position[0] + init_distance * math.cos(angle),
                    chosen_particle.position[1] + init_distance * math.sin(angle))

    # Check if new position is within the screen bounds
    new_position = (max(0, min(width - 1, new_position[0])),
                    max(0, min(height - 1, new_position[1])))

    new_angle = random.uniform(0, 2 * math.pi)
    return Particle(new_position, pygame.Vector2(math.cos(new_angle), math.sin(new_angle)))

def compute_aggregation_probability(n, intensity):
    # Modify the aggregation probability calculation based on pixel intensity
    return (alpha + (1 - alpha) * math.exp(-sigma * ((n - tau) ** 2))) * intensity

def load_image(path):
    image = Image.open(path)
    image = image.resize((width, height))  # Resize image to match canvas size
    return pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()

def find_seed_position(image):
    max_probability = 0
    seed_position = None

    for _ in range(1000):  # Try 1000 random positions
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        #current_particle = Particle((x, y), pygame.Vector2(0, -1))
        current_probability = compute_aggregation_probability(0, image.get_at((x, y))[0] / 255)

        if current_probability > max_probability:
            max_probability = current_probability
            seed_position = (x, y)

    return seed_position

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    # Load image
    background_image = load_image('./images/L.png')
    screen.blit(background_image, (0, 0))

    # Find seed position
    seed_position = find_seed_position(background_image)
    particles = [Particle(seed_position, pygame.Vector2(0, -1))]

    current_particle = init_particle(particles)

    while len(particles) < desired_particles:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        angle = random.uniform(0, 2*math.pi)
        new_direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        new_position = (current_particle.position[0] + new_direction.x * walk_distance,
                       current_particle.position[1] + new_direction.y * walk_distance)

        too_far = True
        for p in particles:
            distance_to_attached = pygame.Vector2(new_position).distance_to(p.position)
            if distance_to_attached < kill_distance:
                too_far = False
                break

        if too_far:
            current_particle = init_particle(particles)
            continue

        # current_particle.position = (new_position[0], new_position[1])
        # Check if new position is within the screen bounds
        if (0 <= new_position[0] < width) and (0 <= new_position[1] < height):
            current_particle.position = new_position
        else:
            current_particle = init_particle(particles)
            continue

        in_contact = False
        for p in particles:
            distance_to_attached = pygame.Vector2(new_position).distance_to(p.position)
            if distance_to_attached <= particle_radius:
                in_contact = True
                break

        if in_contact:
            n = 0
            for p in particles:
                if pygame.Vector2(current_particle.position).distance_to(p.position) < ro:
                    n += 1

            # Get pixel intensity at particle position
            pixel_intensity = background_image.get_at((int(current_particle.position[0]), int(current_particle.position[1]))).r / 255

            aggregation_probability = compute_aggregation_probability(n, pixel_intensity)
            if random.random() < aggregation_probability:
                particles.append(current_particle)
                current_particle = init_particle(particles)
        else:
            current_particle.position = (new_position[0], new_position[1])

        screen.blit(background_image, (0, 0))

        for particle in particles:
            pygame.draw.circle(screen, attached_color, (int(particle.position[0]), int(particle.position[1])),
                                particle_radius)

        pygame.draw.circle(screen, moving_color, (int(current_particle.position[0]), int(current_particle.position[1])),
                            particle_radius)

        pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                waiting = False

if __name__ == "__main__":
    main()
