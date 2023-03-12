import pyautogui as gui

from injector.action import Action


class GestureProfile:

    ## -- Constructors -- ##
    def __init__(self, name):
        self.name = name  # Name of Gesture Profile
        self.actions = {}  # TODO Change to Array for Performance?
        self.disp_x = gui.size()[0]
        self.disp_y = gui.size()[1]

        self.prev_gesture_pair = (None, None)
        self.prev_action = None

    ## -- Gesture Profile Methods -- ##
    def processGesture(self, gesture_pair, xl, yl, xr, yr):
        action, control_hand, is_singleton = self.actions.get(gesture_pair, (None, None, False))

        if action is not None:

            # Do not repeat singleton gestures
            if not (is_singleton and gesture_pair == self.prev_gesture_pair):
                # Get Coordinates of Control Hand
                x, y = (xr, yr) if control_hand == 'right' else (xl, yl)

                action.run(x, y)

        self.prev_action = action
        self.prev_gesture_pair = gesture_pair


    def addActionSequence(self, gesture_pair, action, control_hand, is_singleton):
        self.actions[gesture_pair] = (action, control_hand, is_singleton)
        return self

    def removeActionSequence(self, gesture_pair):
        self.actions.pop(gesture_pair, None)

    def updateDisplaySize(self):
        self.disp_x, self.disp_y = gui.size()
