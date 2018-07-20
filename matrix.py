from matrix_client.client import *
from matrix_client.room import *
from matrix_client.user import *
from matrix_client.checks import *
from matrix_client.errors import *
import time

class matrix:
    
    INVITE_TIMEOUT=300 #seconds
    REFRESH_ROOM_TIMER=30 #seconds

    def __init__(self,name,homeserver,users,username,password):
        self.name=name
        self.client=MatrixClient(homeserver)
        self.homeserver=homeserver
        self.username=username
        self.password=password
        self.users=users #list of user_id

        self.user2room={} #user2room[user_id]=room_id
        self.listeners={} # listeners[room_id]=uuid
        self.invited_users={} # invited_users[room_id]=(user_id,time of invite) , could replace with presence_listener
        self.messages=[] #list of tuple(content,user_id)
        self.last_refresh=time.time()-30

    def login(self):
        logincount=0
        while(logincount<10):
            try:
                token=self.client.login(self.username,self.password)
                self.token=token
                return True
            except MatrixRequestError as ex:
                print(ex)
                logincount+=1
        return False

    def sync(self):
        print("Syncing...")
        missing_users=self.users.copy()
        roooms=self.client.rooms.copy()
        for room_id,room in roooms.items():
            members=room.get_joined_members()
            num_users=len(members)
            if len(members) != 2:
                self.leave_room(room,num_users)
            else:
                for user in self.users:
                    if user in (member.user_id for member in members):
                        if user in missing_users:
                            self.user2room[user]=room_id
                            missing_users.remove(user)
                        else:
                            self.leave_room(room,num_users)
                    else:
                        self.leave_room(room,num_users)
        self.invite_users(missing_users)
        self.refresh_listeners()
        self.last_refresh=time.time()

    def leave_room(self,room,num_users):
        if num_users<2:
            if room.room_id in self.invited_users:
                if( abs(time.time()-self.invited_users[room.room_id][1]) < self.INVITE_TIMEOUT ):
                    return
                else:
                    self.invited_users.pop(room.room_id)
        print("Leaving Room")
        while not room.leave():
            print("Failed to leave room.")

        for user_id,room_id in self.user2room.items():
            if room_id == room:
                self.user2room.pop(user_id)


    def invite_users(self,users):
        for user in users:
            passed=False
            notInvited=True
            for room_id,tup in self.invited_users.items():
                if tup[0] == user and abs(tup[1]-time.time()) < self.INVITE_TIMEOUT:
                    notInvited=False
            if notInvited:
                while not passed:
                    try:
                        room=self.client.create_room(is_public=False,invitees=[user])
                        print("Invited user "+str(user)+" to room "+str(room.room_id))
                        passed=True
                        self.user2room[user]=room.room_id
                        self.invited_users[room.room_id]=(user,time.time())
                    except MatrixRequestError as ex:
                        print(ex)

    def refresh_listeners(self):
        print("Refreshing Listeners")
        missing_listeners=self.listeners.copy()
        for room_id,room in self.client.rooms.items():
            if room_id in self.listeners:
                missing_listeners.pop(room_id)
            else:
                uuid=room.add_listener(self.callback_message,event_type="m.room.message")
                self.listeners[room_id]=uuid

        for room_id,uuid in missing_listeners.items():
            self.client.remove_listener(uuid)

    def callback_message(self,room,event):
        if event['type']=="m.room.message":
            if event['content']['msgtype']=="m.text":
                self.messages.append((event['content']['body'],event['sender']))

    def receive_message(self):
        if( abs(time.time()-self.last_refresh) > self.REFRESH_ROOM_TIMER):
            self.sync()
        self.client.listen_for_events()
        if(len(self.messages)>0):
            return self.messages.pop(0)
        else:
            return (None,None)

    def send_message(self,content,user_id):
        print("Sending "+str(content)+" to "+str(user_id))
        self.client.rooms[self.user2room[user_id]].send_text(content)

    def update_users(self,users):
        self.users=users
        self.sync()

    def validuser(user_id):
        return check_user_id(user_id)
