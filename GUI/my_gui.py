import tkinter as tk

from injector.profile import GestureProfile
from demo.sequences import action_list

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.gesture_profile = GestureProfile("GUI Profile")  # Profile being constructed by GUI

        self.master = master
        self.master.title("Image List")
        self.pack(fill=tk.BOTH, expand=True)

        # create a canvas for scrolling
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # attach the scrollbar to the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # create a frame inside the canvas for the image list
        self.image_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        # create the "Add" button
        self.add_button = tk.Button(self.master, text="Add", command=self.add_rectangle)
        self.add_button.pack(side=tk.TOP, fill=tk.X)

        # list of rectangle images and string options
        self.rectangle_images = [
            tk.PhotoImage(file="img/hand_1.png").subsample(6, 6),
            tk.PhotoImage(file="img/hand_2.png").subsample(6, 6)
        ]
        self.string_options = list(action_list.keys())

        # initialize the list of rectangles
        self.rectangles = []
        self.numRectangles = 0

    def get_profile(self):
        return self.gesture_profile

    def add_rectangle(self):
        # create a new rectangle with an image and a dropdown menu
        rectangle = tk.Frame(self.image_frame, bg="white", highlightthickness=1, highlightbackground="gray",
                             highlightcolor="gray")
        rectangle.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.numRectangles += 1
        rectangle.label = 'rectangle_{}'.format(str(self.numRectangles).zfill(2))

        left_hand_checkbox_var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(rectangle, text='Include left hand', variable=left_hand_checkbox_var, command=self.get_gesture_info)
        checkbox.pack(side=tk.LEFT, padx=10, pady=5)
        rectangle.left_hand_include = left_hand_checkbox_var

        # add the checkboxes to the rectangle
        left_checkboxes_frame = tk.Frame(rectangle, bg="white")
        left_checkboxes_frame.pack(side=tk.LEFT, fill=tk.Y)

        left_hand_checkboxes = []
        labels = ['Thumb', 'First', 'Middle', 'Ring', 'Pinky']
        left_hand_checkbox_vars = []
        for i in range(5):
            checkbox_var = tk.BooleanVar(value=False)
            left_hand_checkbox_vars.append(checkbox_var)
            checkbox = tk.Checkbutton(left_checkboxes_frame, text=labels[i], variable=checkbox_var, command=self.get_gesture_info)
            checkbox.pack(side=tk.TOP, padx=10, pady=5)
            left_hand_checkboxes.append(checkbox)

        # add the image to the rectangle
        image_hand1 = tk.Label(rectangle, image=self.rectangle_images[0])
        image_hand1.pack(side=tk.LEFT, padx=10, pady=10)

        image_hand2 = tk.Label(rectangle, image=self.rectangle_images[1])
        image_hand2.pack(side=tk.LEFT, padx=10, pady=10)

        # right hand checkboxes
        right_checkboxes_frame = tk.Frame(rectangle, bg='white')
        right_checkboxes_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_hand_checkboxes = []
        right_hand_checkbox_vars = []
        for label in labels:
            checkbox_var = tk.BooleanVar(value=False)
            right_hand_checkbox_vars.append(checkbox_var)
            checkbox = tk.Checkbutton(right_checkboxes_frame, text=label, variable=checkbox_var, command=self.get_gesture_info)
            checkbox.pack(side=tk.TOP, padx=10, pady=5)
            right_hand_checkboxes.append(checkbox)

        right_hand_checkbox_var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(rectangle, text='Include right hand', variable=right_hand_checkbox_var,
                                  command=self.get_gesture_info)
        checkbox.pack(side=tk.LEFT, padx=10, pady=5)
        rectangle.right_hand_include = right_hand_checkbox_var

        dominant_hand_options = ['left', 'right']
        dominant_hand_string_var = tk.StringVar(value=dominant_hand_options[0])
        dropdown = tk.OptionMenu(rectangle, dominant_hand_string_var, *dominant_hand_options, command=self.get_gesture_info)
        dropdown.pack(side=tk.LEFT, padx=10, pady=5)
        rectangle.dominant_hand = dominant_hand_string_var

        # add the delete button to the rectangle
        delete_button = tk.Button(rectangle, text="Delete", command=lambda: self.remove_rectangle(rectangle))
        delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # add the dropdown menu to the rectangle
        string_var = tk.StringVar(value=self.string_options[0])
        dropdown = tk.OptionMenu(rectangle, string_var, *self.string_options, command=self.get_gesture_info)
        dropdown.pack(side=tk.RIGHT, padx=10, pady=10)
        rectangle.func_option = string_var

        rectangle.left_hand_checkboxes = left_hand_checkboxes
        rectangle.left_hand_checkbox_vars = left_hand_checkbox_vars
        rectangle.right_hand_checkboxes = right_hand_checkboxes
        rectangle.right_hand_checkbox_vars = right_hand_checkbox_vars

        self.rectangles.append(rectangle)

    def remove_rectangle(self, rectangle):
        self.rectangles.remove(rectangle)
        rectangle.destroy()

    def get_gesture_info(self):
        rectangle_info = []
        for rectangle in self.rectangles:
            info = {
                'label': rectangle.label,
                'FunctionOption': rectangle.func_option.get(),
                'LeftFingers': None,
                'RightFingers': None,
                'ControlHand': rectangle.dominant_hand.get()
            }
            if rectangle.left_hand_include.get():
                info['LeftFingers'] = [1 if i.get() else 0 for i in rectangle.left_hand_checkbox_vars]
            if rectangle.right_hand_include.get():
                info['RightFingers'] = [1 if i.get() else 0 for i in rectangle.right_hand_checkbox_vars]
            rectangle_info.append(info)
        return rectangle_info


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

    info = app.get_gesture_info()
    print(info)


