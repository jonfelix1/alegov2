import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter import ttk as ttk
from PIL import Image as PImage, ImageTk as PImageTK
import time as time
import ntpath as ntpath
import os

#import main as backEnd
import backend_functions as backEnd
import numpy as np
import multiprocessing
import glob
import cv2
from tempfile import TemporaryFile
tempImgArr = TemporaryFile()



#curr_image_desc = None

class BackEndHolder():
    image_db = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Settings():
    def __init__(self, master_dir, to_show, img_size, *args, **kwargs):
        self.master_directory = master_dir
        self.to_show = to_show
        self.image_sizes = img_size
        self.scan_type = 0
        self.scan_image_selected = False
        self.most_similar_db_idx = []
        self.curr_image_desc = None
        self.current_compare = []

        self.image_db = []
        self.image_db_as_path = []
        self.image_desc = []

    def set_to_show(self, neo_to_show):
        self.to_show = neo_to_show
    
    def set_master_dir(self, neo_master_dir):
        self.master_directory = neo_master_dir

    def set_img_size(self, neo_img_size):
        self.image_sizes = neo_img_size

    def set_scan_type(self, neo_scan_type):
        self.scan_type = neo_scan_type
        ##!print("Scan type changed to ", self.get_scan_type())

    def set_scan_img_sel(self, neo_scan_img_status):
        self.scan_image_selected = neo_scan_img_status

    def get_to_show(self):
        return self.to_show
    
    def get_master_dir(self):
        return self.master_directory

    def get_img_size(self):
        return self.image_sizes
    
    def get_scan_type(self):
        return self.scan_type
    
    def get_scan_img_sel(self):
        return self.scan_image_selected

