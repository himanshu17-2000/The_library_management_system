from init_packages import db

class Book(db.Model):
    __tablename__ = "book"
    id=db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(50), unique=True , nullable = False) 
    author = db.Column(db.String(50), nullable = False)
    stock = db.Column(db.Integer , default = 20 ) 
    votes = db.Column(db.Integer , default = 0 ) 
    
    def __init__(self,name,author,votes=0, stock = 0 ):
        self.name = name 
        self.author = author 
        self.votes = votes 
    
    def __str__(self) -> str:
        return str(self.id)+" "+str(self.name)+" "+str(self.author)+" "+str(self.stock)+" "+str(self.votes)+" ."
