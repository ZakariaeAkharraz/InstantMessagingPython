import socket
import json
import threading
import sqlite3
import time
import re
#******the creation of data base*******************************
connection = sqlite3.connect("datab.db")
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS PERSONS (nickname TEXT PRIMARY KEY,firstname TEXT,lastname TEXT,password INTEGER);")
cursor.execute("create table if not exists rooms (room text, users text)")
cursor.execute("create table if not exists history (sender text,receiver text,message text)")
connection.commit()
connection.close()
#+++++++++++the creation of data base+++++++++++++++++++++++++++
Grups=dict()
def restore_grps_infos():
    sql=sqlite3.connect("datab.db")
    cursor=sql.cursor()
    cursor.execute("select * from rooms")
    all_infos=cursor.fetchall()
    if all_infos:
        for line in all_infos:
            grptitle=line[0]
            users=line[1]
            users=users.split(",")
            print("line:",line)
            print("title:",grptitle)
            print("users:",users)
            users.remove(users[0])
            users.remove(users[len(users)-1])
            
            Grups.update({grptitle:users})
    sql.close()
def restore_all_users():
    sql=sqlite3.connect("datab.db")
    cursor=sql.cursor()
    cursor.execute("select nickname from persons")
    all_infos=cursor.fetchall()
    global offlines
    offlines=list()
    for couple in all_infos:
        offlines.append(couple[0])
    
           
            
    sql.close()
def create_sock():
    try:
        global format
        format="utf-8"
        global host
        global thread
        global port
        #this is the socket variable:
        global s

        global accept
        
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    except socket.error as msg:
        print('a socket was not created', str(msg))
        global sql
        global cursor
#\\\\\\\\\\\\\\\\\\\\\HERE I DECLARED THE CLIENTS LIST VARIABLE///////
clients=[]
nick_sock=dict()
#this function is used to collect each client's informations
#endddddddd of function.......
#tryiing a class instead
#this function is used to insert the info in the database
def insert_info(list,sender):
    try:
        global nickname
        sql=sqlite3.connect("datab.db")
        cursor=sql.cursor()
        fname=list["firstname"]
        lname=list["lastname"]
        nickname=list["nickname"]
        password=list["password"]
        
        cursor.execute(f"select nickname from persons where nickname = '{nickname}'")
        
        if cursor.fetchone() is not None:
            sql.commit()
            sql.close()
            print("good")
            sender.send("0".encode(format))
        else:
            
            cursor.execute("insert or ignore into persons values(:nickname,:firstname,:lastname,:password)",
                        {
                        "firstname": fname,
                        "lastname"  : lname,
                        "nickname" : nickname,
                        "password" : password
                        }
                        )
            sql.commit()
            sql.close()
            print("bad")
            sender.send("1".encode(format))
    except Exception as e:
        print("mochkil",e)
def verify_new_pseudo(newname):
    sql=sqlite3.connect("datab.db")
    cursor=sql.cursor()
    cursor.execute(f"select * from PERSONS where nickname='{newname}'")
    sql.commit()
    if cursor.fetchone() is None:
        sql.close()
        return True
    else:
        sql.close()
        return False
#************VERIFY LOGIN*****VERIFY LOGIN*******VERIFY LOGIN*******VERIFY LOGIN********
def verify_login(list):
    sql=sqlite3.connect("datab.db")
    cursor=sql.cursor()
    nick=list["nickname"]
    password=list["password"]
    cursor.execute(f"select * from PERSONS where nickname='{nick}' and password='{password}'")
    sql.commit()
    if cursor.fetchone() is None:
        sql.close()
        return False
    else:
        sql.close()
        
        return True
# ++++++++++++++++++++++++++VERIFY LOGIN++++++++++VERIFY LOGIN+++++VERIFY LOGIN   
#*****************PRIVATE MESSAGES*************PRIVATE MESSAGES*****
def private_msg(msg,sock_dest,nick_source):
    sock_dest.send((f"{nick_source}: "+msg).encode("utf-8"))
#++++++++++++++PRIVATE MESSAGES+++++++++++++++PRIVATE MESSAGES+++++
def store_prv_msg(sender,receiver,mesage):
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute(f"insert into history values ('{sender}','{receiver}','{mesage}')")
    sql.commit()
    sql.close()