class MainApplication(tk.Frame):
    def __init__(self, master, settings_object, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        # This thing is the main container (frame)
        self.master = master
        self.master.minsize(width = 960, height = 512)
        self.master.title("FaceMatcheRank") # Window title
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(row = 0, column = 0, sticky='news')

        self.settings = settings_object 

        #self.show_scanning_window()
        self.show_welcoming_window()



    def compareImages(self):
        self.settings.current_compare.clear();

        #self.settings.most_similar_db_idx.clear();

        if (self.settings.get_scan_type() == 1): # 0 is cosine, 1 is euclid
            #most_similar_db_idx.clear()
            for i in range(len(self.settings.image_desc)): #Gets the similarity metric using Euclidean
                #print("curr_image_desc : ", self.settings.curr_image_desc)
                #print("Image des _ I :", image_desc[i])
                self.settings.current_compare.append(backEnd.euclidean_distance(self.settings.curr_image_desc, self.settings.image_desc[i]))
                if (self.settings.get_to_show() > 0):
                    self.settings.most_similar_db_idx = (np.argsort(self.settings.current_compare)[::-1])[(-1 * self.settings.get_to_show()):]
                    self.settings.most_similar_db_idx = self.settings.most_similar_db_idx[::-1]
                else :
                    self.settings.most_similar_db_idx = []
        else:
            for i in range(len(self.settings.image_desc)): #Gets the similarity metric using cosine
                #print("curr_image_desc : ", self.settings.curr_image_desc)
                #print("Image des _ I :", image_desc[i])
                self.settings.current_compare.append(backEnd.cosine_similarity(self.settings.curr_image_desc, self.settings.image_desc[i]))
                if (self.settings.get_to_show() > 0):
                    self.settings.most_similar_db_idx = np.argsort(self.settings.current_compare)[(-1 * self.settings.get_to_show()):]
                    self.settings.most_similar_db_idx = self.settings.most_similar_db_idx[::-1]
                else :
                    self.settings.most_similar_db_idx = []
        
        ##!print("self.settings.most_similar_db_idx : ", self.settings.most_similar_db_idx)

    def callDetectionAgain(self): # Calls the detection and repopulates the detection frame
        ##!print("DETECT AGAINA")
        self.compareImages()
        self.drame.fill_detections()

    def show_scanning_window(self):
        ## Resets the column and row configurantion
        ##!print("image_db lenth : ", len(image_db))
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(2, weight = 0)
        self.columnconfigure(4, weight = 0)
        self.columnconfigure(6, weight = 0)
        self.rowconfigure(0, weight = 0)
        self.rowconfigure(5, weight = 0)
        self.rowconfigure(7, weight = 0)
        self.rowconfigure(10, weight = 0)
        ##

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 5)

        self.sframe = Scan_Frame(self, borderwidth=5)
        self.sframe.grid(row = 0, column = 0, sticky = 'news')

        self.drame = Detect_Frame(self, borderwidth=5, relief="groove")
        self.drame.grid(row = 0, column = 1, sticky = 'news', columnspan = 2)

        self.scan_progress = scan_progBar(self, mode = 'determinate', maximum = self.settings.get_to_show(), length = self.settings.get_to_show())
        self.scan_progress.grid(row = 999, column = 0, columnspan = 2, sticky='we', padx = 5, pady =5)

        self.info_button = tk.Button(self, text="i", command = self.show_about_window)
        self.info_button.grid(row = 999, column = 2)


    def show_about_window(self):
        a_win = tk.Toplevel(root)
        #a_win.rowconfigure(0, weigth = 1)
        #a_win.columnconfigure(0, weigth = 1)
        #a_win.grid(row = 0, column = 0, sticky = 'news')
        a_win.resizable(False, False)

        a_f = tk.Frame(a_win)
        a_f.grid(row = 0, column = 0)

        about_label = tk.Label(a_f, text = """A face recognition application with a ranker feature.\nA grand task for Linear and Geometric Algebra.\n
        Zaidan Naufal - Extractor, Report\nJon Felix - Extractor, Matcher\nHanif Muhamad - GUI\nCreated with Python 3, OpenCV, Tkinter, PIL, numpy, glob""")
        about_label.grid(row = 0, column = 0)

        about_label['text'] = """A face recognition application with a ranker feature.\nA grand task for Linear and Geometric Algebra.\n
        Zaidan Naufal - Extractor, Report\nJon Felix - Extractor, Matcher\nHanif Muhamad - GUI\n\nCreated with Python 3, OpenCV, Tkinter, PIL, numpy, glob"""

    def show_welcoming_window(self):
        ## Reset grid config
        self.rowconfigure(0, weight = 0)
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 0)
        ##
        self.columnconfigure(0, weight = 3)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)
        self.columnconfigure(6, weight = 3)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(7, weight = 1)
        self.rowconfigure(10, weight = 2)


        welcome_title = tk.Label(self, text = "FaceMatcheRank")
        welcome_title.grid(row = 5, column = 2, columnspan = 3)

        open_db_button = tk.Button(self, text = "Open Extracted Database", command = self.open_extracted_databse)
        open_db_button.grid(row = 7, column = 2)

        scan_neo_dir_button = tk.Button(self, text = "Scan a directory of images", comman = self.open_scan_dir)
        scan_neo_dir_button.grid(row = 7, column = 4)

        self.dbin_prog_bar = scan_progBar(self, mode = 'determinate', value = 0)
        self.dbin_prog_bar.grid(row = 999, column = 0, columnspan = 10, sticky='we', padx = 5, pady =5)
        
        
        self.info_label = tk.Label(self, text = "Welcome!")
        self.info_label.grid(row = 995, column = 0, columnspan = 10, sticky='we', padx = 5, pady =5)

    def open_scan_dir(self, *args):
        scandir = tkfd.askdirectory(title = "Select directory to scan for images")

        if (scandir == ''):
            print("NO FILES SELECTED!!!!")
        else:
            print("scandir : ", scandir)
            globable_dir = scandir + "/*.jpg"
            print("globable_dir : ",globable_dir)
            self.populate_image_db(globable_dir)

            #print(image_db)

            for child in self.winfo_children():
                child.destroy()
            self.show_scanning_window()

        return scandir

    def populate_image_db(self, glob_dir):
        self.dbin_prog_bar['mode'] = 'indeterminate'
        self.info_label['text'] = "Listing images"
        self.dbin_prog_bar.start()
        self.update_idletasks()

        time.sleep(.2)

        for img in glob.glob(glob_dir):
            self.settings.image_db_as_path.append(img)
            self.settings.image_db.append(cv2.imread(img))
        print("Image loading done")
        ##!print("image_db lenth : ", len(image_db))

        self.info_label['text'] = "Extracting image descriptions"
        self.update_idletasks()

        time.sleep(.2)

        for i in range(len(self.settings.image_db_as_path)):
            self.settings.image_desc.append(backEnd.extract_features(self.settings.image_db[i]))

    def open_extracted_databse(self, *args):
        extract_db = tkfd.askopenfile(title = "Select a database of extracted images", filetypes = (("Image Databse",".npy"),("all files","*.* .*")))

        if (extract_db == '' or extract_db == None):
            print("NO FILES SELECTED!!!!")
        else:
            ##!print("extract_db : ", extract_db)
            
            #image_desc = np.load(extract_db)
            # DOESN'T WORK YET

            ##!print(image_desc)
            for child in self.winfo_children():
                child.destroy()
            self.show_scanning_window()

        return extract_db

