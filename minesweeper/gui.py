#BL - Barbara Litvinova
#NM - Nina MAthew
#MK - Minyei Kim


import pygame


LEFT_CLICK = 1 #BL: Assigns the left click of the mouse as a click to 1


def draw_frame(width, height, frame_color): #BL: Creates a rectangular frame on  a surface
    frame = pygame.Surface((width, height), pygame.SRCALPHA) #BL: Creates a surface
    pygame.draw.line(frame, frame_color, (0, 0), (width, 0)) #BL: Creates a horisontal line with 'width' as the length of the line
    pygame.draw.line(frame, frame_color, (0, 0), (0, height)) #BL: Creates a vertical line with 'height' as the length of the line
    pygame.draw.line(frame, frame_color, (width - 1, 0), (width - 1, height)) #BL: Creates lines from the corners 
    pygame.draw.line(frame, frame_color, (0, height - 1), (width, height - 1)) #BL: Creates lines from the corners
    return frame

def draw_crossed_square_with_frame(side, color): #BL: Creates a square frame with a cross
    frame = draw_frame(side, side, color) #BL: Creates a colored frame
    shift = 0.3 * side 
    pygame.draw.line(frame, color,
                     (shift, shift), (side - shift, side - shift)) #BL: Creates an inclined line
    pygame.draw.line(frame, color,
                     (side - shift, shift), (shift, side - shift)) #BL: Creates an inclined line
    return frame

class GUIElement: #BL: Creates a class for all GUI elements assuming there is a frame to display it on. 
#It's using rect to manipulate the rectangular areas (the frame in this case) 
#Uses parameters for a surface: pygame.Surface and Element's surface.
    def __init__(self, surface): #BL: Innit assigns functions to the function properties
    #BL: Self represents instance of the class and acceses the methods in attribute in python 
        self.surface = surface #BL: Accessses the surface variable
        self.rect = self.surface.get_rect() #BL:
    def draw(self, other_surface): #BL: Draws the element in the other surface
    #BL: Self-rect is used for positioning 
        other_surface.blit(self.surface, self.rect) #BL: Draws a source Surface on  a surface

class Label(GUIElement): #BL: Creates a class for text formatting
    def __init__(self, font, font_color, text): #BL: Sets the parameters of the class such as font, color of the text and the actual displayed text string.
        self.font = font #BL: Accesses font variable
        self.font_color = font_color #BL: Accesses font color variable
        super(Label, self).__init__(font.render(text, True, font_color)) #BL: Super function gives access to the parent and a sibling class, initializes the label class. 

    def set_text(self, text): #BL: Sets the way how the text is centered. 
        old_center = self.rect.center #BL: Sets the position of the label
        self.surface = self.font.render(text, True, self.font_color)
        self.rect = self.surface.get_rect(center=old_center)

    def render(self): #BL: Returns surface to the display
        return self.surface


class Button(GUIElement): #BL:Creates a class for a button - a text in a frame

    def __init__(self, font, font_color, text, on_click_callback, #BL: Sets specific measurements of the button + sets the measurements of the text, font
                 frame_color=None):
        self.text = font.render(text, True, font_color) #BL: Renders text into a graphical object
        margin = 1.5 * font.size("_")[0] #BL: Sets the frame margin thickness realted to the font size
        if frame_color is None: #BL: If there's not font color, it sets the font color to the frame color
            frame_color = font_color 

        surface = draw_frame(self.text.get_width() + margin, #BL: Creates another frame around the button
                             1.2 * self.text.get_height(), #BL: Control the height and the color of the frame 
                             frame_color)
        super(Button, self).__init__(surface) #BL: Gives an access from the button to the surface
        rect = self.text.get_rect(center=self.rect.center) #BL: Centers the button in the frame
        self.surface.blit(self.text, rect.topleft) #BL: Locates the text on the top left of the button
        self.on_click_callback = on_click_callback #BL: Calls for the an action when the button is clicked

    def on_mouse_up(self, button): #BL: Handles the mouse button up
        if button != LEFT_CLICK or self.on_click_callback is None: #BL: When the left mouse button is clicked, function calls for an action
            return

        if self.rect.collidepoint(*pygame.mouse.get_pos()): #BL: When  the mouse button is clicked, function detects if it happened on a buttton
            self.on_click_callback()


