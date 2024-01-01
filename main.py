from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from wm_image import WmImage


class MainWindow:
    def __init__(self, r: Tk):
        self.root_c = r
        mainframe = ttk.Frame(self.root_c, padding="3 12 3 12")
        mainframe.grid(column=0, row=0)
        mainframe.configure(borderwidth=10, relief="raised")

        # label to display original file's name
        file_label = ttk.Label(mainframe, width=100, textvariable=wmi.file_name)
        file_label.grid(column=0, row=0, columnspan=4)

        # button to load a .jpg file
        load_button = ttk.Button(mainframe, text="Load image", width=20, command=wmi.load_image)
        load_button.grid(column=5, row=0)

        # canvas to draw the resized image
        wmi.canvas = Canvas(mainframe, width=1024, height=768, background="#83b0f7", borderwidth=0,
                            highlightthickness=0)
        wmi.canvas.grid(column=0, row=1, columnspan=6)
        wmi.canvas_img_id = wmi.canvas.create_image(512, 384, image=wmi.photo_img)

        # the text to be inserted as watermark
        watermark = ttk.Entry(mainframe, textvariable=wmi.watermark_var, width=30)
        watermark.grid(column=0, row=2)

        # font picker
        wm_font = ttk.Combobox(mainframe, textvariable=wmi.font_var)
        wm_font.configure(values=("arial", "comic", "verdana", "segoesc"))
        wm_font.grid(column=1, row=2)

        # font color picker
        wm_color = ttk.Combobox(mainframe, textvariable=wmi.color_var)
        wm_color.configure(values=("white", "black", "blue", "cyan", "red"))
        wm_color.grid(column=2, row=2)

        # font size picker
        wm_size = ttk.Combobox(mainframe, textvariable=wmi.size_var)
        wm_size.configure(values=("20", "24", "28", "32", "36", "40"))
        wm_size.grid(column=3, row=2)

        # watermark position picker
        wm_pos = ttk.Combobox(mainframe, textvariable=wmi.pos_var)
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
        self.root_c.protocol("WM_DELETE_WINDOW", self.window_close)
        watermark.focus()

    def window_close(self):
        if wmi.watermarked and not wmi.saved:
            exit_tk = messagebox.askokcancel(title="Are you sure?",
                                             message="Watermarked image not saved!",
                                             detail="Do you want to continue?")
        else:
            exit_tk = True
        if exit_tk:
            self.root_c.destroy()


# Tkinter configuration
root = Tk()
root.title("Image watermarking")

wmi = WmImage()
MainWindow(root)

root.mainloop()
