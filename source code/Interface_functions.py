#from tkinter import *
import customtkinter as ctk
import json
import time
import CTkMessagebox
import tkinter
import threading
from PIL import Image, ImageTk
import os
import re
from plyer import notification
ctk.set_appearance_mode("light")

global check
check="normal"
global mode
mode="walo"
offlines_list=list()
def show_error():
    # Show some error message
   CTkMessagebox.CTkMessagebox(title="Error", message="you didn't fill all infos!!",icon="icons\\info.png").focus_force()
    
def success():
    CTkMessagebox.CTkMessagebox(title="connected", message="Connected successfully",icon="icons\\check.png",option_1="Thanks")
    
        
    
def invalid():
    # Show some error message
    CTkMessagebox.CTkMessagebox(title="invalid", message="Informations are incorrect",icon="icons\\warning.png").focus_force()
    
def signup(client):
    #***********************************THIS IS THE CHAT INTERFACE***********************************************
#**********************************************************************************************************
    
    def chat_win(log_win):
        global buttons    
        buttons=[]
        def groupchat(info):
           global mode
           mode=f"grp{info}"
           label.configure(text=info)
           print("l7ala daba",mode)
           client.send("@out".encode("utf-8"))
           time.sleep(0.3)
           client.send(f"@msggr {info}".encode("utf-8")) 
           if msgbox:
                msgbox.configure(state="normal")
                msgbox.delete("1.0","end")
                msgbox.configure(state="disabled")
        def privatechat(info):
            global mode
            mode=f"prv{info}"
            label.configure(text=info)
            print("l7ala daba",mode)
            client.send("@out".encode("utf-8"))
            if msgbox:
                msgbox.configure(state="normal")
                msgbox.delete("1.0","end")
                msgbox.configure(state="disabled")
            #time.sleep(0.2)
            client.send(f"@prv {info}".encode("utf-8"))
            
            
        def groupbuttons(grpname):
            
            ctk.CTkButton(frame,
                          text=grpname,
                          width=170,
                          height=30,
                          fg_color="#560196",
                          hover_color="#8402E6",
                          font=("helvatica",15,"bold"),
                          corner_radius=20,
                          command=lambda  info= grpname : groupchat(info)).pack(pady=3)
        def get_history():
            msgbox.configure(state="normal")
            while True:
                try:
                    message=client.recv(1024).decode("utf-8")
                    message=message.strip()
                    if bool(re.search("^@endhist",message))==True: 
                        print("ha lmessage")
                        msgbox.configure(state="disabled")
                        break
                    elif bool(re.search("^@endhist",message))==False:
                        msgbox.insert(ctk.END,message+"\n")
                    
                except:
                    print("shoot!!!")

        def adduser(user):
            if  user!=whoami:
                print("kayn")
                button=ctk.CTkButton(frame,text=user,
                                            font=("helvatica",15,"bold"),
                                            width=175,
                                            height=30,
                                            fg_color="#185EEC",
                                            hover_color="#0095F6",
                                            corner_radius=20,
                                            command=lambda  info= user : privatechat(info))
                button.pack(pady=3)
                buttons.append(button)
                print("sala")
        def add_off_user(user):
            global mode
            mode="historique"
            if  user!=whoami:
                
                button=ctk.CTkButton(frame,text=user,
                                            font=("helvatica",15,"bold"),
                                            width=175,
                                            height=30,
                                            fg_color="#707070",
                                            hover_color="#BABCC1",
                                            corner_radius=20,
                                            command=lambda  info= user : see_history(info))
                button.pack(pady=3)
                buttons.append(button)
        def see_history(info):
            global mode
            mode=f"walo"
            label.configure(text=info)
            print("l7ala daba",mode)
            client.send("@out".encode("utf-8"))
            if msgbox:
                msgbox.configure(state="normal")
                msgbox.delete("1.0","end")
                msgbox.configure(state="disabled")
            #time.sleep(0.2)
            client.send(f"@offlinehist,{info}".encode("utf-8"))        
        def receiving(msgbox):

            
            ls=list()


            
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++
            i=0
            while True:    
                try:
                    
                
                    #time.sleep(0.3)
                    mesg=client.recv(1024).decode("utf-8")
                    mesg=mesg.strip()
                    print(mesg)
                    #*******HERE WHERE THE USER WILL GET THE LLIST OF OTHER USERS*****
                    #******************************************************************
                    if "list$" in mesg:
                        global offlines_list
                        offlines=(mesg.split("$"))[1]
                        offlines_list=json.loads(offlines)
                        for offline in offlines_list:
                            add_off_user(offline)
                            
                    elif "@ls," in mesg:
                        print("now")
                        servermsg=mesg
                        serverlist=re.split(",",(re.sub("^@ls,","",servermsg)))
                        print(serverlist)
                        if len(serverlist)!=0:
                            #try:
                                #print("dkhel")
                                for user in serverlist:
                                    
                                    if user not in ls:
                                        
                                        ls.append(user)
                                        if user in offlines_list:
                                            offlines_list.remove(user)
                                            for button in buttons:
                                                if user==button.cget("text"):
                                                    buttons.remove(button)
                                                    button.destroy()
                                        #time.sleep(0.5)
                                        adduser(user)
                                        #print("dkhel mzyan") 
                    elif bool(re.search("^@grresp",mesg))==True:
                            if "@grresptrue" in mesg:
                                CTkMessagebox.CTkMessagebox(title="Success", message="Group created successfully",icon="icons\\check.png").focus_force()
                            else:
                                CTkMessagebox.CTkMessagebox(title="Error", message="THIS NAME ALREADY EXISTS",icon="icons\\warning.png").focus_force()
                    elif bool(re.search("^@truepseudo,",mesg))==True:
                        whoami=(mesg.split(","))[1]
                        chat.title(whoami)
                        CTkMessagebox.CTkMessagebox(title="Done(:",message="Username was updated successfully", icon="icons\\check.png")
                    elif bool(re.search("^@falsepseudo,",mesg))==True:
                        CTkMessagebox.CTKmessagebox(title="invalid",message="this Username already exists!!", icon="icon\\info.png")
                    elif bool(re.search("^@update",mesg))==True:
                        mesg=mesg.split(",")
                        print(f"oldname: {mesg[2]} newname: {mesg[1]}")
                        for butn in buttons:
                            if butn.cget("text")==mesg[2]:
                                print("found it")
                                buttons.remove(butn)
                                butn.destroy()
                                break
                        ls[ls.index(mesg[2])]=mesg[1]
                        adduser(mesg[1])
                    elif mesg=="" or (i==0 and mesg=="True"):
                        i=1
                        continue    
                    #++++++++++++++++++++HERE WHERE THE USER WILL GET THE LLIST OF OTHER USERS+++++++++++++++++++++++++++++++++++++++++++++++
                    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    #********************HERE WHERE THE DELETION OF DISCONNECTED CLIENTS WILL HAPPEND*******************
                    elif bool(re.search("^@@ ",mesg)):
                        #print("i am here")
                        disconnected=re.sub("^@@ ","",mesg)
                        for button in buttons:
                            if disconnected==button.cget("text"):
                                
                                buttons.remove(button)
                                button.destroy()
                                offlines_list.append(disconnected)
                                if disconnected in ls:
                                    ls.remove(disconnected)
                                add_off_user(disconnected)
                                
                                break
                        
                    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    #***********************HERE WHERE A NEW GROUPE BUTTON IS CREATED****************
                    elif bool(re.search("^@crgr ",mesg)):
                        grpname=re.sub("^@crgr ","",mesg)     
                        groupbuttons(grpname)
                    #++++++++++++++++++++HERE WHERE A NEW GROUPE BUTTON IS CREATED++++++++++++++++++++++++++++
                    
                    #**********************HERE WHERE THE HISTORY IS CALLED*****************************
                    elif bool(re.search("^@hist",mesg)):
                        get_history()
                    #+++++++++++++++++++++++++HERE WHERE THE HISTORY IS CALLED+++++++++++++++++++++
                    elif bool(re.search("^@grpslist",mesg)):
                        
                        grpnames=re.sub("^@grpslist,","",mesg)
                        grpnames=grpnames.split(",")
                        #print(grpnames)
                        for grpname in grpnames:
                            groupbuttons(grpname)
                    else:
                        mesg=mesg.split(",")
                        #print("hada li ja:",mesg[0])
                        #print("mode:",mode)
                        if mesg[0]==mode:
                            
                            msgbox.configure(state="normal")
                            msgbox.insert("end",mesg[1]+"\n")
                            msgbox.configure(state="disabled")
                        else:
                            if "prv" in mesg[0]:
                                temp=re.sub("prv","",mesg[0])
                                temp=f"New message from {temp}"
                            else:
                                temp=re.sub("grp","",mesg[0])
                                temp=f"New message in {temp}"
                            notification.notify(title=temp,message=f"{mesg[1]}",timeout=10)
                        #print("somthing happened")
                    
                    
                except ImportError as moch:
                        print("you didn't recieve the msg")
                        client.close()
                        exit(0)   
                 
        def showmesg():
            if mode!="walo":
                if msgentry.get():
                    msgbox.configure(state="normal")
                    msg=msgentry.get()
                    msgbox.insert(ctk.END,"you: "+msgentry.get()+"\n")
                    
                    msgbox.configure(state="disabled")
                    
                    try:
                        client.send(msg.encode("utf-8"))
                    except:
                        print("message wasn't sent")
                    msgentry.delete("0", "end")
                else:
                    pass
        def change_username():
            #print("am in ")
            newpseudo=ctk.CTkInputDialog(text="Enter your New Username",title="CHANGE USERNAME")
            text=newpseudo.get_input()
            
            if text:
                client.send(f"@out".encode("utf-8"))
                time.sleep(0.2)

                client.send(f"@newname,{text}".encode("utf-8"))
                msgbox.configure(state="normal")
                msgbox.delete("1.0","end")
                msgbox.configure(state="disabled")
                
                
            else:
                CTkMessagebox.CTkMessagebox(title="info",message="you left the entry empty")
                
        def creatgroup(botonat):
            def creation():
               
                
                if groupname.get():
                    gr="@gr"
                    grname=groupname.get()
                    gr +=","+grname
                    gr +=f",{whoami}"
                    for box in boxes:
                        #print((box.cget("variable")).get())
                        if (box.cget("variable")).get()=="on":
                            gr +=","+ box.cget("text")
                    
                    #print(gr)
                    client.send(gr.encode("utf-8"))
                    grtop.destroy()
                    #response=client.recv(1024).decode("utf-8")
                    #print("response:",response)
                    """if "@grresptrue" in response:
                        grtop.destroy()
                    else:
                        CTkMessagebox.CTkMessagebox(title="Error", message="THIS NAME ALREADY EXISTS",icon="icons\\info.png").focus_force()"""
                else:
                     pass
            grtop=ctk.CTkToplevel()
            grtop.resizable(width=False,height=False)
            groupname=ctk.CTkEntry(grtop,width=178,height=38,
                            fg_color="#ECEDEF",
                            corner_radius=14,
                            placeholder_text="Groupe name...")
            groupname.place(x=13,y=0)
            botona=ctk.CTkButton(grtop,text="CREATE",
                                 height=30,
                                 width=50,
                                 font=("Bahnschrift",16,"normal"),
                                 corner_radius=14,
                                 command=creation)
            
            
            topframe=ctk.CTkScrollableFrame(grtop,width=250,
                                            height=130,
                                            fg_color="#A4D5FF")
            topframe.place(x=13,y=40)
            botona.place(x=193,y=5)
            boxes=list()
            for button in botonat:
                  name=button.cget("text")
                  check_var = ctk.StringVar(value="off")
                  checkbox=ctk.CTkCheckBox(topframe,text=f"{name}",
                                          variable=check_var,
                                          onvalue="on",offvalue="off")
                  boxes.append(checkbox)
                  checkbox.pack(pady=3)
            grtop.geometry("300x270")
            grtop.focus()
        chat=ctk.CTk()
        chat.geometry("500x610")
        chat.configure(fg_color="#F2F9FF")
        chat.resizable(width=False,height=False)
        chat.title("Instant Messaging")
        
        msgentry=ctk.CTkEntry(master=chat,
                            width=322,height=38,
                            #fg_color="#ECEDEF",
                            placeholder_text="Message",
                            
                            corner_radius=21)
        msgentry.place(x=9,y=563)
        global msgbox
        
        NewGRP=ctk.CTkButton(chat,text="       Create Groupe      ",
                          text_color="white",
                          hover_color="#01D4A9",
                          font=("Bahnschrift",18,"bold"),
                          fg_color="#01A382",
                          compound="left",
                          corner_radius=25,
                          width=39,
                          command=lambda info=buttons :creatgroup(info))
        NewGRP.place(x=3,y=37)
        pseudo=ctk.CTkButton(chat,text="   Change Username    ",
                          text_color="white",
                          hover_color="#01D4A9",
                          font=("Bahnschrift",18,"bold"),
                          fg_color="#01A382",
                          compound="left",
                          corner_radius=25,
                          width=39,
                          command= change_username)
        pseudo.place(x=3,y=1)
        label=ctk.CTkLabel(chat,width=275,height=30,
                   text="....",
                   font=("Bahnschrift",18,"bold"))
        label.place(x=225,y=40)
        frame=ctk.CTkScrollableFrame(master=chat,
                             width=200,height=475,
                             fg_color="#69A2C7",
                             border_width=0,
                             border_color="#000000")
        msgbox=ctk.CTkTextbox(master=chat,
                            width=275,height=488,
                            corner_radius=10,
                            state="disabled",
                            fg_color="#F9FDFF",                      
                            text_color="#01315B",
                            font=("Neue Helvetica",18),
                            border_color="#C1C5CB",
                            border_width=2
                            )
        msgbox.place(x=225,y=69)
        send_button=ctk.CTkButton(master=chat,text="Send",
                                font=("Segoe UI",18,"bold"),
                                width=72,height=38,
                                fg_color="#0078C7",
                                hover_color="#0095F6",
                                corner_radius=19,
                                command=showmesg)
        send_button.place(x=348,y=563)
        def onclosing_chat():
            try:
                client.send("@out".encode("utf-8"))
                time.sleep(0.3)
                client.send("disconnect".encode("utf-8"))
                log_win.destroy()
                chat.destroy()
                exit(0)
            except:
                exit(0)
        
        frame.place(x=0,y=69)
        reccc=threading.Thread(target=receiving,args=(msgbox,))
        reccc.setDaemon(True)
        chat.after(1000,reccc.start())
        chat.protocol("WM_DELETE_WINDOW",onclosing_chat)
        
        chat.mainloop()
        

            
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #***********************RESPONSABLE FOR SHOWING PASSWORD*************************************************
    def show_pass():
        if password.cget("show")=="":
            password.configure(show="*")
        else:
            password.configure(show="")
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        

    def handle_signup(e):

         
        
        if  all([username.get(),password.get(),lastname.get(),firstname.get()]):
            user_data={
            "firstname":firstname.get(),
            "lastname":lastname.get(),
            "nickname":username.get(),
            "password":password.get()

            }
            list=json.dumps(user_data)
            client.send(list.encode("utf-8"))
            
            check=client.recv(1024).decode("utf-8")
            #print("this is",check)
            if "0" in str(check):
                CTkMessagebox.CTkMessagebox(title="Error", message="username already exists",icon="icons\\info.png").focus_force()
                pass
            else:
                CTkMessagebox.CTkMessagebox(title="Success", message="Account Created Successfully",icon="icons\\check.png").focus_force()
                window.withdraw()
                login()
        else:
            #username.focus_force()
            print("signup problem occured")
            show_error()
    def handle_login(logname,logpass,log_win):
        #the first if statement is to make sure all feilds are filled
        
        if  all([logname.get(),logpass.get()]):
            user_data={
            "nickname":logname.get(),
            "password":logpass.get()

            }
            list=json.dumps(user_data)
            client.send(list.encode("utf-8"))
            verify=client.recv(1024).decode("utf-8")
            verify=verify.strip()
            #print(verify)
            #the 2nd if statement is to make sure the login infos are correct
            if verify=="True" or bool(re.search("^@ls.*$",verify)):
                
                log_win.withdraw()
                log_win.unbind("<Return>")
                global whoami
                whoami=str()
                whoami=user_data["nickname"]
                #threading.Thread(target=chat_win, args=(log_win,)).start()
                chat_win(log_win)
                
            else:
                logname.delete("0","end")
                logpass.delete("0","end")
                invalid()
                #handle_login(logname,logpass,log_win)
                pass
                
                #HERE I SHOW A MESSAGE SAYS INFOS ARE INCORRECT
        else:
            print("problem occured")
            show_error()
            
            pass
    #************************************Login window function*************************************************
    def login():
        try:
            #print("it is here then")
            window.withdraw()
        except:
            print("the job was not completed")
        
        log_win=ctk.CTk()
        log_win.geometry("440x520")
        log_win.configure(fg_color="#F2F9FF")
        log_win.title("Instant Messaging")
        
        login_acount=ctk.CTkLabel(master=log_win,text="Login",font=("Segeo UI",31,"bold"),
                                text_color="#2E447A",
                                width=282,height=41).place(x=79,y=16)
        lab_username= ctk.CTkLabel(master=log_win,
                                text="Username",
                                font=('Segoe UI',18,"bold"),
                                text_color="#01315B",
                                ).place(x=80,y=99)
        logname=ctk.CTkEntry(master=log_win,
                            placeholder_text="enter your username",
                            width=286,height=45,
                            corner_radius=25,
                            border_color="#002168"
                            )

        lab_password= ctk.CTkLabel(master=log_win,
                                text="password",
                                font=('Segoe UI',18,"bold"),
                                text_color="#01315B",
                                ).place(x=80,y=213)
        logpass=ctk.CTkEntry(master=log_win,
                            placeholder_text="enter your password",
                            width=286,height=45,
                            corner_radius=25,
                            border_color="#002168")
        
        login_button= ctk.CTkButton(master=log_win,
                                text_color="#FFFFFF",
                                hover_color="#0078C7",
                                text="Sign in",
                                font=("Segoe UI",18,"bold"),
                                fg_color="#0095F6",
                                width=178,height=37,
                                corner_radius=45,
                                command=lambda : handle_login(logname,logpass,log_win))
        #login_button.cget("text")
        
        logpass.place(x=80,y=261)
        logname.place(x=80,y=138)
        login_button.place(x=131,y=356)
        logname.bind("<Return>",lambda event: handle_login(logname,logpass,log_win))
        logpass.bind("<Return>",lambda event: handle_login(logname,logpass,log_win))
        def on_closing():
            #client.close()
            try:
                print("it is logwin")
                window.deiconify()
                log_win.destroy()
            except:
                exit(0)

        log_win.protocol("WM_DELETE_WINDOW", on_closing)
        log_win.mainloop()
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
        
    #****************************begining of the signup window********************************************   
    window=ctk.CTk()
    #file_path=os.path.dirname(os.path.realpath(__file__))
    eye=ctk.CTkImage(light_image=Image.open(os.path.join("opened.png")), size=(40 , 40))
    
    window.geometry("440x545")
    window.resizable(width=False,height=False)
    window.title("Instant Messaging")
    window.configure(fg_color="#F2F9FF")
    creat_acount=ctk.CTkLabel(master=window,text="Create New Acount:",font=("Segeo UI",31,"bold"),
                              text_color="#2E447A",
                              width=282,height=41).place(x=79,y=16)
    #*********************************the Entry of the firstname*************************************************
    lab_first= ctk.CTkLabel(master=window,
                            text="First name",
                            font=('Segoe UI',18,"bold"),
                            text_color="#01315B",
                            ).place(x=80,y=89)
    firstname=ctk.CTkEntry(master=window,
                          placeholder_text="Enter your First_name",
                          width=286,height=45,
                          corner_radius=25,
                          border_width=2,
                          border_color="#002168")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#*********************************the Entry of the lastname*************************************************
    lab_last= ctk.CTkLabel(master=window,
                            text="Last name",
                            font=('Segoe UI',18,"bold"),
                            text_color="#01315B",
                            ).place(x=80,y=180)
    lastname=ctk.CTkEntry(master=window,
                          placeholder_text="Enter your Last_name",
                          width=286,height=45,
                          corner_radius=25,
                          border_color="#002168")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# *********************************the Entry of the username*************************************************
    lab_username= ctk.CTkLabel(master=window,
                            text="Username",
                            font=('Segoe UI',18,"bold"),
                            text_color="#01315B",
                            ).place(x=80,y=271)
    username=ctk.CTkEntry(master=window,
                          placeholder_text="enter your name",
                          width=286,height=45,
                          corner_radius=25,
                          border_color="#002168")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    lab_password= ctk.CTkLabel(master=window,
                            text="password",
                            font=('Segoe UI',18,"bold"),
                            text_color="#01315B",
                            ).place(x=80,y=362)
    password_button=ctk.CTkButton(master=window,
                                  image=eye,
                                  text="",
                                  hover_color="#E7EEFD",
                                  fg_color="#F2F9FF",
                                  width=43,
                                  height=38,
                                  command=show_pass)
    password=ctk.CTkEntry(master=window,
                          placeholder_text="enter your password",
                          width=286,height=45,
                          corner_radius=25,
                          show="*",
                          border_color="#002168")
    
    sign= ctk.CTkButton(master=window,
                            fg_color="#0095F6",
                            text="Sign up",
                            font=("Segoe UI",18,"bold"),
                            text_color="#FFFFFF",
                            hover_color="#0078C7",
                            width=178,height=37,
                            corner_radius=45,
                            command= lambda event=None:handle_signup(event) )
    #************************************goto login window button*****************************************
    gotolog= ctk.CTkButton(master=window,
                            fg_color="#F2F9FF",
                            text="Log in",
                            font=("Segoe UI",15,"bold"),
                            text_color="#002168",
                            
                            hover_color="#E7EEFD",
                            width=44,height=20,
                            corner_radius=45,     
                            command= login  )
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    already=ctk.CTkLabel(master=window,
                         text="Already have an account ?",
                         font=("Segoe UI",15),
                         text_color="#034F91",
                         ).place(x=71,y=514)
    password_button.place(x=376,y=397)
    firstname.place(x=80,y=124)
    lastname.place(x=77,y=215)
    password.place(x=80,y=397)
    username.place(x=80,y=306)
    gotolog.place(x=288,y=514)
    sign.place(x=136,y=453)
    window.bind("<Return>",lambda event:handle_signup(event))
    def onclosing_window():
        client.close()
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", onclosing_window)
    window.mainloop()




#login()


