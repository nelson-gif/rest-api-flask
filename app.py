from flask import Flask, jsonify, request
from config import DevelopmentConfig
from models import *

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'



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
    db.session.delete(author)
    db.session.commit()
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
