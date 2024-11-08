from flask import Response, abort
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

import json
import re

from DB.Models import User
from DB.Extension import db


create_user_args = reqparse.RequestParser()
create_user_args.add_argument("name", type=str, required=True, help="Name is required")
create_user_args.add_argument("email", type=str, required=True, help="Email is required")
create_user_args.add_argument("password", type=str, required=True, help="Password is required")

login_user_args = reqparse.RequestParser()
login_user_args.add_argument("email", type=str, required=True, help="Email is required")
login_user_args.add_argument("password", type=str, required=True, help="Password is required")


userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
}



class Register(Resource):
    @marshal_with(userFields)
    def post(self):
        args = create_user_args.parse_args()

        errors = []

        # Validate email
        if not args["name"] or args["name"].isspace():
            errors.append("Name is required")

        # Validate email
        if not args["email"] or args["email"].isspace():
            errors.append("Email is required")
        else:
            email = args["email"].strip()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Invalid email format")

        # Validate password
        if not args["password"] or args["password"].isspace():
            errors.append("Password is required")
        else:
            password = args["password"].strip()
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            if not any(char.isdigit() for char in password):
                errors.append("Password must contain at least one digit")
            if not any(char.isupper() for char in password):
                errors.append("Password must contain at least one uppercase letter")

        # If errors, send the response
        if errors:
            response = Response(
                json.dumps({"errors": errors}),
                status=400,
                mimetype="application/json",
            )
            return abort(response)

        name = args["name"]
        email = args["email"]
        password = args["password"]

        hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")

        # Verify if the user exists
        if User.query.filter_by(email=email).first():
            return {"message": "User with that email already exists"}, 400

        # Create new user
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return user, 201


class Login(Resource):
    def post(self):
        args = login_user_args.parse_args()

        email = args["email"]
        password = args["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found"}, 404

        if not Bcrypt().check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        accessToken = create_access_token(identity=user.id)

        response_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "accessToken": accessToken
        }

        return response_data, 200
    

class Logout(Resource):
        def post(self):
            return {"message": "Logout successful"}, 200