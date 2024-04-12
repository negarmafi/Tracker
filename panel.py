import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import messagebox
import random
from datetime import datetime
import pygame
from PIL import Image, ImageTk

def plot_map(ax, map_array, circles, selected_circle_index):
    ax.clear()
    ax.imshow(map_array, cmap='binary', interpolation='nearest')
    ax.set_xlim(0, len(map_array[0]) - 1)
    ax.set_ylim(0, len(map_array) - 1)
    ax.axis('off')
    ax.invert_yaxis()
    for i, circle in enumerate(circles):
        color = 'r' if i in selected_circle_index else 'b'
        ax.plot(circle[1], circle[0], 'o', color=color)

def generate_random_circles(map_array, num_circles):
    circles = []
    for _ in range(num_circles):
        x, y = random.randint(0, len(map_array)-1), random.randint(0, len(map_array[0])-1)
        if map_array[x][y] == 1:
            circles.append((x, y))
    return circles

def move_circles(circles, map_array):
    new_circles = []
    for circle in circles:
        x, y = circle
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        new_x, new_y = x, y
        while (new_x == x and new_y == y) or not (0 <= new_x < len(map_array) and 0 <= new_y < len(map_array[0])) or \
                map_array[new_x][new_y] == 0:
            direction = random.choice(directions)
            new_x, new_y = x + direction[0], y + direction[1]
        new_circles.append((new_x, new_y))
    return new_circles

