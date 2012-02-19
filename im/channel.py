'''
Created on Jun 2, 2011

@author: zhangsheimi
'''
import uuid

class Channel(object):
    '''
    classdocs
    '''
    _instance = None
    waiters = {}
    cache = []
    cache_size = 200
    sessions = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Channel, cls).__new__(
                                        cls, *args, **kwargs)
        return cls._instance
    
    def new_session(self, session_name, *users):
        session = {
            'session_id'    :   str(uuid.uuid4()),
            'session_name'  :   session_name,
            'users'         :   list(users),
        }
        s_id = session["session_id"]
        self.sessions[s_id] = session
        return session
     
    def quit(self, session_id, user_id):
        self.sessions[session_id]['users'].remove(user_id)
        self.check_session(session_id)  
        
    def add_users(self, session_id, *users):
        session = self.sessions[session_id]
        for user in users:
            if not session["users"].__contains__(user) and self.is_online(user):
                session["users"].append(user)
                
    def new_im(self, message, session_id):
        users_id = self.sessions[session_id]['users']
        for id in users_id:
            if not (id == message["sender_id"]):
                self.on_new_messages(message, id)
            
    def check_session(self, session_id):
        session = self.sessions.has_key(session_id) and self.sessions[session_id] or None
        if not session:
            return False
        users_id = session['users']
        for i in range(0, len(users_id)):
            if not self.is_online(users_id[i]):
                users_id.remove(users_id[i])
        if len(users_id) - 1:
            return session
        self.sessions.pop(session_id)
        return False
        

    def wait_for_messages(self, callback, id, cursor=None):
        if cursor:
            index = 0
            for i in xrange(len(self.cache)):
                index = len(self.cache) - i - 1
                if self.cache[index]["id"] == cursor: break
            recent = self.cache[index + 1:]
            if recent:
                callback(recent)
                return
        if self.waiters.has_key(id):
            self.waiters[id].append(callback)
        else: 
            self.waiters[id] = [callback]

    def on_new_messages(self, message, id):
        if not self.waiters.has_key(id):
            return
        callbacks = self.waiters[id]
        while len(callbacks):
            callback = callbacks.pop()
            callback(message)
    
    def is_online(self, id):
        if not self.waiters.has_key(id):
            return False;
        callbacks = self.waiters[id]
        if len(callbacks) == 0:
            return False;
        return True;
    
