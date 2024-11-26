#Nina Mathew - NM 
#Minyei Kim - MK 
#Barbara Litvinova - BL
import os
import json
import pygame
from . board import Board
from . gui import SelectionGroup, Input, Button, Label, InputDialogue
from . leaderboard import Leaderboard #
#NM: above are imported files and python code for graphics and the visual part of the Mindsweeper game.  

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')#NM: os.path is used to see and modify files and for accessing the filesystem.
#NM: The directory is to allow access to all of the fonts, graphics, and images.


def load_image(name, size=None):#NM: This function loads and image and allows for the resize of it. 
    path = os.path.join(ASSETS_DIR, name) #NM: It brings the files from the directory, like images.
    try: #NM: It tries to execute the code here, but if anything goes wrong or an exception occurs it goes to the except block.
        image = pygame.image.load(path) #NM: If the try block is true it allows for the image to be printed. 
    except pygame.error as error:#NM: Since there is an error it allows for a fail safe and notifies the user of the error.
        print('Cannot load image: ', path)
        raise SystemError(error)

    if size is not None:
        if isinstance(size, int):#NM: isinstance function returns True if the object is an int, otherwise False.
            size = (size, size)
        image = pygame.transform.scale(image, size)#NM: It scales the image to the correct size and shape.

    return image


def load_font(name, size):
    path = os.path.join(ASSETS_DIR, name) #NM: It brings the fonts from the directory files.
    try:
        font = pygame.font.Font(path, size)
    except pygame.error as error:
        print('Cannot load font: ', path)
        raise SystemError(error) #NM: The raise statement forces an error to happen to either print text to the user, stop the program, and make special exceptions.
    return font


class Timer: #NM: Starts event on timer.
#NM: self in python is an instance of the class.
#NM: A class is an object builder, contructor, or blueprint for making objects.
#NM: Self allows us to access the attributes and methods of class.
#NM: Attributes are the variables to an object that have information about it's characteristics. 
#NM: When new classes are created it makes a new type of object which  allows new instances to occur. 
    def __init__(self, on_time_event): #NM: Starts timer with a callback function. A callback function is when the function is passed as an argument and then after the first function is completed the function is called back at a specific time. 
        self.on_time_event = on_time_event
        self.start_time = None
        self.interval = None
        self.running = False #NM: This makes sure the game does not start again unless the timer is also started again. 

    def start(self, interval): #NM: Start timer now and trigger event after interval
        self.running = True
        self.interval = interval
        self.start_time = pygame.time.get_ticks() #NM: This Pygame function is running in milliseconds and time is printed for every millisecond. 

    def check(self): #NM: This function checks if the timer is finished and if it is done it triggers the event below to occur. 
        if (self.running and #NM: Checks if the timer is currently on but if the timer is not running it skips the rest of the code.
                pygame.time.get_ticks() - self.start_time >= self.interval):#NM This part of the code checks to see how much time has passed since the start of teh game.
            self.running = False
            self.on_time_event()#NM: 


def create_count_tiles(tile_size, font_name): #NM: This function makes tiles for the amount bombs in the game. 
    colors = [
        None,
        'Blue',
        'Dark Green',
        'Red',
        'Navy',
        'Brown',
        'Light Sea Green',
        'Black',
        'Dim Gray'
    ]#NM: The colours listed above are the games custom colour palette. 

    font_size = int(tile_size * 0.9)#NM: This adjusts the font size to fit the tile dimensions.
    font = load_font(font_name, font_size)

    empty_tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)#NM This brings the graphics for the tiles. 
    center = empty_tile.get_rect().center#NM: Places the font in the centre and adjusts it. 

    tiles = [empty_tile.copy()]#NM: Is a blank tile for the background of Mindsweeper game.

    for count in range(1, 9):#NM: Each number corresponds to a tile that displays the number.
        glyph = font.render(str(count), True, pygame.Color(colors[count]))#NM: converts the number as string so it can be shown on the tile. It also sets the color od the text and allows for a smoother look as the text is displayed.
        width = glyph.get_rect().width#NM: The get_rect function returns a new rectangle covering the entire surface. 

        glyph_center = (center[0] + int(0.15 * width), center[1])#NM: This centers the text horizontally and vertically. 
        rect = glyph.get_rect(center=glyph_center)
        tile = empty_tile.copy()#NM: This line allows for a blank tile on the game. 
        tile.blit(glyph, rect.topleft)#NM The .blit function takes the source onto this code or surface.
        tiles.append(tile)#NM: The .append function adds something extra to the end of the list. 

    return tiles