def call_prv_history(source,destination,sender):
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute("select * from history where (sender in (?,?)) and (receiver in (?,?))",(source,destination,destination,source))
    historique=curse.fetchall()
    time.sleep(0.3)
    print("history")
    if historique:
        sender.send("@hist".encode(format))
        for line in historique:
            if line[0]==source:
                sender.send(f"you: {line[2]}\n".encode(format))
            else:
                sender.send(f"{line[0]}: {line[2]}\n".encode(format))
        time.sleep(0.2)
        sender.send(f"@endhist".encode(format))
    else:
        pass
    
def send_list():
    
    try:
        global ls
        ls="@ls"
        users_list=list(nick_sock.keys())
        print(users_list)
        for name in users_list:
            ls =ls+","+name
        
        for client in clients:
            client.send(ls.encode("utf-8"))

        
            
        
    except socket.error as prob:
        print("list problem",prob)
    return
def send_disconnected(name):
    try:
        msg="@@ "+name
        for client in clients:
            client.send(msg.encode("utf-8"))
        print("removed")
    except:
        print("couldn\'t send name of disconnected one")

def send_grp_buttons(name,sender):
    
    
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute(f"select room from rooms where INSTR(users,',{name},')>0")
    grpslist="@grpslist"
    
    
    for grup in curse.fetchall():
        grpslist+=","+grup[0]
    if re.sub("@grpslist","",grpslist)=="":
        pass
    else:
        sender.send(grpslist.encode(format))

    sql.close()
def update_DB_infos(old,new,grptitle,grpusers,i):
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    #curse.execute(f"select room from rooms where room={grptitle}")
    print("title: "+grptitle)
    print("grpusers: "+grpusers)
    curse.execute(f"select users from rooms where room = '{grptitle}' ")
    print("fetched before:",curse.fetchall())
    curse.execute(f"update rooms set users='{grpusers}' where room ='{grptitle}'")
    curse.execute(f"select users from rooms where room = '{grptitle}' ")
    print("fetched after:",curse.fetchall())
    print("room updated")
    if i==0:
        curse.execute(f"update persons set nickname='{new}' where nickname = '{old}'")
        curse.execute(f"update history set sender='{new}' where sender = '{old}'")
        curse.execute(f"update history set receiver='{new}' where receiver = '{old}'")
    sql.commit()
    sql.close()
def creategroup(msg,sender):
    msg=re.sub("^@gr,","",msg)
    groupe=msg.split(",")
    grptitle=groupe[0]
    msg=re.sub(f"{grptitle},","",msg)
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute(f"select room from rooms where room = '{grptitle}'")
    check_rooms=curse.fetchone()
    print("chechrooms: ",check_rooms)
    curse.execute(f"select nickname from PERSONS where nickname = '{grptitle}'")
    check_persons=curse.fetchone()
    print("chechrooms: ",check_persons)
    sql.close()
    if check_rooms is not None or check_persons is not None:
        sender.send("@grrespfalse".encode(format))
    else:
        grp_elements=msg.split(",")
        print("CRmsg:",msg)
        users=","+msg+","
    
        Grups.update({grptitle:grp_elements})
        print(f"this is the groupe: {grptitle} users: {grp_elements}")
        for user in grp_elements:
            print("user: ",user)
            try:
                user_sock=nick_sock[f"{user}"]
                user_sock.send(f"@crgr {grptitle}".encode(format))
            except:
                pass
        sender.send("@grresptrue".encode(format))
        print("CRusers:",users)
        insert_grp_infos(grptitle,users)
def insert_grp_infos(grptitle,users):
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute(f"insert into rooms values ('{grptitle}','{users}')")
    sql.commit()
    sql.close()
def store_grp_msg(title,sender,message):
    print(f"title {title} sender {sender} message {message}")
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute("insert into history values (?,?,?)",(sender,title,message))
    sql.commit()
    sql.close()
def call_grp_infos():
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute("select * from rooms")
    result=curse.fetchall()
    print(result)
def groupmsg(title,sender,model,source):
    
    print(title)
    print("Grups:",Grups)
    dests=Grups[title]
    print("dests:",dests)
    message=str()
    while True:
        
        message=sender.recv(1024).decode('utf-8')
        message=message.strip()
        if message=="@out":
            print("out of grup")
            break
        elif message:
            for dest in dests :
                
                destsock=nick_sock[dest]
                if destsock!=sender:
                    print("dest:",dest)
                    destsock.send((model+f"{source}: "+message).encode("utf-8"))
                else:
                    pass
                
            store_grp_msg(title,source,message)
        elif re.search("^@msggr.*$",title):
            message=re.sub("^@msggr ","",message)
            dests=Grups[message]
