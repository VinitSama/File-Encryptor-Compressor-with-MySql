###################################################################################################################################################
from tkinter import*
from tkinter import messagebox
from tkinter import filedialog
from module import*
from PIL import Image,ImageTk
import mysql.connector as sql
###################################################################################################################################################
###################################################################################################################################################





"""
Hello Guys, This Program is purely Python Based.

Before starting we have to fullfill all the requirenments.
For this follow this steps:-

STEP 1: Installing Dependencies <PIL and MySql.Connector>.
            Run in terminal
            > pip install pillow mysql.connector

STEP 2: We should have Mysql DBMS in our system.

STEP 3: Creating a database named "profile" and a relation named "info" in it.
            run commands in Mysql
            > CREATE DATABASE profile;
            > USE profile;
            > CREATE TABLE info ( USERNAME VARCHAR(25), PASSWORD VARCHAR(25), EMAIL VARCHR(25));
            close MySql

STEP 4: Write your MySQL login Password below in "passwd=" attribute belown in line 45.

Voila! Run main.py.

"""





###################################################################################################################################################
# Write Mysql Login Password in below line.
mycon=sql.connect(host='localhost',user='root',passwd='',database='profile')
cursor=mycon.cursor()
iniadd="C:/"
###################################################################################################################################################




###################################################################################################################################################

def logged():
    btn1.focus_set()
    username=user_log_var.get()
    password=pass_log_var.get()
    if username==''or username=='USERNAME':
        ent1.config(fg='red')
        ent1.delete(0,'end')
        ent1.insert(0,'Invalid Username')
        return
    for i in username:
        k=ord(i)
        if (k<49 or k>57)and(k<97 or k>122)and(k<65 or k>90):
            ent1.config(fg='red')
            ent1.delete(0,'end')
            ent1.insert(0,'Invalid Username')
            return
    if password=='' or password=='PASSWORD':
        ent2.config(fg='red')
        ent2.delete(0,'end')
        ent2.insert(0,'Invalid Password')
        return
    elif len(password)<6:
        ent2.config(fg='red')
        ent2.delete(0,'end')
        ent2.insert(0,'Password must contain atleast 6 digits')
        return
    query="select * from info where username='{}'".format(username)
    cursor.execute(query)
    dataset=cursor.fetchall()
    if dataset==[]:
        ent1.config(fg='red')
        ent1.delete(0,'end')
        ent1.insert(0,'Invalid Username')
        return
    if dataset[0][1]!=password:
        ent2.config(fg='red')
        ent2.delete(0,'end')
        ent2.insert(0,'Invalid Password')
        return
    frame1.grid_remove()
    frame10.grid()
    mycon.close()

def to_sign_up():
    frame1.focus_set()
    ent1.delete(0,'end')
    ent2.delete(0,'end')
    ent1.insert(0,'USERNAME')
    ent2.insert(0,'PASSWORD')
    ent1.config(fg='#1A3636')
    ent2.config(fg='#1A3636')
    frame1.grid_remove()
    frame4.grid()

