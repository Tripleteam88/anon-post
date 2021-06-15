import hashlib
import random
from datetime import datetime as dt

class User:
    def __init__(self, username:str, password:str):
        self.username = username
        hash_obj = hashlib.sha256(bytes(password, 'utf8'))
        self.password = hash_obj.hexdigest()
        self.posts = []
        self.genID()
    def genID(self):
        self.ID = random.randint(1000000, 9999999)
    def toHash(self, value:str):
        hash_obj = hashlib.sha256(bytes(value, 'utf8'))
        return hash_obj.hexdigest()

class Post:
    def __init__(self, title:str, author:str, content:str, ID:int):
        self.title = title
        self.author = author
        self.content = content
        self.datePosted = dt.now().strftime('%b. %e %Y %r')
        self.ID = ID