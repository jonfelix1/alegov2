import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk as ttk
from PIL import Image as PImage, ImageTk as PImageTK
import time as time
import ntpath as ntpath

class Settings():
    def __init__(self, master_dir, to_show, img_size, *args, **kwargs):
        self.master_directory = master_dir
        self.to_show = to_show
        self.image_sizes = img_size

    def set_to_show(self, neo_to_show):
        self.to_show = neo_to_show
    
    def set_master_dir(self, neo_master_dir):
        self.master_directory = neo_master_dir

    def set_img_size(self, neo_img_size):
        self.image_sizes = neo_img_size

    def get_to_show(self):
        return self.to_show
    
    def get_master_dir(self):
        return self.master_directory

    def get_img_size(self):
        return self.image_sizes

class MainApplication(tk.Frame):
    def __init__(self, master, settings_object, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        # This thing is the main container (frame)
        self.master = master
        self.master.minsize(width = 900, height = 500)
        self.master.title("GIVE ME LAW PLEASE T_T")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(row = 0, column = 0, sticky='news')

        self.settings = settings_object


        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 5)

        self.sframe = Scan_Frame(self, borderwidth=5)
        self.sframe.grid(row = 0, column = 0, sticky = 'news')

        self.drame = Detect_Frame(self, borderwidth=5, relief="groove")
        self.drame.grid(row = 0, column = 1, sticky = 'news')

    def callDetectionAgain(self):
        print("DETECT AGAINA")
        self.drame.fill_detections()


class Scan_Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.grid(sticky='news')
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        open_bt = tk.Button(self, text = "Open Image", command = self.open_file)
        open_bt.grid(row = 2, column = 0)

        img_bt_sep = ttk.Separator(self, orient = 'horizontal')
        img_bt_sep.grid(row = 1, column = 0, sticky = 'we', padx = "5", pady= "5")

        bt_set_sep = ttk.Separator(self, orient = 'horizontal')
        bt_set_sep.grid(row = 3, column = 0, sticky = 'we', padx = "5", pady= "5")

        settings_frame = Set_Frame(self)
        settings_frame.grid(row = 4, column = 0, sticky = 'news', padx = "5", pady= "5")

        self.scan_image_file = PImage.open(settings.get_master_dir() + "gui/17750982_muscle_practice.jpeg")
        self.scan_image_file.thumbnail(settings.get_img_size(), PImage.ANTIALIAS)
        self.scan_image = PImageTK.PhotoImage(image=self.scan_image_file)

        self.scan_image_label = tk.Label(self, image = self.scan_image, text = ntpath.basename(self.scan_image_file.filename), compound = "top", padx = "5", pady= "5")
        self.scan_image_label.image = self.scan_image
        self.scan_image_label.grid(row = 0, column = 0)

    def open_file(self, *args):
        filename = tkfd.askopenfilename(title = "Select image to scan",filetypes = (("image files",".jpg .jpeg .png"),("all files","*.* .*")))

        print(filename)

        self.change_scan_image(filename)

        #Detect_Frame.fill_detections()

        return filename

    def change_scan_image(self, image_path):
        self.scan_image_file = PImage.open(image_path)
        self.scan_image_file.thumbnail(settings.get_img_size(), PImage.ANTIALIAS)
        self.scan_image = PImageTK.PhotoImage(image=self.scan_image_file)

        self.scan_image_label['image'] = self.scan_image
        self.scan_image_label['text'] = ntpath.basename(self.scan_image_file.filename)
        self.scan_image_label.image = self.scan_image

