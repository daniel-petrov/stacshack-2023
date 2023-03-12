import pyautogui as gui

# TODO
# - Add One Time Use Flags to Actions   (pass to superclass)
# - Add Duration Tolerances to Actions  (pass to superclass)
# - Add lookup list of actions
# - Add


class Action:
    """Generic Action"""
    def __init__(self):
        self.width = gui.size()[0]
        self.height = gui.size()[1]
        pass

    def run(self, x, y):
        pass

    def onLeave(self):
        pass


class CustomSequence(Action):
    """Wrapper class for generic sequence of actions."""

    def __init__(self):
        super().__init__()
        self.actions = []

    def addAction(self, new_action):
        self.actions.append(new_action)
        return self

    def run(self, x, y):
        for action in self.actions:
            action.run(x, y)


class MouseMoveToAction(Action):
    """Action that moves mouse to a specified position on the display."""
    def __init__(self):
        super().__init__()

    def run(self, x, y):
        x *= self.width
        y *= self.height
        gui.moveTo(x, y)


class DragToAction(Action):
    """Drags the mouse to a specified position on the display."""
    def __init__(self):
        super().__init__()

    def run(self, x, y):
        x *= self.width
        y *= self.height
        gui.dragTo(x, y)


class MouseUpAction(Action):
    """Simulates releasing the specified mouse button."""
    def __init__(self, button):
        super().__init__()
        self.button = button

    def run(self, x, y):
        gui.mouseUp(button=self.button)


class MouseDownAction(Action):
    """Simulates pushing down the specified mouse button."""
    def __init__(self, button):
        super().__init__()
        self.button = button

    def run(self, x, y):
        gui.mouseDown(button=self.button)


class ClickAction(Action):
    """Clicks the mouse at the current position."""
    def __init__(self):
        super().__init__()

    def run(self, x, y):
        gui.click()


class TypeWordAction(Action):
    """Types a specified word to the keyboard"""
    def __init__(self, word):
        super().__init__()
        self.word = word

    def run(self, x, y):
        gui.write(self.word)


class HotKeyAction(Action):
    """Simulates hot key action with hot keys..."""
    def __init__(self, hotkeys):
        super().__init__()
        self.hotkeys = hotkeys

    def run(self, x, y):
        gui.hotkey(*self.hotkeys)


class PressKeyAction(Action):
    """Simulates hot key action with hot keys..."""
    def __init__(self, key):
        super().__init__()
        self.key = key

    def run(self, x, y):
        gui.press(self.key)



class PlayPauseAction(Action):
    """Presses the Play/Pause button."""
    pass

class ChangeVolumeAction(Action):
    """..."""
    pass


class ScrollAction(Action):
    scroll_clicks = 1  # must be integer

    def __init__(self):
        super().__init__()

    def run(self, x, y):
        if y < 0.25:
            gui.scroll(2 * self.scroll_clicks)
        elif y < 0.5:
            gui.scroll(self.scroll_clicks)
        elif y < 0.75:
            gui.scroll(-self.scroll_clicks)
        else:
            gui.scroll(-2 * self.scroll_clicks)


class OpenApplicationAction(Action):
    pass


