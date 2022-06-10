import pyrebase
from datetime import date
from collections import OrderedDict
import json
import pandas as pd

FirebaseConfig = { "apiKey": "AIzaSyBneAh9iN7NJRPYB3BzytZSsabNnYVVZtQ",
  "authDomain": "unix-database-c2b8f.firebaseapp.com",
  "databaseURL": "https://unix-database-c2b8f-default-rtdb.firebaseio.com",
  "projectId": "unix-database-c2b8f",
  "storageBucket": "unix-database-c2b8f.appspot.com",
  "messagingSenderId": "805162713903",
  "appId": "1:805162713903:web:0d5d006898d8a10f6b57da",
  "measurementId": "G-8BQ4FD4VM6"}


firebase = pyrebase.initialize_app(FirebaseConfig)

db = firebase.database()
auth = firebase.auth()
#Push data


#login
def email(email,password): #email login
    try:
        auth.sign_in_with_email_and_password(email,password)
        return True
    except:
        return False

def signup(email,password): #sign up
    try:
        auth.create_user_with_email_and_password(email,password)
        print("Success! Sign up done!")
        return True
    except:
        print("Existing user or password incorrect!")
        return False

def checker(userName):
    OD = json.loads(json.dumps(SearchStudentuserName(userName)))
    if(OD == None):
        return False
    else:
        return True

def loanout(userName,fileNo): #Adds userName,fileNo and date into the loanout table
    try:
        time = date.today()
        time = time.strftime('%m/%d/%Y')
        data = {"userName":userName,"fileNo":fileNo,"Date":time}
        db.child("outLoan").child(userName).push(data)
    except:
        print("Error")

def returnLoan(userName,fileNo): #returns book back to book table and deletes entity
    try:
        db.child("outLoan").child(userName).remove()
    except:
        print("Error")

def AddBook(fileNo,Title,Author,Catergory,Year): #add book in books table
    data = {"fileNo":fileNo,"Title":Title,"Author":Author,"Category":Catergory,"Year":Year}
    db.child("books").child(fileNo).push(data)
    print(Title+" Has been Successfully added")

def AddStudent(userName,Name,Surname,email,password): #add students in students table
    if(checker(userName)==False):
        data = {"userName":userName,"Name":Name,"Surname":Surname,"Email":email,"Password":password}
        db.child("students").child(userName).push(data)
        print("User added to database")
        return True
    else:
        return False

def UpdateStudent(userName,Column,Change):
    db.child("students").child(userName).update({Column:Change})

def UpdateBooks(fileNo,Column,Change):
    OD = json.loads(json.dumps(SearchBookfileNo(fileNo)))
    dict = []
    for i in OD:
        dict = OD[i]
    change =(dict["fileNo"])
    db.child("books").child(fileNo).update({Column:Change})

def viewStudents(): # view students
    keyuserName = []
    num = 0
    students = db.child("students").get()
    for person in students.each():
        print("key: ",person.key())
        keyuserName.append((person.key()))
    return(keyuserName)

def viewBooks(): #view books
    keyuserName = []
    num = 0
    books = db.child("books").get()
    for person in books.each():
        keyuserName.append(person.key())
    return(keyuserName)

def viewloans():#checks the books that are onloan
    keyuserName = []
    fileNo = []
    num = 0
    loans = db.child("outLoan").get()
    try:
        for person in loans.each():
            keyuserName.append(person.key())
            print("Pers: ",keyuserName)
            loaned = db.child("outLoan").child(keyuserName[num]).get()
            print("loan: ", loaned)
            num = num+1
            loaned = loaned[0].val()
            fileNo.append(loaned["fileNo"])
        return(keyuserName,fileNo)
    except:
        print("No files being used")
        return 0,0

def displayloans(keyuserName,ufileNo):
    print("Displaying files being used")
    print("key: ", keyuserName)
    stringhead =("{:<30} {:<30} {:<30} {:<30} {:<30}".format('userName','Email','fileNo','Title','Date'))
    for i in range(len(keyuserName)):
        Email,Name,userName,Password,Surname = splitStudent(keyuserName[i])
        fileNo,Title,Author,Catergory,Year = splitBook(ufileNo[i])
        userName,fileNo,Date = splitOuts(keyuserName[i])
        stringhead = stringhead + "\n{:<30} {:<30} {:<30} {:<30} {:<30}".format(userName,Email,fileNo,Title,Date)
    return stringhead


def displaybooks(keyuserName):#allows the books to be viewed in a table
    stringhead =("{:<10} {:<30} {:<30} {:<30} {:<30}".format('fileNo', 'Title', 'Author', 'Category', 'Year'))
    #print each data item.
    for i in range(len(keyuserName)):
        fileNo,Title,Author,Catergory,Year = splitBook(keyuserName[i])
        stringhead = stringhead + "\n{:<10} {:<30} {:<30} {:<30} {:<30}".format(fileNo,Title,Author,Catergory,Year)
    return stringhead

def displaystudents(keyuserName):#allows the students to be viewed in a table
    stringhead =("{:<40} {:<40} {:<40} {:<40} {:<40}".format('Email', 'userName', 'Name','Password','Surname'))
    stringhead = stringhead + (f"\n----------------------------------------------------------------------------")
