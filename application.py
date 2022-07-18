from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


'''initialize flask'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booksData.db'
'''stores data into a database and checks API for .db to determine and or create booksData.db'''
db = SQLAlchemy(app)
'''create a database from sqlalchemy to pass in the app instance'''

'''inherits from db.model, class of a book and not with a table of books yet'''
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable = False) #unique implies only one name
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.book_name} by {self.author}"


@app.route('/')
def index():
    return 'Hello'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'book_name': book.book_name, 'author': book.author, 'publisher': book. publisher}
        output.append(book_data)
    return{"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return{"book_name": book.book_name, "author": book.author, "publisher": book.publisher}

@app.route('/books', methods = ['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return{'id:book.id'}

@app.route('/books/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message": "doh!"}