class SelectionGroup(GUIElement): #BL: Creates a class for selection of options
    def __init__(self, font, font_color,
                 title, options,
                 on_change_callback=None,
                 initial_value=None):
        item_size = font.get_height() #BL: Height of the text is ised as the size of the frame

        self.unselected_image = draw_frame(item_size, item_size,
                                           font_color) #BL: Function draws another frame with the size of the inserted picture.
        self.selected_image = draw_crossed_square_with_frame(item_size,
                                                             font_color) #BL:Function creates a crossed square with a frame with the size of the picture.

        self.options = options #BL: Function calls the same options as before
        self.n_options = len(options) #BL: Function calls the length of the option

        self.title_image = font.render(title, True, font_color) #BL: Renders the title 
        option_images = [font.render(option, True, font_color)
                         for option in options] #BL: Creates  a loop which goes for every string in the options and creates a surface

        item_widths = [1.5 * item_size + option_image.get_width() 
                       for option_image in option_images] #BL: Calculates the total width of the items 
        width = max(max(item_widths), self.title_image.get_width()) #BL: Calculates the maximum width
        height = (self.title_image.get_height()
                  + 0.5 * item_size
                  + 1.5 * item_size * self.n_options) #BL: Calculates the height of the items

        super(SelectionGroup, self).__init__(pygame.Surface((width, height),
                                                            pygame.SRCALPHA))
        title_rect = self.title_image.get_rect(centerx=self.rect.centerx) #BL: Calls the parent function and positions the inage title

        self.button_rects = [] 
        self.item_rects = []
        option_rects = []
        y = title_rect.bottom + 0.5 * item_size
        for option_image, item_width in zip(option_images, item_widths): #BL: Creates a loop which positions the button and the text
            button_rect = self.unselected_image.get_rect(y=y)
            option_rect = option_image.get_rect(
                x=button_rect.right + 0.5 * button_rect.width,
                centery=button_rect.centery)
            item_rect = pygame.Rect(0, y, item_width, item_size)
            self.button_rects.append(button_rect)
            option_rects.append(option_rect)
            self.item_rects.append(item_rect)
            y += 1.5 * item_size

        self._selected = 0 
        if initial_value is not None:
            for i, option in enumerate(self.options):
                if option == initial_value:
                    self._selected = i
                    break

        self.callback = on_change_callback

        self.surface_stub = pygame.Surface((width, height), pygame.SRCALPHA) #BL: Uses pygame to create transparent surface to display transparent pixels.
        self.surface_stub.fill((0, 0, 0, 0)) #BL: Calls the surface and makes it transparent
        self.surface_stub.blit(self.title_image, title_rect.topleft)
        for option_rect, option_image in zip(option_rects, option_images): #BL: Loop goes throught rect and lets display it.
            self.surface_stub.blit(option_image, option_rect)
        self._render()

    @property #BL: '@' works as a decorator and grants the function special property
    def selected(self): 
        return self.options[self._selected]

    def _render(self): #BL: Function is responsible for rendering of the surfaces and objects
        self.surface.fill((0, 0, 0, 0)) 
        self.surface.blit(self.surface_stub, (0, 0))
        for i, rect in enumerate(self.button_rects):  #BL: Loop goes through the list of button positioning
            if i == self._selected: #BL: Loop goes through selected button
                self.surface.blit(self.selected_image, rect)
            else:
                self.surface.blit(self.unselected_image, rect)

    def on_mouse_up(self, button):
        if button != LEFT_CLICK:
            return

        mouse_pos = pygame.mouse.get_pos() #BL: When the button is left-clicked, function is triggered, callback function is used.
        x = mouse_pos[0] - self.rect.left #BL: Calls for the position of the mouse in the rectangular(left-right)
        y = mouse_pos[1] - self.rect.top #BL: Calls for the position fo the mouse in the rectangular (top-bottom)
        selected_old = self._selected
        for i, (button_rect, item_rect) in enumerate( #BL: Loop goes through two lists
                zip(self.button_rects, self.item_rects)): #BL: Combines two lists 
            if item_rect.collidepoint(x, y):
                if self.callback is not None and i != self._selected:
                    self.callback(self.options[i])
                self._selected = i
                break

        if self._selected != selected_old: #BL: Compares old and new index
            self._render() #BL:Compares two indexes between each other


