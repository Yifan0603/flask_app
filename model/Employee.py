from app import db

#tao ra model tuong ung voi 1 bang trong db
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250))
    file_name = db.Column(db.String(255))
    
    def __init__(self, username, email, address, file_name):
        self.username = username
        self.email = email
        self.address = address
        self.file_name = file_name

    def obj_person(self):
        obj = dict(id=self.id,username=self.username,email=self.email,address=self.address, file_name=self.file_name)
        return obj
