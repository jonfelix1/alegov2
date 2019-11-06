from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import *
from PIL import Image as pimage
from PIL import ImageTk as itk


to_show = 15

thumb_size_x = 192
thumb_size_y = 192


d_im = []
d_p_im = []
detect_images = []

def donothing():
    pass

def open_file():
    filename = filedialog.askopenfilename(title = "Select image to scan",filetypes = (("image files",".jpg .jpeg .png"),("all files","*.* .*")))

    return filename

def show_settings():
    sett_win = Toplevel(root)
    sett_win.title("Make me get better at getting Law plz")
    #sett_win.geometry('200x100')

    sett_win_frame = ttk.Frame(sett_win, padding=(3,3,12,12))
    sett_win_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    sett_label = ttk.Label(sett_win_frame, text = "Amount of closest matches to show : ")
    sett_label.grid(column=1, row=1, sticky=(W,E))

    num_show_entry = ttk.Entry(sett_win_frame, textvariable=num_to_show)
    
    num_show_entry.grid(column=2, row=1, sticky=(W,E))
    

def show_about_window():
    about_win = Toplevel(root)
    about_win.title("About helping me get Law")
    about_win.geometry('400x200')
    about_win.resizable(FALSE,FALSE)

    about_win_frame = ttk.Frame(about_win, padding=(3,3,12,12))
    #about_win_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    #about_win_frame.columnconfigure(weight=1)
    #about_win_frame.rowconfigure(weight=1)

    help_label = ttk.Label(about_win,text = "A Grand Task created by Miku Church Group of DECRYPT 2018\nHanif\nJohn\nZaidan", justify="center")
    #help_label.grid(column=0, row=0)
    help_label.place(x=200,y=100,anchor="center")

    #help_label.columnconfigure(weight=1)
    #help_label.rowconfigure(weight=1)

def fill_detections(frame):
    max_img = frame.winfo_width() // 256
    emptyImage = PhotoImage(file='gui/empty.png')
    column = 0
    row = 0
    i = 0;
    for image in range(to_show):
        print("Row ", row," column ", column)
        #d_im.append(pimage.open("gui/empty.png"))

        d_p_im.append(itk.PhotoImage(pimage.open("gui/empty.png")))

        #d_imeg = PhotoImage(d_im[i])

        #print(d_im)

        d_imeg = itk.PhotoImage(file = "gui/empty.png")

        detect_images.append(ttk.Label(frame, text="detect images", image = d_p_im[i]))
        #detect_images[i]['image'] = d_p_im[i]
        detect_images[i].grid(column = column, row = row)

        i += 1
        #print("i is ",i)

        """
        dt_img = pimage.open("gui/empty.png")

        d_img = PhotoImage(file='gui/empty.png')

        d_imeg = PhotoImage(dt_img)

        dt_image = ttk.Label(frame, text="detect images", image = d_imeg)
        #dt_image['image'] = d_img
        dt_image['compound'] = 'top'
        dt_image.grid(column = image, row = column)
        detect_images.append(dt_image)
        """
        # ttk.Label(frame, image=emptyImage).grid(row=image, column=column)
        column = (column + 1) % 2
        if (column == 0):
            row += 1
            

        
        print("AAAA")

def on_mousewheel(event):
    shift = (event.state & 0x1) != 0
    scroll = -1 if event.delta > 0 else 1
    if shift:
        detect_canvas.xview_scroll(scroll * 2, "units")
    else:
        detect_canvas.yview_scroll(scroll * 2, "units")

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

root = Tk()
root.option_add('*tearOff', FALSE)
root.title("GIVE ME LAW PLEASE T_T")

num_to_show = StringVar(root, value=to_show)
#num_to_show.set(to_show)

menubar = Menu(root)
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menu_about = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_edit, label='Edit')
menubar.add_cascade(menu=menu_about, label='About')

#menu_file.add_command(label='New', command=donothing)
menu_file.add_command(label='Open...', command=open_file)
menu_file.add_command(label='Close', command=donothing)

menu_edit.add_command(label='Settings', command=show_settings)

menu_about.add_command(label='Help', command=donothing)
menu_about.add_command(label='About', command=show_about_window)

mainframe = ttk.Frame(root, borderwidth=5, relief="flat", width=200, height=100)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=4)
mainframe.rowconfigure(0, weight=1)

scan_frame = ttk.Frame(mainframe, borderwidth=5, relief="sunken",width=100, height=100)
scan_frame.grid(column = 0, row = 0, sticky=(N, S, E, W))
scan_frame.columnconfigure(0, weight=1)
scan_frame.rowconfigure(0, weight=1)


outer_detect_frame = ttk.Frame(mainframe)
outer_detect_frame.grid(row=0, column=1, pady=(5, 0), sticky='news')
outer_detect_frame.grid_rowconfigure(0, weight=1)
outer_detect_frame.grid_columnconfigure(0, weight=1)



detect_canvas = Canvas(outer_detect_frame, borderwidth=0, background="#ffffff")
detect_canvas.grid(column = 0, row = 0, sticky=(N, S, E, W))
detect_canvas.bind_all("<MouseWheel>", on_mousewheel)
detect_canvas.columnconfigure(0, weight=1)
detect_canvas.rowconfigure(0, weight=1)

detect_frame = ttk.Frame(detect_canvas, borderwidth=5, relief="groove",width=312, height=312)
detect_frame.grid(column = 0, row = 0, sticky=(N, S, E, W))
#detect_frame.columnconfigure(0, weight=1)
#detect_frame.rowconfigure(0, weight=1)


detect_vsb = ttk.Scrollbar(outer_detect_frame, orient="vertical", command=detect_canvas.yview)
detect_vsb.grid(row = 0, column = 999, sticky=(N,S))
detect_canvas.configure(yscrollcommand=detect_vsb.set)
detect_canvas.create_window((0, 0), window=detect_frame, anchor='nw')

detect_frame.bind("<Configure>", lambda event, canvas=detect_canvas: onFrameConfigure(detect_canvas))

test_s_label = ttk.Label(scan_frame, text="this is the scan frame")
test_s_label.grid(column = 0, row = 1)

emptyImage = PhotoImage(file='gui/empty.png')
scan_image = ttk.Label(scan_frame, text="Scan images")
scan_image['image'] = emptyImage
scan_image.grid(column = 0, row = 0)


#test_d_label = ttk.Label(detect_frame, text="this is the detect frame")
#test_d_label.grid(column = 0, row = 0)

fill_detections(detect_frame)


emptyImage = PhotoImage(file='gui/empty.png')
scan_image = ttk.Label(scan_frame, text="Scan images")
scan_image['image'] = emptyImage
scan_image.grid(column = 0, row = 0)

for image in detect_images:
    print(image['image'])

for img in detect_images:
    print(d_im)

root.config(menu=menubar)
root.mainloop()