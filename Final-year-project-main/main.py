from datetime import date, datetime
import json
import time
from tkinter import *
from tkinter import ttk,messagebox
import tkinter as tk 
import cv2
from MyQR import myqr
import os
import pyzbar.pyzbar as pyzbar
from PIL import ImageTk, Image




from utils import add_student, check_class_name, check_email, check_student_name, send_email

PATH_TO_ATTENDANCE = "./attendance/"
WINDOW_SIZE = '1920x1080'
PATH_TO_DATA = "./data/"

if __name__=="__main__":

    window = Tk()
    window.geometry(WINDOW_SIZE)
    window.title("QR-code attendance system")

    tab_control = ttk.Notebook(window)

    # styling
    #Manag_Frame=Frame(window,bg="lavender")

    #canvas = Canvas(Manag_Frame, width = 300, height = 300,background="lavender")      
    #canvas.pack()      
    #img = PhotoImage(file="Bg.png")      
    #canvas.create_image(50,50, anchor=NW, image=img) )

    style = ttk.Style()
    style.theme_use('clam')


    # tabs

    # about-tab
    about = ttk.Frame(tab_control)
    ttk.Label(about,text ="the main mission of this project is to implement unique and new ideas of attendence system and bring up new technologies in the hand of the future of society. ").grid(column = 0, row = 0,padx = 30,pady = 30) 
    ttk.Label(about,text ="Tracking attendance is a necessary task that can take a lot of time and present some challenges. Keeping accurate records for your employees or students is important, but manually tracking attendance can lead to errors. ").grid(column = 0, row = 1,padx = 30,pady = 30) 
    ttk.Label(about,text ="Consider using a quick response (QR) code to track attendance. QR codes can streamline the attendance tracking process in any setting and ensure accuracy for both attendees and administrators. ").grid(column = 0, row = 3,padx = 30,pady = 30)
    img=Image.open("pic1.jpg")
    resized_image= img.resize((300,205), Image.ANTIALIAS)
    new_image= ImageTk.PhotoImage(resized_image)
    label = Label(about, image = new_image)
    label.grid()
    
    # img = ImageTk.PhotoImage(Image.open("pic1.jpg"))
    # panel = Label(about, image = img)
    # panel.pack(side = "bottom", fill = "both", expand = "yes")
    # about.mainloop()
    

    # take-attendance
    class_name= tk.StringVar() 
    take_attendance = ttk.Frame(tab_control)
    ttk.Label(take_attendance, text = "Class", foreground ="black",font = ("Times New Roman", 15)).place(x=550,y=550)
    img1=Image.open("qrpic.jpg")
    resized_image1= img1.resize((1500,500), Image.ANTIALIAS)
    new_image1= ImageTk.PhotoImage(resized_image1)
    label1 = Label(take_attendance, image = new_image1)
    label1.grid()
    combo_search=ttk.Combobox(take_attendance,textvariable=class_name,font=("times new roman",13),state='readonly')
    if (os.path.exists(PATH_TO_DATA)):
        combo_search['values']=[ f.path.split("/")[-1] for f in os.scandir(PATH_TO_DATA) if f.is_dir() ]
    else:
        combo_search['values']=[]
    combo_search.place(x=650,y=550)

    def attendance_taker():
        if(class_name.get()):
            path_name = PATH_TO_ATTENDANCE+class_name.get()
            if not os.path.isdir(path_name):
                os.makedirs(path_name)

            cap = cv2.VideoCapture(0)
            # initialize the cv2 QRCode detector
            names=[]
            today=date.today()
            d= today.strftime("%b-%d-%Y")
            filename = path_name+"/"+d+".xls"

            if not os.path.isfile(filename):
                fob=open(filename,'a+')
                fob.write("Registration No."+'\t')
                fob.write("Class Name"+'\t')
                fob.write("Student Name"+'\t')
                fob.write("Email ID"+'\t')
                fob.write("Attendance Time"+'\n')
                fob.close()
            
            
            while True:
                _, frame = cap.read()         
                decodedObjects = pyzbar.decode(frame)
                for obj in decodedObjects:
                    
                    data = json.loads(str(obj.data)[2:-1])
                    
                    # checking and entering data

                    rg_no = str(data["registration_number"])
                    cls_nm = str(data['class_name'])
                    std_nm = str(data['student_name'])
                    e_id = str(data['email_id'])
                    it=datetime.now()
                    
                    if std_nm in names:
                        messagebox.showinfo("Warning", "Already Present!!")
                    else:
                        names.append(std_nm)
                        data=''.join(str(data))
                        intime = it.strftime("%H:%M:%S")
                        fob=open(filename,'a+')
                        fob.write(rg_no+'\t'
                        + cls_nm+'\t'
                        + std_nm+'\t'
                        + e_id+'\t'
                        + intime+'\n') 
                        fob.close()
                        messagebox.showinfo("Warning",'Attendance Recorded')

                    time.sleep(1)
                cv2.imshow("QRCODEscanner", frame)   
                keyCode = cv2.waitKey(1)

                if cv2.getWindowProperty("QRCODEscanner", cv2.WND_PROP_VISIBLE) <1:
                    messagebox.showwarning("Warning", "Closing the camera!!")
                    break
            cap.release()
            cv2.destroyAllWindows()
            fob.close()
        else:
            messagebox.showwarning("Warning", "All fields required!!")
    
    exit_button = tk.Button(take_attendance, text="Submit",font=("Times New Roman", 15),command=attendance_taker,relief=RIDGE)
    exit_button.place(x=700,y=650)


    # check attendance -- showcase the attendance of the class
    check_attendance = ttk.Frame(tab_control)

    class_name_check= tk.StringVar()
    date_select= tk.StringVar() 


    ttk.Label(check_attendance, text = "Class", foreground ="black",font = ("Times New Roman", 15)).place(x=550,y=550)
    Entry(check_attendance,textvariable=class_name_check,font=("times new roman",13)).place(x=620,y=550)
    
    ttk.Label(check_attendance, text = "Date", foreground ="black",font = ("Times New Roman", 15)).place(x=850,y=550)
    Entry(check_attendance,textvariable=date_select,font=("times new roman",13)).place(x=920,y=550)
    img2=Image.open("pic1.jpg")
    resized_image2= img.resize((600,405), Image.ANTIALIAS)
    new_image2= ImageTk.PhotoImage(resized_image2)
    label2 = Label(check_attendance, image = new_image2)
    label2.grid()

    def attendance_checker():
        # Create an object of Style widget

        class_nm = str(class_name_check.get())
        date = str(date_select.get())
        path_to_date = PATH_TO_ATTENDANCE+class_nm+"/"+date+".xls"

        if not os.path.exists(path_to_date):
            messagebox.showwarning("Warning","Class or Date is incorrect proper format. Make sure Date is e.g. Nov-05-2022")


        tree = ttk.Treeview(check_attendance, column=("FName", "LName", "Roll No"), show='headings', height=5)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Name")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Roll No")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Attendance Time")

        file = open(path_to_date,'r')
        lines = file.readlines()[1:]
        for line in lines:
            vals = line.split("\t")
            tree.insert('', 'end', text="1", values=(vals[2],vals[0],vals[-1]))
        file.close()

        tree.pack()
        tree.place(x=300,y=150)
        check_attendance.mainloop()
        return

    exit_button_check = tk.Button(check_attendance, text="Submit",font=("Times New Roman", 15),command=attendance_checker,relief=RIDGE)
    exit_button_check.place(x=1400,y=250)

    #register user

    # UI part to register
    register = ttk.Frame(tab_control)

    registration_number = tk.StringVar()
    student_name = tk.StringVar()
    email_id = tk.StringVar()
    class_to_register = tk.StringVar()

    ttk.Label(register, text = "Registration Number", foreground ="black",font = ("Times New Roman", 15)).place(x=100,y=150)
    Entry(register,textvariable=registration_number, width= 40).place(x=300,y=150)
    ttk.Label(register, text = "Student Name", foreground ="black",font = ("Times New Roman", 15)).place(x=100,y=250)
    Entry(register,textvariable=student_name, width= 40).place(x=300,y=250)
    ttk.Label(register, text = "Email ID", foreground ="black",font = ("Times New Roman", 15)).place(x=100,y=350)
    Entry(register,textvariable=email_id, width= 40).place(x=300,y=350)
    ttk.Label(register, text = "Class", foreground ="black",font = ("Times New Roman", 15)).place(x=100,y=450)
    Entry(register,textvariable=class_to_register, width= 40).place(x=300,y=450)



    def register_student():
        if(registration_number.get() and class_to_register.get() and student_name.get() and email_id.get()):
            
            # validations
            
            if not (str(registration_number.get()).isdigit()):
                messagebox.showwarning("Warning","Registration Number should be an Integer")
            elif not check_email(str(email_id.get())):
                messagebox.showwarning("Warning","Email ID not correct!")
            elif not check_student_name(str(student_name.get())):
                 messagebox.showwarning("Warning","Student Name is not proper format")
            elif not check_class_name(str(class_to_register.get())):
                 messagebox.showwarning("Warning","Class is not in proper format")
            else:
                # acutal code    
                if (add_student(str(registration_number.get()),
                                str(email_id.get()),
                                str(student_name.get()),
                                str(class_to_register.get()))==True):
                    if (send_email(str(registration_number.get()),
                                str(email_id.get()),
                                str(student_name.get()),
                                str(class_to_register.get()))==True):
                        messagebox.showwarning("Warning", "Student has been registered ")
                        # this is to update a new class in the combo box if a student is added in a new class
                        combo_search['values']=[ f.path.split("/")[-1] for f in os.scandir(PATH_TO_DATA) if f.is_dir() ]

                else:
                    messagebox.showwarning("Warning","Student is not registered,- internal error")
        else:
            messagebox.showwarning("Warning", "All fields required!!")
        

    register_student_btn = tk.Button(register,width=13, text="Submit",font=("Times New Roman", 15),command=register_student,bd=2,relief=RIDGE)
    register_student_btn.place(x=600,y=300)


    # adding tabs to GUI
    tab_control.add(about, text='About')
    tab_control.add(take_attendance, text='Take attendance')
    tab_control.add(check_attendance, text='Check attendance')
    tab_control.add(register, text='Register')
    
    tab_control.pack(expand=1, fill='both')

    window.mainloop()
    