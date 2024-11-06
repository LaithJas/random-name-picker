import random, pygame


class name_picker:
    def __init__(self, name_list):
        self.names = name_list
        self.times = dict()  # Dictionary to store each name and their display time

    #deleting a name from the list
    def delete_name(self, name):
        self.names.remove(name)

    # choosing a random name from the list, and then deleting it
    # the chosen name is returned, if no names are left in the list
    # The string "DONE" is returned
    def choose_name(self):
        if len(self.names) > 0:
            chosen_name = random.choice(self.names)
            self.delete_name(chosen_name)  # Remove the name once it’s chosen
            return chosen_name
        else:
            return "DONE"  # Indicates all names have been displayed

    # sets a time for a player given player's name 
    def set_player_time(self, name, display_time):
        self.times[name] = display_time  # Store the display duration for the name

    # find_losers() will calucualte the players who got the longest and shortest times
    # then return the names as a list of tubles.
    # the tubles has the information in a (name, time) format 
    def find_losers(self):
        high_player_time = max(self.times.values())
        low_player_time = min(self.times.values())
        high_player_name = low_player_name = ""

        for name, time in self.times.items():
            if time == high_player_time:
                high_player_name = name
            if time == low_player_time:
                low_player_name = name

        return [(high_player_name, high_player_time), (low_player_name, low_player_time)]
    

# Button class is used to define buttons and their clicking functionality
class Button:
    def __init__(self, x, y, image, scale, screen):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) # scales the icon button
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # Position of the icoon on the screen in pix
        self.clicked = False
        self.screen = screen

    # draw() function will draw the button and check if it's  clicked or not
    # it will return True if the button is clicked. otherwise False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos() #gets the position of the mosue on the screen  

        if self.rect.collidepoint(pos): # check if the mouse is above the icon/button
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        return action