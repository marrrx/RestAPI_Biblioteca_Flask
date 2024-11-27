from datetime import datetime
from flask import jsonify
from flask_restful import Resource, marshal, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required


from DB.Models import Book, Category, User
from DB.Extension import db



create_book_args = reqparse.RequestParser()
create_book_args.add_argument(
    "title", type=str, required=True, help="Title is required"
)
create_book_args.add_argument(
    "author", type=str, required=True, help="Author is required"
)
create_book_args.add_argument(
    "category_id", type=int, required=True, help="Category is required"
)
create_book_args.add_argument(
    "description", type=str, required=True, help="Description is required"
)
create_book_args.add_argument(
    "publication_date", type=str, required=True, help="Publication date is required"
)


book_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "category_id": fields.Integer,
    "description": fields.String,
    "publication_date": fields.String,
}


class createBook(Resource):
    @jwt_required()
    def post(self):
        args = create_book_args.parse_args()

        # Lista de errores para validaciones personalizadas
        errors = []

        # Validación de campos individuales
        if not args["title"] or args["title"].isspace():
            errors.append("Title is required")

        if not args["author"] or args["author"].isspace():
            errors.append("Author is required")

        if not args["category_id"]:
            errors.append("Category is required")

        if not args["description"] or args["description"].isspace():
            errors.append("Description is required")

        if not args["publication_date"] or args["publication_date"].isspace():
            errors.append("Publication date is required")

        # Validación de existencia de categoría
        session = db.session
        category = session.get(Category, args["category_id"])
        if not category:
            errors.append("Invalid category ID")

        # Validación de formato de fecha (YYYY-MM-DD)
        try:
            publication_date = datetime.strptime(args["publication_date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid publication date format. Use YYYY-MM-DD.")

        # Validación de unicidad del título y autor del libro
        existing_book = Book.query.filter_by(title=args["title"], author=args["author"]).first()
        if existing_book:
            errors.append("A book with the same title and author already exists")

        # Si hay errores, devuelve una respuesta con código 400
        if errors:
            return ({"errors": errors}), 400  # Utiliza jsonify para retornar el diccionario de errores

        # Crea el nuevo libro
        book = Book(
            title=args["title"],
            author=args["author"],
            category_id=args["category_id"],
            description=args["description"],
            publication_date=publication_date,
        )

        # Agrega y guarda el libro en la base de datos
        db.session.add(book)
        db.session.commit() 

        return marshal(book, book_fields), 201
    

class readBook(Resource):
    def get(self, id):
        book = Book.query.get(id)
        if book:
            return book, 200
        else:
            return {"message": "Book not found"}, 404
        
class readBooks(Resource):
    def get(self):
        books = Book.query.all()
        return books, 200
    
class updateBook(Resource):
    @jwt_required()
    def put(self, id):
        # Verificar si el libro existe
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404

        args = create_book_args.parse_args()
        errors = []

        # Validaciones de campos individuales
        if not args["title"] or args["title"].isspace():
            errors.append("Title is required")
        if not args["author"] or args["author"].isspace():
            errors.append("Author is required")
        if not args["category_id"]:
            errors.append("Category is required")
        if not args["description"] or args["description"].isspace():
            errors.append("Description is required")
        if not args["publication_date"] or args["publication_date"].isspace():
            errors.append("Publication date is required")

        # Validación de unicidad para título y autor (evita duplicados)
        existing_book = Book.query.filter(
            Book.title == args["title"],
            Book.author == args["author"],
            Book.id != id  # Ignora el libro actual en la verificación
        ).first()
        if existing_book:
            errors.append("A book with the same title and author already exists")

        # Validación de existencia de categoría
        category = Category.query.get(args["category_id"])
        if not category:
            errors.append("Invalid category ID")

        # Validación de formato de fecha (YYYY-MM-DD)
        try:
            publication_date = datetime.strptime(args["publication_date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid publication date format. Use YYYY-MM-DD.")

        # Validación de longitud de campos
        if len(args["title"]) > 100:
            errors.append("Title cannot exceed 100 characters")
        if len(args["author"]) > 50:
            errors.append("Author cannot exceed 50 characters")
        if len(args["description"]) > 500:
            errors.append("Description cannot exceed 500 characters")

        # Si hay errores, devuelve una respuesta con código 400
        if errors:
            return {"errors": errors}, 400

        # Actualiza los campos del libro
        book.title = args["title"]
        book.author = args["author"]
        book.category_id = args["category_id"]
        book.description = args["description"]
        book.publication_date = publication_date

        # Guarda los cambios en la base de datos
        db.session.commit()

        # Serializa el objeto `book` antes de devolverlo
        return marshal(book, book_fields), 200
    
class deleteBook(Resource):
    @jwt_required()
    def delete(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404

        # Elimina el libro de la base de datos
        db.session.delete(book)
        db.session.commit()

        return {"message": "Book deleted successfully"}, 200