class Input(GUIElement): #BL: Class for a text input. 
    
    def __init__(self, font, font_color, title, value, delimiter="  ", #BL: Function calls the visual elements, makes them visibile?
                 frame_color=None, active_input=False,
                 width=None, max_value_length=None, key_filter=None,
                 on_enter_callback=None):
        self.font = font
        self.font_color = font_color
        self.width = width
        self._active_input = active_input
        self.in_input = False
        self.title = title
        self.value = str(value)
        self.current_value = self.value
        self.delimiter = delimiter
        if frame_color is None:
            frame_color = font_color
        self.frame_color = frame_color
        self.max_value_length = max_value_length
        self.key_filter = key_filter
        self.on_enter_callback = on_enter_callback

        self.surface = None
        self.text = None
        self.boarder = None
        self.text_rect = None
        self.value_rect = None
        self.rect = None
        self._render()
        super(Input, self).__init__(self.surface) 

    def _render(self): #BL: Prepares data for render if necessary
        value = self.current_value
        if self.in_input:
            value += '_'

        text = self.font.render(self.title + self.delimiter + value, #BL: Prepares text for render
                                True,
                                self.font_color)

        if self.width is None:
            width = text.get_width() #BL: Calls for width, If there's no width initialized, uses the width of the text
        else:
            width = self.width
        height = text.get_height()
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        text_rect = text.get_rect(center=surface.get_rect().center)

        title_width = self.font.size(self.title + self.delimiter)[0]
        value_width, value_height = self.font.size(value)
        margin = self.font.size('|')[0]
        value_rect = pygame.Rect(text_rect.left + title_width - margin,
                                 text_rect.top,
                                 value_width + 2 * margin,
                                 value_height)

        if self._active_input:  #BL: Creates a rectangular frame and calls for the surface
            frame = draw_frame(value_rect.width,
                               value_rect.height,
                               self.frame_color)
            surface.blit(frame, value_rect)
        surface.blit(text, text_rect)
        self.surface = surface
        self.value_rect = value_rect
        if self.rect is not None:
            self.rect.size = surface.get_size()

    @property #BL: Calls the active _input function
    def active_input(self):
        return self._active_input

    @active_input.setter
    def active_input(self, value):
        if value != self._active_input:
            self._active_input = value
            self._render()

    def set_value(self, value): #BL: Calls the previous value and sets it again, then renderd it
        value = str(value)
        self.current_value = value
        self.value = self.current_value
        self._render()

    def on_mouse_up(self, button):
        if not self._active_input or button != LEFT_CLICK: #BL: When the button is left-clicked, an action is commited
            return

        mouse_pos = pygame.mouse.get_pos() #BL: Calculates the position on the mouse on the screen
        x = mouse_pos[0] - self.rect.x 
        y = mouse_pos[1] - self.rect.y

        if self.value_rect.collidepoint(x, y): #BL: Checks if the mouse positon is within the rectangular. Yes=true, No=false
            self.in_input = True
        else:
            self.in_input = False
            self.current_value = self.value

        self._render()

    def on_key_down(self, event): #BL: Id self input is true, the key is handled down
        if not self.in_input:
            return

        key = event.key
        if key == pygame.K_BACKSPACE: #BL: If key is held down with the backspace key, it calls for a current input value and updates it 
            if self.current_value:
                self.current_value = self.current_value[:-1]
                self._render()
        elif key == pygame.K_RETURN: #BL: If key is held down with the return key, it calls for a current input value and updates it 
            self.in_input = False
            if self.on_enter_callback is not None:
                new_value = str(self.on_enter_callback(self.current_value))
            else:
                new_value = self.current_value
            self.set_value(new_value)
            self._render()
        else:
            if len(self.current_value) == self.max_value_length: #BL: If the length of the updated current value overexceeeds the maximum length, it is nor taken into account
                return

            key_name = event.unicode
            if self.key_filter is None or self.key_filter(key_name): #BL: Filter applied to a key and gets updated
                self.current_value += key_name
                self._render()


class InputDialogue(GUIElement): #BL: A class for the design of the Dialogue Window

    def __init__(self, font, font_color, title, on_enter_callback,
                 max_length=None, key_filter=None):
        self.font = font
        self.font_color = font_color
        self.title_image = font.render(title, True, font_color)
        line_height = font.get_height()
        vertical_margin = 0.5 * line_height
        horizontal_margin = font.size("_")[0]

        width = self.title_image.get_width() + 2 * horizontal_margin #BL: Adjusts the width b y the width of the image
        height = 3 * vertical_margin + 2 * line_height

        super(InputDialogue, self).__init__(draw_frame(width, height,
                                                       self.font_color))

        self.title_image_rect = self.title_image.get_rect(x=horizontal_margin,
                                                          y=vertical_margin)

        self.rect = self.surface.get_rect()

        self.value_top = 2 * vertical_margin + line_height

        self.value = ""
        self.on_enter_callback = on_enter_callback
        self.max_length = max_length
        self.key_filter = key_filter

        self._render()

    def _render(self): #BL: Updates the Dialogue Window for necessary changes
        width, height = self.surface.get_size()
        self.surface = draw_frame(width, height, self.font_color)
        self.surface.blit(self.title_image, self.title_image_rect)
        value_image = self.font.render(self.value + "_", True, self.font_color)
        rect = value_image.get_rect(top=self.value_top,
                                    centerx=0.5 * self.surface.get_width())
        self.surface.blit(value_image, rect)

    def set_value(self, value): #BL: Updates the set value
        self.value = value
        self._render()

    def on_key_down(self, event): 
        key = event.key
        if key == pygame.K_BACKSPACE:
            if self.value:
                self.value = self.value[:-1]
                self._render()
                self._render()
        elif key == pygame.K_RETURN:
            self.on_enter_callback(self.value)
        else:
            if (self.max_length is not None
                    and len(self.value) == self.max_length):
                return

            key_name = event.unicode
            if self.key_filter is None or self.key_filter(key_name):
                self.value += key_name
                self._render()
