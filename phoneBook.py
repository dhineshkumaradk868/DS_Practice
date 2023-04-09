import pymongo
import certifi
import re

# Creating Mongo connection and creating a new DB & Collection
client = pymongo.MongoClient("mongodb+srv://admin:12345@cluster0.vbxqbgu.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db= client.PhoneBook
coll= db.Contacts

#initializing options
options = {1:"1. Create contact", 2:"2. Search contact", 3:"3. Delete contact", 4:"4. Display all contacts"}
option=0

#function to display available options
def display_options():
    print("Welcome to Phone book")
    for i in options.values():
        print(i)

#function to get option from user
def get_option():
    option = int(input("Enter an option: "))
    print("You have selected, ", options[option])
    return option

#validation for the input values
def validation(name, number, email):
    name_pat = p=r"[A-Z][a-z]"
    if re.search(name_pat,name):
        pass
    else:
        return "Enter a valid name, Name can only contain alphabets"
    number_pat=r"^\d{10}$"
    if re.search(number_pat,number):
        pass
    else:
        return "Enter a valid phone number, Name can only contain numbers and 10 digits"
    email_pat=r"^([\w]+)@([\w]+)\.([\w]+)$"
    if re.search(email_pat,email):
        pass
    else:
        return "Enter a valid email"

#construct a document to insert
def execute_query(option,**kwargs):
    if option==1:
        document = {"_id":kwargs.get("name"), "phone_number":kwargs.get("number"), "email":kwargs.get("email")}
        coll.insert_one(document)
    elif option==2:
        result = coll.find({"$or":[{"_id": {"$regex":kwargs.get("text")}}, {"phone_number": {"$regex":kwargs.get("text")}}]})
        return result
    elif option==3:
        coll.delete_one({"_id":kwargs.get("text")})
    elif option==4:
        result=coll.find()
        return result


#create a new contact
def create_contact():
    print("---------------------------------------")
    name=input("Enter name: ")
    number=input("Enter number: ")
    email=input("Enter email: ")
    if validation(name,number,email) == None:
        document= execute_query(option,name=name,number=number,email=email)
        print(name, ": contact created")

    else:
        print(validation(name,number,email))
        print("Try again !")

#search a contact
def search_contact():
    text=input("Enter text to search: ")
    result = execute_query(option,text=text)
    if result == None:
        print("No match found !")
    else:
        print("Contact found !")
        for rec in result:
            print(rec.get('_id'), ":", rec.get('phone_number'))


#Delete a contact
def delete_contact():
    text = input("Enter text to delete: ")
    check = coll.find({"_id":text})
    if check != None:
        execute_query(option, text = text)
        print("Contact deleted !")
    else:
        print("Contact not found !")

#Display all contacts
def display_all():
    result=execute_query(option)
    for rec in result:
        print(rec.get('_id'), ":", rec.get('phone_number'), ",",rec.get('email'))


#Driver code
try:
    display_options()
    option=get_option()
    if option == 1:
        create_contact()
    elif option == 2:
        search_contact()
    elif option==3:
        delete_contact()
    elif option==4:
        display_all()
    elif option>4:
        print("Invalid choice, choose a valid one")
except KeyError:
    print("An error occured, select a valid choice")
    raise