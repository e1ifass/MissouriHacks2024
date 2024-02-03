import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Initialize variables
running = True
dt = 0
dots_eaten = 0
screen_fill_points = 0
current_dot_amount = 0

# Initial size of the ball
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_radius = 40  

# Generate dots with closer proximity
dots = [pygame.Vector2(random.randint(100, screen.get_width() - 100), random.randint(100, screen.get_height() - 100)) for _ in range(15)]

# Generate dangerous black dots
small_dots = [pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())) for _ in range(5)]

# Colors for circle and background
circle_colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan", "brown", "white"]
background_colors = ["blue", "darkorange", "darkmagenta", "darkgreen", "darkred", "black", "darkviolet", "darkcyan", "darkgoldenrod", "black"]
current_color_index = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with the current background color
    screen.fill(background_colors[current_color_index])

    # Move the dots
    for i in range(len(dots)):
        dots[i].x += random.uniform(-1, 1) * 100 * dt
        dots[i].y += random.uniform(-1, 1) * 100 * dt

    # Move the black dots
    for i in range(len(small_dots)):
        small_dots[i].x += random.uniform(-1, 1) * 150 * dt
        small_dots[i].y += random.uniform(-1, 1) * 150 * dt

        # Draw the black dots
        pygame.draw.circle(screen, "black", (int(small_dots[i].x), int(small_dots[i].y)), 3)

        # Check for collisions with the main ball and reset its size
        if player_pos.distance_to(small_dots[i]) < player_radius + 3:
            player_radius = 40
            current_dot_amount = 0

    # Draw random dots
    for dot_pos in dots:
        pygame.draw.circle(screen, "white", (int(dot_pos.x), int(dot_pos.y)), 5)

    # Check for collisions and eat dots
    for dot_pos in dots.copy():
        distance = player_pos.distance_to(dot_pos)
        if distance < player_radius + 5:  # Adjust this value based on the desired collision radius
            dots.remove(dot_pos)
            dots_eaten += 1
            current_dot_amount += 1

            # Grow the ball when eating a dot
            player_radius += 3

            # Check if the ball dot amt reaches the target
            if current_dot_amount == 50:
                screen_fill_points += 1
                current_dot_amount = 0
                player_radius = 40

            # Change colors every 10 dots
            if dots_eaten % 10 == 0:
                current_color_index = (current_color_index + 1) % len(circle_colors)

            # Generate a new dot at a random position with closer proximity
            new_dot_pos = pygame.Vector2(random.randint(100, screen.get_width() - 100), random.randint(100, screen.get_height() - 100))
            dots.append(new_dot_pos)

    # Draw the moving circle with the current color and size
    pygame.draw.circle(screen, circle_colors[current_color_index], (int(player_pos.x), int(player_pos.y)), player_radius)

    # Draw the dots eaten counter at the top right
    counter_text = font.render(f"Dots Eaten: {dots_eaten}", True, (255, 255, 255))
    screen.blit(counter_text, (screen.get_width() - counter_text.get_width() - 10, 10))

    # Draw the ball dot amt
    
    counter_text = font.render(f"Ball Dot Amount: {current_dot_amount}", True, (255, 255, 255))
    screen.blit(counter_text, (screen.get_width() - counter_text.get_width() - 10, 50))

    # Draw the screen fill points counter at the top middle
    screen_fill_text = font.render(f"Points (eat 50 dots): {screen_fill_points}", True, (255, 255, 255))
    screen.blit(screen_fill_text, ((screen.get_width() - screen_fill_text.get_width()) // 2, 10))

    # Draw the title at the top left
    title_text = font.render("Dont eat the black dots!", True, (255, 255, 255))
    screen.blit(title_text, (10, 10))

    # Draw warning sign if the background is black
    if background_colors[current_color_index] == "black":
        warning_text = font.render("WARNING: Black Background", True, (255, 0, 0))
        screen.blit(warning_text, ((screen.get_width() - warning_text.get_width()) // 2, screen.get_height() - 
    warning_text.get_height() - 10))

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
