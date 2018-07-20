#!/usr/bin/python3

import json
import getpass
import secrets
import string
import time
import base64
import os
import matrix_client.checks
from matrix_client.client import *

cfgfile="cfg/config"
def main():
    options=(
        {
            "1":bot_account,
            "2":homeserver,
            "3":users,
            "4":bot_name,
            "5":_exit
        })
    if os.path.isfile(cfgfile):
        f=open(cfgfile,"r+")
    else:
        f=open(cfgfile,"w+")
        f.write("{\n}")
        f.seek(0)
    js=json.loads(f.read())
    while True:
        print(  "Select an option:",
                "1) Edit bot account.",
                "2) Edit homeserver.",
                "3) Edit users.",
                "4) Edit bot name",
                "5) Exit.",
                sep="\n")
        choice=input()
        try:
            options[choice](f,js)
        except KeyError:
            print("Invalid Selection.")

def bot_account(fd,js):
    if not ('username' in js and 'password' in js):
        print("There are no current credentials.")
    else:
        print("Username: "+js['username'])
    username=input("Enter the new username:")
    username="".join(username.split())
    while True:
        choice=input("Would you like to generate a random password?(Y/N)")
        choice=choice.lower()
        if choice=="y":
            password=genpass()
            break
        if choice=="n":
            notMatch=True
            while notMatch:
                password=getpass.getpass(prompt="Enter the password:")
                verify=getpass.getpass(prompt="Reenter your password:")
                if verify==password:
                    notMatch=False
                else:
                    print("Passwords didn't match, try again.")
            break
        else:
            print("Invalid choice.")
    while True:
        print(  "1) Register credentials online and store them.(Doesn't work on matrix.org)",
                "2) Store credentials.",sep='\n')

        choice=input()
        if choice=="1":
            register(username,password,js)
        elif choice=="2":
            break
        else:
            print("Invalid choice.")
    js['username']=username
    js['password']=base64.b64encode(bytes(password,"UTF-8")).decode(encoding='UTF-8')
    save_changes(fd,js)
    while True:
        print("Would you like to print your password?(Y/N)")
        choice=input()
        choice=choice.lower()
        if choice=="y":
            print(password)
        elif choice=="n":
            break
        else:
            print("Invalid choice.")

def register(username,password,js):
    MAX_RETRIES=30
    count=0
    homeserver=""
    while homeserver=="":
        if not ('homeserver' in js) or js['homeserver']=="":
            print("Set a homeserver")
            homeserver()
        homeserver=js['homeserver']
    while True:
        if count>=MAX_RETRIES:
            break
        client=MatrixClient(homeserver)
        try:
            client.register_with_password(username=username,password=password)
        except:
            time.sleep(2)
            count+=1
        
    try:
        client.logout()
    except:
        pass


def genpass(length=64):
    password=""
    charset=string.digits+string.ascii_letters+string.punctuation
    charset.replace(r"\\","")
    for i in range(length):
        choice=(secrets.choice(charset))
        password+=choice
    return password

def homeserver(fd,js):
    if not ('homeserver' in js) or js['homeserver']=="":
        print("There is no current homeserver.")
    else:
        print("Homeserver: "+js['homeserver'])
    hs=input("Enter the new homeserver:")
    hs="".join(hs.split())
    if(hs==""):
        save_changes(fd,js)
        return
    js['homeserver']=hs
    save_changes(fd,js)

def users(fd,js):
    if not ('users' in js) or type(js['users'])!=list:
        js['users']=[]
        print("There are no users.")
    else:
        print("Users:",js['users'])
    while True:
        count=0
        for user in js['users']:
            print(str(count)+") Remove "+user+".")
            count+=1
        print(str(count)+") Add a new user.")
        count+=1
        print(str(count)+") Return to main menu.")
        try:
            choice=int(input())
        except:
            choice=count+1
        if choice==count:
            save_changes(fd,js)
            return
        elif choice==count-1:
            while True:
                newuser=input("Enter the new user:")
                if(newuser==''):
                    break
                try:
                    matrix_client.checks.check_user_id(newuser)
                    js['users'].append(newuser)
                    save_changes(fd,js)
                    break
                except Exception as ex:
                    print("Invalid user: "+str(ex)+".")
        else:
            try:
                js['users'].pop(choice)
                save_changes(fd,js)
            except:
                print("Invalid choice.")
    save_changes(fd,js)

def bot_name(fd,js):
    if not ('name' in js) or js['name']=="":
        print("There is no current name.")
    else:
        print("name: "+js['name'])
    name=input("Enter the new name:")
    name="".join(name.split())
    if(name==""):
        save_changes(fd,js)
        return
    js['name']=name
    save_changes(fd,js)


def _exit(fd,js):
    save_changes(fd,js)
    fd.close()
    exit(0)

def save_changes(fd,js):
    fd.seek(0)
    fd.write(json.dumps(js,sort_keys=True,indent=4))
    fd.truncate()


if __name__=="__main__":
    main()
