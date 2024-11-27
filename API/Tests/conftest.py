from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from DB.Extension import db
from controllers.AuthController import Login, Register, Logout
from controllers.LoanController import createLoan, deleteLoan, readLoan, readLoans, updateLoan
from controllers.CategoryController import createCategory, deleteCategory, readCategories, readCategory, updateCategory
from controllers.BookController import createBook, deleteBook, readBook, readBooks, updateBook


import pytest
import sqlite3
from datetime import datetime

def adapt_datetime(val):
    return val.isoformat()

def convert_datetime(val):
    return datetime.fromisoformat(val.decode("utf-8"))

# Registro del adaptador y convertidor
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("DATETIME", convert_datetime)



@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = '3F659B45-33BE-4D88-A5D1-C5D337315142'
    api = Api(app)
    db.init_app(app)

    jwt = JWTManager(app)

    api.add_resource(Register, "/api/auth/register")
    api.add_resource(Login, "/api/auth/login")
    api.add_resource(Logout, "/api/auth/logout")

    api.add_resource(createBook, "/api/book/create")
    api.add_resource(readBook, "/api/book/<int:id>")
    api.add_resource(readBooks, "/api/book")
    api.add_resource(updateBook, "/api/book/update/<int:id>")
    api.add_resource(deleteBook, "/api/book/delete/<int:id>")

    api.add_resource(createLoan, "/api/loan/create")
    api.add_resource(readLoan, "/api/loan/<int:id>")
    api.add_resource(readLoans, "/api/loan")
    api.add_resource(updateLoan, "/api/loan/update/<int:id>")
    api.add_resource(deleteLoan, "/api/loan/delete/<int:id>")

    api.add_resource(createCategory,"/api/category/create")
    api.add_resource(readCategory, "/api/category/<int:id>")
    api.add_resource(readCategories, "/api/category")
    api.add_resource(updateCategory, "/api/category/update/<int:id>")
    api.add_resource(deleteCategory, "/api/category/delete/<int:id>")

    with app.app_context():
        db.create_all()
    
    yield app  # Yield the Flask app instead of the test client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()  

