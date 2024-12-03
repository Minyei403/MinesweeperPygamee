#MK - Minyei Kim
#NM - Nina Mathew
#BL - Barbara Litvinova

import pygame #MK: Import pygame to access pygame


class Leaderboard:
    
    """Store, update and display leaderboard.

    Parameters
    ----------
    font : pygame.Font
        Font to use.
    font_color : pygame.Color compatible
        Font color.
    max_items : int
        Maximum number of items to store for each difficulty.
    width : int
        Total width of the leaderboard.
    data : dict
        Dictionary with keys 'EASY', 'NORMAL', 'HARD', for each key there is
        a list of (name, time) tuples describing player results.
        If None (default), create empty dictionary.
    """
    def __init__(self, font, font_color, max_items, width,
                 data=None): #MK: This is a function to store the parameters. 
        self.font = font #MK: This is the font.
        self.font_color = font_color #MK: This is the font colour. 
        self.max_items = max_items  #MK: Maximum number of items to store for each difficulty. 

        self.section_width = width // 3 #MK: This divides the toal width into three sectins for each difficulty. 
        self.text_height = font.get_height() #MK: This is to calculate the height of the font. 
        self.horizontal_margin = 2 * font.size("|")[0] #MK: The width of 2 of | for margin. 
        self.vertical_margin = 0.5 * self.text_height #MK: This is the half the text heights as vertical margin. 

        self.width = 3 * self.section_width #MK: Finding the total width that spans three sections to calculate the total leaderboard dimensions. 
        self.height = ((4 + max_items) * self.vertical_margin #MK: Top and bottom margins
                       + (2 + max_items) * self.text_height) #MK: Titles and leaderboard entries. 

        self.surface = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA) #MK: SRCALPHA tells a newly created surface to create a transparent surface to measure the length. 
        self.rect = self.surface.get_rect() #MK: This will get rectangular bounds of the surface. 
        
        #MK: Title for each difficulty level. 
        self.title = font.render("LEADER BOARD", True, font_color)
        self.easy_title = font.render("EASY", True, font_color)
        self.normal_title = font.render("NORMAL", True, font_color)
        self.hard_title = font.render("Prof. Pendar", True, font_color)
        self.list_start_y = (self.vertical_margin + 2 * self.text_height
                             + self.text_height + self.vertical_margin)
        #MK: It calculates the starting y coordinate for leaderboard entries. 
        if data is None: #MK: Initialize leaderboard data. 
            self.data = {'EASY': [], 'NORMAL': [], 'Prof. Pendar': []} #MK: If no data is provided, intialize empty lists for each difficulty level. 
        else:
            self.data = data #MK: It uses the data. 

        self._prepare_render() #MK: Prepare to render the initial state of the leaderboard. 
        pygame.init()
        
    def _prepare_surface(self):
        """Prepare surface with all titles."""
        self.surface.fill((0, 0, 0, 0)) #MK: Fill the surface with a transparent colour to reset it. 

        title_top = self.vertical_margin #MK: Define positions for titles and lines. 
        section_titles_top = title_top + 2 * self.text_height
        line_top = section_titles_top + self.text_height

        frame_x = 0 #MK: Draw the border and section dividers. 
        frame_y = title_top + self.text_height + self.vertical_margin
        pygame.draw.line(self.surface, self.font_color,
                         (frame_x, frame_y),
                         (self.width, frame_y)) #MK: This is the top horizontal line. 
        pygame.draw.line(self.surface, self.font_color,
                         (frame_x, frame_y),
                         (frame_x, self.height)) #MK: This is the left vertical line. 
        pygame.draw.line(self.surface, self.font_color,
                         (self.width - 1, frame_y),
                         (self.width - 1, self.height)) #MK: This is the right vertical line. 
        pygame.draw.line(self.surface, self.font_color,
                         (frame_x, self.height - 1),
                         (self.width, self.height - 1)) #MK: This is the bottom horizontal line. 
        pygame.draw.line(self.surface, self.font_color, #MK: This draws the vertical dividers between sections. 
                         (self.section_width, line_top),
                         (self.section_width,
                          self.height - self.vertical_margin))
        pygame.draw.line(self.surface, self.font_color,
                         (2 * self.section_width, line_top),
                         (2 * self.section_width,
                          self.height - self.vertical_margin))

        title_rect = self.title.get_rect( #MK: Position titles for the leaderboard and each difficulty section. 
            top=self.vertical_margin, centerx=0.5 * self.width)
        easy_title_rect = self.easy_title.get_rect(
            top=section_titles_top, centerx=0.5 * self.section_width)
        normal_title_rect = self.normal_title.get_rect(
            top=section_titles_top, centerx=1.5 * self.section_width)
        hard_title_rect = self.hard_title.get_rect(
            top=section_titles_top, centerx=2.5 * self.section_width)

        self.surface.blit(self.title, title_rect)
        self.surface.blit(self.easy_title, easy_title_rect)
        self.surface.blit(self.normal_title, normal_title_rect)
        self.surface.blit(self.hard_title, hard_title_rect)

    def _prepare_render(self):
        """Prepare surface to render."""
        self._prepare_surface() #MK: This calls to prepare titles and section dividers. 
        x_name = self.horizontal_margin #MK: Define intial x coordinates for name and time columns. 
        x_time = self.section_width - self.horizontal_margin
        for difficulty in ["EASY", "NORMAL", "HARD"]: #MK: Loop through difficulty levels to render leaderboard entries. 
            y = self.list_start_y #MK: Starting y coordinates for entries. 
            for name, time in self.data[difficulty]: #MK: Render the name and time as images. 
                name_image = self.font.render(name, True, self.font_color)
                score_image = self.font.render(str(time), True, self.font_color)
                time_width = self.font.size(str(time))[0] #MK: Calculate width of the time string. 
                self.surface.blit(name_image, (x_name, y)) #MK: Blit the name and time onto the surface. 
                self.surface.blit(score_image,
                                  (x_time - time_width, y))
                y += self.text_height + self.vertical_margin #MK: This will move to the next line. 

            x_name += self.section_width #MK: Move x coordinates to the next section.
            x_time += self.section_width

    def needs_update(self, difficulty, time):
        """Check whether the leaderboard needs to be updated."""
        if difficulty not in self.data:
            return False #MK: Invalid difficulty level will return False. 

        data = self.data[difficulty]
        if len(data) < self.max_items: #MK: This provides room for more entries. 
            return True

        return data[-1][1] > time #MK: This checks if the new time is better than the worst. 

    def update(self, difficulty, name, time):
        """Update the leaderboard."""
        if difficulty not in self.data:
            return #MK: Ignore invalid difficulty levels. 

        data = self.data[difficulty]
        i = 0 #MK: Find the correct position to insert the new score. 
        while i < len(data) and time >= data[i][1]:
            i += 1
        data.insert(i, (name, time)) #MK: This will insert the new entry. 

        if len(data) > self.max_items:
            data.pop()

        self._prepare_render() #MK: Re render the leaderboard. 

    def draw(self, surface): #This is a function that draws on the surface. 
        """Draw on the surface."""
        surface.blit(self.surface, self.rect)
        