class scan_progBar(ttk.Progressbar):
    # Progressbar for detection and current population run
    def __init__(self, master, *args, **kwargs):
        ttk.Progressbar.__init__(self, master, *args, **kwargs)
        self.master = master

    def set_max_len(self, max_Len):
        self['maximum'] = max_Len
        self['length'] = max_Len

    def set_val(self, cur_val):
        self['value'] = cur_val

class Scan_Frame(tk.Frame):
    # The Frame on which the currently scan image and settings resides
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.grid(sticky='news')
        #self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(30, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        top_frame = tk.Frame(self)
        top_frame.grid(row = 0, column = 0, columnspan = 4)#, sticky = 'we')

        back_bt = tk.Button(top_frame, text = "BACK", command=self.back_to_welcome)
        back_bt.grid(row = 0, column = 1, sticky = 'w')

        open_bt = tk.Button(self, text = "Open Image", command = self.open_file) # Open image file to use as scan image
        open_bt.grid(row = 11, column = 0)

        img_bt_sep = ttk.Separator(self, orient = 'horizontal') # Separater
        img_bt_sep.grid(row = 1, column = 0, padx = "5", pady= "5")

        bt_set_sep = ttk.Separator(self, orient = 'horizontal')
        bt_set_sep.grid(row = 30, column = 0, padx = "5", pady= "5")

        settings_frame = Set_Frame(self)
        settings_frame.grid(row = 40, column = 0, padx = "5", pady= "5")

        self.scan_image_file = PImage.open(settings.get_master_dir() + "/gui/empty.png")
        self.scan_image_file.thumbnail(settings.get_img_size(), PImage.ANTIALIAS)
        self.scan_image = PImageTK.PhotoImage(image=self.scan_image_file)

        #self.scan_image_label = tk.Label(self, image = self.scan_image, text = ntpath.basename(self.scan_image_file.filename), compound = "top", padx = "5", pady= "5")
        self.scan_image_label = tk.Label(self, image = self.scan_image, text = "Please select an image to scan", compound = "top", padx = "5", pady= "5")
        self.scan_image_label.image = self.scan_image
        self.scan_image_label.grid(row = 10, column = 0)

    def open_file(self, *args):
        filename = tkfd.askopenfilename(title = "Select image to scan",filetypes = (("image files",".jpg .jpeg .png"),("all files","*.* .*")))

        if (filename == '' or filename == None):
            print("NO FILES SELECTED!!!!")
        else:
            print(filename)
            self.change_scan_image(filename)
            self.master.callDetectionAgain()

        return filename

    def change_scan_image(self, image_path):
        self.scan_image_file = PImage.open(image_path)
        self.scan_image_file.thumbnail(settings.get_img_size(), PImage.ANTIALIAS)
        self.scan_image = PImageTK.PhotoImage(image=self.scan_image_file)

        self.scan_image_label['image'] = self.scan_image
        self.scan_image_label['text'] = ntpath.basename(self.scan_image_file.filename)
        self.scan_image_label.image = self.scan_image
        self.master.settings.set_scan_img_sel(True)

        self.master.settings.curr_image_desc = backEnd.extract_features(cv2.imread(image_path))
        ##!print("curr_image_desc : ", self.master.settings.curr_image_desc)

    def back_to_welcome(self):
        for child in self.master.winfo_children():
            child.destroy()

        for img in self.master.settings.image_db:
            img = None
        self.master.settings.image_db = []
        self.master.settings.image_db_as_path = []
        self.master.settings.image_desc = []
        self.master.show_welcoming_window()

