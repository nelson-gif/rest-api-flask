from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'book'

    def __init__(self, book_isbn, genre_id, author_id,
                 title, stock, price, pages, publication_date):
        self.book_isbn = book_isbn
        self.genre_id = genre_id
        self.author_id = author_id
        self.title = title
        self.stock = stock
        self.price = price
        self.pages = pages
        self.publication_date = publication_date

    book_isbn = db.Column(db.Integer, primary_key=True, unsigned=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'))


class Author(db.Model):
    __tablename__ = 'author'

    def __init__(self, name, last_name, country, gender, dob):
        self.name = name
        self.last_name = last_name
        self.country = country
        self.gender = gender
        self.dob = dob

    author_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    country = db.Column(db.String(255))
    gender = db.Column(db.String(25))
    dob = db.Column(db.DateTime)

    def __repr__(self):
        return (f'<Author - {self.author_id} - {self.name} - {self.last_name}'
                f'- {self.country} - {self.gender} - {self.dob}>')

class Genre(db.Model):
    __tablename__ = 'genre'

    def __init__(self,genre, description):
        self.genre = genre
        self.description = description

    genre_id = db.Column(db.Integer, primary_key = True)
    genre = db.Column(db.String(255), unique = True, nullable = False)
    description = db.Column(db.String(255), nullable = True)
    author = db.relationship('Book')

    def __repr__(self):
        return f'<Genre - {self.genre_id} - {self.genre} - {self.description}>'

