import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Light Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
ROAD_COLOR = (50, 50, 50)  # Dark gray for roads
LINE_COLOR = (255, 255, 255)  # White lines for lanes
CAR_COLOR = (0, 255, 255)  # Cyan for cars
TRUCK_COLOR = (255, 165, 0)  # Orange for trucks
BUS_COLOR = (255, 0, 255)  # Magenta for buses

# Light positions
LIGHT_RADIUS = 20
lights = {
    "NW": (200, 200),
    "NE": (600, 200),
    "SE": (600, 600),
    "SW": (200, 600),
}

# Vehicle properties
VEHICLE_TYPES = ["car", "truck", "bus"]
VEHICLE_COLORS = {"car": CAR_COLOR, "truck": TRUCK_COLOR, "bus": BUS_COLOR}
VEHICLE_SIZES = {"car": (20, 10), "truck": (30, 15), "bus": (25, 20)}
VEHICLE_SPEEDS = {"car": 3, "truck": 2, "bus": 2.5}
vehicles = []

# Traffic light cases
cases = [
    {"NW": "R", "NE": "R", "SE": "R", "SW": "GS"},  # Case 1: SW green
    {"NW": "R", "NE": "GS", "SE": "R", "SW": "R"},  # Case 2: NE green
    {"NW": "R", "NE": "R", "SE": "GS", "SW": "R"},  # Case 3: SE green
    {"NW": "GS", "NE": "R", "SE": "R", "SW": "R"},  # Case 4: NW green
]

# Font setup
font = pygame.font.SysFont('Arial', 30)

# Timing
CASE_DURATION = 5  # Time in seconds for each case
last_case_change = time.time()
last_spawn_time = time.time()

# Sound effects
pygame.mixer.init()
horn_sound = pygame.mixer.Sound("horn.wav")  # Replace with your sound file
light_change_sound = pygame.mixer.Sound("light_change.wav")  # Replace with your sound file

def draw_light(position, state):
    """
    Draw the light at the given position based on the state.
    'R' for Red, 'GS' for Green Straight, 'GR' for Green Right, '-' for no light.
    """
    color = GRAY  # Default no light color
    if state == "R":
        color = RED
    elif state == "GS" or state == "GR":
        color = GREEN

    pygame.draw.circle(screen, color, position, LIGHT_RADIUS)

def draw_roads():
    """
    Draw basic road paths with lanes.
    """
    # Horizontal road
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT // 3, WIDTH, HEIGHT // 3))
    # Vertical road
    pygame.draw.rect(screen, ROAD_COLOR, (WIDTH // 3, 0, WIDTH // 3, HEIGHT))

    # Road lines
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)  # Vertical line
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 5)  # Horizontal line

def display_case_number(case_num):
    """
    Display the current case number on the screen.
    """
    text = font.render(f"Case {case_num + 1}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

def draw_traffic_lights(case):
    """
    Draw all traffic lights based on the current case configuration.
    """
    for light, position in lights.items():
        state = case[light]
        draw_light(position, state)

def spawn_vehicle():
    """
    Spawn a vehicle at a random edge of the screen.
    """
    vehicle_type = random.choice(VEHICLE_TYPES)
    direction = random.choice(["up", "down", "left", "right"])
    if direction == "up":
        pos = [random.randint(WIDTH // 3, 2 * WIDTH // 3 - VEHICLE_SIZES[vehicle_type][0]), HEIGHT]
    elif direction == "down":
        pos = [random.randint(WIDTH // 3, 2 * WIDTH // 3 - VEHICLE_SIZES[vehicle_type][0]), -VEHICLE_SIZES[vehicle_type][1]]
    elif direction == "left":
        pos = [WIDTH, random.randint(HEIGHT // 3, 2 * HEIGHT // 3 - VEHICLE_SIZES[vehicle_type][1])]
    elif direction == "right":
        pos = [-VEHICLE_SIZES[vehicle_type][0], random.randint(HEIGHT // 3, 2 * HEIGHT // 3 - VEHICLE_SIZES[vehicle_type][1])]
    vehicles.append({"pos": pos, "direction": direction, "type": vehicle_type})

def draw_vehicles():
    """
    Draw all vehicles on the roads.
    """
    for vehicle in vehicles:
        x, y = vehicle["pos"]
        vehicle_type = vehicle["type"]
        color = VEHICLE_COLORS[vehicle_type]
        width, height = VEHICLE_SIZES[vehicle_type]
        pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

def update_vehicles(case):
    """
    Update vehicle positions based on traffic light rules.
    """
    for vehicle in vehicles:
        x, y = vehicle["pos"]
        direction = vehicle["direction"]
        vehicle_type = vehicle["type"]
        speed = VEHICLE_SPEEDS[vehicle_type]

        # Check if the vehicle is at an intersection
        at_intersection = (WIDTH // 3 <= x <= 2 * WIDTH // 3) and (HEIGHT // 3 <= y <= 2 * HEIGHT // 3)

        if at_intersection:
            # Determine the traffic light state for the vehicle's direction
            if direction == "up":
                light_state = case["SW"]
            elif direction == "down":
                light_state = case["NE"]
            elif direction == "left":
                light_state = case["SE"]
            elif direction == "right":
                light_state = case["NW"]

            # Stop if the light is red
            if light_state == "R":
                continue

        # Move the vehicle based on its direction
        if direction == "up":
            vehicle["pos"][1] -= speed
        elif direction == "down":
            vehicle["pos"][1] += speed
        elif direction == "left":
            vehicle["pos"][0] -= speed
        elif direction == "right":
            vehicle["pos"][0] += speed

        # Remove vehicles that go off-screen
        if x < -VEHICLE_SIZES[vehicle_type][0] or x > WIDTH or y < -VEHICLE_SIZES[vehicle_type][1] or y > HEIGHT:
            vehicles.remove(vehicle)

def main():
    case_index = 0  # Start with the first case
    running = True
    clock = pygame.time.Clock()
    last_spawn_time = time.time()

    while running:
        screen.fill(BLACK)

        # Draw roads
        draw_roads()

        # Display current case number
        display_case_number(case_index)

        # Draw the lights based on the case
        draw_traffic_lights(cases[case_index])

        # Spawn vehicles randomly
        if time.time() - last_spawn_time > 1:  # Spawn a vehicle every second
            spawn_vehicle()
            last_spawn_time = time.time()

        # Draw vehicles on the road
        draw_vehicles()

        # Update vehicle positions based on the current case
        update_vehicles(cases[case_index])

        pygame.display.flip()

        # Automatically change cases after a set duration
        if time.time() - last_case_change > CASE_DURATION:
            case_index = (case_index + 1) % len(cases)
            last_case_change = time.time()
            light_change_sound.play()  # Play sound when traffic lights change

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()