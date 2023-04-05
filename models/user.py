from init_packages import db

class User(db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50), unique=True , nullable = False) 
    password = db.Column(db.String(50), nullable = False ,)
    email = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(10), nullable = False)
    debt = db.Column(db.Integer , default = 0 )
    admin   = db.Column(db.Boolean )
    
    # admin = db.Column(db.Bool, nullable = False)
    def __init__(self,username,password,admin,email,phone):
        self.username = username 
        self.password = password 
        self.admin = admin 
        self.email = email 
        self.phone = phone 
    
    def __str__(self) -> str:
        return str(self.id)+" "+str(self.username)+" "+str(self.email)+" "+str(self.phone)+" "+str(self.password)+" "+str(self.admin)+str(self.debt)+" ."
