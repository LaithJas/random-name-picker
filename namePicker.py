# Developer: Laith
# A small game that display names randomly and shows fastest and slowest results at the end

import pygame, time, namePickerLogic


#Enter the names of the players here
engineers = [ 
]

gamers = namePickerLogic.name_picker(engineers)

pygame.init()

# Game window def
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAIN_SCENE = "main"
NAME_SCENE = "names"
RESULTS_SCENE = "results"

# Color def
BG_COLOR = (240, 255, 235)
BLACK = (0, 0, 0)

# Game window setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #define a window
pygame.display.set_caption('Daily Standup :)')
wide_font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 48)

# Load images
start_image = pygame.image.load('start_btn.png').convert_alpha()
next_image = pygame.image.load('next2.png').convert_alpha()

# Instantiate buttons
start_btn = namePickerLogic.Button(200, 400, start_image, 0.75, screen)
next_btn =  namePickerLogic.Button(400, 400, next_image, 0.50, screen)

# switch_scence() is responsible for switching between the 3 main scences
# the start/intro, the name display, and the results scences
# it will also choose the first player and start the timer
# If you want to choose a player that starts the game, you change the display_name var in here 
def switch_scene(scene):
    global current_scene, displayed_name, name_display_start_time
    current_scene = scene
    if scene == NAME_SCENE:
        displayed_name = gamers.choose_name()  # Choose a new name only when switching to NAME_SCENE
        name_display_start_time = time.time()  # Record the start time for the current name

# Initial setup
current_scene = MAIN_SCENE
displayed_name = None  # Holds the current name to be displayed
name_display_start_time = None  # Start time for the displayed name
run = True

# Game loop start------------------------------
while run:
    screen.fill(BG_COLOR)

   # catches when you close the game using the X on the top right 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Scene handling
    if current_scene == MAIN_SCENE:
        # Switch the scence if the start button is pressed
        if start_btn.draw():
            switch_scene(NAME_SCENE)

        # every time you see this pattern, it is rendering something and then printing it on the screen
        main_text = wide_font.render("Press Start to Begin", True, BLACK)
        screen.blit(main_text, (SCREEN_WIDTH // 2 - main_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
         
    elif current_scene == NAME_SCENE:
        if displayed_name is not None:
            name_text = wide_font.render(displayed_name, True, BLACK)
            screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - name_text.get_height() // 2))

            # Draw the next button and check for clicks
            if next_btn.draw():
                # Calculate display time for the current name
                if displayed_name != "DONE":
                    display_time = time.time() - name_display_start_time
                    gamers.set_player_time(displayed_name, display_time)
                
                # Choose a new name and reset the display
                displayed_name = gamers.choose_name()
                if displayed_name != "DONE":
                    name_display_start_time = time.time() 
                else:
                    # When all names are done, switch to RESULTS_SCENE
                    switch_scene(RESULTS_SCENE)

    elif current_scene == RESULTS_SCENE:
        # Get the highest and lowest times to display
        names = gamers.find_losers()
        high_name, high_time = names[0]
        low_name, low_time = names[1]

        # Display results
        result_text = wide_font.render("Results", True, BLACK)
        screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 5))

        high_text = small_font.render(f"Longest Time: {high_name} - {high_time:.2f}s", True, BLACK)
        screen.blit(high_text, (SCREEN_WIDTH // 2 - high_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        low_text = small_font.render(f"Shortest Time: {low_name} - {low_time:.2f}s", True, BLACK)
        screen.blit(low_text, (SCREEN_WIDTH // 2 - low_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    # Update the display
    pygame.display.update()

pygame.quit()