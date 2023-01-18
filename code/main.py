from pymongo import *
import getpass

#paste here your VScode link from MongoDB
mongodblink = 'link'
connessione = MongoClient(mongodblink)
#change this name with your DB name
db_name = 'db_name'
db = connessione[db_name]

#your password to enter
password = "your_password"

# here there are all color for this project
global g # green
g = '\033[92m'
global r #red
r = '\033[91m'
global y #yellow
y = '\033[93m'
global res #reset
res = '\033[0m'

def add_user():
    sez = input(y+"Section name: "+res)
    col = db['sections']
    ok=False
    for document in col.find():
        if document["name"]==sez:
            ok=True
    if ok:
        col = db['pw']
        name = input(y+"Name to add: "+res)
        pw = getpass.getpass()
        col.insert_one( {"sez":sez , "name":name , "pw":pw} )
        print(g+"Name added."+res)
    else:
        print(r+"This Section doesn't exist."+res)

def search():
    sez = input(y+"Section name: "+res)
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
        print(r+"This Section doesn't exist."+res)

def remove_user():
    sez = input(y+"Section name to delete: "+res)
    col = db['sections']
    #cerco se esiste già
    ok=False
    for document in col.find():
        #print(document["name"])
        if document["name"]==sez:
            ok=True
    if ok:
        name = input(y+"Name to delete: "+res)
        col = db['pw']
        col.delete_many({"name":name})
        print(g+name+" deleted."+res)
    else:
        print(r+"This Section doesn't exist."+res)

def change():
    sez = input(y+"Section name: "+res)
    col = db['sections']
    #cerco se esiste già
    ok=False
    for document in col.find():
        #print(document["name"])
        if document["name"]==sez:
            ok=True
    if ok:
        name = input(y+"Name to change password: "+res)
        col = db['pw']
        exsist=False
        for name in col.find():
            if name['name']==name:
                exsist=True
        if exsist:
            col.delete_many({"name":name})
            new_pw = input(y+"New password for "+name+" in "+sez+" : "+res)
            col.insert_one( {"sez":sez , "name":name , "pw":new_pw} )
            print(g+"password changed."+res)
        else:
            print(r+"Name doesn't exist."+res)
    else:
        print(r+"This Section doesn't exist."+res)

def remove():
    sez = input(y+"Section to delete: "+res)
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
        print(g+"Section "+sez+" deleted."+res)
    else:
        print(r+"This Section doesn't exist."+res)

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
    print(y+"\nAll sections:"+res)
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
    pw_status = False
    while pw_status==False:
        print(y)
        pw = getpass.getpass()
        print(res)
        if pw != password:
            print(r+"Password errata"+res)
        else:
            print(g+"Password corretta"+res)
            pw_status=True
    while 1:
        opt = input(
            y+"\n-USER MENU-"+res
            + "\nchoose option:"
            + "\n[ "+g+"0"+res+" ] Add section"
            + "\n[ "+g+"1"+res+" ] Delete Section"
            + "\n[ "+g+"2"+res+" ] Print all sections"
            + "\n[ "+g+"3"+res+" ] Search data aboud section"
            + "\n[ "+g+"4"+res+" ] Add name and his pw"
            + "\n[ "+g+"5"+res+" ] Delete name from section"
            + "\n[ "+g+"6"+res+" ] Change pw of one name in specific section"
            + r+"\n[ x ] Exit"+res
            + y+"\nWrite: "+res
        )
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