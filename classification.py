import cv2
from cvzone.HandTrackingModule import HandDetector

import pyautogui as gui

gui.FAILSAFE = False
gui.PAUSE = 0

import tkinter as tk
from GUI.my_gui import Application

from injector.profile import GestureProfile

from demo.profiles import demo_profile
from demo.sequences import action_list, action_is_singleton

# variables
width, height = 1280, 720
# to define inner rectangle where mouse is valid
mouse_offset_1 = 50
mouse_offset_2 = 200

# camera setup
cap = cv2.VideoCapture(0)  # 0 = id for webcam
cap.set(3, width)
cap.set(4, height)

# hand detector
detector = HandDetector(maxHands=2, detectionCon=0.8)

current_fingers = []

fingers_L = [1, 1, 0, 0, 0]  # makes letter "L"
fingers_up = [0, 1, 0, 0, 0]
fingers_2up = [0, 1, 1, 0, 0]
fingers_five = [1, 1, 1, 1, 1]
fingers_fist = [0, 0, 0, 0, 0]
fingers_pinky = [0, 0, 0, 0, 1]
fingers_thumb = [1, 0, 0, 0, 0]
known_gestures = [fingers_L, fingers_up, fingers_2up, fingers_five, fingers_fist, fingers_pinky, fingers_thumb]


def camera():
    left_gesture, right_gesture, left_anchor, right_anchor = None, None, (-1, -1), (-1, -1)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 1 for horizontal axis (to flip)
        hands, img = detector.findHands(img, flipType=False)

        tip = [0, 0, 0]
        current_gesture = "none"

        if hands:
            # Extract Hands
            left_hand, right_hand = get_hands(hands)

            left_gesture, left_anchor = process_hand(left_hand)
            right_gesture, right_anchor = process_hand(right_hand)

        img = cv2.rectangle(img, (mouse_offset_1, mouse_offset_1), (width - mouse_offset_2, height - mouse_offset_2),
                            (255, 0, 0), 2)

        yield img, left_gesture, right_gesture, left_anchor, right_anchor

        key = cv2.waitKey(1)
        if key == ord('q'):
            # end program
            break


def process_hand(hand):
    if hand != None:
        fingers = detector.fingersUp(hand)
        fingers[0] = 1 - fingers[0]

        gesture = fingers_to_gesture(fingers)
        anchor = hand_to_anchor(hand, gesture)

    else:
        gesture = None
        anchor = (-1, -1)

    return gesture, anchor


def hand_to_anchor(hand, gesture):
    # TODO Return different anchor for different gestures
    # if gesture == "zoom":
    #     return
    return hand['lmList'][8][0:2]


def within_rectangle(x, y, offsets=None, width=width, height=height) -> bool:
    if offsets is None:
        offsets = [mouse_offset_1, mouse_offset_2]
    return offsets[0] <= x <= width - offsets[1] and offsets[0] <= y <= height - offsets[1]


def scale_coords(x, y, offsets=None, width=width, height=height) -> tuple:
    if offsets is None:
        offsets = [mouse_offset_1, mouse_offset_2]
    rectangle_width = width - offsets[0] - offsets[1]
    rectangle_height = height - offsets[0] - offsets[1]
    return (x - offsets[0]) / rectangle_width, (y - offsets[0]) / rectangle_height


def get_hands(hands):
    left_hand = None
    right_hand = None

    for i in range(len(hands)):
        if hands[i]['type'] == 'Left':
            left_hand = hands[i]
        elif hands[i]['type'] == 'Right':
            right_hand = hands[i]

    return left_hand, right_hand


def fingers_to_gesture(fingers):

    if fingers is None:
        return None

    return ''.join([str(x) for x in fingers])

def gesture_info_to_profile(gesture_info):

    gesture_profile = GestureProfile("GUI Profile")

    for info in gesture_info:
        gesture_profile.addActionSequence(
            (fingers_to_gesture(info['LeftFingers']), fingers_to_gesture(info['RightFingers'])),
            action_list[info['FunctionOption']],
            info['ControlHand'],
            action_is_singleton[info['FunctionOption']]
        )

    return gesture_profile



# -- Main Testing Section -- #

# Run GUI
run_gui = True

if run_gui:
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

    gesture_info = app.get_gesture_info()
    gesture_profile = gesture_info_to_profile(gesture_info)
else:
    gesture_profile = demo_profile

for obj in camera():
    cv2.imshow('Camera', obj[0])
    left_gesture, right_gesture, left_anchor, right_anchor = obj[1:]

    xl, yl = left_anchor
    xr, yr = right_anchor

    if within_rectangle(xl, yl) or within_rectangle(xr, yr):
        xl, yl = scale_coords(xl, yl)
        xr, yr = scale_coords(xr, yr)

        # print("x: {}, y: {}".format(round(x, 3), round(y, 3)))
        gesture_profile.processGesture((left_gesture, right_gesture), xl, yl, xr, yr)
