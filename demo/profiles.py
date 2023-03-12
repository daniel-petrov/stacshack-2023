from injector.profile import GestureProfile
from demo.sequences import *

# -- Helper Functions -- #
fingers_L = [1, 1, 0, 0, 0]  # makes letter "L"
fingers_up = [0, 1, 0, 0, 0]
fingers_2up = [0, 1, 1, 0, 0]
fingers_five = [1, 1, 1, 1, 1]
fingers_fist = [0, 0, 0, 0, 0]
fingers_pinky = [0, 0, 0, 0, 1]
fingers_thumb = [1, 0, 0, 0, 0]
known_gestures = [fingers_L, fingers_up, fingers_2up, fingers_five, fingers_fist, fingers_pinky, fingers_thumb]

def fingers_to_gesture(fingers):
    if fingers is None:
        return None

    return ''.join([str(x) for x in fingers])


# -- DEMO PROFILE -- #
demo_profile = GestureProfile("Demo Profile")

# Mouse Movement
demo_profile.addActionSequence((None, fingers_to_gesture(fingers_L)), on_mouse, 'right', False)
demo_profile.addActionSequence((fingers_to_gesture(fingers_L), None), on_mouse, 'left', False)

# Drag Movement
demo_profile.addActionSequence((fingers_to_gesture(fingers_up), None), on_drag, 'left', False)  # Left Click and Drag
demo_profile.addActionSequence((None, fingers_to_gesture(fingers_up)), on_drag, 'right', False)

# Scroll Movement
demo_profile.addActionSequence((fingers_to_gesture(fingers_2up), fingers_to_gesture(fingers_fist)), on_scroll, 'left', False)  # scroll

# Undo/Redo Action
demo_profile.addActionSequence((None, fingers_to_gesture(fingers_pinky)), undo, 'right', True)
demo_profile.addActionSequence((None, fingers_to_gesture(fingers_thumb)), redo, 'right', True)

# Type Word