def call_grp_history(title,source,sender):
    sql=sqlite3.connect("datab.db")
    curse=sql.cursor()
    curse.execute(f"select * from history where receiver='{title}'")
    historique=curse.fetchall()
    time.sleep(0.3)
    print("history")
    if historique:
        sender.send("@hist".encode(format))
        for line in historique:
            if line[0]==source:
                sender.send(f"you: {line[2]}\n".encode(format))
            else:
                sender.send(f"{line[0]}: {line[2]}\n".encode(format))
        time.sleep(0.2)
        sender.send(f"@endhist".encode(format))
    else:
        pass
def bind_sock():
    try:
        
        host='127.0.0.1'
        global port
        port=9999
        print('binding to the port:', port)
        s.bind((host,port))
        s.listen()
    except socket.error as msg:
        print('the socket was not binded', str(msg),'rebinding socket')
        bind_sock()

def accept_connection():
#the accept objects; a connection object,
# and a list contains the ip address of the client and the port he's using
    #clients=[]
    users=[]
    accept=True
    while accept:
        try:
            connection,address = s.accept()
            #username=connection.recv(1024).decode("utf-8")
            #users.append(username)
            clients.append(connection)
            
            print('connection has been established; ip:',address[0],'port:',str(address[1]))
            
            thread= threading.Thread(target=send_message, args=(connection,users))
            
            thread.start()
            threading.Thread(target=handle_messages,args=(connection,)).start()
            
        
            print(f"[ACTIVE CLIENTS] {len(clients)}")
            #s.close()
        except socket.error as msg:
            #print("accepting the connection didn't work\n ", str(msg))
            accept=False
            break
        
def send_message(client,nickname):
    #client is the connection
    #client.send('enter username'.encode('utf-8'))
        
    
    while True:
        
        msg= input()
        if msg=='quit':
            
            for client in clients:
                client.close()
            s.close()
            break
        elif msg=="sendls":
            try:    
                send_list()
                time.sleep(0.2)
            except:
                print("errrooooor")
                continue

        else:
            for client in clients:
                try:
                    client.send((f"{nickname}: "+msg).encode('utf-8'))
                except socket.error as prob:
                    print("there is a problem in the send function:",prob)
                    client.close()
                    clients.remove(client)
        
        #handle_messages(conn)
def broadcast(sender,msg,nickname):
    
#sender is the connection
    for conn in clients:
        if conn != sender:
            try:
                print("this is my pos")
                print(f"{msg}")
                conn.send((f"{nickname}: "+msg).encode('utf-8'))
            except socket.error as prob:
                print("there is a problem in the send function:",prob)


