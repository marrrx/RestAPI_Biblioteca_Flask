from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from DB.Extension import db
from DB.Seeders import runSeeders

from controllers.AuthController import Login, Register, Logout
from controllers.BookController import createBook, deleteBook, readBook, readBooks, updateBook
from controllers.LoanController import createLoan, deleteLoan, readLoan, readLoans, updateLoan
from controllers.CategoryController import createCategory, deleteCategory, readCategories, readCategory, updateCategory

import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


api = Api(app)

with app.app_context():
    db.init_app(app)
    db.create_all()
    runSeeders()

    

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






if __name__ == "__main__":
    @app.errorhandler(401)
    def not_authorized_error(error):
        return jsonify({"message": "Missing or invalid token"}), 401

    app.run(debug=True)
    
