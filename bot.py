#!/usr/bin/python3

import bot_shell
import string
from matrix import matrix
import json
import base64

class bot:
    
    def __init__(self):
        commands=[]
        self.shell=bot_shell.bot_shell(commands)
        with open("cfg/config") as F:
            data=F.read()
        cfg=json.loads(data)
        for user in cfg['users']:
            try:
                matrix.validuser(user)
            except:
                print("Invalid user: "+user)
                exit(1)
        self.users=cfg['users']
        password=base64.b64decode(cfg['password']).decode(encoding='UTF-8')
        self.matrix=matrix(cfg['name'],cfg['homeserver'],cfg['users'],username=cfg['username'],password=password)
        try:
            self.matrix.login()
        except Exception as ex:
            print(ex)

    def receive_message(self):
        return self.matrix.receive_message()

    def send_message(self,text,user_id):
        self.matrix.send_message(text,user_id)

    def verify_message(self,message):
        text=message[0]
        user_id=message[1]
        if not (user_id in self.users):
            return False
        for c in text:
            if not (c in string.printable):
                return False
        return True

    def process_message(self,message):
        return self.shell.process(message)

    def loop(self):
        while(True):
            print("Receiving message")
            message=self.receive_message()
            if self.verify_message(message):
                print(message)
                response,status=self.process_message(message)
                if response!=None or len(response)>0:
                    self.send_message(response,message[1])
                if status != 0:
                    exit(0)

def main():
    b=bot()
    print("Listening")
    b.loop()


if __name__=="__main__":
    main()