def signed():
    email=email_var.get()
    username=user_sign_var.get()
    password=pass_sign_var.get()
    if email=='' or '@' not in email or ' 'in email:
        ent3.config(highlightbackground='red')
        lab5_1.grid()
        return
    k=email.index('@')
    if k==0 or '.' not in email[k+1:]:
        ent3.config(highlightbackground='red')
        lab5_1.grid()
        return
    if email[k+1]=='.':
        ent3.config(highlightbackground='red')
        lab5_1.grid()
        return
    if email[k+1:].index('.')==len(email[k+1:])-1:
        ent3.config(highlightbackground='red')
        lab5_1.grid()
        return
    if username=='':
        lab6_1.config(fg='Red',text="Ussername can't be blank!!!")
        ent4.config(highlightbackground='red')
        lab6_1.grid()
        return
    if username=='USERNAME':
        lab6_1.config(fg='Red',text="You can't use this Username.")
        ent4.config(highlightbackground='red')
        lab6_1.grid()
        return
    f=0
    for i in username:
        k=ord(i)
        if (k<49 or k>57)and(k<97 or k>122)and(k<65 or k>90):
            lab6_1.config(fg='Red')
            ent4.config(highlightbackground='red',text="Username musn't containt any special character.")
            lab6_1.grid()
            f=1
            break
    if f==0:
        lab6_1.config(fg='#03b2fc',text="Username musn't containt any special character.")
        ent4.config(highlightbackground='#d1cec5')
        lab6_1.grid_remove()
    if password=='':
        lab7_1.config(fg='Red',text="Password can't be blank!!!")
        ent5.config(highlightbackground='red')
        lab7_1.grid()
        return
    if len(password)<6:
        lab7_1.config(fg='Red',text="Password must contain atleast 6 digits.")
        ent5.config(highlightbackground='Red')
        lab7_1.grid()
        return
    lab7_1.config(fg='#03b2fc',text="Password must contain atleast 6 digits.")
    ent5.config(highlightbackground='#d1cec5')
    lab7_1.grid_remove()
    query="select * from info where username='{}'".format(username)
    cursor.execute(query)
    dataset=cursor.fetchall()
    if dataset!=[]:
        lab6_1.config(fg='Red',text="Username Already Taken.")
        ent4.config(highlightbackground='red')
        lab6_1.grid()
        return
    query="Insert into info (USERNAME,PASSWORD,EMAIL) values('{}','{}','{}')".format(username,password,email)
    cursor.execute(query)
    mycon.commit()
    mycon.close()
    frame4.grid_remove()
    frame10.grid()


def to_log_in():
    frame4.focus_set()
    ent3.delete(0,'end')
    ent4.delete(0,'end')
    ent5.delete(0,'end')
    ent3.config(highlightbackground='#d1cec5')
    ent4.config(highlightbackground='#d1cec5')
    ent5.config(highlightbackground='#d1cec5')
    lab6_1.config(text="Username musn't containt any special character.",fg='#03b2fc')
    lab7_1.config(text="Password must contain atleast 6 digits.",fg='#03b2fc')
    lab5_1.grid_remove()
    lab6_1.grid_remove()
    lab7_1.grid_remove()
    frame4.grid_remove()
    frame1.grid()

def compress():
    global iniadd
    filepath=filedialog.askopenfilename(initialdir=iniadd,title="Select A File",filetypes=(("text files","*.txt"),('all files','*.*')))
    if filepath=='':
        messagebox.showinfo("Attention!","Invalid File Please Choose Correct File.")
        return
    iniadd=filepath
    compression(filepath)
    messagebox.showinfo("showinfo","File Compressed")

def decompress():
    global iniadd
    filepath=filedialog.askopenfilename(initialdir=iniadd,title="Select A File",filetypes=(("binary files","*.bin"),('all files','*.*')))
    if filepath=='':
        messagebox.showinfo("Attention!","Invalid File Please Choose Correct File.")
        return
    iniadd=filepath
    decompression(filepath)
    messagebox.showinfo("showinfo","File Decompressed")

def encypter():
    global iniadd
    filepath=filedialog.askopenfilename(initialdir=iniadd,title="Select A File",filetypes=(("text files","*.txt"),('all files','*.*')))
    if filepath=='':
        messagebox.showinfo("Attention!","Invalid File Please Choose Correct File.")
        return
    iniadd=filepath
    encyption(filepath)
    messagebox.showinfo("showinfo","File Encrypted")

