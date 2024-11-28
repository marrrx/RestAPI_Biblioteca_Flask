from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, marshal, marshal_with, reqparse, fields

from DB.Models import Category
from DB.Extension import db

create_category_args = reqparse.RequestParser()
create_category_args.add_argument(
    "name", type=str, required=True, help="Name is required"
)

categoryFields = {
    "id": fields.Integer,
    "name": fields.String,
}


class createCategory(Resource):
    @jwt_required()
    def post(self):
        args = create_category_args.parse_args()

        # Validación de existencia de categoría
        existing_category = Category.query.filter_by(name=args["name"]).first()
        if existing_category:
            return {"message": "Category already exists"}, 409

        # Crear la nueva categoría
        category = Category(name=args["name"])

        # Guardar la categoría en la base de datos
        db.session.add(category)
        db.session.commit()

        return marshal(category, categoryFields), 201


class readCategories(Resource):
    def get(self):
        categories = Category.query.all()
        if categories:
            return marshal(categories, categoryFields), 200
        else:
            return {"message": "Category not found"}, 404


class readCategory(Resource):
    def get(self, id):
        category = Category.query.get(id)
        if category:
            return marshal(category, categoryFields), 200
        else:
            return {"message": "Category not found"}, 404


class updateCategory(Resource):
    @jwt_required()
    def post(self, id):
        category = Category.query.get(id)
        if not category:
            return {"message": "Category not found"}, 404

        args = create_category_args.parse_args()
        errors = []

        # Validaciones de campos individuales
        if not args["name"]:
            errors.append("Name is required")

        # Validación de existencia de categoría
        existing_category = Category.query.filter_by(name=args["name"]).first()
        if existing_category:
            return {"message": "Category already exists"}, 409

        # Si hay errores, devuelve una respuesta con código 400
        if errors:
            return {"errors": errors}, 400

        # Actualiza los campos de la categoría
        category.name = args["name"]

        # Guarda los cambios en la base de datos
        db.session.commit()

        return marshal(category, categoryFields), 200


class deleteCategory(Resource):
    @jwt_required()
    def delete(self, id):
        category = Category.query.get(id)
        if not category:
            return {"message": "Category not found"}, 404

        # Elimina la categoría de la base de datos
        db.session.delete(category)
        db.session.commit()

        return {"message": "Category deleted successfully"}, 200
