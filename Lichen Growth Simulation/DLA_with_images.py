import pygame
import random
import math

# Constants
width = 384
height = 384
background_color = (0, 0, 0) #(27, 30, 32)
moving_color = (255, 0, 0)  # New color for moving particle
attached_color = (255, 255, 255)   # Color for attached particles   (13, 128, 128)

# Parameters
desired_particles = 1000
particle_radius = 2
epsilon = particle_radius/2
alpha = 10**-4  # Adjust as needed
sigma = 0.3  # Adjust as needed
tau = 1.5 # Adjust as needed

# Distances
init_distance = 2 * particle_radius + epsilon #2
walk_distance = particle_radius/2
ro = 2.5 * particle_radius
kill_distance = 10 * ro

positions = []

class Particle:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


def init_particle(particles, cluster_radius):
    global positions
    positions = []

    #chosen_particle = random.choice(particles)
    chosen_particle = particles[0]

    angle = random.uniform(0, 2*math.pi)
    new_position = (chosen_particle.position[0] + cluster_radius * math.cos(angle),
                    chosen_particle.position[1] + cluster_radius * math.sin(angle))
    new_angle = random.uniform(0, 2 * math.pi)


    return Particle(new_position, pygame.Vector2(math.cos(new_angle), math.sin(new_angle)))


def compute_aggregation_probability(n, intensity):
    return (alpha + (1 - alpha) * math.exp(-sigma * ((n - tau) ** 2))) * intensity


def find_seed_position(image):
    max_probability = 0
    seed_position = None

    for _ in range(1000):  # Try 1000 random positions
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # current_particle = Particle((x, y), pygame.Vector2(0, -1))
        current_probability = compute_aggregation_probability(0, image.get_at((x, y))[0] / 255)

        if current_probability > max_probability:
            max_probability = current_probability
            seed_position = (x, y)

    return seed_position


def main():
    global positions

    cluster_radius = particle_radius

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Open DLA Lichen Simulation")

    # Load background image and probability map image and scale it to fit the screen
    probability_image = pygame.image.load('./images/probability_map/probability_map_teulada1_S.png')
    probability_image = pygame.transform.scale(probability_image, (width, height))

    #background_image = pygame.image.load('./images/textures/teulada1.jpg')
    #background_image = pygame.transform.scale(background_image, (probability_image.get_width(), probability_image.get_height()))

    # Find the seed position with the highest probability
    seed_position = find_seed_position(probability_image)
    particles = [Particle(seed_position, pygame.Vector2(0, -1))]
    #particles = [Particle((2/3 * width, height // 2), pygame.Vector2(0, -1))]


    # Initialize the current particle
    current_particle = init_particle(particles, cluster_radius)


    while len(particles) < desired_particles:
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
            current_particle = init_particle(particles, cluster_radius)
            continue  # Skip this iteration and get a new random direction

        #positions.append(current_particle.position)
        #current_particle.position = (new_position[0], new_position[1])

        # Check if new position is within the screen bounds
        if (0 <= new_position[0] < width) and (0 <= new_position[1] < height):
            positions.append(current_particle.position)
            current_particle.position = new_position
        else:
            current_particle = init_particle(particles, cluster_radius)
            continue

        # Check if the particle is in contact with any attached particle
        in_contact = False
        for p in particles:
            distance_to_attached = pygame.Vector2(new_position).distance_to(p.position)
            if distance_to_attached < 2 * particle_radius:
                in_contact = True
                break

        if in_contact:
            # Get the number of neighborhood particles
            n = 0
            for p in particles:
                if pygame.Vector2(current_particle.position).distance_to(p.position) < ro:
                    n += 1

            # Get pixel intensity at particle position
            pixel_intensity = probability_image.get_at((int(current_particle.position[0]), int(current_particle.position[1]))).r / 255

            aggregation_probability = compute_aggregation_probability(n, pixel_intensity)
            if random.random() < aggregation_probability:
                particles.append(current_particle)
                current_particle = init_particle(particles, cluster_radius)
                distance_to_center = pygame.Vector2(particles[-1].position).distance_to(particles[0].position)
                cluster_radius = max(cluster_radius, distance_to_center)
        else:
            current_particle.position = (new_position[0], new_position[1])

        # Draw the background image
        #screen.blit(probability_image, (0, 0))
        screen.fill(background_color)

        for particle in particles:
            pygame.draw.circle(screen, attached_color, (int(particle.position[0]), int(particle.position[1])),
                               particle_radius)

        pygame.draw.circle(screen, moving_color, (int(current_particle.position[0]), int(current_particle.position[1])),
                           particle_radius)


        # Draw the walk of particle before been aggregated
        #if len(positions) >= 2:
         #   pygame.draw.lines(screen, (255, 255, 255), False, positions)

        pygame.display.flip()

    # Save the final screen as a PNG image
    pygame.image.save(screen, "simulation_result.png")

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                waiting = False


if __name__ == "__main__":
    main()
