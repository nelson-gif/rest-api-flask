from flask import Flask, jsonify, request
from config import DevelopmentConfig
from models import *

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

#code for table BOOK
@app.route('/book', methods=['POST'])
def create_book():
    data = request.get_json()
    book_isbn = data.get('book_isbn')
    genre_id = data.get('genre_id')
    author_id = data.get('author_id')
    title = data.get('title')
    stock = data.get('stock')
    price = data.get('price')
    pages = data.get('pages')
    publication_date = data.get('publication_date')

    if book_isbn is None and genre_id is None and author_id is None and title is None and stock is None:
        return jsonify({'error' : 'books_isbn, genre_id, author_id, title and stock cannot be null'}), 406

    try:
        book = Book(book_isbn, genre_id, author_id, title, stock, price, pages, publication_date)

        db.session.add(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error message' : 'an error ocurred while saving the book',
                        'error' : f'{e}'}), 400

    return jsonify({'message' : 'the book was added successfully',
                    'book added' : f'{data}'}), 201

@app.route('/book', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    books_list = []
    for book in books:
        temporary_book = {
            'book_isbn' : book.book_isbn,
            'genre' : {
                'genre' : f'{Genre.query.get(book.genre_id)}'
            },
            'author' : {
                'author' : f'{Author.query.get(book.author_id)}'
            },
            'title' : book.title,
            'stock' : book.stock,
            'price' : book.price,
            'pages' : book.pages,
            'publication_date' : book.publication_date,
            'stock_added_date' : book.stock_added_date
        }
        books_list.append(temporary_book)
    return jsonify(books_list), 200

@app.route('/book/<int:id>', methods = ['GET'])
def get_book_by_id(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error' : 'book not found'}), 404
    temporary_book = {
        'book_isbn' : book.book_isbn,
        'genre_id' : {
            'genre' : f'{Genre.query.get(book.genre_id)}'
        },
        'author_id' : {
            'author' : f'{Author.query.get(book.author_id)}'
        },
        'title' : book.title,
        'stock' : book.stock,
        'price' : book.price,
        'pages' : book.pages,
        'publication_date' : book.publication_date,
        'stock_added_date' : book.stock_added_date
    }
    return jsonify(temporary_book), 200

@app.route('/book/<int:id>', methods=['PUT'])
def update_book_by_id(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error' : 'book not found'}), 404
    data = request.get_json()
    book_isbn = data.get('book_isbn')
    genre_id = data.get('genre_id')
    author_id = data.get('author_id')
    title = data.get('title')
    stock = data.get('stock')
    price = data.get('price')
    pages = data.get('pages')
    publication_date = data.get('publication_date')

    if book_isbn is None and genre_id is None and author_id is None and title is None and stock is None:
        return jsonify({'error': 'books_isbn, genre_id, author_id, title and stock cannot be null'}), 406

    try:
        book.book_isbn = book_isbn
        book.genre_id = genre_id
        book.author_id = author_id
        book.title = title
        book.stock = stock
        book.price = price
        book.pages = pages
        book.publication_date = publication_date

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error message' : 'an error ocurred while updating the book',
                        'error' : f'{e}'}), 400
    return jsonify({'message' : 'the book was updated successfully'}), 200

@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book_by_id(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'error' : 'book not found'}), 404
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error message' : 'an error ocurred while deleting the book',
                        'error' : f'{e}'}), 400
    return jsonify({'message' : 'the book was deleted successfully'}), 200

#code for table AUTHOR
@app.route('/author', methods=['POST'])
def create_author():
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')
    country = data.get('country')
    gender = data.get('gender')
    dob = data.get('dob')

    if name is None and last_name is None:
        return jsonify({'error' : 'name and last_name cannot be null'}), 406

    try:
        author = Author(name, last_name, country, gender, dob)
        db.session.add(author)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : f'{e}'}), 400
    return jsonify({'message' : 'author was added successfully',
                    'author added' : f'{author}'})

@app.route('/author', methods=['GET'])
def get_all_authors():
    authors = Author.query.all()
    author_list = []

    for author in authors:
        author_data = {
            'author_id' : author.author_id,
            'name' : author.name,
            'last_name' : author.last_name,
            'country' : author.country,
            'gender' : author.gender,
            'dob' : author.dob
        }
        author_list.append(author_data)
    return jsonify(author_list), 200

