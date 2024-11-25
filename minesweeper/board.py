#Minyei Kim - MK
#Nina Mathew - NM
#Barbara Litvinova - BL

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
        if n_mines is not None:
            self.n_mines = n_mines

        if n_rows is not None or n_cols is not None:
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
        allowed_positions = []
        n_tiles = self.n_rows * self.n_cols
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if any((
                    abs(i - i_click) > 1 or abs(j - j_click) > 1,
                    self.n_mines > n_tiles - 9
                    and (i != i_click or j != j_click),
                    self.n_mines == self.n_rows * self.n_cols
                )):
                    allowed_positions.append((i, j))

        selected_positions = numpy.asarray(random.sample(allowed_positions,
                                                         self.n_mines))
        self.is_mine[selected_positions[:, 0], selected_positions[:, 1]] = True

        self.mine_count = numpy.zeros((self.n_rows, self.n_cols),
                                      dtype=numpy.int8)

        for i, j in selected_positions:
            ind = self._get_neighbors_flat(i, j)
            self.mine_count.flat[ind] += 1

    def get_neighbors(self, i, j):
        """Return pairs of indices of neighbor cells."""
        ret = []

        if i > 0:
            ret.append((i - 1, j))
            if j > 0:
                ret.append((i - 1, j - 1))
            if j < self.n_cols - 1:
                ret.append((i - 1, j + 1))

        if j > 0:
            ret.append((i, j - 1))

        if j < self.n_cols - 1:
            ret.append((i, j + 1))

        if i < self.n_rows - 1:
            ret.append((i + 1, j))
            if j > 0:
                ret.append((i + 1, j - 1))
            if j < self.n_cols - 1:
                ret.append((i + 1, j + 1))

        return ret

    def _get_neighbors_flat(self, i, j):
        """Return indices of neighbor cells as a single number."""
        return [k * self.n_cols + l for (k, l) in self.get_neighbors(i, j)]

    def _open_tiles(self, i, j):
        """Open tiles on click using the wave algorithm."""
        queue = deque()
        queue.append((i, j))
        self.tile_status[i, j] = self.TILE_OPENED
        self.tiles_to_open -= 1

        while queue:
            i, j = queue.popleft()
            if self.mine_count[i, j] > 0:
                continue

            neighbors = self.get_neighbors(i, j)
            for k, l in neighbors:
                if self.tile_status[k, l] == self.TILE_CLOSED:
                    self.tile_status[k, l] = self.TILE_OPENED
                    self.tiles_to_open -= 1
                    queue.append((k, l))

        if self.tiles_to_open == 0:
            self._change_game_status("victory")
            self.n_mines_left = 0
            self.tile_status[self.is_mine] = self.TILE_CHECKED

    def _check_tile(self, i, j):
        """Check tile with a flag (right click action)."""
        if self.tile_status[i, j] == self.TILE_CLOSED:
            self.tile_status[i, j] = self.TILE_CHECKED
            self.n_mines_left -= 1
        elif self.tile_status[i, j] == self.TILE_CHECKED:
            self.tile_status[i, j] = self.TILE_CLOSED
            self.n_mines_left += 1

    def _open_tile(self, i, j): #MK: This function opens tile. 
        """Open tile (left click action)."""
        status = self.tile_status[i, j]
        if status == self.TILE_CHECKED:
            return

        if self.is_mine[i, j]:
            self._change_game_status("game_over")
            self.losing_indices = (i, j)
            self.tile_status[i, j] = self.TILE_OPENED
            return

        if status == self.TILE_CLOSED:
            if self.game_status == "before_start":
                self._put_mines(i, j)
                self.start_time = pygame.time.get_ticks()
                self._change_game_status("running")
            self._open_tiles(i, j)
            return

        if self.mine_count[i, j] == 0:
            return

        neighbors = self.get_neighbors(i, j)
        checked_count = sum(self.tile_status[k, l] == self.TILE_CHECKED
                            for k, l in neighbors)
        if checked_count == self.mine_count[i, j]:
            for k, l in neighbors:
                if self.tile_status[k, l] == self.TILE_CLOSED:
                    if self.is_mine[k, l]:
                        self.losing_indices = (k, l)
                        self._change_game_status("game_over")
                        self.tile_status[k, l] = self.TILE_OPENED
                        return

                    self._open_tiles(k, l)

    def _update_view_game_over(self):
        """Update view for game over state."""
        k = 0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                status = self.tile_status[i, j]
                tile = self.tiles[k]
                if self.is_mine[i, j]:
                    if (i, j) == self.losing_indices:
                        tile.image = self.mine_image_red_bg
                    elif self.tile_status[i, j] == Board.TILE_CHECKED:
                        tile.image = self.tile_image.copy()
                        rect = self.flag_image.get_rect(
                            center=tile.image.get_rect().center)
                        tile.image.blit(self.flag_image, rect.topleft)
                    else:
                        tile.image = self.mine_image
                elif status == Board.TILE_CLOSED:
                    tile.image = self.tile_image
                elif status == Board.TILE_OPENED:
                    tile.image = self.mine_count_images[self.mine_count[i, j]]
                elif status == Board.TILE_CHECKED:
                    tile.image = self.mine_image_crossed

                k += 1

    def _prepare_highlight(self, i_hold, j_hold):
        """Compute tile indices to highlight as being pressed.

        This happens when the mouse button is held down.
        """
        if i_hold is None or j_hold is None:
            return set()

        if self.tile_status[i_hold, j_hold] == Board.TILE_CLOSED:
            return {(i_hold, j_hold)}

        if self.tile_status[i_hold, j_hold] == Board.TILE_CHECKED:
            return set()

        if self.mine_count[i_hold, j_hold] == 0:
            return set()

        return {
            (i, j) for i, j in self.get_neighbors(i_hold, j_hold)
            if self.tile_status[i, j] == Board.TILE_CLOSED
        }

    def _update_view_running(self):
        """Update view in running state."""
        if pygame.mouse.get_pressed()[0]:
            i_hold, j_hold = self._get_tile_indices_at_mouse()
            highlight = self._prepare_highlight(i_hold, j_hold)
        else:
            highlight = None

        k = 0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                status = self.tile_status[i, j]
                tile = self.tiles[k]

                if highlight is not None and (i, j) in highlight:
                    tile.image = self.mine_count_images[0]
                    k += 1
                    continue

                if status == Board.TILE_CLOSED:
                    tile.image = self.tile_image
                elif status == Board.TILE_OPENED:
                    if self.is_mine[i, j]:
                        tile.image = self.mine_image
                    else:
                        mine_count = self.mine_count[i, j]
                        tile.image = self.mine_count_images[mine_count]
                elif status == Board.TILE_CHECKED:
                    tile.image = self.tile_image.copy()
                    rect = self.flag_image.get_rect(
                        center=tile.image.get_rect().center)
                    tile.image.blit(self.flag_image, rect.topleft)

                k += 1

    def _get_tile_indices_at_mouse(self):
        """Return tile indices at the mouse cursor.

        If mouse cursor is outside of the board region, one or both of the
        indices will be None.
        """
        xm, ym = pygame.mouse.get_pos()
        xc, yc = self.rect.topleft

        i = (ym - yc) // self.tile_size
        j = (xm - xc) // self.tile_size

        if i < 0 or i >= self.n_rows:
            i = None

        if j < 0 or j >= self.n_cols:
            j = None

        return i, j

    def _update_view(self):
        """Update board view."""
        if self.game_status == "game_over":
            self._update_view_game_over()
        else:
            self._update_view_running()

    def on_mouse_down(self, button):
        """Process mouse button down."""
        if self.game_status in ["before_start", "victory", "game_over"]:
            return

        if button == RIGHT_BUTTON:
            i, j = self._get_tile_indices_at_mouse()
            if i is not None and j is not None:
                self._check_tile(i, j)
                self._update_view()

    def on_mouse_up(self, button):
        """Process mouse button up."""
        if self.game_status in ["victory", "game_over"]:
            return

        if button == LEFT_BUTTON:
            i, j = self._get_tile_indices_at_mouse()
            if i is not None and j is not None:
                self._open_tile(i, j)
                self._update_view()

    def draw(self, surface):
        """Draw board on surface."""
        # In this case we need to update tiles being pressed due to the mouse
        # hold.
        if self.game_status in ["before_start", "running"]:
            if pygame.mouse.get_pressed()[0]:
                self._update_view_running()

        bg = self.bg_image.copy()
        self.tiles_group.draw(bg)
        surface.blit(bg, self.rect)
