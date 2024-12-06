# Developer: Laith, AJ
# A small game that display names randomly and shows fastest and slowest results at the end

import threading
import pygame, time, namePickerLogic, datetime, pyttsx3  


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
pygame.display.set_caption(f"Week 6 - {datetime.datetime.now().strftime('%A')} Morning's Standup")
wide_font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 48)

# Load images
start_image = pygame.image.load('start_btn.png').convert_alpha()
next_image = pygame.image.load('next2.png').convert_alpha()

# Instantiate buttons
start_btn = namePickerLogic.Button(295.375, 400, start_image, 0.75, screen)
next_btn =  namePickerLogic.Button(303.25, 400, next_image, 0.50, screen)


# start_btn = namePickerLogic.Button(295.375, 400, start_image, 0.75, screen)
# next_btn = namePickerLogic.Button(303.25, 400, next_image, 0.50, screen)

# switch_scence() is responsible for switching between the 3 main scences
# the start/intro, the name display, and the results scences
# it will also choose the first player and start the timer
# If you want to choose a player that starts the game, you change the display_name var in here 
def switch_scene(scene):
    global current_scene, displayed_name, name_display_start_time
    current_scene = scene
    if scene == NAME_SCENE:
        displayed_name = gamers.choose_name()  # Choose a new name only when switching to NAME_SCENE
        speak_name(displayed_name)
        name_display_start_time = time.time()  # Record the start time for the current name
        

engine = pyttsx3.init()
def speak_name(name):
    # Use a separate thread to speak the name, allowing the program to continue running
    def speak():
        engine.say(name)  # Speak the name
        engine.runAndWait()  # Wait for the speech to finish (in the background)
    
    # Start the speech in a new thread
    threading.Thread(target=speak).start()
# Initial setup
current_scene = MAIN_SCENE
displayed_name = None  # Holds the current name to be displayed
name_display_start_time = None  # Start time for the displayed name
run = True
next_button_click_count = 1
num_participants=len(engineers)
color_r = 0
color_g = 0
color_b = 255
color_change_speed = 0.125/2/2/2
say_end=True

# Game loop start------------------------------
while run:
    screen.fill((color_r, color_g, color_b))
        # Smooth color transition logic
    if color_r < 255 and color_b == 255:
        color_r += color_change_speed
    elif color_g < 255 and color_r == 255:
        color_g += color_change_speed
    elif color_b > 0 and color_g == 255:
        color_b -= color_change_speed
    elif color_r > 0 and color_b == 0:
        color_r -= color_change_speed
    elif color_g > 0 and color_r == 0:
        color_g -= color_change_speed
    elif color_b < 255 and color_g == 0:
        color_b += color_change_speed
    
    if color_r < 75 and color_b < 75 and color_g < 75:
        color_r = 0
        color_b = 0
        color_b = 255

   # catches when you close the game using the X on the top right 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Scene handling
    if current_scene == MAIN_SCENE:
        # Switch the scence if the start button is pressed
        if start_btn.draw():
            pygame.time.wait(100)
            switch_scene(NAME_SCENE)
        
        good_morning_text = wide_font.render(f"Happy {datetime.datetime.now().strftime('%A')}!", True, BLACK)
        screen.blit(good_morning_text, (SCREEN_WIDTH // 2 - good_morning_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))

        # every time you see this pattern, it is rendering something and then printing it on the screen
        main_text = wide_font.render("Press Start to Begin", True, BLACK)
        screen.blit(main_text, (SCREEN_WIDTH // 2 - main_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
         
    elif current_scene == NAME_SCENE:
        if displayed_name is not None:
            name_text = wide_font.render(displayed_name, True, BLACK)
            screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - name_text.get_height() // 2))

            click_count_text = small_font.render(f"Participant: {next_button_click_count}/{num_participants}", True, BLACK)
            screen.blit(click_count_text, (10, 10 + 5))  

            elapsed_time = time.time() - name_display_start_time
            timer_text = small_font.render(f"Timer: {elapsed_time:.1f}s", True, BLACK)  
            screen.blit(timer_text, (10, 60))  

            # Draw the next button and check for clicks
            if next_btn.draw():
                next_button_click_count+=1
                # Calculate display time for the current name
                if displayed_name != "DONE":
                    display_time = time.time() - name_display_start_time
                    print(f"Recorded time for {displayed_name}: {display_time}s")
                    gamers.set_player_time(displayed_name, display_time)
                
                # Choose a new name and reset the display
                displayed_name = gamers.choose_name()
                if displayed_name != "DONE":
                    name_display_start_time = time.time()
                    speak_name(displayed_name) 
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
        if (say_end):
            speak_name(f"{high_name} was the highest and {low_name} was the lowest, if you have a joke prepared the stage is all yours")
            say_end=False

    # Update the display
    pygame.display.update()

pygame.quit()