@app.route('/author/<int:id>')
def get_author_by_id(id):
    author = Author.query.get(id)
    if author is None:
        return jsonify({'error' : f'there is no author with the id {id}'}), 404
    author_data = {
        'author_id' : author.author_id,
        'name' : author.name,
        'last_name' : author.last_name,
        'country' : author.country,
        'gender' : author.gender,
        'dob' : author.dob
    }
    return jsonify(author_data), 200

@app.route('/author/<int:id>', methods=['PUT'])
def update_author_by_id(id):
    author = Author.query.get(id)
    if author is None:
        return jsonify({'error' : f'there is no author with the id {id}'}), 404
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')
    country = data.get('country')
    gender = data.get('gender')
    dob = data.get('dob')

    if name is None and last_name is None:
        return jsonify({'error' : 'name and last_name cannot be null'}), 406

    try:
        author.name = name
        author.last_name = last_name
        author.country  = country
        author.gender = gender
        author.dob = dob
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message' : 'an error ocured','error' : f'{e}'}), 400

    return jsonify({'message' : 'author was updated successfully',
                    'author updated' : f'{author}'}), 200

@app.route('/author/<int:id>', methods=['DELETE'])
def delete_author_by_id(id):
    author = Author.query.get(id)
    if author is None:
        return jsonify({'error' : f'there is no author with the id {id}'}), 404
    try:
        db.session.delete(author)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message' : 'an error ocurred while deleting author'
                           ,'error' : f'{e}'}), 400
    return jsonify({'message' : 'author was deleted successfully'}), 200


#code for table GENRE

@app.route('/genre', methods=['POST'])
def createGenre():
    data = request.get_json()
    if data.get('genre') is None:
        return jsonify({'error' : 'genre cannot be null'}), 406
    try:
        genre = Genre(data.get('genre').upper(), data.get('description'))
        db.session.add(genre)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error message' : 'There was an error while adding the genre',
                        'error' : f'{e}'}), 400
    return jsonify(f'The genre was added successfully {data}'), 201


@app.route('/genre', methods=['GET'])
def getAllGenre():
    genres = Genre.query.all()
    genres_list = []

    for genre in genres:
        genre_data = {
            "genre_id" : genre.genre_id,
            "genre" : genre.genre,
            "description" : genre.description
        }
        genres_list.append(genre_data)

    return jsonify(genres_list), 200

@app.route('/genre/<int:id>', methods = ['GET'])
def getGenreById(id):
    genre = Genre.query.get(id)
    if genre is None:
        return jsonify({'error message' : f'the Genre with the id {id} doesn\'t exist'}), 404
    genre_data = {
        'genre_id' : genre.genre_id,
        'genre' : genre.genre,
        'description' : genre.description
    }
    return jsonify(genre_data), 200

@app.route('/genre/<int:id>', methods=['PUT'])
def updateGenreById(id):
    genre = Genre.query.get(id)
    if genre is None:
        return jsonify({'error' : f'the genre with the id: {id} doesn\'t exist'}), 404
    data = request.get_json()
    genre_name = data.get('genre')
    description = data.get('description')
    if genre_name is None:
        return jsonify({'error' : 'genre cannot be null'}), 406

    try:
        genre.genre = genre_name
        genre.description = description
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error message' : 'An error ocurred while updating the genre',
                       'error' : f'{e}'}), 400
    return jsonify({'message': 'the genre was updated successfully',
                    'genre updated' : f'{genre}'}), 200

@app.route('/genre/<int:id>', methods=['DELETE'])
def deleteGenreById(id):
    genre = Genre.query.get(id)
    if genre is None:
        return jsonify({'error' : f'the genre with the id: {id} doesn\'t exist'}), 404
    try:
        db.session.delete(genre)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error message': 'An error ocurred while deleting the genre',
                        'error': f'{e}'}), 400
    return jsonify({'message': f'the genre with id {id} was deleted successfully'}), 200



if __name__ == '__main__':
    app.run()