def handle_messages(sender):
    global mode
    
    #*****************THE CLIENT SENDS INFORMATIONS****************************************************
    try:
        #print("client signing in")
        trytosign=True
        while trytosign:
            try:
                user_data=sender.recv(1024).decode("utf-8")
                #print(user_data)
                data=json.loads(user_data)
            except:
                clients.remove(sender)
                sender.close()
                return
            if len(data)==4:
                print("dkhel")              
                insert_info(data,sender)
                
                
            elif len(data)==2:
                print("chi7ja")
                check=verify_login(data)
                if check==True:

                    nick_sock.update({f"{data["nickname"]}":sender})
                    
                    
                    send_list()
                    
                    print(f"{data["nickname"]} connected successfully")
                    
                    time.sleep(1)
                    send_grp_buttons(data["nickname"],sender)

                    sender.send(ls.encode(format))
                    time.sleep(1)
                    offlines.remove(data["nickname"])
                    print(offlines)
                    offlines_str=json.dumps(offlines)
                    sender.send(f"list${offlines_str}".encode(format))
                    #trytosign=False
                    break
                else:
                    print("informations are incorrect")
                    sender.send(str(check).encode(format))
                    continue
    except:
        print("the client disconnected")
        sender.close()
        clients.remove(sender)
    
    #******************INFORMATION ADDED TO THE DATABASE***********************************************
    connected=True
    #same=True
    while connected:
        try:
            
            mode="pub"
            msg=sender.recv(1024).decode('utf-8')
            msg=msg.strip()
        except:
            del nick_sock[f"{data["nickname"]}"]
            clients.remove(sender)
            sender.close()
            offlines.append(data["nickname"])
            send_disconnected(data["nickname"])
            
            print(f"{data["nickname"]}: is disconnected")
            
            break
        if msg=="@out":
            continue
        elif msg=='disconnect':
            try: 
               
                clients.remove(sender)
                del nick_sock[f"{data["nickname"]}"]
                send_disconnected(data["nickname"])
                offlines.append(data["nickname"])
                print("offlines now",offlines)
                connected=False
                print(f"{data["nickname"]} disconnected")
            except:
                print("didn't disconnect properly")
                break
        elif bool(re.search("^@newname.+$",msg))==True:
            msg=msg.split(",")
            if verify_new_pseudo(msg[1]):
                for client in clients:
                    if client!=sender:
                        client.send(f"@update,{msg[1]},{data["nickname"]}".encode(format))
                
                grpnames=list(Grups.keys())
                #this index is to avoid the update of other tables than the room table each time
                i=0
                for grpname in grpnames:
                    if data["nickname"] in Grups[grpname]:
                        grpusers=Grups[grpname]
                        users=""
                        for user in grpusers:
                            
                            if user==data["nickname"]:
                                grpusers[grpusers.index(user)]=msg[1]
                                del Grups[grpname]
                                Grups.update({grpname:grpusers})
                                users+=","+msg[1]
                            else:
                                users+=","+user
                        users+=","
                        print("updated users:",users)
                        update_DB_infos(data["nickname"],msg[1],grpname,users,i)
                        i=1     
                print(Grups)
                del nick_sock[data["nickname"]]
                data["nickname"]=msg[1]
                nick_sock.update({f"{msg[1]}":sender})
                sender.send(f"@truepseudo,{msg[1]}".encode(format))
            else:
                sender.send("@falsepseudo".encode(format))
        #******sending a list of connected users***********
        elif msg=="@ls":
            #print("demanding")
            try:    
                send_list()
                #time.sleep(0.2)
            except:
                print("errrooooor")
                continue
        elif bool(re.search("^@offlinehist.+$",msg))==True:
            offline_dest=re.sub("^@offlinehist,","",msg)
            call_prv_history(data["nickname"],offline_dest,sender)
    #**************PRIVATE MESSAGING****************************
        elif bool(re.search("^@prv.+$",msg))==True:
            destination=re.sub("^@prv","",msg)
            destination=destination.strip()
            mode=f"prv{data["nickname"]},"
            print(mode)
            
            call_prv_history(data["nickname"],destination,sender)
            print("fine")
            #********HERE I GOT THE CONNECTION OF THE DESTINATION******
            sock_dest=nick_sock[destination]
            #print("in private")
            while True:
                try:
                    msg=sender.recv(1024).decode('utf-8')
                    msg=msg.strip()
                except:
                    offlines.append(data["nickname"])
                    send_disconnected(data["nickname"])
                    del nick_sock[f"{data["nickname"]}"]
                    sender.close()
                    #clients.remove(sender)
                    print(nick_sock)
                    
                if msg=="@out":
                    break
                else:
                    #print(f"msg b4 send prv{data["nickname"]},{data["nickname"]}: "+msg)
                    try:
                        sock_dest.send((f"prv{data["nickname"]},{data["nickname"]}: "+msg).encode("utf-8"))
                        store_prv_msg(data["nickname"],destination,msg)
                    except:
                        offlines.append(destination)
                        send_disconnected(destination)
                        del nick_sock[f"{destination}"]
                        sock_dest.close()
                        clients.remove(sock_dest)       
    #++++++++++++++++++++PRIVATE MESSAGING++++++++++++++++++++++++
        #***********CREATION OF GROUP**********************************
        elif re.search("^@gr.*$",msg):
            
            creategroup(msg,sender)
            time.sleep(0.1)
        #++++++++++++++++++++++++CREATION OF GROUP++++++++++++++++++++++
        #************************CHATTING IN A GROUP********************
        elif re.search("^@msggr.*$",msg):
            msg=re.sub("^@msggr ","",msg)
            mode=f"grp{msg},"
            call_grp_history(msg,data["nickname"],sender)

            groupmsg(msg,sender,f"grp{msg},",data["nickname"])

        #+++++++++++++++++++++++++CHATTING IN A GROUP+++++++++++++++++++
        else:
            try:
                if str(msg):
                    broadcast(sender,msg,data["nickname"])
                    print(f"{data["nickname"]}:",str(msg))
            except socket.error as prob:
                print("there is an error in receiving ",prob)
                
                break
restore_all_users()
restore_grps_infos()
print(offlines)
print(Grups)
create_sock()
bind_sock()
accept_connection()
