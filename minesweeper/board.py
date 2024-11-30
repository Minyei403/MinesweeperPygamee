#Minyei Kim - MK
#Nina Mathew - NM
#Barbara Litvinova - BL
#for test(github web)
from collections import deque
import random
import numpy
import pygame


LEFT_BUTTON = 1
RIGHT_BUTTON = 3


def cross_image(image, color, line_width): #MK: This fuction draws a cross over the tile.
    """Draw a cross over the tile."""
    image = image.copy() #MK: .copy method returns the copy of image. 
    w, h = image.get_size() #MK: .get_size() method returns the width and height of the image. 
    pygame.draw.line(image, color, (0, 0), (w, h), line_width) #MK: It draws a line on the screen: line(surface, color, start_pos, end_pos)
    pygame.draw.line(image, color, (w, 0), (0, h), line_width) 
    return image


def add_background_color(tile, color): #MK: This function draws a tile on the solid colour background. 
    """Draw a tile on the solid color background."""
    background = pygame.Surface(tile.get_size()) #MK: pygame.Surface() is a module that create a new image object. 
    background.fill(color) #MK: This will fill the colour of the background. 
    background.blit(tile, (0, 0)) #MK: This will draw the screen at (0,0) position. 
    return background


class Tile(pygame.sprite.Sprite): #MK: Class is a code template for creating objects. Sprites are objects with different properties. 
    """Sprite for a board tile."""
    def __init__(self, image, i, j, tile_size): #MK: __init__ method is to initialize the data members of a class when an object of that class is created. Self is the instance of the class and is used to access variables that belong to the class. 
        super(Tile, self).__init__() #MK: Super() function gives access to methods and properties of the class. 
        self.image = image #MK: The image is automatically passed as the first argument using the 'self' parameter. 
        self.rect = pygame.Rect(j * tile_size, i * tile_size,
                                tile_size, tile_size) #MK: pygame.Rect is a data structure that represents a 2D area. 


def create_field(n_rows, n_cols, tile_size, bg_color, line_color): #MK: This fuction will create the field. 
    """Create a checkered field.

    Parameters
    ----------
    n_rows, n_cols : int
        Number of rows and columns.
    tile_size : int
        Length of tile's side.
    bg_color : pygame.Color compatible
        Background color.
    line_color : pygame.Color compatible
        Color of lines.

    Returns
    -------
    pygame.Surface
        Image of the field.
    """
    field = pygame.Surface((n_cols * tile_size, n_rows * tile_size)) #MK: This will create a new image according to the size described. 
    field.fill(bg_color) #MK: This fills the field image with the colour. 

    for i in range(n_rows): #MK: This loop will run number of n_rows times. 
        pygame.draw.line(field, line_color,
                         (0, i * tile_size),
                         (n_cols * tile_size, i * tile_size)) #MK: This will draw a line according to the assigned values as much as the number of rows. 

    for j in range(n_cols): #MK: This is the same function for the columns. 
        pygame.draw.line(field, line_color,
                         (j * tile_size, 0),
                         (j * tile_size, n_rows * tile_size))

    return field


