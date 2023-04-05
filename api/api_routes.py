from flask import jsonify , Blueprint , request
from flask_jwt_extended import  jwt_required , get_jwt_identity
import requests
import datetime
from datetime import date 
from random import randint 
from init_packages import jwt ,db
from models.user import User
from models.book import Book
from models.transaction import Transaction

import json
api = Blueprint('api' , __name__ )

@api.route("/")
def home():
    try:
        args = request.args
        global url
        url = "https://hapi-books.p.rapidapi.com/nominees/romance/2020"
        genre = "romance"
        year = "2020"
        print(args.to_dict())
        if args.to_dict() != {}:
            if args["genre"]:
                genre = args["genre"]
            if args["year"]:
                year = args["year"]
            url = f"https://hapi-books.p.rapidapi.com/nominees/{genre}/{year}"
        print(url)
        headers = {
            "X-RapidAPI-Key": "9c254922afmsh6ac51f1b70c0bdep1978f1jsn7f9444b252cf",
            "X-RapidAPI-Host": "hapi-books.p.rapidapi.com",
        }

        response = requests.request("GET", url, headers=headers)
        print(response)
        books = response.json()
        print(books)
        for book in books:
            print(book)
            prevbook = Book.query.filter_by(name=book['name']).first()
            # book_id = None    
            if prevbook != None:
                prevbook.stock += 1
            else:
                new_book = Book(name=book['name'] , author=book['author'] ,votes=book['votes'] )
                db.session.add(new_book)

        db.session.commit()
    except:
        return (
            jsonify({"message": "Some Thing went wrong with 3rd party Rapid api "}), 500
        )
    return (
            jsonify({"message": "Books are fetched and stored in data base"}), 200
        )
 

@api.route("/register", methods=["POST"])
def register_member():
    username = ""
    email = ""
    phone = None
    password = ""
    admin = None
    try:
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]
        phone = request.json["phone"]
        admin = request.json["admin"]


    except KeyError:
        return jsonify({"message": "Key Error = All values not Available"}), 404

    if username == "" or email == "" or phone == None  or password == ""  or admin == None :
        return jsonify({"message": "Please fill all values"}), 400
    new_user = None
    single_user = User.query.filter_by(username = username).first()
    if single_user == None :
        new_mem = User(username=username, email=email, phone=phone , password=password, admin=admin)
        db.session.add(new_mem)
        db.session.commit()
        return jsonify({"message": "member added", "mem_id": new_mem.id}), 200

    return (
        jsonify(
            {"message": "member already exists", "mem_id": single_user.id}
        ),
        401,
    )

@api.route("/borrow", methods=["POST"])
def borrow_book():
    
    boro_book_id = None
    boro_user_id = None
    try:
        boro_book_id = request.json["book_id"]
        boro_user_id = request.json["user_id"]
    except KeyError:
        return jsonify({"message": "Key Error = All values not Available"}), 404

    if boro_book_id == None or boro_user_id == None:
        return jsonify({"message": "Please fill all values"}), 400

    # ================= checking if user id exists ================================
    prev_user = User.query.get(boro_user_id)
    print(prev_user)
    if prev_user == None :
        return jsonify({"message": "Member Does not exists , Please register"}), 404
    # =============== Making New Tuple in Transactions =============================
    prev_user = User.query.get(boro_user_id)
    if prev_user.debt >= 500:
        return (
            jsonify(
                {"message": "Your debt exceeded 500rs repay before borrowing book"}
            ),
            200,
        )

   
    prev_book = Book.query.filter_by(id = boro_book_id).first()
    if prev_book.stock <= 0:
        return jsonify({"message": "Book Out of stock"}), 404
    
    prev_tra = Transaction.query.filter_by(book_id=boro_book_id, user_id=boro_user_id, borrowed=True).first()
    print(prev_tra)
    if prev_tra != None :
        return jsonify({"message": "First_return the previouly borrowed book"}),400
    
    new_tra= Transaction( book_id=boro_book_id, user_id=boro_user_id)
    prev_book.stock -= 1
    prev_book.votes += 1 
    db.session.add(new_tra)
    db.session.commit()

    return jsonify({"message": "Thanks for Borrowing Book", "tra_id": new_tra.id}), 200



@api.route("/return", methods=["POST"])
def return_book():
    tra_id = None
    try:
        tra_id = request.json["tra_id"]
    except KeyError:
        return jsonify({"message": "Key Error = All values not Available"}), 404
    if tra_id == None:
        return jsonify({"message": "Please fill all values"}), 400
    try:
        temp_tra = Transaction.query.get(tra_id)
        if(temp_tra ==  None):
            raise ("Exception")
    except :
        return (
            jsonify({"message": "Invalid Transaction id"}),
            400,
        )

    test = Transaction.query.filter_by(id=tra_id, borrowed=False).first()
    if test != None :
        return (
            jsonify({"message": "Old Record,Book already Returned"}),
            200,
        )

    tra = Transaction.query.filter_by(id=tra_id, borrowed=True).first()
    book = Book.query.filter_by(id=tra.book_id).first()
    print(book)
    user = User.query.filter_by(id=tra.user_id).first()
    print(user)
    book.stock += 1
    tra.borrowed = False
    f_date = tra.from_date
    # t_date = datetime.now().date()
    t_date = date(2023, 3, 30)
    diff = t_date - f_date
    new_fine = (diff.days) * 10
    new_debt = user.debt + new_fine
    tra.fine = new_debt
    user.debt= new_debt
    db.session.commit()
    return jsonify({"message": "Book has been Returned", "rent": tra.fine}), 200




