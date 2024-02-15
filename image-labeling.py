import os
from tkinter import Tk, Label, Button, Entry, filedialog
from PIL import Image, ImageTk

class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling Program")

        self.image_dir = None
        self.images = []
        self.current_index = 0
        self.labels = {}

        self.root.geometry("1024x768")  # Set a fixed size for the window

        self.label_text = Label(root, text="Enter image directory:")
        self.label_text.grid(row=0, column=0, columnspan=1, sticky="w")

        self.browse_button = Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, sticky="e")

        self.label_image = Label(root)
        self.label_image.grid(row=1, column=0, columnspan=4)

        self.label_prompt = Label(root, text="Enter your label name:")
        self.label_prompt.grid(row=2, column=0, columnspan=1, sticky="w")

        self.label_entry = Entry(root, width=30)
        self.label_entry.grid(row=2, column=1, columnspan=1, sticky="ew")

        self.label1_button = Button(root, text="True", command=lambda: self.submit_and_next("1"))
        self.label1_button.grid(row=3, column=0, sticky="ew")

        self.label2_button = Button(root, text="False", command=lambda: self.submit_and_next("0"))
        self.label2_button.grid(row=3, column=1, sticky="ew")

        self.rotate_clockwise_button = Button(root, text="Rotate Clockwise", command=self.rotate_clockwise)
        self.rotate_clockwise_button.grid(row=4, column=0, sticky="ew")

        self.rotate_counter_clockwise_button = Button(root, text="Rotate Counter Clockwise", command=self.rotate_counter_clockwise)
        self.rotate_counter_clockwise_button.grid(row=4, column=1, sticky="ew")

        self.previous_button = Button(root, text="Previous Image", command=self.show_previous_image)
        self.previous_button.grid(row=5, column=0, sticky="ew")

        self.next_button = Button(root, text="Next Image", command=self.show_next_image)
        self.next_button.grid(row=5, column=1, sticky="ew")

        self.save_button = Button(root, text="Save Labels", command=self.save_labels)
        self.save_button.grid(row=6, column=0, columnspan=2, sticky="ew")

    def browse_directory(self):
        self.image_dir = filedialog.askdirectory()
        self.load_images()

    def load_images(self):
        if self.image_dir:
            self.images = self.get_image_relative_paths(self.image_dir)
            self.show_next_image()

    def get_image_relative_paths(self, directory):
        image_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    relative_path = os.path.relpath(os.path.join(root, file), directory)
                    image_paths.append(relative_path)
        return image_paths

    def show_next_image(self):
        if self.image_dir and self.current_index < len(self.images):
            image_path = os.path.join(self.image_dir, self.images[self.current_index])
            self.display_image(image_path)
            self.current_index += 1
        elif not self.image_dir:
            self.label_text.config(text="Select an image directory.")
        else:
            self.label_text.config(text="All images labeled!")

    def show_previous_image(self):
        if self.image_dir and self.current_index > 1:
            self.current_index -= 2  # Move back two steps to show the previous image
            self.show_next_image()

    def display_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((1024, 600))  # Adjust the image size to fit within the fixed window size
        img = ImageTk.PhotoImage(img)
        self.label_image.config(image=img)
        self.label_image.image = img
        self.label_text.config(text=f"Current Image: {os.path.basename(image_path)}")

    def rotate_clockwise(self):
        self.rotate_image(90)

    def rotate_counter_clockwise(self):
        self.rotate_image(-90)

    def rotate_image(self, angle):
        if self.image_dir and 0 <= self.current_index - 1 < len(self.images):
            image_path = os.path.join(self.image_dir, self.images[self.current_index - 1])
            img = Image.open(image_path)
            img = img.rotate(angle)  # Rotate specified degrees
            img.thumbnail((1024, 600))
            img = ImageTk.PhotoImage(img)
            self.label_image.config(image=img)
            self.label_image.image = img

    def submit_label(self, label_value):
        if self.image_dir and 0 <= self.current_index - 1 < len(self.images):
            label = self.label_entry.get()
            relative_path = self.images[self.current_index - 1]
            self.labels[relative_path] = label_value
            print(f"{label_value} for {relative_path}: {label}")

    def submit_and_next(self, label_value):
        self.submit_label(label_value)
        self.show_next_image()

    def save_labels(self):
        if self.image_dir and self.labels:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            with open(save_path, 'w') as file:
                file.write(f"[\n");
                for image_path, labels in self.labels.items():
                    file.write("{");
                    file.write(f"\"{image_path}\" : {labels}");
                    file.write("},\n");
                file.write(f"]\n");
            print(f"Labels saved to {save_path}")

if __name__ == "__main__":
    root = Tk()
    app = ImageLabelingApp(root)
    root.mainloop()