#print each data item.
    for i in range(len(keyuserName)):
        Email,Name,userName,Password,Surname = splitStudent(keyuserName[i])
        stringhead = stringhead + "\n{:<40} {:<40} {:<40} {:<40} {:<40}".format(Email,userName,Name,Password,Surname)

    return stringhead

def SearchBookfileNo(fileNo): #search book by fileNo in books table
    try:
        pr = db.child("books").child(fileNo).get()
        return(pr.val())
    except:
        print("Incorrect file no")

def SearchStudentuserName(userName): #search student by userName in student table
    try:
        pr = db.child("students").child(userName).get()
        return(pr.val())
    except:
        print("Incorrect userName")

def SearchLoanuserName(userName): #search student by userName in student table
    try:
        pr = db.child("outLoan").child(userName).get()
        return(pr.val())
    except:
        print("Incorrect userName")

def deleteStudent(userName):# delete student
    db.child("students").child(userName).remove()

def deleteBook(fileNo):# delete book
    db.child("books").child(fileNo).remove()

def myprofile(userName): #Views my profile
    pr = db.child("outLoan").child(userName).get()
    return(pr.val())


def booksonloan():#checks the books that are onloan
    books = db.child("books").child("Loaned").get()
    return(books.val())


def splitStudent(userName): #Split the students attributes
    try:
        OD = json.loads(json.dumps(SearchStudentuserName(userName)))
        dict = []
        for i in OD:
            dict = OD[i]
            
        Email = (dict["Email"])
        Name = (dict["Name"])
        userName = (dict["userName"])
        Surname = (dict["Surname"])
        Password = (dict["Password"])
        return Email,Name,userName,Password,Surname
    except:
        print("userName does not exist")

def splitBook(fileNo):
    OD = json.loads(json.dumps(SearchBookfileNo(fileNo)))
    dict = []
    for i in OD:
        dict = OD[i]
        
    fileNo = (dict["fileNo"])
    Author = (dict["Author"])
    Title = (dict["Title"])
    Catergory = (dict["Category"])
    Year = (dict["Year"])
    return fileNo,Title,Author,Catergory,Year

def splitOuts(userName):
    OD = json.loads(json.dumps(SearchLoanuserName(userName)))
    dict = []
    for i in OD:
        dict = OD[i]
    userName = (dict["userName"])
    fileNo = (dict["fileNo"])
    Date = (dict["Date"])
    return userName,fileNo,Date


def Field(fileNo,column):
    OD = json.loads(json.dumps(SearchBookfileNo(fileNo)))
    dict = []
    for i in OD:
        dict = OD[i]
    field= dict[column]
    return field

def editBook(fileNo, column, change):
    OD = json.loads(json.dumps(SearchBookfileNo(fileNo)))
    dict = []
    for i in OD:
        dict = OD[i]
    dict[column] = change

def SearchTitle(title):
    keyuserName = []
    keyuserName = viewBooks()
    Out = []
    for i in range(len(keyuserName)):
        if(Field(keyuserName[i],"Title") == title):
                fileNo,Title,Author,Catergory,Year = splitBook(keyuserName[i])
                Out.append(fileNo)
    return(Out)

def SearchCat(cat):
    keyuserName = []
    keyuserName = viewBooks()
    Out = []
    for i in range(len(keyuserName)):
        if(Field(keyuserName[i],"Category") == cat):
                fileNo,Title,Author,Catergory,Year = splitBook(keyuserName[i])
                Out.append(fileNo)
    return(Out)

def SearchYear(year):
    keyuserName = []
    keyuserName = viewBooks()
    Out = []
    for i in range(len(keyuserName)):
        if(Field(keyuserName[i],"Year") == year):
                fileNo,Title,Author,Catergory,Year = splitBook(keyuserName[i])
                Out.append(fileNo)
    return(Out)

def myprofile(userName): #Views my profile
    key = userName
    stringhead =("{:<30} {:<30} {:<30} {:<30} {:<30}".format('Email', 'userName', 'Name','Password','Surname',))
    Email,Name,userName,Password,Surname = splitStudent(key)
    stringhead = stringhead + "\n{:<30} {:<30} {:<30} {:<30} {:<30}".format(Email,userName,Name,Password,Surname)
    return(stringhead)

def mybooks(userName): #views my books
    try:
        key = userName
        userName,fileNo,Date = splitOuts(key)
        ufileNo,Title,Author,Catergory,Year = splitBook(fileNo)
        stringhead =("{:<30} {:<30} {:<30} {:<30} {:<30}{:<30}".format('Title','fileNo','Author','Catergory','Year','Date'))
        stringhead = stringhead + "\n{:<30} {:<30} {:<30} {:<30} {:<30} {:<30}".format(Title,fileNo,Author,Catergory,Year,Date)
        return stringhead
    except:
        return "No files being used"

def isAdmin(gmail):
    if(gmail.lower() == "dj.njini@cs.up.ac.za"):
        return True
    else:
        return False
displaybooks(viewBooks())
