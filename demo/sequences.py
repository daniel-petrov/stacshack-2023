from injector.profile import GestureProfile
from injector.action import *

action_list = {}
action_is_singleton = {}

# MOUSE ACTION
on_mouse = CustomSequence()
on_mouse.addAction(MouseUpAction('left'))
on_mouse.addAction(MouseMoveToAction())

action_list["MOUSE_MOVE"] = on_mouse
action_is_singleton["MOUSE_MOVE"] = False

# DRAG ACTION
on_drag = CustomSequence()
on_drag.addAction(MouseDownAction('left'))
on_drag.addAction(MouseMoveToAction())

action_list["DRAG_MOVE"] = on_drag
action_is_singleton["DRAG_MOVE"] = False

# SCROLL ACTION
on_scroll = CustomSequence()
on_scroll.addAction(ScrollAction())

action_list["SCROLL_ACTION"] = on_scroll
action_is_singleton["SCROLL_ACTION"] = False

# UNDO ACTION
undo = CustomSequence()
undo.addAction(HotKeyAction(('ctrl', 'z')))

action_list["UNDO_ACTION"] = undo
action_is_singleton["UNDO_ACTION"] = True

# REDO ACTION
redo = CustomSequence()
redo.addAction(HotKeyAction(('ctrl', 'shiftleft', 'z')))

action_list["REDO_ACTION"] = undo
action_is_singleton["REDO_ACTION"] = True

# VOLUME UP
vol_up_single = CustomSequence()
vol_up_single.addAction(HotKeyAction(('volumeup')))

action_list["VOL_UP_ACTION"] = vol_up_single
action_is_singleton["VOL_UP_ACTION"] = True

# VOLUME_DOWN
vol_down_single = CustomSequence()
vol_down_single.addAction(HotKeyAction(('volumedown')))

action_list["VOL_DOWN_ACTION"] = vol_down_single
action_is_singleton["VOL_DOWN_ACTION"] = True


# POETRY
poetry = CustomSequence()
poetry.addAction(HotKeyAction(('ctrl', 't')))
poetry.addAction(TypeWordAction("https://www.youtube.com/watch?v=xvFZjo5PgG0"))
poetry.addAction(PressKeyAction('enter'))

action_list["CULTURE"] = poetry
action_is_singleton["CULTURE"] = True


# PRESS ENTER
enter = CustomSequence()
enter.addAction(PressKeyAction('enter'))

action_list["PRESS_ENTER"] = enter
action_is_singleton["PRESS_ENTER"] = enter

# CLOSE WINDOW?


# SCREENSHOT


#