@api.route("/debt", methods=["POST"])
def pay_debt():
    user_id = None
    amount = None
    try:
        user_id = request.json["user_id"]
        amount = request.json["amount"]
    except KeyError:
        return jsonify({"message": "Key Error = All values not Available"}), 404
    if user_id == None and amount == None:
        return jsonify({"message": "Please fill all values"}), 400
    try:

        user = User.query.get(user_id)
        if(user == None):
            raise("exception")
        if user.debt == 0:
            return jsonify({"message": "No Debt left", "fine": user.debt}), 200

    except :
        return jsonify({"message": "Object Not Found"}), 404

    p_debt = user.debt
    n_debt = p_debt - amount
    user.debt = n_debt
    db.session.commit()
    return (
        jsonify(
            {"message": "Amount returned", "amount": amount, "remaining": user.debt}
        ),
        200,
    )




#==========================================================
@api.route("/getmembers", methods=["GET"])
def get_members():
    user = User.query.filter_by()

    def get_dict(item):
        return {
            "member_id": item.id,
            "username": item.username,
            "email": item.email,
            "phone": item.phone,
            "debt": item.debt, 
            "admin": item.admin, 
        }

    arr = list(map(get_dict, user))
    return jsonify(arr), 200




@api.route("/getmember/<int:_id>", methods=["GET"])
def get_member(_id):
    user = None
    try:
        user = User.query.get(_id)
        if(user is None):
            raise ('Sql Oject not found')
        print(user)
    except :
        return jsonify({"message": "member not found"}), 404
    else:
        return jsonify( {
            "member_id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "debt": user.debt, 
            "admin": user.admin, 
        }), 200
    

@api.route("/delmember/<int:_id>", methods=["DELETE"])
def delete_member(_id):
    user = None 
    try:
        user = User.query.get(_id)
        if(user == None):
            raise ('exception')
    except:
        return jsonify({"message": "Object Not found"}), 404 
    else:
        pending_tra = Transaction.query.filter_by(member_id=user.id, borrowed=True).first()
        pending_debt = User.query.filter_by(id=user.id).first().debt

        if pending_tra != None:
            return (
                jsonify(
                    {"message": "Can't Revoke member ship please return borrowed book"}
                ),
                400,
            )
        if pending_debt > 10:
            return (
                jsonify(
                    {
                        "message": "Can't Revoke member ship please pay your remaining rent"
                    }
                ),
                400,
            )

        db.session.delete(user)
        db.session.commit() 
        return jsonify({"message": "Member Deleted"}), 200
    



#==========================================================
@api.route("/books", methods=["GET"])
def fetchbooks():
    def get_dict(item):
        return {
            "book_id": item.id,
            "book_name": item.name,
            "book_author": item.author,
            "book_stock": item.stock,
            "votes": item.votes,
        }

    data = Book.query.filter_by()
    return jsonify(list(map(get_dict, list(data)))), 200


@api.route("/addbook", methods=["POST"])
def addbook():
    name = None
    author = None
    stock = None
    try:
        try:
            name = request.json["name"]
            author = request.json["author"]
            stock = request.json["stock"]
        except KeyError:
            return jsonify({"message": "Key Error = All values not Available"}), 404
        
        if name == "" or author == "" or stock == None:
            return jsonify({"message": "Please fill all values"}), 400

        prevbook = Book.query.filter_by(name=name, author=author).first()
        new_book = None
        if prevbook != None :
            prevbook.stock += stock
            db.session.commit()
            return jsonify({"message": "Book stock Added", "book_id": prevbook.id}), 200

        else:
            new_book = Book(name=name, author=author, stock=stock)
            db.session.add(new_book)

    except:
        return jsonify({"message": "Something Went Wrong"}), 400
    db.session.commit()
    return jsonify({"message": "Book Added", "book_id": new_book.id}), 200


@api.route("/deletebook/<int:_id>", methods=["DELETE"])
def deletebook(_id):
    book = None
    try:
        book = Book.query.get(_id)
        if(book is None):
            raise ('exception')
    except :
        return jsonify({"message": "Book Not Found"}), 404
    else:
        db.session.delete(book)
    
    db.session.commit()

    return jsonify({"message": "Book deleted"}), 200

#========================================================================

@api.route("/transactions", methods=["GET"])
def transactions():
    def get_dict(item):
        return {
            "tra_id": item.id,
            "book_id": item.book_id,
            "user_id": item.user_id,
            "from_date": str(item.from_date),
            "fine": item.fine,
            "borrowed": item.borrowed,
        }

    tras = Transaction.query.filter_by()
    return jsonify(list(map(get_dict, list(tras)))) ,200

@api.route("/transactions/<int:_id>", methods=["GET"])
def transaction_by_id(_id):
    def get_dict(item):
        return {
            "tra_id": item.id,
            "book_id": item.book_id,
            "member_id": item.member_id,
            "book_name": item.book_name,
            "from_date": str(item.from_date),
            "fine": item.fine,
            "borrowed": item.borrowed,
        }
    tras = None 
    try:
        tras = Transaction.query.get(_id)
        if(tras is None):
            raise ('exception')
    except:
        return "object not found ", 404
    
    return jsonify(list(map(get_dict, list(tras))))