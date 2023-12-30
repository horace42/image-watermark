from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFont


class WmImage:
    def __init__(self):
        self.img_original: Image = None
        self.img_resized: Image = None
        self.photo_img: PhotoImage = None
        self.watermarked: bool = False
        self.saved: bool = False
        self.wm_position = (0, 0)  # watermark position for the original picture
        self.wm_position_resized = (0, 0)  # watermark position for the resized picture
        self.anchor = "ms"  # watermark anchor
        self.factor = 1.0  # resize factor, used in the position and font size calculation for the original image

    def load_image(self):
        file = filedialog.askopenfile(mode="r", filetypes=[("image files", "*.jpg")])
        if file:
            file_name_var.set(file.name)
            self.watermarked = False
            self.saved = False
            self.img_original = Image.open(file.name)
            # print(self.img_original.format, self.img_original.size, self.img_original.mode)

            # resize image to fit canvas
            self.img_resized = ImageOps.contain(self.img_original, (1024, 768))
            self.factor = self.img_original.size[0] / self.img_resized.size[0]
            # print(self.img_resized.format, self.img_resized.size, self.img_resized.mode)

            # create a PhotoImage object for display within Tk canvas
            self.photo_img = ImageTk.PhotoImage(self.img_resized)
            canvas.create_image(512, 384, image=self.photo_img)
            file.close()

    def wm_image(self):
        if self.img_original:
            # calculate watermark positions depending on user input
            self.update_position()

            # watermark displayed image
            font_resized_img = ImageFont.truetype(f"{font_var.get()}.ttf", int(size_var.get()))
            d = ImageDraw.Draw(self.img_resized)
            d.text(self.wm_position_resized, watermark_var.get(), anchor=self.anchor,
                   fill=color_var.get(), font=font_resized_img)
            self.photo_img = ImageTk.PhotoImage(self.img_resized)
            canvas.create_image(512, 384, image=self.photo_img)

            # watermark original image
            font_original_img = ImageFont.truetype(f"{font_var.get()}.ttf",
                                                   int(round(int(size_var.get()) * self.factor, 0)))
            d = ImageDraw.Draw(self.img_original)
            d.text(self.wm_position, watermark_var.get(), anchor=self.anchor,
                   fill=color_var.get(), font=font_original_img)

            # display confirmation
            self.watermarked = True
            messagebox.showinfo(title="Information", message="Watermark added!",
                                detail=f"{watermark_var.get()}, {font_var.get()}, {color_var.get()}, "
                                       f"{size_var.get()}, {pos_var.get()}")
        else:
            messagebox.showwarning(title="Warning", message="No file opened!",
                                   detail="Use load button to open a JPG file.")

    def save_image(self):
        if self.img_original:
            # check if a watermark was applied
            if self.watermarked:
                if self.saved:
                    overwrite = messagebox.askokcancel(title="Are you sure?",
                                                       message="Watermarked image already saved!",
                                                       detail="Do you want to continue?")
                else:
                    overwrite = True
                if overwrite:
                    wm_file_name = file_name_var.get().replace(".jpg", "_wm.jpg")
                    self.img_original.save(wm_file_name)
                    messagebox.showinfo(title="Information", message="Watermarked image saved!",
                                        detail=wm_file_name)
                    self.saved = True
            else:
                messagebox.showwarning(title="Warning", message="Original file not modified!",
                                       detail="Use watermark button to insert watermark.")
        else:
            messagebox.showwarning(title="Warning", message="No file opened!",
                                   detail="Use load button to open a JPG file.")

    def update_position(self):
        # calculate watermark position and anchor for both images (original and resized for display in canvas)
        w_size, h_size = self.img_original.size
        w_resize, h_resize = self.img_resized.size

        # if not centered, watermark will be placed at a gap of 50 pixels horizontal and vertical from the corner
        gap_resize = 50
        # increase/decrease the gap for the original image
        gap = round(gap_resize * self.factor, 0)
        if wm_pos.get() == "center":
            self.wm_position = (w_size // 2, h_size // 2)
            self.wm_position_resized = (w_resize // 2, h_resize // 2)
            self.anchor = "ms"
        elif wm_pos.get() == "top left":
            self.wm_position = (gap, gap)
            self.wm_position_resized = (gap_resize, gap_resize)
            self.anchor = "lt"
        elif wm_pos.get() == "top right":
            self.wm_position = (w_size - gap, gap)
            self.wm_position_resized = (w_resize - gap_resize, gap_resize)
            self.anchor = "rt"
        elif wm_pos.get() == "bottom left":
            self.wm_position = (gap, h_size - gap)
            self.wm_position_resized = (gap_resize, h_resize - gap_resize)
            self.anchor = "lb"
        elif wm_pos.get() == "bottom right":
            self.wm_position = (w_size - gap, h_size - gap)
            self.wm_position_resized = (w_resize - gap_resize, h_resize - gap_resize)
            self.anchor = "rb"

    def window_close(self):
        if self.watermarked and not self.saved:
            exit_tk = messagebox.askokcancel(title="Are you sure?",
                                             message="Watermarked image not saved!",
                                             detail="Do you want to continue?")
        else:
            exit_tk = True
        if exit_tk:
            root.destroy()


wmi = WmImage()

# Tkinter configuration
root = Tk()
root.title("Image watermarking")

mainframe = ttk.Frame(root, padding="3 12 3 12")
mainframe.grid(column=0, row=0)
mainframe.configure(borderwidth=10, relief="raised")

# label to display original file's name
file_name_var = StringVar(value="No file loaded")
file_label = ttk.Label(mainframe, width=100, textvariable=file_name_var)
file_label.grid(column=0, row=0, columnspan=4)

# button to load a .jpg file
load_button = ttk.Button(mainframe, text="Load image", width=20, command=wmi.load_image)
load_button.grid(column=5, row=0)

# canvas to draw the resized image
canvas = Canvas(mainframe, width=1024, height=768, background="#83b0f7", borderwidth=0, highlightthickness=0)
canvas.grid(column=0, row=1, columnspan=6)

# the text to be inserted as watermark
watermark_var = StringVar(value="watermark")
watermark = ttk.Entry(mainframe, textvariable=watermark_var, width=30)
watermark.grid(column=0, row=2)

# font picker
font_var = StringVar(value="arial")
wm_font = ttk.Combobox(mainframe, textvariable=font_var)
wm_font.configure(values=("arial", "comic", "verdana", "segoesc"))
wm_font.grid(column=1, row=2)

# font color picker
color_var = StringVar(value="white")
wm_color = ttk.Combobox(mainframe, textvariable=color_var)
wm_color.configure(values=("white", "black", "blue", "cyan", "red"))
wm_color.grid(column=2, row=2)

# font size picker
size_var = StringVar(value="20")
wm_size = ttk.Combobox(mainframe, textvariable=size_var)
wm_size.configure(values=("20", "24", "28", "32", "36", "40"))
wm_size.grid(column=3, row=2)

# watermark position picker
pos_var = StringVar(value="center")
wm_pos = ttk.Combobox(mainframe, textvariable=pos_var)
wm_pos.configure(values=("center", "top left", "top right", "bottom left", "bottom right"))
wm_pos.grid(column=4, row=2)

# button to insert the watermark as per chose parameters
wm_button = ttk.Button(mainframe, text="Watermark", width=20, command=wmi.wm_image)
wm_button.grid(column=5, row=2)

# text labels for configuration options
ttk.Label(mainframe, text="Input watermark").grid(column=0, row=3)
ttk.Label(mainframe, text="Choose font").grid(column=1, row=3)
ttk.Label(mainframe, text="Font color").grid(column=2, row=3)
ttk.Label(mainframe, text="Font size").grid(column=3, row=3)
ttk.Label(mainframe, text="Watermark position").grid(column=4, row=3)

# button to save the modified image
save_button = ttk.Button(mainframe, text="Save", width=20, command=wmi.save_image)
save_button.grid(column=5, row=3)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# close button intercept
root.protocol("WM_DELETE_WINDOW", wmi.window_close)

watermark.focus()
root.mainloop()