def decrypter():
    global iniadd
    filepath=filedialog.askopenfilename(initialdir=iniadd,title="Select A File",filetypes=(("text files","*.txt"),('all files','*.*')))
    if filepath=='':
        messagebox.showinfo("Attention!","Invalid File Please Choose Correct File.")
        return
    iniadd=filepath
    root2=Tk()
    root2.title("Enter Key")
    root2.config(bg='#89ABE3')
    root2.geometry('500x200+525+200')
    root2.resizable('False','False')
    root2.focus_set()
    k_var=StringVar()
    label1=Label(root2,text='Enter Key',bg='#89ABE3',fg='#000000',font=('Microsoft YaHei UI',15)).grid(row=0,column=0,padx=20,pady=40)
    entry1=Entry(root2,width=25,fg='#000000',bg='#89ABE3',border=2,font=('Microsoft YaHei UI',15),textvariable=k_var)
    entry1.focus_set()
    entry1.grid(row=0,column=1)

    def decrypt2():
        k=entry1.get()
        root2.destroy()
        decrption(filepath,k)
        messagebox.showinfo("showinfo","File Decrypted")
    
    def decrypt3():
        global iniadd
        key_path=filedialog.askopenfilename(initialdir=iniadd,title="Select A File",filetypes=(("text files","*.txt"),('all files','*.*')))
        if key_path=='':
            messagebox.showinfo("Attention!","Invalid File Please Choose Correct File.")
            return
        iniadd=filepath
        root2.destroy()
        file=open(key_path,'r')
        k=file.read()
        file.flush()
        file.close()
        decrption(filepath,k)
        messagebox.showinfo("showinfo","File Decrypted")


    button1=Button(root2,text='Submit',font=('Microsoft YaHei UI',15),command=decrypt2).grid(row=1,column=0)
    button2=Button(root2,text='Use File',font=('Microsoft YaHei UI',15),command=decrypt3).grid(row=1,column=1,sticky='w',padx=35)
    root2.mainloop()
###################################################################################################################################################






root=Tk()
root.geometry('900x700+325+50')
root.config(bg='#89ABE3')
root.resizable('False','False')
root.title("Encrypt|Compress! What do you want?")
img1=Image.open('images/login.png')
sign_in=ImageTk.PhotoImage(img1)
img2=Image.open('images/bg1.png')
bg1=ImageTk.PhotoImage(img2)
img3=Image.open('images/loginbtn.png')
log_in=ImageTk.PhotoImage(img3)
img4=Image.open('images/signupbtn.png')
sign_up=ImageTk.PhotoImage(img4)
img5=Image.open('images/bg2.png')
bg2=ImageTk.PhotoImage(img5)
img6=Image.open('images/encrypt.png')
encrypimg=ImageTk.PhotoImage(img6)
img7=Image.open('images/decrypt.png')
decryptimg=ImageTk.PhotoImage(img7)
img8=Image.open('images/compress.png')
compressimg=ImageTk.PhotoImage(img8)
img9=Image.open('images/decompress.png')
decompressimg=ImageTk.PhotoImage(img9)
iniadd="C:/"

###################################################################################################################################################

frame1=Frame(root,bg='#89ABE3')

frame2=Frame(frame1,bg='#89ABE3')
lab1=Label(frame2,image=sign_in,bg='#89ABE3').grid(row=0,column=0,padx=70,pady=150)
frame2.grid(row=0,column=0,sticky='n')

frame3=Frame(frame1,bg='#89ABE3')
lab2=Label(frame3,text='ACCOUNT LOGIN',fg='#472D2D',bg='#89ABE3',font=('Microsoft YaHei UI',23)).grid(row=0,column=0,pady=45,sticky='w')
frame3_0=Frame(frame3,bg='#89ABE3')

frame4=Frame(frame3_0,bg='#89ABE3')
def on_enter(e):
    name=ent1.get()
    ent1.config(fg='#1A3636')
    if name=='USERNAME':
        ent1.delete(0,'end')
def in_focus(e):
    name=ent1.get()
    ent1.config(fg='#1A3636')
    if name=='USERNAME'or name=='Invalid Username':
        ent1.delete(0,'end')
    
def on_leave(e):
    name=ent1.get()
    if name=='Invalid Username':
        ent1.config(fg='red')
    if str(root.focus_get())=='.!frame.!frame2.!frame.!frame.!entry':
        return
    if name=='':
        ent1.insert(0,'USERNAME')
    
    
def out_focus(e):
    name=ent1.get()
    if name=='':
        ent1.insert(0,'USERNAME')

def on_click(e):
    ent1.config(fg='#1A3636')

