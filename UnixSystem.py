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

def loanout(userName,ISBN): #Adds userName,ISBN and date into the loanout table
    try:
        time = date.today()
        time = time.strftime('%m/%d/%Y')
        data = {"userName":userName,"ISBN":ISBN,"Date":time}
        db.child("outLoan").child(userName).push(data)
    except:
        print("Error")

def returnLoan(userName,ISBN): #returns book back to book table and deletes entity
    try:
        db.child("outLoan").child(userName).remove()
    except:
        print("Error")

def AddBook(ISBN,Title,Author,Catergory,Year): #add book in books table
    data = {"ISBN":ISBN,"Title":Title,"Author":Author,"Category":Catergory,"Year":Year}
    db.child("books").child(ISBN).push(data)
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

def UpdateBooks(ISBN,Column,Change):
    OD = json.loads(json.dumps(SearchBookISBN(ISBN)))
    dict = []
    for i in OD:
        dict = OD[i]
    change =(dict["ISBN"])
    db.child("books").child(ISBN).update({Column:Change})

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
    ISBN = []
    num = 0
    loans = db.child("outLoan").get()
    try:
        for person in loans.each():
            keyuserName.append(person.key())
            loaned = db.child("outLoan").child(keyuserName[num]).get()
            num = num+1
            loaned = loaned[0].val()
            ISBN.append(int(loaned["ISBN"]))
        return(keyuserName,ISBN)
    except:
        print("No files being used")

def displayloans(keyuserName,uISBN):
    print("Displaying files being used")
    stringhead =("{:<30} {:<30} {:<30} {:<30} {:<30}".format('userName','Email','file no','Title','Date'))
    for i in range(len(keyuserName)):
        Email,Name,userName,Password,Surname = splitStudent(keyuserName[i])
        ISBN,Title,Author,Catergory,Year = splitBook(uISBN[i])
        userName,ISBN,Date = splitOuts(keyuserName[i])
        stringhead = stringhead + "\n{:<30} {:<30} {:<30} {:<30} {:<30}".format(userName,Email,ISBN,Title,Date)
    return stringhead


def displaybooks(keyuserName):#allows the books to be viewed in a table
    stringhead =("{:<10} {:<30} {:<30} {:<30} {:<30}".format('file no', 'Title', 'Author', 'Category', 'Year'))
    #print each data item.
    for i in range(len(keyuserName)):
        ISBN,Title,Author,Catergory,Year = splitBook(keyuserName[i])
        stringhead = stringhead + "\n{:<10} {:<30} {:<30} {:<30} {:<30}".format(ISBN,Title,Author,Catergory,Year)
    return stringhead

def displaystudents(keyuserName):#allows the students to be viewed in a table
    stringhead =("{:<40} {:<40} {:<40} {:<40} {:<40}".format('Email', 'userName', 'Name','Password','Surname'))
    stringhead = stringhead + (f"\n----------------------------------------------------------------------------")
#print each data item.
    for i in range(len(keyuserName)):
        Email,Name,userName,Password,Surname = splitStudent(keyuserName[i])
        stringhead = stringhead + "\n{:<40} {:<40} {:<40} {:<40} {:<40}".format(Email,userName,Name,Password,Surname)

    return stringhead

def SearchBookISBN(ISBN): #search book by ISBN in books table
    try:
        pr = db.child("books").child(ISBN).get()
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

def deleteBook(ISBN):# delete book
    db.child("books").child(ISBN).remove()

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

def splitBook(ISBN):
    OD = json.loads(json.dumps(SearchBookISBN(ISBN)))
    dict = []
    for i in OD:
        dict = OD[i]
    uISBN = (dict["ISBN"])
    Author = (dict["Author"])
    Title = (dict["Title"])
    Catergory = (dict["Category"])
    Year = (dict["Year"])
    return uISBN,Title,Author,Catergory,Year

def splitOuts(userName):
    OD = json.loads(json.dumps(SearchLoanuserName(userName)))
    dict = []
    for i in OD:
        dict = OD[i]
    userName = (dict["userName"])
    ISBN = (dict["ISBN"])
    Date = (dict["Date"])
    return userName,ISBN,Date


def Field(ISBN,column):
    OD = json.loads(json.dumps(SearchBookISBN(ISBN)))
    dict = []
    for i in OD:
        dict = OD[i]
    field= dict[column]
    return field

def editBook(ISBN, column, change):
    OD = json.loads(json.dumps(SearchBookISBN(ISBN)))
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
                ISBN,Title,Author,Catergory,Year = splitBook(keyuserName[i])
                Out.append(ISBN)
    return(Out)

def SearchCat(cat):
    keyuserName = []
    keyuserName = viewBooks()
    Out = []
    for i in range(len(keyuserName)):
        if(Field(keyuserName[i],"Category") == cat):
                ISBN,Title,Author,Catergory,Year = splitBook(keyuserName[i])
                Out.append(ISBN)
    return(Out)

def SearchYear(year):
    keyuserName = []
    keyuserName = viewBooks()
    Out = []
    for i in range(len(keyuserName)):
        if(Field(keyuserName[i],"Year") == year):
                ISBN,Title,Author,Catergory,Year = splitBook(keyuserName[i])
                Out.append(ISBN)
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
        userName,ISBN,Date = splitOuts(key)
        uISBN,Title,Author,Catergory,Year = splitBook(ISBN)
        stringhead =("{:<30} {:<30} {:<30} {:<30} {:<30}{:<30}".format('Title','file no','Author','Catergory','Year','Date'))
        stringhead = stringhead + "\n{:<30} {:<30} {:<30} {:<30} {:<30} {:<30}".format(Title,ISBN,Author,Catergory,Year,Date)
        return stringhead
    except:
        return "No files being used"

def isAdmin(gmail):
    if(gmail.lower() == "dj.njini@cs.up.ac.za"):
        return True
    else:
        return False
displaybooks(viewBooks())