class Set_Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        sett_label = ttk.Label(self, text = "Show ")
        sett_label.grid(column=1, row=1)

        self.num_to_show = tk.StringVar(root, value=settings.get_to_show())
        num_show_entry = ttk.Entry(self, textvariable = self.num_to_show)
        num_show_entry.textvariable = self.num_to_show
        num_show_entry.grid(column=2, row=1)

        sett_label = ttk.Label(self, text = " closest matching images")
        sett_label.grid(column=3, row=1)

        apply_bt = tk.Button(self, text = "Apply", command = self.apply_settings)
        apply_bt.grid(row = 1, column = 9)

    def apply_settings(self, *args):
        settings.set_to_show(int(self.num_to_show.get()))
        print("to show : ", settings.get_to_show())
        self.master.master.callDetectionAgain()

class Detect_Frame(tk.Frame):
    image_paths = []
    detect_images = []
    detect_labels = []
    max_img_showed = 0

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.relief = "sunken"
        self.grid(sticky = 'news')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.canvas.grid(column = 0, row = 0, sticky='news')
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)

        self.images_frame = tk.Frame(self.canvas)
        self.images_frame.grid(column = 0, row = 0, sticky='news')
        

        self.vsb = tk.Scrollbar(self, orient="vertical", command = self.canvas.yview)
        self.vsb.grid(row = 0, column = 999, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.create_window((0, 0), window=self.images_frame, anchor='nw')

        self.images_frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.checkImgRow)

        print(settings.get_img_size())
        self.update_idletasks()
        max_img = self.winfo_reqwidth() // settings.get_img_size()[0]
        self.max_img_showed = max_img
        print("frame.winfo_width : ", self.winfo_reqwidth())
        print("max_img_showed :::", self.max_img_showed)

        self.fill_detections()


    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas.xview_scroll(scroll * 2, "units")
        else:
            self.canvas.yview_scroll(scroll * 2, "units")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        

    def checkImgRow(self, event):
        max_img = event.width // settings.get_img_size()[0]
        print("neo self.winfo_reqwidth() ", event.width)
        print("max_row_neo : ", max_img)
        if (self.max_img_showed != max_img):
            print("RESIZE!!!")
            self.max_img_showed = max_img
            #self.images_frame.grid_forget()
            self.change_image_place()
            #self.canvas.configure(scrollregion=self.canvas.bbox("all"))



    def fill_detections(self):
        print("FILLING YOU UP!!!")
        print("Current to show : ", settings.get_to_show())
        padding = 3 , 3
        column = 0
        row = 0
        i = 0;

        for widget in self.images_frame.winfo_children():
            widget.destroy()

        #self.image_paths.clear()
        self.detect_labels.clear()
        self.detect_images.clear()
        for image in self.image_paths:
            image.close()
        self.image_paths.clear()

        for image in range(settings.get_to_show()):
            #print("img num : ",image)
            #print("Row ", row," column ", column)

            self.image_paths.append( PImage.open(settings.get_master_dir() + "gui/empty.png") )
            self.image_paths[i].thumbnail(settings.get_img_size(), PImage.ANTIALIAS)
            self.detect_images.append(PImageTK.PhotoImage(image = self.image_paths[i]))

            self.detect_labels.append(tk.Label(self.images_frame, text=ntpath.basename(self.image_paths[i].filename), image = self.detect_images[i], compound ='top'))
            #print(self.detect_labels)
            #detect_images[i]['image'] = d_p_im[i]
            self.detect_labels[i].grid(column = column, row = row, padx = padding[0], pady= padding[0])

            i += 1
            column = (column + 1) % self.max_img_showed
            if (column == 0):
                row += 1
                
            self.update_idletasks()
            time.sleep(.001)

    def change_image_place(self):
        padding = 3 , 3
        column = 0
        row = 0
        for image_label in self.detect_labels:
            image_label.grid(column = column, row = row, padx = padding[0], pady= padding[0])
            column = (column + 1) % self.max_img_showed
            if (column == 0):
                row += 1

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = tk.Tk()
    settings = Settings("D:/github/alegov2/", 15, (192, 192))
    MainApplication(root, settings).grid(column=0, row=0, sticky="NEWS")
    root.mainloop()