user_log_var=StringVar()
ent1=Entry(frame4,width=30,fg='#1A3636',bg='#89ABE3',border=0,font=('Microsoft YaHei UI',15),textvariable=user_log_var)
ent1.grid(row=0,column=0)
ent1.insert(0,'USERNAME')
ent1.bind('<Enter>',on_enter)
ent1.bind('<Leave>',on_leave)
ent1.bind('<FocusIn>',in_focus)
ent1.bind('<FocusOut>',out_focus)
ent1.bind("<ButtonRelease>",on_click)
Frame(frame4,width=295,height=2,bg='#000000').grid(row=1,column=0,sticky='w')
frame4.grid(row=1,column=0,sticky='w')

frame5=Frame(frame3_0,bg='#89ABE3')
def on_enter(e):
    name=ent2.get()
    ent2.config(fg='#1A3636')
    if name=='PASSWORD':
        ent2.delete(0,'end')
def in_focus(e):
    name=ent2.get()
    if name=='PASSWORD'or name=='Invalid Password'or name=='Password must contain atleast 6 digits':
        ent2.delete(0,'end')
def on_leave(e):
    name=ent2.get()
    if name=='Invalid Password'or name=='Password must contain atleast 6 digits':
        ent2.config(fg='red')
    if str(root.focus_get())=='.!frame.!frame2.!frame.!frame2.!entry':
        return
    if name=='':
        ent2.insert(0,'PASSWORD')
def out_focus(e):
    name=ent2.get()
    if name=='':
        ent2.insert(0,'PASSWORD')
def on_click(e):
    ent2.config(fg='#1A3636')

pass_log_var=StringVar()
ent2=Entry(frame5,width=30,fg='#1A3636',bg='#89ABE3',border=0,font=('Microsoft YaHei UI',15),textvariable=pass_log_var)
ent2.grid(row=0,column=0)
ent2.bind('<FocusIn>',in_focus)
ent2.bind('<FocusOut>',out_focus)
ent2.bind('<Enter>',on_enter)
ent2.bind('<Leave>',on_leave)
ent2.bind("<ButtonRelease>",on_click)
ent2.insert(0,'PASSWORD')
Frame(frame5,width=295,height=2,bg='#000000').grid(row=1,column=0,sticky='w')
frame5.grid(row=2,column=0,sticky='w',pady=50)
frame3_0.grid(row=2,column=0,sticky='w')
btn1=Button(frame3,image=log_in,border=0,command=logged,bg='#89ABE3',activebackground='#89ABE3')
btn1.grid(row=3,column=0,sticky='w',padx=30)
frame3_1=Frame(frame3,bg='#89ABE3')
lab3=Label(frame3_1,text='New User!',fg='#000000',bg='#89ABE3',font=('Microsoft YaHei UI',12)).grid(row=0,column=0)
btn2=Button(frame3_1,text='Sign Up',border=0,bg='#89ABE3',fg='#363062',cursor='hand2',font=('Microsoft YaHei UI',12),command=to_sign_up,activebackground='#89ABE3').grid(row=0,column=1)
frame3_1.grid(row=4,column=0,pady=15,sticky='w')
frame3.grid(row=0,column=1,sticky='n',pady=60)

frame1.grid(row=0,column=0)

###################################################################################################################################################


frame4=Frame(root,bg='#ffffff')
lab4=Label(frame4,bg='#ffffff',image=bg1).grid(row=0,column=0)

frame5=Frame(frame4,bg='#ffffff',width=450,height=500,highlightbackground='#d1cec5',highlightcolor='#d1cec5', highlightthickness=3)
frame5_1=Frame(frame5,bg='#ffffff')
lab5=Label(frame5_1,text='Create Account',font=('Microsoft JhengHei Light',35),bg='#ffffff',fg='#000000').grid(row=0,column=0,padx=50)

frame6=Frame(frame5_1,bg='#ffffff')