class Board: #MK: This is the game board. 
    """Game board.

    Parameters
    ----------
    n_rows : int
        Number of rows.
    n_cols : int
        Number of columns.
    n_mines : int
        Number of columns. Must be not greater than ``n_rows * n_cols``.
    tile_size : int
        Length of a tile's side in pixels.
    tile_image : pygame.Surface
        Image for a closed tile.
    mine_count_images : list of pygame.Surface
        Nine images for mine counts (from 0 to 8).
    flag_image : pygame.Surface
        Image for a flag.
    mine_image : pygame.Surface
        Image for a mine.
    on_status_change_callback : callable
        Call when game status changes. The signature is
        ``on_status_change_callback(news_status)``, where ``new_status`` is
        one of ["before_start", "running", "victory", "game_over"].
    """
    TILE_CLOSED = 0
    TILE_OPENED = 1
    TILE_CHECKED = 2

    def __init__(self, n_rows, n_cols, n_mines, bg_color, bg_lines_color,
                 tile_size, tile_image, mine_count_images, flag_image,
                 mine_image, on_status_change_callback=None): #MK: Assigning the sizes of all objects. 
        self.n_rows = n_rows #MK: number of rows
        self.n_cols = n_cols #MK: number of columns
        self.n_mines = n_mines #MK: number of columns, must be not greater than 'n_row'*'n_cols'
        self.n_mines_left = n_mines 

        self.is_mine = numpy.zeros((n_rows, n_cols), dtype=bool) #MK: This creates a new array of number of n_rows, n_cols and the bool type. 
        self.mine_count = None
        self.tile_status = numpy.full((n_rows, n_cols), self.TILE_CLOSED,
                                      dtype=numpy.int32)
        self.losing_indices = None
        self.start_time = None
        self.tiles_to_open = self.n_rows * self.n_cols - self.n_mines
        self._time = 0

        self.tile_size = tile_size #MK: The length of a tile's side in pixels. 

        self.bg_color = bg_color
        self.bg_lines_color = bg_lines_color
        self.bg_image = create_field(self.n_rows, self.n_cols,
                                     self.tile_size, bg_color,
                                     bg_lines_color)
        self.tile_image = tile_image
        self.mine_count_images = mine_count_images
        self.flag_image = flag_image #MK: image of the flag in png
        self.mine_image = mine_image #MK: image of the mine in png
        self.mine_image_crossed = cross_image(mine_image,
                                              pygame.Color('red'),
                                              2)
        self.mine_image_red_bg = add_background_color(mine_image,
                                                      pygame.Color('red')) #Mk: Mine image with red background. 
        self.rect = pygame.Rect(
            0, 0, self.n_cols * self.tile_size, self.n_rows * self.tile_size)

        self.tiles = None
        self.tiles_group = None
        self._init_tiles()

        self.on_status_change_callback = on_status_change_callback
        self.game_status = "before_start"

    def _init_tiles(self): #MK: This function initialzies list of tiles with closed tiles. 
        """Initialize list of tiles with closed tiles."""
        self.tiles = []
        for i in range(self.n_rows): #MK: This will call the items in n_rows n times.  
            for j in range(self.n_cols): #MK: This will call the items in n_cols n times.
                self.tiles.append(Tile(self.tile_image, i, j, self.tile_size)) #MK: add the tile image to the list 'tiles'. 
        self.tiles_group = pygame.sprite.Group(*self.tiles) #MK: This is a container class to hold and manage multiple Sprite objects. 

    def reset(self, n_rows=None, n_cols=None, n_mines=None): #MK: This function is a reset board. 
        """Reset board.

        Optional arguments will replace ones set in the class (if presented).
        """
        if n_mines is not None: #MK: If n_mines from the argument is not None, n_mines updates its number to the current value. 
            self.n_mines = n_mines

        if n_rows is not None or n_cols is not None: #MK: It will update the value to the currrent value for the rows and cols too. 
            if n_rows is None:
                n_rows = self.n_rows
            if n_cols is None:
                n_cols = self.n_cols

            self.tile_status = numpy.empty((n_rows, n_cols), dtype=numpy.int32)
            self.is_mine = numpy.zeros((n_rows, n_cols), dtype=bool)

            self.n_rows = n_rows
            self.n_cols = n_cols

        self.bg_image = create_field(self.n_rows, self.n_cols, self.tile_size,
                                     self.bg_color, self.bg_lines_color)
        self.n_mines_left = self.n_mines
        self.is_mine.fill(0)
        self.mine_count = None
        self.tile_status.fill(self.TILE_CLOSED)
        self.losing_indices = None
        self.start_time = None
        self.tiles_to_open = self.n_rows * self.n_cols - self.n_mines
        self._init_tiles()
        self._time = 0
        self._change_game_status("before_start")

    def _change_game_status(self, new_status): #MK: Setting the game to a new status 
        self.game_status = new_status
        if self.on_status_change_callback is not None:
            self.on_status_change_callback(self.game_status)

    @property
    def time(self): #MK: This function tracks the time of the game from the start. 
        """Return time passed from the game start."""
        if self.game_status == 'running' and self.start_time is not None:
            self._time = (pygame.time.get_ticks() - self.start_time) // 1000 #MK: Dividing the time by 1000 will show the time in seconds. 

        return self._time

    def _put_mines(self, i_click, j_click): #MK: This function will add the mines. 
        """Put mines after the first click."""
        allowed_positions = [] #MK: This creates an empty list to add mines. 
        n_tiles = self.n_rows * self.n_cols #MK: The size of rows by cols 
        for i in range(self.n_rows): #MK: This is a for loop for i in range of number of rows. 
            for j in range(self.n_cols): #MK: This is a for loop for j in range of number of columns. 
                if any((
                    abs(i - i_click) > 1 or abs(j - j_click) > 1, #MK: This checks if the absolute value of i-i_clicker is greater than 1, and if j-j_clicker is greater than 1. 
                    self.n_mines > n_tiles - 9 #MK: check if the number of tiles is less than the number of mines. 
                    and (i != i_click or j != j_click), 
                    self.n_mines == self.n_rows * self.n_cols
                )):
                    allowed_positions.append((i, j)) #MK: When the above conditions are achieved, i and j will be added to the list. 

        selected_positions = numpy.asarray(random.sample(allowed_positions,
                                                         self.n_mines))
        self.is_mine[selected_positions[:, 0], selected_positions[:, 1]] = True

        self.mine_count = numpy.zeros((self.n_rows, self.n_cols), #MK: It creates zeros in number of n rows and n columns. 
                                      dtype=numpy.int8)

        for i, j in selected_positions:
            ind = self._get_neighbors_flat(i, j)
            self.mine_count.flat[ind] += 1

    def get_neighbors(self, i, j): #MK: This function returns pairs of indices of neighbour cells. 
        """Return pairs of indices of neighbor cells."""
        ret = [] #MK: It's an empty list that will be updated based on the number i and j arguments. 

        if i > 0: #MK: This checks if the i exists. 
            ret.append((i - 1, j)) #MK: The ret function will check if the imaginary array is available and return True. 
            if j > 0: #MK: This is checking if the top left diagonal cell exitst and it will add it. 
                ret.append((i - 1, j - 1))
            if j < self.n_cols - 1: #MK: It checks for the top right diagonal cell and adds it. 
                ret.append((i - 1, j + 1))

        if j > 0: #MK: It checks for the cell 'j-1' exists and adds it. 
            ret.append((i, j - 1))

        if j < self.n_cols - 1: #MK: This will check if the cell to the right (j+1) exists and adds it. 
            ret.append((i, j + 1))

        if i < self.n_rows - 1: #MK: Check if the cell below exists and adds it. 
            ret.append((i + 1, j))
            if j > 0: #MK Checks if the bottom left exists and add it. 
                ret.append((i + 1, j - 1))
            if j < self.n_cols - 1: #MK: Checks if the bottom right cell exists and adds it. 
                ret.append((i + 1, j + 1))

        return ret #MK: It returns the list of neighbouring cell indices. 

    def _get_neighbors_flat(self, i, j): #MK: This returns indices of neighbour cells as a single number. 
        """Return indices of neighbor cells as a single number."""
        return [k * self.n_cols + l for (k, l) in self.get_neighbors(i, j)]

    def _open_tiles(self, i, j): #MK: This opens tiles on click using the wave algorithm. Wave algorithm propages information within a distributed network of nodes. 
        """Open tiles on click using the wave algorithm."""
        queue = deque() #MK: deque() is a data structure that efficiently adds and removes elements from both ends. 
        queue.append((i, j)) #MK: i and j are added to the deque(). 
        self.tile_status[i, j] = self.TILE_OPENED #MK: This will indicate which tiles are opened. 
        self.tiles_to_open -= 1 

        while queue: 
            i, j = queue.popleft() #MK: It removes the first element from the queue. 
            if self.mine_count[i, j] > 0: #MK: If the current tile has a mine, it stops the process. 
                continue

            neighbors = self.get_neighbors(i, j) #MK: Retrieve the neighbouring tiles of the current tile. 
            for k, l in neighbors: #MK: There is a loop for each neighbouring tile. 
                if self.tile_status[k, l] == self.TILE_CLOSED: #MK: If the neightouring tile is closed, 
                    self.tile_status[k, l] = self.TILE_OPENED #MK: It marks it as opened. 
                    self.tiles_to_open -= 1 #MK: It will subtract a number for tiles to open. 
                    queue.append((k, l)) #MK: It adds the neighbour to the queue for further processing. 

        if self.tiles_to_open == 0: #MK: After the final process, it checks if the opened tiles are zero. 
            self._change_game_status("victory") #MK: It will update the game status to victory if it's zero. 
            self.n_mines_left = 0 
            self.tile_status[self.is_mine] = self.TILE_CHECKED #MK: It will flag all the mines. 

    def _check_tile(self, i, j): #MK: This will check tile with a flag. 
        """Check tile with a flag (right click action)."""
        if self.tile_status[i, j] == self.TILE_CLOSED: #MK: if the tile is closed, the status is changed to "checked". 
            self.tile_status[i, j] = self.TILE_CHECKED
            self.n_mines_left -= 1 #MK: It will subtract one from the counter for remaining mines. 
        elif self.tile_status[i, j] == self.TILE_CHECKED: #MK: If the tile is checked, it will change the status to "closed". 
            self.tile_status[i, j] = self.TILE_CLOSED
            self.n_mines_left += 1 #MK: It will add one from the counter for remaining mines. 

    def _open_tile(self, i, j): #MK: This function opens tile. 
        """Open tile (left click action)."""
        status = self.tile_status[i, j]
        if status == self.TILE_CHECKED: #MK: if the tile is checked, it will change nothing and return. 
            return

        if self.is_mine[i, j]: #MK: If the tile contains a mine, it will return "game_over".
            self._change_game_status("game_over")
            self.losing_indices = (i, j) #MK: It will store the losing tiles' indices. 
            self.tile_status[i, j] = self.TILE_OPENED
            return

        if status == self.TILE_CLOSED: #MK: If the tile is closed and game is before start, it resets the mines. 
            if self.game_status == "before_start":
                self._put_mines(i, j)
                self.start_time = pygame.time.get_ticks() #MK: It records the time.
                self._change_game_status("running") #MK: It updates the game status. 
            self._open_tiles(i, j) #MK: It opens the tiles repeatedly starting from this tile. 
            return

        if self.mine_count[i, j] == 0: #MK: If the tile is a number not a mine, check for the adjacent tiles if they can be opened. 
            return #MK: This will return nothing. 

        neighbors = self.get_neighbors(i, j)#MK: It gets a list of nighbouring tiles.
        checked_count = sum(self.tile_status[k, l] == self.TILE_CHECKED #MK: This counts the number of flagged neighbours. 
                            for k, l in neighbors)
        if checked_count == self.mine_count[i, j]: #MK: if the number of flagged nighbours is equal to the mine count of this tile, the following will happen. 
            for k, l in neighbors:
                if self.tile_status[k, l] == self.TILE_CLOSED: #MK: This is for the remaining closed neighbours. 
                    if self.is_mine[k, l]:
                        self.losing_indices = (k, l) #MK: If a neighbouring closed tile contains a mine, it will end the game. 
                        self._change_game_status("game_over")
                        self.tile_status[k, l] = self.TILE_OPENED
                        return

                    self._open_tiles(k, l) #MK: If not, it will open the neighbouring tiles. 

    def _update_view_game_over(self):
        """Update view for game over state."""
        k = 0 #MK: This will be the index for accessing the list of tiles. 
        for i in range(self.n_rows): #MK: This loop will iterate through each tile in the grid with i and j. 
            for j in range(self.n_cols):
                status = self.tile_status[i, j] #MK: This gets the current status of the tile. 
                tile = self.tiles[k] #MK: This accesses the corresponding tile. 
                if self.is_mine[i, j]: #MK: If the tile contains the mine and,
                    if (i, j) == self.losing_indices: #MK: If the tile is the one where the game was lost, it shows the red background. 
                        tile.image = self.mine_image_red_bg #MK: red background
                    elif self.tile_status[i, j] == Board.TILE_CHECKED: #MK: If the mine was flagged, it puts the flage image onto the tile. 
                        tile.image = self.tile_image.copy()
                        rect = self.flag_image.get_rect(
                            center=tile.image.get_rect().center) #MK: This will position the flag at the center of the tile. 
                        tile.image.blit(self.flag_image, rect.topleft) #MK: This line draws the flag on the tile. 
                    else:
                        tile.image = self.mine_image #MK: Else, it displays the mine image. 
                elif status == Board.TILE_CLOSED: #MK: If the mine was closed, it will keep it as the dafault closed tile image. 
                    tile.image = self.tile_image
                elif status == Board.TILE_OPENED: #MK: If the mine is opened, it displays the corresponding mine count image. 
                    tile.image = self.mine_count_images[self.mine_count[i, j]]
                elif status == Board.TILE_CHECKED: #MK: It displays a crossed mine if the tile was incorrectly flagged. 
                    tile.image = self.mine_image_crossed

                k += 1 #MK: The index will be added to move to the next tile in the list. 

    def _prepare_highlight(self, i_hold, j_hold): #MK: It computes tile indices to highlight as being pressed. 
        """Compute tile indices to highlight as being pressed.

        This happens when the mouse button is held down.
        """
        if i_hold is None or j_hold is None: #MK: If there is no tile being held, it returns an empty set. 
            return set()

        if self.tile_status[i_hold, j_hold] == Board.TILE_CLOSED: #MK: if the tile being held is closed, it will highlight it. 
            return {(i_hold, j_hold)}

        if self.tile_status[i_hold, j_hold] == Board.TILE_CHECKED: #MK: if the tile being held is flagged, there will be no tiles highlighted. 
            return set()

        if self.mine_count[i_hold, j_hold] == 0: #MK: If the tile being has has no adjacent mines, non tiles will be highlighted. 
            return set()

        return {
            (i, j) for i, j in self.get_neighbors(i_hold, j_hold) #MK: For tiles who contain mines, it will compute the set of neighbouring closed tiles to highlight. 
            if self.tile_status[i, j] == Board.TILE_CLOSED
        }

    def _update_view_running(self):
        """Update view in running state."""
        if pygame.mouse.get_pressed()[0]: #MK: It checks if the left mouse is pressed. 
            i_hold, j_hold = self._get_tile_indices_at_mouse() #MK: It gets the tile indices under the mouse cursor. 
            highlight = self._prepare_highlight(i_hold, j_hold) #MK: It determines which tiles should be highlighted based on the tile being held. 
        else:
            highlight = None #MK: If the mouse is not pressed, no tiles will be highlighted. 

        k = 0 #MK: Index for accessing the list of tiles. 
        for i in range(self.n_rows): #MK: This function will iterate over all tiles on the board using i and j indices. 
            for j in range(self.n_cols):
                status = self.tile_status[i, j] #MK: It gets the current status of the tile. 
                tile = self.tiles[k] #MK: This is for accessing the corresponding tile object. 

                if highlight is not None and (i, j) in highlight: #MK: If highlight is not None, the current tile is in the highlight set. 
                    tile.image = self.mine_count_images[0] #MK: It uses the empty image to visualize the location of tile being pressed. 
                    k += 1 #MK: It will move to the next tile by adding the index. 
                    continue

                if status == Board.TILE_CLOSED: #MK: If the tile is closed, it will display the default tile image. 
                    tile.image = self.tile_image
                elif status == Board.TILE_OPENED: #MK: If the tile is opened, it displays the mine image if the tile has a mine. 
                    if self.is_mine[i, j]:
                        tile.image = self.mine_image
                    else:
                        mine_count = self.mine_count[i, j] #MK: Else, it will display the corresponding mine count image. 
                        tile.image = self.mine_count_images[mine_count]
                elif status == Board.TILE_CHECKED: #MK: If the tile is flagged, it puts the flag image on the tile. 
                    tile.image = self.tile_image.copy() #MK: It copies the tile image. 
                    rect = self.flag_image.get_rect(
                        center=tile.image.get_rect().center) #MK: It will locate the image to the center. 
                    tile.image.blit(self.flag_image, rect.topleft) #MK: It draws the flag on the tile. 

                k += 1 #MK: Adds one to process the next tile. 

    def _get_tile_indices_at_mouse(self): #MK: This returns tile indices at the mouse cursor. 
        """Return tile indices at the mouse cursor.

        If mouse cursor is outside of the board region, one or both of the
        indices will be None.
        """
        xm, ym = pygame.mouse.get_pos() #MK: This method returns the x and y position of the mouse cursor. 
        xc, yc = self.rect.topleft #MK: self.rect.topleft provides the top left corner of the game board. 

        i = (ym - yc) // self.tile_size #MK: It calculates the row by determining the number of tile heights is from the top of the board. 
        j = (xm - xc) // self.tile_size #MK: It calculates the column by determining the number of tile widths is from the left of the board. 

        if i < 0 or i >= self.n_rows: #MK: It checks if the row is outside the bounds of the board. 
            i = None #MK: If yes, it will set i to None. 

        if j < 0 or j >= self.n_cols: #MK: It checks if the column is outside the bounds of the board. 
            j = None #MK: If yes, it sets the j to None. 

        return i, j #MK: It returns i and j. 

    def _update_view(self): #MK: This function updates board view. 
        """Update board view."""
        if self.game_status == "game_over": #MK: If the game_status is equal to "game_over", This will update a new board. 
            self._update_view_game_over()
        else:
            self._update_view_running() #MK: Else, this will not update a new board, but keep the current view. 

    def on_mouse_down(self, button): #MK: This function is for mouse button down. 
        """Process mouse button down."""
        if self.game_status in ["before_start", "victory", "game_over"]: #MK: It checks for the game status. 
            return

        if button == RIGHT_BUTTON: #MK: If the right button is clicked, 
            i, j = self._get_tile_indices_at_mouse() #MK: It gets the tile indices under the mourse cursor. 
            if i is not None and j is not None: #MK: It also checks if the mouse is within the board bounds. 
                self._check_tile(i, j) 
                self._update_view() #MK: It will update the board view. 

    def on_mouse_up(self, button):  #MK: This function will be used when mouse is up. 
        """Process mouse button up."""
        if self.game_status in ["victory", "game_over"]: #MK: It checks for the game status. 
            return

        if button == LEFT_BUTTON: #MK: It checks if the left mouse is released. 
            i, j = self._get_tile_indices_at_mouse() #MK: It gets the tile indices under the mouse cursor. 
            if i is not None and j is not None: #MK: It checks if the mouse is within the board bounds. 
                self._open_tile(i, j) #MK: It opens the tile when the mouse is clicked. 
                self._update_view() #MK: It updates the board view. 

    def draw(self, surface): #MK: This function draws a board on surface. 
        """Draw board on surface."""
        # In this case we need to update tiles being pressed due to the mouse
        # hold.
        if self.game_status in ["before_start", "running"]: #MK: If the game is before start or running, 
            if pygame.mouse.get_pressed()[0]: #MK: It will check of the left mouse is pressed, 
                self._update_view_running() #MK: And update the view. 

        bg = self.bg_image.copy() #MK: It creates a copy of background image. 
        self.tiles_group.draw(bg) #MK: It draws all the tiles on copied background. 
        surface.blit(bg, self.rect) #MK: It updates the background with tiles at the location. 
