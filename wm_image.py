from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageFont


class WmImage:
    def __init__(self):
        self.img_original = Image.new(mode="RGB", size=(1024, 768), color="#83b0f7")
        self.img_resized = Image.new(mode="RGB", size=(1024, 768), color="#83b0f7")
        self.photo_img = ImageTk.PhotoImage(self.img_resized)
        self.watermarked: bool = False
        self.saved: bool = False
        self.wm_position = (0, 0)  # watermark position for the original picture
        self.wm_position_resized = (0, 0)  # watermark position for the resized picture
        self.anchor = "ms"  # watermark anchor
        self.factor = 1.0  # resize factor, used in the position and font size calculation for the original image
        self.file_name = StringVar(value="No file loaded")
        self.canvas: Canvas  # Canvas object to display the image from within the WmImage class
        self.canvas_img_id = 0  # canvas image ID used to update the image
        self.watermark_var = StringVar(value="watermark")
        self.font_var = StringVar(value="arial")
        self.color_var = StringVar(value="white")
        self.size_var = StringVar(value="20")
        self.pos_var = StringVar(value="center")

    def load_image(self):
        if self.watermarked and not self.saved:
            ok_to_load = messagebox.askokcancel(title="Are you sure?",
                                                message="Watermarked image not saved!",
                                                detail="Do you want to continue?")
        else:
            ok_to_load = True
        if ok_to_load:
            file = filedialog.askopenfile(mode="r", filetypes=[("image files", "*.jpg")])
            if file:
                self.file_name.set(file.name)
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
                self.canvas.itemconfigure(self.canvas_img_id, image=self.photo_img)
                file.close()

    def wm_image(self):
        if self.img_original:
            # calculate watermark positions depending on user input
            self.update_position()

            # watermark displayed image
            font_resized_img = ImageFont.truetype(f"{self.font_var.get()}.ttf", int(self.size_var.get()))
            d = ImageDraw.Draw(self.img_resized)
            d.text(xy=self.wm_position_resized, text=self.watermark_var.get(), anchor=self.anchor,
                   fill=self.color_var.get(), font=font_resized_img)
            self.photo_img = ImageTk.PhotoImage(self.img_resized)
            self.canvas.itemconfigure(self.canvas_img_id, image=self.photo_img)

            # watermark original image
            font_original_img = ImageFont.truetype(f"{self.font_var.get()}.ttf",
                                                   int(round(int(self.size_var.get()) * self.factor, 0)))
            d = ImageDraw.Draw(self.img_original)
            d.text(xy=self.wm_position, text=self.watermark_var.get(), anchor=self.anchor,
                   fill=self.color_var.get(), font=font_original_img)

            # display confirmation
            self.watermarked = True
            messagebox.showinfo(title="Information", message="Watermark added!",
                                detail=f"{self.watermark_var.get()}, {self.font_var.get()}, {self.color_var.get()}, "
                                       f"{self.size_var.get()}, {self.pos_var.get()}")
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
                    wm_file_name = self.file_name.get().replace(".jpg", "_wm.jpg")
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
        if self.pos_var.get() == "center":
            self.wm_position = (w_size // 2, h_size // 2)
            self.wm_position_resized = (w_resize // 2, h_resize // 2)
            self.anchor = "ms"
        elif self.pos_var.get() == "top left":
            self.wm_position = (gap, gap)
            self.wm_position_resized = (gap_resize, gap_resize)
            self.anchor = "lt"
        elif self.pos_var.get() == "top right":
            self.wm_position = (w_size - gap, gap)
            self.wm_position_resized = (w_resize - gap_resize, gap_resize)
            self.anchor = "rt"
        elif self.pos_var.get() == "bottom left":
            self.wm_position = (gap, h_size - gap)
            self.wm_position_resized = (gap_resize, h_resize - gap_resize)
            self.anchor = "lb"
        elif self.pos_var.get() == "bottom right":
            self.wm_position = (w_size - gap, h_size - gap)
            self.wm_position_resized = (w_resize - gap_resize, h_resize - gap_resize)
            self.anchor = "rb"