frame7=Frame(frame6,bg='#ffffff',width=450,height=500)
def do2(e):
    name=ent3.get()
    if name=='' or '@' not in name or ' 'in name:
        ent3.config(highlightbackground='red')
        lab5_1.grid()
    else:
        k=name.index('@')
        if k==0 or '.' not in name[k+1:]:
            ent3.config(highlightbackground='red')
            lab5_1.grid()
        elif name[k+1]=='.':
            ent3.config(highlightbackground='red')
            lab5_1.grid()
        if name[k+1:].index('.')==len(name[k+1:])-1:
            ent3.config(highlightbackground='red')
            lab5_1.grid()
def do1(e):
    ent3.config(highlightbackground='#d1cec5')
    lab5_1.grid_remove()
lab5=Label(frame7,text='Email',font=('Microsoft JhengHei Light',15),bg='#ffffff',fg='#000000').grid(row=0,column=0,sticky='w')
email_var=StringVar()
ent3=Entry(frame7,width=42,border=1,relief=GROOVE,highlightbackground='#d1cec5',highlightcolor='#03b2fc',highlightthickness=1,font=('Microsoft JhengHei Light',12),textvariable=email_var)
ent3.grid(row=1,column=0,sticky='w')
ent3.bind('<FocusIn>',do1)
ent3.bind('<FocusOut>',do2)
lab5_1=Label(frame7,text='Invalid Email Address!!!',font=('Microsoft JhengHei Light',13),bg='#ffffff',fg='red')
lab5_1.grid(row=2,column=0)
lab5_1.grid_remove()
frame7.grid(row=0,column=0,pady=10,padx=10)

frame8=Frame(frame6,bg='#ffffff',width=450,height=500)

a=1
def do1(e):
    global a
    name=ent4.get()
    if name=='':
        lab6_1.config(fg='#03b2fc',text="Username musn't containt any special character.")
        ent4.config(highlightbackground='#03b2fc')
        lab6_1.grid()
    else:
        lab6_1.config(fg='#03b2fc',text="Username musn't containt any special character.")
        ent4.config(highlightbackground='#03b2fc')
        lab6_1.grid()

def do2(e):
    name=ent4.get()
    if name=='':
        lab6_1.config(fg='Red',text="Ussername can't be blank!!!")
        ent4.config(highlightbackground='red')
        lab6_1.grid()
        return
    if name=='USERNAME':
        lab6_1.config(fg='Red',text="You can't use this Username.")
        ent4.config(highlightbackground='red')
        lab6_1.grid()
        return  
    else:
        f=0
        for i in name:
            k=ord(i)
            if (k<49 or k>57)and(k<97 or k>122)and(k<65 or k>90):
                lab6_1.config(fg='Red')
                ent4.config(highlightbackground='red',text="Username musn't containt any special character.")
                lab6_1.grid()
                f=1
                break
        if f==0:
            lab6_1.config(fg='#03b2fc',text="Username musn't containt any special character.")
            ent4.config(highlightbackground='#d1cec5')
            lab6_1.grid_remove()
lab6=Label(frame8,text='Username',font=('Microsoft JhengHei Light',15),bg='#ffffff',fg='#000000').grid(row=0,column=0,sticky='w')
user_sign_var=StringVar()
ent4=Entry(frame8,width=42,border=1,relief=GROOVE,highlightbackground='#d1cec5',highlightcolor='#03b2fc',highlightthickness=1,font=('Microsoft JhengHei Light',12),textvariable=user_sign_var)
ent4.grid(row=1,column=0,sticky='w')
ent4.bind('<FocusIn>',do1)
ent4.bind('<FocusOut>',do2)
lab6_1=Label(frame8,text="Username musn't containt any special character.",font=('Microsoft JhengHei Light',13),bg='#ffffff',fg='#03b2fc')
lab6_1.grid(row=2,column=0)
lab6_1.grid_remove()
frame8.grid(row=1,column=0,pady=10,padx=10)

frame9=Frame(frame6,bg='#ffffff',width=450,height=500)
def do1(e):
    name=ent5.get()
    if name=='':
        lab7_1.config(fg='red',text="Password can't be blank!!!")
        ent5.config(highlightbackground='red')
        lab7_1.grid()
    if name=='PASSWORD':
        lab7_1.config(fg='red',text="You can't use this Password.")
        ent5.config(highlightbackground='red')
        lab7_1.grid()
    else:
        lab7_1.config(fg='#03b2fc',text="Password must contain atleast 6 digit.")
        ent5.config(highlightbackground='#03b2fc')
        lab7_1.grid()
