from pymongo import *
import getpass

#paste here your VScode link from MongoDB
mongodblink = 'link'
connessione = MongoClient(mongodblink)
#change this name with your DB name
db_name = 'db_name'
db = connessione[db_name]

def add_user():
    sez = input("Section name: ")
    col = db['sections']
    ok=False
    for document in col.find():
        if document["name"]==sez:
            ok=True
    if ok:
        col = db['pw']
        name = input("Name to add: ")
        pw = getpass.getpass()
        col.insert_one( {"sez":sez , "name":name , "pw":pw} )
    else:
        print("This Section doesn't exist.")

def search():
    sez = input("Section name: ")
    col = db['sections']
    ok=False
    for document in col.find():
        if document["name"]==sez:
            ok=True
    if ok:
        col = db['pw']
        for document in col.find():
            if document["sez"]==sez:
                print(document["name"]+" | "+document['pw'])
    else:
        print("This Section doesn't exist.")

def remove_user():
    sez = input("Section name to delte: ")
    col = db['sections']
    #cerco se esiste già
    ok=False
    for document in col.find():
        #print(document["name"])
        if document["name"]==sez:
            ok=True
    if ok:
        name = input("Name to delete: ")
        col = db['pw']
        col.delete_many({"name":name})
    else:
        print("This Section doesn't exist.")

def change():
    sez = input("Section name: ")
    col = db['sections']
    #cerco se esiste già
    ok=False
    for document in col.find():
        #print(document["name"])
        if document["name"]==sez:
            ok=True
    if ok:
        name = input("Name to change password: ")
        col = db['pw']
        exsist=False
        for name in col.find():
            if name['name']==name:
                exsist=True
        if exsist:
            col.delete_many({"name":name})
            new_pw = input("New password for "+name+" in "+sez+" : ")
            col.insert_one( {"sez":sez , "name":name , "pw":new_pw} )
        else:
            print("Name doesn't exist.")
    else:
        print("This Section doesn't exist.")

def remove():
    sez = input("Section to delete: ")
    col = db['sections']
    #cerco se esiste già
    ok=False
    for document in col.find():
        #print(document["name"])
        if document["name"]==sez:
            ok=True
    if ok:
        col.delete_one({"name":sez})
        col = db['pw']
        col.delete_many({"sez":sez})
        print("Section "+sez+" deleted.")
    else:
        print("This Section doesn't exist.")

def add():
    sez = input("Section name to add: ")
    col = db['sections']
    #cerco se esiste già
    ok=True
    for document in col.find():
        #print(document["name"])
        if document["name"]==sez:
            ok=False
    if ok:
        col.insert_one({"name": sez })
        print("Section created.")
    else:
        print("This Section already exist.")
    

def get_all():
    print("\nAll sections:")
    collection = db['sections']
    for document in collection.find():
        print(document["name"])
    
def check():
    collections = db.list_collection_names()
    pw = False
    sez = False
    for col in collections:
        if col == 'pw':
            pw=True
        if col == 'sections':
            sez = True

    if pw==False:
        db.create_collection('pw')
    if sez==False:
        db.create_collection('sections')


def main():
    while 1:
        opt = input("\n-USER MENU-\nchoose option:\n[ 0 ] Add section\n[ 1 ] Delete Section\n[ 2 ] Print all sections\n[ 3 ] Search data aboud section\n[ 4 ] Add name and his pw\n[ 5 ] Delete name from section\n[ 6 ] Change pw of one name in specific section\n[ x ] Exit\nWrite: ")
        match opt:
            case '0':
                add()
            case '1':
                remove()
            case '2':
                get_all()
            case '3':
                search()
            case '4':
                add_user()
            case '5':
                remove_user()
            case '6':
                change()
            case 'x':
                exit()

check()
main()