def main():
    root = tk.Tk()
    root.title("OPAL PROJECT")
    root.geometry("10000x10000")
    root.configure(bg="peachpuff3")
    root.attributes('-fullscreen', True)  # Make the window full screen

    # Your code for generating map and setting up matplotlib canvas

    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    def close_application():
        pygame.quit()  # Quit pygame properly
        root.destroy()  # Close the Tkinter window

    # Add a close button at the top-right of the window
    close_button = tk.Button(root, text="X", command=close_application, font=("Arial", 12), fg="black", bg="white",
                             borderwidth=0)
    close_button.place(relx=1.0, rely=0.0, x=-2, y=2, anchor="ne")

    # Load the image
    try:
        image_path = "C:/Users/LOOP/Downloads/MAP.png"
        image = pygame.image.load(image_path)
        print("Image loaded successfully!")
        # Process your image here
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image from {image_path}: {str(e)}")
        return  # Stop the function if image fails to load
    image = pygame.image.load("C:/Users/LOOP/Downloads/MAP.png")
    original_width, original_height = image.get_size()
    resized_width, resized_height = original_width // 3 * 2, original_height // 3 * 2
    image = pygame.transform.scale(image, (resized_width, resized_height))


    # Set up the screen
    pygame_screen = pygame.Surface((resized_width, resized_height))

    # Set up the colors
    RED = (255, 0, 0)
    EDENEF = (237, 237, 239)

    # Find all #EDENEF pixels in the image
    ededef_pixels = []
    for y in range(resized_height):
        for x in range(resized_width):
            if image.get_at((x, y)) == EDENEF:
                ededef_pixels.append((x, y))

    # Movement variables
    square_size = 5
    squares = []
    num_squares = random.randint(5, 100)  # Choose a random number of squares between 5 and 100
    for _ in range(num_squares):
        start_x, start_y = random.choice(ededef_pixels)
        squares.append(pygame.Rect(start_x, start_y, square_size, square_size))

    # Create a frame for the map image with a red border
    map_frame = tk.Frame(root, highlightthickness=5, highlightbackground="deepskyblue")
    map_frame.grid(row=0, column=0, padx=10, pady=10)

    # Convert the Pygame surface to a PIL Image
    pygame_image = pygame.surfarray.array3d(pygame_screen)
    pygame_image = np.swapaxes(pygame_image, 0, 1)
    pygame_image = np.flip(pygame_image, 0)
    pil_image = Image.fromarray(pygame_image)

    # Convert the PIL Image to a Tkinter PhotoImage
    tk_image = ImageTk.PhotoImage(pil_image)

    # Display the image on a Tkinter Label inside the frame
    map_label = tk.Label(map_frame, image=tk_image)
    map_label.pack(padx=10, pady=10)

    timer_label = tk.Label(root, text="Time: 08:00:00", font=("Palatino Linotype", 16), bg="darkslategray3")
    timer_label.grid(row=1, column=0, padx=10, pady=10)

    # Day label
    day_label = tk.Label(root, text="Day: Saturday", font=("Palatino Linotype", 16), bg="lightskyblue")
    day_label.grid(row=2, column=0, padx=10, pady=10)

    # Initialize timer and day count
    timer_value = 8 * 3600  # Initial timer value (8:00:00)
    current_day = 5  # Saturday (0: Monday, 1: Tuesday, ..., 5: Saturday)

    # Horizontal slider to adjust speed
    def change_speed(value):
        global timer_speed
        coefficient = int(value) / 1000
        timer_speed = int(1000 / coefficient)  # Update timer speed based on slider value
        speed_label.config(text=f"Speed: {coefficient:.1f}x")

    speed_scale = tk.Scale(root, from_=500, to=20000, orient=tk.HORIZONTAL, resolution=100, length=300,
                           label="Speed:", command=change_speed)
    speed_scale.set(1000)  # Default speed: 1x
    speed_scale.grid(row=3, column=0, padx=10, pady=10)

    speed_label = tk.Label(root, text=f"Speed: {1000 / 1000:.1f}x", font=("Palatino Linotype", 16), bg="darkslategray1")
    speed_label.grid(row=4, column=0, padx=10, pady=10)

    # Create info_text widget
    info_text = tk.Text(root, height=33, width=30, highlightthickness=5, highlightbackground="deepskyblue")
    info_text.grid(row=0, column=10, padx=10, pady=10)

    def update_timer():
        nonlocal timer_value
        nonlocal current_day
        timer_value += 1
        if timer_value % (24 * 3600) == 0:  # If timer reaches 24 hours
            timer_value = 8 * 3600  # Reset timer to 8:00:00
            current_day = (current_day + 1) % 7  # Increment day by 1 (cycling from 0 to 6)
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_label.config(text=f"Day: {days_of_week[current_day]}")
        hours = (timer_value // 3600) % 24  # Extract hours
        minutes = (timer_value % 3600) // 60  # Extract minutes
        seconds = timer_value % 60  # Extract seconds
        timer_label.config(text=f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        root.after(1000, update_timer)  # Update after 1 second (1000 milliseconds)

    update_timer()  # Start the timer

    def draw_squares(screen):
        for square in squares:
            pygame.draw.rect(screen, RED, square)  # Draw the square with red color

    # Pygame loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    # Check if any square is clicked and display its coordinates
                    mouse_pos = pygame.mouse.get_pos()
                    for square in squares:
                        if square.collidepoint(mouse_pos):
                            info_text.insert(tk.END, f"Clicked Square: {square.topleft}\n")

        # Move the squares
        for square in squares:
            move_x = random.randint(-10, 10)  # Wider random movements
            move_y = random.randint(-10, 10)
            new_square = square.move(move_x, move_y)

            new_square.centerx = np.clip(new_square.centerx, 0, resized_width - 1)
            new_square.centery = np.clip(new_square.centery, 0, resized_height - 1)

            # Check if the new square position is in the #ededef color
            if image.get_at((new_square.centerx, new_square.centery)) == EDENEF:
                square.move_ip(move_x, move_y)

        # Clear the Pygame screen
        pygame_screen.fill((0, 0, 0))

        # Draw the image
        pygame_screen.blit(image, (0, 0))

        # Draw the squares
        draw_squares(pygame_screen)

        # Convert the Pygame surface to a PIL Image
        pygame_image = pygame.surfarray.array3d(pygame_screen)
        pygame_image = np.swapaxes(pygame_image, 0, 1)
        pygame_image = np.flip(pygame_image, 0)
        pil_image = Image.fromarray(pygame_image)

        # Convert the PIL Image to a Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)

        # Display the image on a Tkinter Label
        map_label.config(image=tk_image)
        map_label.image = tk_image  # Keep a reference to prevent garbage collection

        # Update the Tkinter window
        root.update()

        # Control the frame rate
        clock.tick(20)

    pygame.quit()
    root.mainloop()

if __name__ == "__main__":
    main()