def do2(e):
    name=ent5.get()
    if name=='':
        lab7_1.config(fg='Red',text="Password can't be blank!!!")
        ent5.config(highlightbackground='red')
        lab7_1.grid()
    elif len(name)<6:
        lab7_1.config(fg='Red',text="Password must contain atleast 6 digits.")
        ent5.config(highlightbackground='Red')
        lab7_1.grid()
    else:
        lab7_1.config(fg='#03b2fc',text="Password must contain atleast 6 digits.")
        ent5.config(highlightbackground='#d1cec5')
        lab7_1.grid_remove()
lab7=Label(frame9,text='Password',border=0,font=('Microsoft JhengHei Light',15),bg='#ffffff',fg='#000000').grid(row=0,column=0,sticky='w')
pass_sign_var=StringVar()
ent5=Entry(frame9,width=42,border=1,relief=GROOVE,highlightbackground='#d1cec5',highlightcolor='#03b2fc',highlightthickness=1,font=('Microsoft JhengHei Light',12),textvariable=pass_sign_var)
ent5.grid(row=1,column=0,sticky='w')
ent5.bind('<FocusIn>',do1)
ent5.bind('<FocusOut>',do2)
lab7_1=Label(frame9,text="Password must contain atleast 6 digits.",font=('Microsoft JhengHei Light',13),bg='#ffffff',fg='#03b2fc')
frame9.grid(row=2,column=0,pady=10,padx=10)

frame6.grid(row=1,column=0,sticky='w',padx=20,columnspan=2)

btn3=Button(frame5_1,border=0,image=sign_up,command=signed,bg='#ffffff',activebackground='#ffffff').grid(row=2,column=0)
btn4=Button(frame5_1,text='Go Back',font=('Microsoft JhengHei Light',15),border=0,bg='#ffffff',fg='#AB2508',cursor='hand2',command=to_log_in,activebackground='#ffffff',activeforeground='#000000').grid(row=3,column=0,sticky='w',padx=30)


frame5_1.grid(row=0,column=0,pady=40)

frame5.grid(row=0,column=0)


frame4.grid(row=0,column=0)


###################################################################################################################################################

frame10=Frame(root,bg='#ffffff')

lab8=Label(frame10,image=bg2,bg='#ffffff').grid(row=0,column=0)
frame11_0=Frame(frame10,highlightbackground='#adadad',highlightthickness=3,bg='#ffffff')
frame11=Frame(frame11_0,bg='#ffffff')

lab10=Label(frame11,text='What do you want to choose?',font=('Microsoft JhengHei Light ',40),bg='#ffffff',fg='#184D47').grid(row=0,column=0,columnspan=2)

frame12=Frame(frame11,bg='#ffffff')
btn5=Button(frame12,image=encrypimg,border=0,bg='#ffffff',activebackground='#ffffff',command=encypter,cursor='hand2').grid(row=0,column=0,pady=30)
btn6=Button(frame12,image=decryptimg,border=0,bg='#ffffff',activebackground='#ffffff',command=decrypter,cursor='hand2').grid(row=1,column=0)
frame13=Frame(frame11,bg='#ffffff')
btn7=Button(frame13,image=compressimg,border=0,bg='#ffffff',activebackground='#ffffff',command=compress,cursor='hand2').grid(row=0,column=0,pady=30)
btn8=Button(frame13,image=decompressimg,border=0,bg='#ffffff',activebackground='#ffffff',command=decompress,cursor='hand2').grid(row=1,column=0)



frame12.grid(row=1,column=0)
frame13.grid(row=1,column=1)


frame11.grid(row=0,column=0,padx=25,pady=30)
frame11_0.grid(row=0,column=0)

frame10.grid(row=0,column=0)

frame4.grid_remove()
frame10.grid_remove()
root.mainloop()
###################################################################################################################################################