class Set_Frame(tk.Frame):
    # The frame for the settings stuffs, this used to be in a separate window
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
        apply_bt.grid(row = 9, column = 1, columnspan = 3)

        self.scan_type_var = tk.IntVar()
        self.scan_type_var.set(self.master.master.settings.get_scan_type())
        ##!print("self.master.master.settings.get_scan_type() : ", self.master.master.settings.get_scan_type())
        ##!print("self.scan_type_var : ", self.scan_type_var.get())

        scan_type_label = ttk.Label(self, text = "Similarity Metric : ")
        scan_type_label.grid(row = 5, column = 1)

        cos_radio_button = ttk.Radiobutton(self, text = "Cosine", variable = self.scan_type_var, value = 0, command = self.set_scan_to_cosine)
        cos_radio_button.grid(row = 5, column = 2)


        euc_radio_button = ttk.Radiobutton(self, text = "Euclidean", variable = self.scan_type_var, value = 1, command = self.set_scan_to_euclid)
        euc_radio_button.grid(row = 5, column = 3)

    def apply_settings(self, *args):
        settings.set_to_show(int(self.num_to_show.get()))
        ##!print("to show : ", settings.get_to_show())
        if (self.master.master.settings.get_scan_img_sel()):
            self.master.master.callDetectionAgain()

    
    def set_scan_to_cosine(self):
        self.set_settings_scan_type(0)

    def set_scan_to_euclid(self):
        self.set_settings_scan_type(1)

    
    def set_settings_scan_type(self, scan_type_value):
        self.scan_type_var.set(scan_type_value)
        self.master.master.settings.set_scan_type(scan_type_value)
        ##!print("AA")

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
        self.images_frame.grid(column = 0, row = 0, sticky = 'news')
        self.images_frame.columnconfigure(0, weight=1)
        self.images_frame.rowconfigure(0, weight=1)
        

        self.vsb = tk.Scrollbar(self, orient="vertical", command = self.canvas.yview)
        self.vsb.grid(row = 0, column = 999, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row = 0, column = 0, sticky = 'news')
        self.canvas.create_window((0, 0), window=self.images_frame, anchor='nw')

        self.images_frame.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.checkImgRow)

        ##!print(settings.get_img_size())
        self.update_idletasks()
        max_img = self.winfo_reqwidth() // settings.get_img_size()[0]
        self.max_img_showed = max_img
        ##!print("frame.winfo_width : ", self.winfo_reqwidth())
        ##!print("max_img_showed :::", self.max_img_showed)

        self.empty_label = tk.Label(self, text="Please select an image to scan first")
        self.empty_label.grid(row = 0, column = 0, sticky = 'news')

        #self.fill_detections()


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
        ##!print("neo self.winfo_reqwidth() ", event.width)
        ##!print("max_row_neo : ", max_img)
        if (self.max_img_showed != max_img):
            print("RESIZE!!!")
            self.max_img_showed = max_img
            #self.images_frame.grid_forget()
            self.change_image_place()
            #self.canvas.configure(scrollregion=self.canvas.bbox("all"))



    def fill_detections(self):
        ##!print("FILLING YOU UP!!!")
        ##!print("Current to show : ", settings.get_to_show())
        padding = 3 , 3
        column = 0
        row = 0
        i = 0;

        self.empty_label.destroy()

        for widget in self.images_frame.winfo_children():
            widget.destroy()


        #self.image_paths.clear()
        self.detect_labels.clear()
        self.detect_images.clear()
        for image in self.image_paths:
            image.close()
        self.image_paths.clear()

        self.master.scan_progress.set_max_len(self.master.settings.get_to_show())

        #for image in range(settings.get_to_show()):
        ##!print("most_similar_db_idx len : ", len(self.master.settings.most_similar_db_idx))
        for image in self.master.settings.most_similar_db_idx:
            #print("img num : ",image)
            #print("Row ", row," column ", column)

            self.master.scan_progress.set_val(i)

            #self.image_paths.append( PImage.open(settings.get_master_dir() + "/gui/empty.png") )
            self.image_paths.append( PImage.open(self.master.settings.image_db_as_path[image]) )
            self.image_paths[i].thumbnail(settings.get_img_size(), PImage.ANTIALIAS)
            self.detect_images.append(PImageTK.PhotoImage(image = self.image_paths[i]))

            ##!print("Image DB I : ", image_db_as_path[image])

            self.detect_labels.append(tk.Label(self.images_frame, text=ntpath.basename(self.image_paths[i].filename) + "\n" + str(round(self.master.settings.current_compare[image], 4)), image = self.detect_images[i], compound ='top'))
            #print(self.detect_labels)
            #detect_images[i]['image'] = d_p_im[i]
            self.detect_labels[i].grid(column = column, row = row, padx = padding[0], pady= padding[0])

            i += 1
            column = (column + 1) % self.max_img_showed
            if (column == 0):
                row += 1
                
            self.update_idletasks()
            time.sleep(.001)

        self.master.scan_progress.set_val(self.master.settings.get_to_show())

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
    root = tk.Tk() # Main Window
    root.style = ttk.Style()
    #root.style.theme_use("clam") #Uses Clam theme
    current_path = os.path.dirname(os.path.realpath(__file__)) #Gets the current gui script directory in order to get gui images
    current_path = current_path.replace("\\", "/")

    backEndHelper = BackEndHolder()

    settings = Settings(current_path, 15, (192, 192)) #Sets the master gui directory, default amount of images to show, and the default image size to show in the gui
    mainframe = MainApplication(root, settings).grid(column=0, row=0, sticky="NEWS") #Creates the main frame. populates it, and places it on the window
    root.mainloop()