def is_key_suitable_for_name(key_name):#NM: This checks if a key is valid for entering names. 
    return len(key_name) == 1 and key_name.isalnum() or key_name in ['-', '_']#NM The isalnum() method checks if all the characters are alphanumeric which means Letters are first and then numbers.


def is_digit(key_name):#NM: This checks if the key is a numeric digit.
    return len(key_name) == 1 and key_name.isnumeric()#NM:It returns True if the key is one digit. 


class Game:
    """Main game class."""
    TILE_SIZE = 20 #NM: This represents the size of every tile in the game. 
    GUI_WIDTH = 91
    HUD_HEIGHT = 30
    MARGIN = 20
    BG_COLOR = pygame.Color('Light Slate Gray')#NM: This is the background colour.
    FIELD_BG_COLOR = pygame.Color('#d7dcdc')#NM: Field background colour
    FIELD_LINES_COLOR = pygame.Color('#738383')
    GUI_FONT_COLOR = pygame.Color('Light Yellow')#NM: The colour of the font. 
    GUI_FONT_SIZE = 13
    DIGITS = {chr(c) for c in range(ord('0'), ord('9') + 1)}
    MAX_BOARD_DIMENSION = 50
    MIN_BOARD_DIMENSION_DISPLAY = 10
    MAX_NAME_LENGTH = 8
    DELAY_BEFORE_NAME_INPUT_MS = 1000
    #NM: The above code gives restrictions to teh graphics and gives it a limit to the width, height, and other dimensions. 

    def __init__(self, state_file_path):#NM: Te goal of this function is to try to load the game from the file state_file. 
        try:
            with open(state_file_path) as state_file:#NM: The with open() opens a file so the code below can acces and work on the file. In this case the file state_file.
                state = json.load(state_file)#NM: The json.load() is used to store and transer data like state_file.
        except (IOError, json.JSONDecodeError):#NM: In case of an error the game goes to an empty state. 
            state = {}

        display_info = pygame.display.Info()#NM: The fucntion below shows the information for the dimensions of the game.
        self.max_cols = (int(0.95 * display_info.current_w) - self.GUI_WIDTH
                         - 3 * self.MARGIN) // self.TILE_SIZE #NM: This line codes for the maximum numbers of coloumns allowed in the game. 
        self.max_rows = (int(0.95 * display_info.current_h) - self.HUD_HEIGHT#NM This line shows the maximum number of rows alllowed in the game. 
                         - 3 * self.MARGIN) // self.TILE_SIZE

        difficulty = state.get('difficulty', 'EASY')#NM: The .get() function tries to get the difficulty from a different file called state.
        if difficulty not in ['EASY', 'NORMAL', 'HARD', 'CUSTOM']:#NM: This line makes the default level Easy if state does not exist.  
            difficulty = 'EASY'

        if "leaderboard" in state: #NM It checks if leadership is in state if it's not it only displays the basic levels(Easy, Normal, Hard)
            leaderboard_data = state['leaderboard']
        else:
            leaderboard_data = {'EASY': [], 'NORMAL': [], 'HARD': []}

        self.n_rows = state.get('n_rows', 10)#NM: state.get gets the value of n_rows but if n_rows doesn't exist it defaults the value to 10 rows.  
        self.n_cols = state.get('n_cols', 10)#NM: As stated above if n_cols or n_mines doesn't exist the code defaults to 10.
        self.n_mines = state.get('n_mines', 10)
        self.set_difficulty(difficulty)#NM: This line increases the number of rows, coloumns, mines based on the difficulty level. 

        mine_count_images = create_count_tiles(self.TILE_SIZE,
                                               "kenvector_future.ttf")
        tile_image = load_image('tile.png', self.TILE_SIZE)#NM: tile.png is a blank unclicked tile.
        mine_image = load_image('mine.png', self.TILE_SIZE)#NM: Mine and flag png represents the mines and flags in the game. 
        flag_image = load_image('flag.png', self.TILE_SIZE)#NM: The load image part of the file retrieves the images and resizes it to match the tile size(TILE_SIZE). 
        gui_font = load_font("Akrobat-Bold.otf", self.GUI_FONT_SIZE)#NM: Loads the font type into the GUI of the game. GUI is the graphical user interface.
        #NM: The above code first tries to find the number of rows, coloumnc, and mines from the state directory but if nothing is saved in the directory then it defaults to the easiest level with 10 rows, 10 columns, and 10 mines.

        self.board = Board(
            self.n_rows, self.n_cols, self.n_mines,#NM: These are the dimensions of the game.
            self.FIELD_BG_COLOR, self.FIELD_LINES_COLOR, self.TILE_SIZE, #NM: This has the background colour, colour of teh gridlines, and size of each tile in the game. 
            tile_image, mine_count_images, flag_image, mine_image, #NM: This line brings the saved images of the mines and flags. 
            on_status_change_callback=self.on_status_change)

        self.screen = None
        self.screen_rect = None #NM: Represents the screens boundaries.
        self.board_rect = None #NM: This represents the minesweeper board area.
        self.hud_rect = None 
        self.gui_rect = None 
        self.board_area_rect = None #NM: The part of teh game that has the board.
        self.init_screen()#NM: Arranges the attributes above and sets up the game.

        self.difficulty_selector = SelectionGroup( #NM: Allows the user to select options by adding drop-down or buttons in the game. 
            gui_font,
            self.GUI_FONT_COLOR,
            "DIFFICULTY",
            ["EASY", "NORMAL", "HARD", "CUSTOM"],
            initial_value=state.get('difficulty', 'EASY'))

        self.difficulty_selector.rect.centerx = self.gui_rect.centerx #NM: The .rect function is used to draw rectangles. In this case the selector is aligned horizontally to the centre of the GUI.
        self.difficulty_selector.rect.y = self.MARGIN
        self.difficulty_selector.callback = self.on_difficulty_change #NM: Everytime this function runs it updates teh game dimensions to match the difficulty level. 
        #NM (from . gui import SelectionGroup, Input, Button, Label, InputDialogue) Input is already defined, so it doesn't ask the user for input. 
        active_input = self.difficulty_selector.selected == "CUSTOM" #NM: Checks to see if the difficulty level is custom and if its true it changes the dimensions of the game based on the input from the user.
        self.width_input = Input(gui_font, self.GUI_FONT_COLOR,
                                 "WIDTH", self.n_cols, #NM: Makes a section for width input. 
                                 active_input=active_input,
                                 width=self.GUI_WIDTH, max_value_length=3,#NM: The part with max_value_length restricts the users input to 3 digits so 999 columns is the maximum amount of coloumns allowed. 
                                 key_filter=is_digit,#NM: Prevents the user from inputing anything but numbers.
                                 on_enter_callback=self.on_cols_enter)#NM: The game dimensions chan ges after the user confirms their customization by pressing enter. 
        self.height_input = Input(gui_font, self.GUI_FONT_COLOR, #NM: Makes a section for height input and repeats the same code as the one for width.
                                  "HEIGHT", self.n_rows, width=self.GUI_WIDTH,
                                  active_input=active_input,
                                  max_value_length=3,
                                  key_filter=is_digit,
                                  on_enter_callback=self.on_rows_enter)
        self.mines_input = Input(gui_font, self.GUI_FONT_COLOR, #NM: Makes a section for mines input and repeats the same code as the one for width and height.
                                 "MINES", self.n_mines, width=self.GUI_WIDTH,
                                 active_input=active_input,
                                 max_value_length=3,
                                 key_filter=is_digit,
                                 on_enter_callback=self.on_mines_enter)

        self.timer = Input(gui_font, self.GUI_FONT_COLOR,
                           "TIME", self.board.time) #NM: Shows the time while the user is playing the game, and determines the font and colour of the text. 
        self.current_mines = Input(gui_font, self.GUI_FONT_COLOR,
                                   "MINES", self.board.n_mines) #NM: Codes for the font and colour of the text that shows mine count. 

        self.status = Label(gui_font, self.GUI_FONT_COLOR, "READY TO GO!") #NM: This line also codes for the color and font of the text. 

        self.restart_button = Button(gui_font,
                                     self.GUI_FONT_COLOR,
                                     "RESTART",
                                     self.board.reset)#NM: Codes for the appearance of teh reset button like the colour and font.

        self.show_leaderboard_button = Button(gui_font, self.GUI_FONT_COLOR,
                                              "LEADER BOARD",
                                              self.show_leaderboard)#NM: Codes for the font and color for the phrase "LEADER BOARD"

        leaderboard_width = (
            self.GUI_WIDTH + 2 * self.MARGIN #NM: 2 * self.MARGIN takes is the spacing added to each side of the leadership board. 
            + self.MIN_BOARD_DIMENSION_DISPLAY * self.TILE_SIZE)#NM: This code determines the width and spacing for the leaderboard. 
        self.leaderboard = Leaderboard(gui_font, self.GUI_FONT_COLOR,
                                       5, leaderboard_width, #NM: 5 is the limit of playerrs allowed on the leardership board. 
                                       data=leaderboard_data) 
        self.leaderboard_hint = Label(gui_font, self.GUI_FONT_COLOR,
                                      "CLICK TO CONTINUE")#NM: This line codes for the font and colour of the text. 

        self.name_input = InputDialogue(gui_font, self.GUI_FONT_COLOR,
                                        "ENTER YOUR NAME",#NM: Codes for the text and  font colour. 
                                        self.on_name_enter,
                                        max_length=self.MAX_NAME_LENGTH,
                                        key_filter=is_key_suitable_for_name)#NM: After the player finishes their level the game asks the user for their name but this code restricts the amount of characters the user is allowed to input. 

        self.victory_time = Label(gui_font, self.GUI_FONT_COLOR, "") #NM: Shows the time when the player marks all the mines correctly.
        self.leaderboard_announcement = Label(
            gui_font, self.GUI_FONT_COLOR,
            "YOU MADE IT TO THE LEADERBOARD!")
        self.show_name_input_timer = Timer(self.show_name_input)
        #NM: The above section codes for the font and colour of the text outputs after the player wins the level. 

        self.place_gui()#NM: This calls the GUI components to position and organizes it on the game. 
        self.keep_running = None#NM: Like a placeholder before the loop starts.   
        self.mode = "game" #NM: Assigns a string to the .mode and allows the game to keep track of everything. There is probably another mode when the mode is "game" that means you are playing minesweeper. 

    def init_screen(self): #NM: Initialize screen and compute rectangles for different regions.
        board_area_width = \
            max(self.n_cols, self.MIN_BOARD_DIMENSION_DISPLAY) * self.TILE_SIZE #NM: The two lines of code uses the number of coloumns to calculate the width and height of the board.
        board_area_height = \
            max(self.n_rows, self.MIN_BOARD_DIMENSION_DISPLAY) * self.TILE_SIZE
        window_width = 3 * self.MARGIN + self.GUI_WIDTH + board_area_width#NM: This adds space on the width sides of the screen.
        window_height = 3 * self.MARGIN + self.HUD_HEIGHT + board_area_height#NM: This adds space on the height sides of the screen.

        self.board_area_rect = pygame.Rect(2 * self.MARGIN + self.GUI_WIDTH, #NM: Determines the amount of space between the GUI and left side and makes sure the rectangle starts to the right of the GUI.
                                           2 * self.MARGIN + self.HUD_HEIGHT, #NM: Adds spacing to the board and makes sure the rectangle starts below timer, mine count, levels, etc.
                                           board_area_width,
                                           board_area_height)

        self.board.rect.size = (self.n_cols * self.TILE_SIZE,
                                self.n_rows * self.TILE_SIZE)#NM: MAkes the rectangle based on coloumns and rows. 
        self.board.rect.center = self.board_area_rect.center#NM: Centres the rectangle

        self.hud_rect = pygame.Rect(2 * self.MARGIN + self.GUI_WIDTH,
                                    self.MARGIN,
                                    board_area_width,
                                    self.HUD_HEIGHT) #NM: Makes the rectangle part of HUD(heads-up display command).

        self.screen = pygame.display.set_mode((window_width, window_height)) #NM: Uses the calculated dimensions from above to set the main Pygame window
        self.screen_rect = self.screen.get_rect()#NM: This code represents the rectangle for the entire board.
        self.screen.fill(self.BG_COLOR)#NM: makes the entire screen the background colour. 
        self.gui_rect = pygame.Rect(self.MARGIN,
                                    2 * self.MARGIN + self.HUD_HEIGHT,
                                    self.GUI_WIDTH,
                                    board_area_height)#NM: Sets the dimensions for the rectangle

    def set_difficulty(self, difficulty):
        if difficulty == "EASY": #NM: determines the dimensions of the board when the level is easy.
            self.n_rows = 10
            self.n_cols = 10
            self.n_mines = 10
        elif difficulty == "NORMAL": #NM: determines the dimensions of the board when the level is normal.
            self.n_rows = 16
            self.n_cols = 16
            self.n_mines = 40
        elif difficulty == "HARD": #NM: determines the dimensions of the board when the level is hard.
            self.n_rows = 16
            self.n_cols = 30
            self.n_mines = 99

    def place_gui(self):
        self.width_input.rect.topleft = (
            self.gui_rect.x,
            self.difficulty_selector.rect.bottom#NM: aligns the width_input based on the x-coordinate. 
            + 0.2 * self.difficulty_selector.rect.height)#NM: Adds vertical space thats about 20% of the height.
        self.height_input.rect.topleft = (
            self.gui_rect.x,
            self.width_input.rect.bottom + 0.4 * self.height_input.rect.height)#NM: adds space thats around 40% of the height. 
        self.mines_input.rect.topleft = (
            self.gui_rect.x,
            self.height_input.rect.bottom + 0.4 * self.width_input.rect.height)

        hud_width = self.place_hud()

        self.restart_button.rect.top = self.timer.rect.top
        self.restart_button.rect.centerx = 0.5 * (self.hud_rect.left
                                                  + self.hud_rect.right
                                                  - hud_width)

        self.show_leaderboard_button.rect.bottom = (self.screen_rect.height
                                                    - self.MARGIN)
        self.show_leaderboard_button.rect.centerx = (self.MARGIN
                                                     + 0.5 * self.GUI_WIDTH)

        screen_center = self.screen.get_rect().centerx
        self.status.rect.top = self.current_mines.rect.top
        self.status.rect.centerx = self.restart_button.rect.centerx

        self.leaderboard.rect.top = self.MARGIN
        self.leaderboard.rect.centerx = screen_center

        self.leaderboard_hint.rect.bottom = (self.screen_rect.height
                                             - self.MARGIN)
        self.leaderboard_hint.rect.centerx = self.screen_rect.centerx

        self.victory_time.rect.top = self.MARGIN
        self.victory_time.rect.centerx = self.screen_rect.centerx
        self.leaderboard_announcement.rect.top = (
            self.victory_time.rect.bottom
            + 0.4 * self.victory_time.rect.height)
        self.leaderboard_announcement.rect.centerx = self.screen_rect.centerx

        self.name_input.rect.top = (
            self.leaderboard_announcement.rect.bottom
            + self.leaderboard_announcement.rect.height)
        self.name_input.rect.centerx = self.screen_rect.centerx

    def place_hud(self):
        """Place timer and mines info and return width of this block."""
        hud_width = max(self.timer.rect.width, self.current_mines.rect.width)
        self.timer.rect.topleft = (self.hud_rect.right - hud_width,
                                   self.hud_rect.top)
        self.current_mines.rect.topleft = (
            self.timer.rect.left,
            self.timer.rect.bottom + 0.4 * self.timer.rect.height)
        return hud_width

    def reset_game(self):
        """Reset the game."""
        self.board.reset(n_rows=self.n_rows,
                         n_cols=self.n_cols,
                         n_mines=self.n_mines)

    def show_leaderboard(self):
        """Change screen to leaderboard."""
        self.mode = "leaderboard"

    def show_name_input(self):
        """Change screen to name input."""
        self.mode = "name_input"
        self.victory_time.set_text("YOUR TIME IS {} SECONDS"
                                   .format(self.board.time))
        self.name_input.set_value("")
        self.place_gui()

    def on_name_enter(self, name):
        """Handle name enter for the leaderboard."""
        if not name:
            return
        self.leaderboard.update(self.difficulty_selector.selected,
                                name,
                                self.board.time)
        self.mode = "leaderboard"

    def on_status_change(self, new_status):
        """Handle game status change."""
        if new_status == 'game_over':
            self.status.set_text("GAME OVER!")
        elif new_status == 'victory':
            self.status.set_text("VICTORY!")
            if self.leaderboard.needs_update(self.difficulty_selector.selected,
                                             self.board.time):
                self.show_name_input_timer.start(
                    self.DELAY_BEFORE_NAME_INPUT_MS)
        elif new_status == 'before_start':
            self.status.set_text("READY TO GO!")
        else:
            self.status.set_text("GOOD LUCK!")

    def on_difficulty_change(self, difficulty):
        """Handle difficulty change."""
        self.height_input.active_input = False
        self.width_input.active_input = False
        self.mines_input.active_input = False
        self.set_difficulty(difficulty)
        if difficulty == "CUSTOM":
            self.height_input.active_input = True
            self.width_input.active_input = True
            self.mines_input.active_input = True

        self.height_input.set_value(self.n_rows)
        self.width_input.set_value(self.n_cols)
        self.mines_input.set_value(self.n_mines)

        self.init_screen()
        self.place_gui()
        self.reset_game()

    def set_game_parameter(self, parameter, max_value, value):
        """Set either n_rows, n_cols, n_mines."""
        if not value:
            value = 1

        value = int(value)
        value = min(max(1, value), max_value)
        setattr(self, parameter, value)
        self.n_mines = min(self.n_mines, self.n_rows * self.n_cols - 1)
        self.mines_input.set_value(self.n_mines)
        self.init_screen()
        self.place_gui()
        self.reset_game()
        return value

    def on_rows_enter(self, value):
        """Handle n_rows input."""
        return self.set_game_parameter('n_rows',
                                       self.max_rows,
                                       value)

    def on_cols_enter(self, value):
        """Handle n_cols input."""
        return self.set_game_parameter('n_cols',
                                       self.max_cols,
                                       value)

    def on_mines_enter(self, value):
        """Hand n_mines input."""
        return self.set_game_parameter('n_mines',
                                       self.n_rows * self.n_cols - 1,
                                       value)

    def draw_all(self):
        """Draw all elements."""
        self.screen.fill(self.BG_COLOR)

        if self.mode == "leaderboard":
            self.leaderboard.draw(self.screen)
            self.leaderboard_hint.draw(self.screen)
            pygame.display.flip()
            return
        elif self.mode == "name_input":
            self.victory_time.draw(self.screen)
            self.leaderboard_announcement.draw(self.screen)
            self.name_input.draw(self.screen)
            pygame.display.flip()
            return

        self.board.draw(self.screen)

        self.difficulty_selector.draw(self.screen)
        self.height_input.draw(self.screen)
        self.width_input.draw(self.screen)
        self.mines_input.draw(self.screen)

        self.timer.draw(self.screen)
        self.current_mines.draw(self.screen)
        self.status.draw(self.screen)

        self.restart_button.draw(self.screen)
        self.show_leaderboard_button.draw(self.screen)

        pygame.display.flip()

    def process_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_running = False
                break

            if self.mode == "leaderboard":
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mode = "game"
                break
            elif self.mode == "name_input":
                if event.type == pygame.KEYDOWN:
                    self.name_input.on_key_down(event)
                break

            if event.type == pygame.MOUSEBUTTONUP:
                self.difficulty_selector.on_mouse_up(event.button)
                self.height_input.on_mouse_up(event.button)
                self.width_input.on_mouse_up(event.button)
                self.mines_input.on_mouse_up(event.button)
                self.restart_button.on_mouse_up(event.button)
                self.show_leaderboard_button.on_mouse_up(event.button)
                self.board.on_mouse_up(event.button)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.board.on_mouse_down(event.button)
            elif event.type == pygame.KEYDOWN:
                self.height_input.on_key_down(event)
                self.width_input.on_key_down(event)
                self.mines_input.on_key_down(event)

    def start_main_loop(self):
        """Start main game loop."""
        clock = pygame.time.Clock()
        self.keep_running = True
        while self.keep_running:
            clock.tick(30)
            self.timer.set_value(self.board.time)
            self.current_mines.set_value(self.board.n_mines_left)
            self.place_hud()
            self.process_events()
            self.show_name_input_timer.check()
            self.draw_all()

    def save_state(self, state_file_path):
        """Save game state on disk."""
        state = {
            "difficulty": self.difficulty_selector.selected,
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "n_mines": self.n_mines,
            "leaderboard": self.leaderboard.data
        }
        with open(state_file_path, "w") as state_file:
            json.dump(state, state_file)


def run(state_file_path):
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    pygame.mouse.set_visible(True)
    game = Game(state_file_path)
    game.start_main_loop()
    game.save_state(state_file_path)
