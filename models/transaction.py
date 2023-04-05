from init_packages import db
from datetime import datetime


class Transaction(db.Model):
    __tablename__ = "transaction"
    id=db.Column(db.Integer , primary_key = True)
    book_id = db.Column(db.Integer , nullable = False) 
    user_id = db.Column(db.Integer , nullable = False)
    from_date =db.Column(db.Date , nullable = False ,default=datetime.now().date())
    borrowed= db.Column(db.Boolean , default = True)
    fine= db.Column(db.Integer , default = 0)

    def __init__(self,book_id,user_id):
        self.book_id = book_id 
        self.user_id = user_id 
    
    def __str__(self) -> str:
        return str(self.id)+" "+str(self.book_id)+" "+str(self.user_id)+" "+str(self.borrowed)+" "+str(self.fine)+" "+str(self.from_date)+" ."
