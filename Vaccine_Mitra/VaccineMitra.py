#import all necessary modules
import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
from PIL import ImageTk, Image
from tkinter.ttk import Combobox
import requests
import webbrowser
import pandas as pd
from datetime import datetime


class Vaccines:
    def __init__ (self,root):
        global bg
        global flag
        self.root = root
        self.root.title("Vaccine Mitra")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="white")
        #beautify...........
        image = Image.open("bg.jpg")

        # Resize the image using resize() method
        resize_image = image.resize((1920, 1080))

        img = ImageTk.PhotoImage(resize_image)

        # create label and add resize image

        label1 = Label(self.root, image=img)
        label1.image = img
        label1.pack()

        #inserting logo....................

        image_logo=Image.open("VM.png")

        img_logo=ImageTk.PhotoImage(image_logo)

        logo = Label(self.root, image=img_logo)

        logo.image_logo=img_logo

        logo.place(x=195, y=120)







        f1 = Frame(self.root, bg="white", height=503, width=450, pady=10, padx=10,bd=5)
        f1.place(x=850, y=120)

        #taking input
        ip1 = Label(f1, text ="Enter Pin code", font=("arial",20,"bold"),bg="white")
        ip1.place(x=50, y=40)
        self.txt1 = Entry(f1, width=25,bg="light gray", font=("arial",12,"bold"),bd=1)
        self.txt1.place(x=50,y=90)

        ip2 = Label(f1, text="Enter Date(dd-mm-yyyy)", font=("arial", 20, "bold"),bg="white")
        ip2.place(x=50, y=160)
        self.txt2 = Entry(f1, width=25, bg="light gray", font=("times new roman", 12, "bold"))
        self.txt2.place(x=50, y=210)

        ip3 = Label(f1, text="Minimum Age", font=("times new roman", 20, "bold"),bg="white")
        ip3.place(x=20, y=280)

        sel_age=tk.StringVar()
        self.cmb1=Combobox(f1, textvariable=sel_age, state="readonly", values=("select",'18',"45"), font=("times new roman",20), width=10 )
        self.cmb1.place(x=20, y=330)

        ip4 = Label(f1, text="Fee Type", font=("times new roman", 20, "bold"), bg="white")
        ip4.place(x=200, y=280)

        sel_fee = tk.StringVar()
        self.cmb2 = Combobox(f1, textvariable=sel_fee, state="readonly", values=("select", 'Paid', "Free"),
                            font=("times new roman", 20), width=13)
        self.cmb2.place(x=200, y=330)



        btn1 = Button(f1, text="Submit", height=2, width=10, command=self.Sample)
        btn1.place(x=150, y=400)



    def vac_data(self):
        global df
        global kk
        global flag
        pincode = self.txt1.get()
        digits = len(pincode)

        date = self.txt2.get()

        age = self.cmb1.get()
        fee = self.cmb2.get()

        #checking if date is entered in correct format

        try:
            if date== datetime.strptime(date, "%d-%m-%Y").strftime('%d-%m-%Y'):
                d=1
        except:
                d=0







        #Handling the situation if valid data is not entered


        if digits==6 and age!="" and fee!="" and d==1 :

            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="\
                + pincode + "&date=" + date + ""

            r = requests.get(url)

            if r.status_code==200:

                flag = 0
                kk = r.json()

                df = pd.DataFrame(columns=['Name','Address','Dose 1','Dose 2','Vaccine'])


                for i in kk["sessions"]:
                 # print(i["name"],i["block_name"],i["available_capacity"],i["min_age_limit"],i["slots"])
                    if i["min_age_limit"] == int(age) and i["fee_type"]==fee and ((i["available_capacity_dose2"]>0) or (i["available_capacity_dose1"]>0)):
                        df = df.append({'Name': i["name"],
                                        'Address': i["address"],'Dose 1': i["available_capacity_dose1"],
                                        'Dose 2': i["available_capacity_dose2"],'Vaccine':i['vaccine']
                                    },ignore_index=True)


            #if response code is not 200, this will notify the user

            else:
                messagebox.showerror("Error", "Unresponsive URL, check internet connection and retry!!!")
                flag = 1





        else:
            messagebox.showerror("Error","Invalid Data, Please recheck!!!")

            flag=1


    #for opening cowin portal

    def auth(self):
        url1 = "https://selfregistration.cowin.gov.in/"
        return webbrowser.open(url1)

    def join(self):
        url2="https://t.me/joinchat/1Lyo6xcB4sA1NmVl"
        return webbrowser.open(url2)






    def Sample(self):


        self.vac_data()

        #if invalid data is entered, this will stop from loading next screen

        try:
            if flag==0:
                f2 = Frame(self.root, bg="white", height=1080, width=1920)
                f2.place(x=0, y=0)
                image3 = Image.open("bg.jpg")

                # Reszie the image using resize() method
                resize_image3 = image3.resize((1920, 1080))

                img3 = ImageTk.PhotoImage(resize_image3)

                # create label and add resize image

                bg2 = Label(f2, image=img3)
                bg2.image = img3
                bg2.pack()

                f3=Frame(f2,bg='white',height=200, width=300)
                f3.place(x=1220, y=200)
                tel_text=Label(f3, text="Attention!!", font=("times new roman", 20, "bold"),bg="white")
                tel_text.place(x=80, y=10)
                tel_text2=Label(f3, text="If you are a resident of Panipat\nand want to receive updates about\n"
                                         "vaccine availability(18-45) then click the button below\n "
                                         "to join our telegram grp ", font=("times new roman", 12),bg="white")
                tel_text2.place(x=10, y=80)

                join = Button(f2, text="Join", height=2, width=10, command=self.join)
                join.place(x=1330, y=420)

                image4 = Image.open("s21.png")

                # Reszie the image using resize() method
                #resize_image4 = image4.resize((1500, 200))

                img4 = ImageTk.PhotoImage(image4)

                # create label and add resize image

                pos1 = Label(f2, image=img4)
                pos1.image = img4
                pos1.place(x=400,y=20)


                #opens cowin portal
                book = Button(f2, text="Book", height=2, width=10, command=self.auth)
                book.place(x=620, y=450)

                #brings you back to the main window
                back = Button(f2, text="Back", height=2, width=10, command=f2.destroy)
                back.place(x=750, y=450)


                t1 = ttk.Treeview(f2)
                t1.place(x=200, y=200)
                t1["column"] = list(df.columns)
                t1["show"] = "headings"
                for column in t1["column"]:
                    t1.heading(column, text=column)
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    t1.insert("", "end", values=row)

                image_lab_1 = Image.open("get_vac.png")

                Lab_1_resize=image_lab_1.resize((1100,220))

                img_lab_1 = ImageTk.PhotoImage(Lab_1_resize)

                Lab_1 = Label(f2, image=img_lab_1)


                Lab_1.image_lab_1 = img_lab_1



                Lab_1.place(x=250, y=550)




        except:
            if flag==1:
                messagebox.showerror("Error","Something went wrong, Please Retry")





root = Tk()
obj = Vaccines(root)
root.mainloop()
