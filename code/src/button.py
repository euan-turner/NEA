import pygame

class Button():
    """Redefine a generic button class, and inheriting block, text and image button classes
    """

    def __init__(self, rect : pygame.Rect, default : pygame.Surface,
            hovered : pygame.Surface, code : int):
        """Constructor method for a button
        Requires default, hovered, and clicked surface to be preconstructed

        Args:
            rect (pygame.Rect): Position and dimensions of button on surface
            default (pygame.Surface): Image surface of button as default
            hovered (pygame.Surface): Image surface of button when hovered
            code (int): Code to identify button
        """
        self.rect = rect
        self.default = default
        self.hovered_surface = hovered
        self.hovered = False
        self.clicked = False
        self.code = code

    def check_click(self, event : pygame.event, window : pygame.Surface, background : tuple) -> tuple:
        """Check if button has been clicked

        Args:
            event (pygame.event): Event instance, only passing in mousedown
                events will be more efficient
            window (pygame.Surface): Surface buttons exists on
            background (tuple): Background colour to wipe with before blit

        Returns:
            int: Code to identify button
        """
        if self.rect.collidepoint(event.pos) and not self.clicked:
            self.clicked = True
            return self.code
        else:
            return None

    def check_hover(self):
        """Checks if mouse is hovering over button
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def update(self, window : pygame.Surface, background : tuple):
        """Updates the buttons appearance in the window
        Should be called every frame for each button

        Args:
            window (pygame.Surface): Surface button exists on
            background (tuple): Background colour to wipe with before blit
        """
        self.check_hover()
        if self.hovered:
            self.clear(window, background)
            window.blit(self.hovered_surface, self.rect)
        else:
            self.clear(window, background)
            window.blit(self.default, self.rect)
        pygame.display.flip()

    def clear(self, window : pygame.Surface, background : tuple):
        """Clears the button's pixels from the screen

        Args:
            window (pygame.Surface): Surface buttons exists on
            background (tuple): Background colour to wipe with
        """
        window.fill(background, self.rect)