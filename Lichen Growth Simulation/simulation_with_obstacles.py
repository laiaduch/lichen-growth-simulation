import pygame
import random
import math

class Simulation:
    def __init__(self):
        self.size = self.width, self.height = 640, 480
        self.startX, self.startY = round(self.width/2), round(self.height/2)
        self.X, self.Y = self.startX, self.startY

        self.minX, self.minY = self.X, self.Y
        self.maxX, self.maxY = self.X, self.Y
        self.padSize = 50

        self.domainMinX = self.startX - self.padSize
        self.domainMaxX = self.startX + self.padSize
        self.domainMinY = self.startY - self.padSize
        self.domainMaxY = self.startY + self.padSize

        self.lichenColor = 0xFFFFFF

        self.displaySurface = None
        self.pixelArray = None
        self.updateFlag = False

        self.obstacleColor = (173, 216, 230)  # Color for obstacles
        self.obstacles = []  # Array to save obstacles

    def init(self):
        pygame.init()
        pygame.display.set_caption("Lichen Growth with Obstacles")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.pixelArray = pygame.PixelArray(self.displaySurface)
        self.isRunning = True

        # Set a seed point
        self.pixelArray[self.startX, self.startY + 10] = self.lichenColor

        # Create some obstacles randomly (rectangles, triangles, and polygons)
        for _ in range(10):
            if random.choice([True, False]):  # Randomly choose between rectangle, triangle, and polygon
                obstacle_rect = pygame.Rect(
                    random.randint(self.domainMinX, self.domainMaxX - 20),
                    random.randint(self.domainMinY, self.domainMaxY - 20),
                    20,
                    20)
                if self.distance_to_start(obstacle_rect.center) > 30:
                    self.obstacles.append(obstacle_rect)
                    pygame.draw.rect(self.displaySurface, self.obstacleColor, obstacle_rect)
            else:
                if random.choice([True, False]):  # Randomly choose between triangle and polygon
                    side_length = 20
                    x = random.randint(self.domainMinX, self.domainMaxX - side_length)
                    y = random.randint(self.domainMinY, self.domainMaxY - side_length)
                    obstacle_shape = [
                        (x, y),
                        (x + side_length, y),
                        (x + side_length / 2, y - math.sqrt(3) / 2 * side_length)
                    ]
                else:
                    num_sides = random.randint(5, 9)  # Random number of sides for the polygon
                    radius = 15
                    center = (
                    random.randint(self.domainMinX, self.domainMaxX), random.randint(self.domainMinY, self.domainMaxY))
                    angle = 2 * math.pi / num_sides
                    obstacle_shape = [
                        (center[0] + int(radius * math.cos(i * angle)), center[1] + int(radius * math.sin(i * angle)))
                        for i in range(num_sides)
                    ]

                    if self.distance_to_start(center) > 30:
                        self.obstacles.append(obstacle_shape)
                        pygame.draw.polygon(self.displaySurface, self.obstacleColor, obstacle_shape)
        pygame.display.update()

    def distance_to_start(self, point): # Let the lichen start to growth
        return math.sqrt((self.startX - point[0]) ** 2 + (self.startY - point[1]) ** 2)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def check_collision(self, x, y):
        # Check if the coordinates (x, y) are inside any obstacle
        for obstacle in self.obstacles:
            if isinstance(obstacle, pygame.Rect):
                if obstacle.collidepoint(x, y):
                    return True
            elif isinstance(obstacle, list):
                if pygame.draw.polygon(self.displaySurface, self.obstacleColor, obstacle).collidepoint(x, y):
                    return True
        return False

    def on_loop(self):
        # Random direction in which to move
        newDir = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)))

        # Extract dx and dy
        dX, dY = newDir
        newX = self.X + dX  # Apply dx and dy to the coordinates
        newY = self.Y + dY

        # Check if the new coordinates are inside the domain
        if(newX < self.domainMinX):
            newX = self.domainMaxX

        if(newX > self.domainMaxX):
            newX = self.domainMinX

        if (newY < self.domainMinY):
            newY = self.domainMaxY

        if (newY > self.domainMaxY):
            newY = self.domainMinY

        # check if the pixel has been already set
        if (self.pixelArray[newX, newY] == self.lichenColor):
            self.updateFlag = True

            # Modify the extent of the simulation domain
            if (self.X < self.minX):
                self.minX = self.X

            if (self.X > self.maxX):
                self.maxX = self.X

            if (self.Y < self.minY):
                self.minY = self.Y

            if (self.Y > self.maxY):
                self.maxY = self.Y

            # Modify the domain
            self.domainMinX = max(self.minX - self.padSize, 1)
            self.domainMaxX = min(self.maxX + self.padSize, self.width - 1)
            self.domainMinY = max(self.minY - self.padSize, 1)
            self.domainMaxY = min(self.maxY + self.padSize, self.height - 1)

        else:
            self.updateFlag = False
            self.X, self.Y = newX, newY

    def render(self):
        if self.updateFlag:
            # check if the new position is inside some obstacle
            if not self.check_collision(self.X, self.Y):
                # Update the pixel
                self.pixelArray[self.X, self.Y] = self.lichenColor

                # Update the display
                pygame.display.update()

            # Reset update
            self.updateFlag = False

            # Select one of the four sides of the domain to start from
            newSide = random.choice((1, 2, 3, 4))
            if (newSide == 1):
                self.X = self.domainMinX
                self.Y = int(random.uniform(self.domainMinY, self.domainMaxY))
            elif (newSide == 2):
                self.X = int(random.uniform(self.domainMinX, self.domainMaxX))
                self.Y = self.domainMinY
            elif (newSide == 3):
                self.X = self.domainMaxX
                self.Y = int(random.uniform(self.domainMinY, self.domainMaxY))
            else:
                self.X = int(random.uniform(self.domainMinX, self.domainMaxX))
                self.Y = self.domainMaxY

    def execute(self):
        if self.init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.render()
        pygame.quit()

if __name__ == "__main__":
    t = Simulation()
    t.execute()
