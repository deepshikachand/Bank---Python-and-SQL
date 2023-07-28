
from datetime import datetime
import mysql.connector as mysql
conn=mysql.connect(host='localhost', user='root', password='manager')


rec=conn.cursor()

def menu1():
    ch=0
    while ch<2:
        print("******************************")
        print("-_-_-B A N K-_-_-")
        print()
        print("1.Main Menu")
        print("----------")
        print("2.Exit")
        print("----------")
        ch=int(input("Enter your choice: "))
        if ch==1:
            mainmenu()
        else:
            conn.close()
            print ("T H A N K S  V I S I T   A G A I N  . . .  .")
           
            
def mainmenu():
    ch=0
    while ch<4:
        print("********************")
        print(" ____M A I N   M E N U____ ")
        print()
        print("-----------------")
        print("1.Bank Services")
        print("-----------------")
        print("2.Transaction")
        print("-----------------")
        print("3.Report")
        print("-----------------")
        print("4.Exit")
        print("-----------------")
        ch=int(input("Enter your choice: "))
        if ch==1:
            bankservices()
        if ch==2:
            transaction()
        if ch==3:
            reports()

def bankservices():
    ch=0
    while ch<4:
        print("---------------------------")
        print("B A N K   S E R V I C E S")
        print()
        print("1.Create an account: ")
        print()
        print("2.Display an account: ")
        print()
        print("3.Delete an account: ")
        print()
        print("4.Return to main menu: ")
        print("---------------------------")
        ch=int(input("Enter your choice: "))
        if ch==1:
            createaccount()
        if ch==2:
            displayaccount()
        if ch==3:
            deleteaccount()

def createaccount():
    import mysql.connector as mysql
    conn=mysql.connect(host="localhost",user="root",passwd="manager")
    sql="create database if not exists bank"
    rec=conn.cursor()
    rec.execute(sql)
    conn.commit()
    rec.execute("use bank")
    conn.commit()
    
    sql1="create table if not exists accountmaster (Account_Number  integer, name  char(40), Account_Type  char(40), DateOfOpening  date, Adress_1 char(100), Adress_2 char(100), City char(20), Opening_Balance integer)"
            
    rec=conn.cursor()
    rec.execute(sql1)
    conn.commit()
    print ("Table Created successfully....")
    print("-----CREATE ACCOUNT-----")
    print()
    
    
    
    a=eval(input("Enter the account no. to be created: "))
    b=input("Enter the name: ")
    c=input("Enter the account type Saving/Current :")
    d=datetime.date(datetime.now())
    print ("Date of transaction is :",d)
    e=input("Enter the address1: ")
    f=input("Enter the address2: ")
    g=input("Enter the city: ")
    h=eval(input("Enter the opening balance: "))
    
    sql2="insert into accountmaster values({},'{}','{}','{}','{}','{}','{}',{})".format(a,b,c,d,e,f,g,h)
    rec.execute(sql2)
    conn.commit()
    print("")
    print("")
    print("Account created successfully")
   
    

def displayaccount():
   
    import mysql.connector as mysql
    conn=mysql.connect(host='localhost', user='root', password='manager', database='bank')
    if conn.is_connected():
        print("Database connectivity is successful")
    else:
        print("Database does not exixt")
    rec=conn.cursor()
    a=int(input("Enter the account number to be displayed: "))
    b="select * from accountmaster where Account_Number={}".format(a)
    rec.execute(b)
    result = rec.fetchall()
    for i in result:
        print(i)
    
  
            

def deleteaccount():
    a=int(input("Enter the account to be deleted: "))
    w="select * from accountmaster where Account_Number={}".format(a)
    rec.execute(w)
    no = rec.fetchone()
    if no == None:
        print("Account associated with the provided account number does not exist")
    else:
         s="delete from accountmaster where Account_Number={}".format(a)
         rec.execute(s)
         conn.commit()
         print("Account associated with the account number you've provided has been deleted")
   
    
        
    
        
    

def transaction():
    rec=conn.cursor()
    rec.execute("use bank")
    s1="Create table if not exists Transaction (Account_Number integer,Date_Of_Transaction date , Transaction_Type char(1),Amount integer )"
    print(s1)
   
    rec.execute(s1)
    conn.commit()
    a=int(input("Enter account number: "))
    s="select name from accountmaster where Account_Number={}".format(a)
    rec.execute(s)
    res = rec.fetchone()
    
    
    print("Name is:", res[0])

    d=datetime.date(datetime.now())
    print ("Date of transaction is :",d)
    x=input("Enter( 'W' for withdrawal / 'D' for deposit) ")
    if x=='w' or x=='W':
        c=int(input("Enter the amount to be withdrawn: "))
        p="select Opening_Balance from accountmaster where account_number={}".format(a)
        rec.execute(p)
        q = rec.fetchone()
        if q == None:
            print("Account does not exist!!")
            
        else:
            bal=q[0]
            
            
        if c<bal:
            r="update accountmaster set Opening_Balance= Opening_Balance-{} where Account_Number={}".format(c,a)
            rec.execute(r)
            conn.commit()
            print("Given amount has been withdrawn...")
            s2="insert into Transaction values ({},'{}','{}',{})".format(a,d,x,c)
            rec.execute(s2)
            conn.commit()
        else:
            print("Not enough money, u broke")
       
    elif x=='D' or x=='d':
        c=int(input("Enter the amount to be deposited:"))
        r=r="update accountmaster set Opening_Balance= Opening_Balance+{} where Account_Number={}".format(c,a)
        rec.execute(r)
        conn.commit()
        print("Given amount has been deposited")
        s2="insert into Transaction values ({},'{}','{}',{})".format(a,d,x,c)
        rec.execute(s2)
        conn.commit()
        
    else:
        print("Given input doesn't respond")


def reports():
    ch=0
    while ch<2:
        print("---------------------------")
        print("R E P O R T S")
        print()
        print("1.Account list")
        print()
        print("2.Individual account list")
        print()
        print("3.Return to main menu")
        print("---------------------------")
        ch=int(input("Enter your choice: "))
        if ch==1:
            account_list()
        if ch==2:
            individuallist()

def individuallist():
    ch=0
    while ch<3:
        print("-------------------------------------------------")
        print("I N D I V I D U A L    A C C O U N T    L I S T")
        print()
        print("1.Current statement")
        print()
        print("2.Mini statement list")
        print()
        print("3.Return reports")
        print("-------------------------------------------------")
        ch=int(input("Enter your choice: "))
        if ch==1:
            current_list()
        elif ch==2:
            mini_list()
        elif ch==3:
            reports()
def account_list():
    rec=conn.cursor()
    s="select * from accountmaster"
    rec.execute(s)
    data=rec.fetchall()
    print("Account_Number", "name"," Account_Type ", "DateOfOpening", "Adress_1", "Adress_2", "City", "Opening_Balance")
    for x in data:
        print(x[0],x[2],x[3],x[4],x[5],x[6],x[7])
    
def current_list():
    a=int(input("Enter Account Number: "))
    s="select distinct name, Account_Type, Opening_Balance from accountmaster where Account_Number={}".format(a)
    rec.execute(s)
    data=rec.fetchall()
    for x in data:
        print ("Name :",x[0])
        print("Account type: ",x[1])
        print("Opening Balance: ",x[2])
    
def mini_list():
    a=int(input("Enter Account Number:"))
    s="select * from transaction where Account_Number={}".format(a)
    rec.execute(s)
    data=rec.fetchall()
    print("Account_Number","Date of Transaction", "Transaction Type", "Amount")
    for x in data:
        print(x[0],x[1],x[2],x[3])    

menu1()

