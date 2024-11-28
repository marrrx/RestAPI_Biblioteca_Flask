from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, marshal, reqparse, fields

from DB.Models import Book, Loan, User
from DB.Extension import db


create_loan_args = reqparse.RequestParser()
create_loan_args.add_argument(
    "book_id", type=int, required=True, help="Book is required"
),
create_loan_args.add_argument(
    "loan_date", type=str, required=True, help="Loan date is required"
),
create_loan_args.add_argument(
    "return_date", type=str, required=True, help="Return date is required"
)

loan_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "book_id": fields.Integer,
    "loan_date": fields.String,
    "return_date": fields.String,
}


class createLoan(Resource):
    @jwt_required()
    def post(self):
        session = db.session

        # Obtener el user_id directamente desde el JWT
        user_idd = get_jwt_identity()

        # Obtener los argumentos de la solicitud
        args = create_loan_args.parse_args()

        # Validación de existencia de usuario y libro
        user = session.get(User, user_idd)  # Usamos el user_id del JWT
        if not user:
            return {"message": "User not found"}, 404

        book = session.get(Book, args["book_id"])
        if not book:
            return {"message": "Book not found"}, 404

        # Validación de fechas
        try:
            loan_date = datetime.strptime(args["loan_date"], "%Y-%m-%d")
            return_date = datetime.strptime(args["return_date"], "%Y-%m-%d")
        except ValueError:
            return {"message": "Invalid date format. Please use YYYY-MM-DD."}, 400

        if return_date <= loan_date:
            return {"message": "Return date must be after loan date."}, 400

        # Crear el nuevo préstamo
        loan = Loan(
            user_id=user_idd,
            book_id=args["book_id"],
            loan_date=loan_date,
            return_date=return_date,
        )

        # Guardar el préstamo en la base de datos
        db.session.add(loan)
        db.session.commit()

        return marshal(loan, loan_fields), 201


class readLoans(Resource):
    @jwt_required()
    def get(self):
        loans = Loan.query.all()
        return marshal(loans, loan_fields), 200


class readLoan(Resource):
    @jwt_required()
    def get(self, id):
        session = db.session
        loan = session.get(Loan, id)
        if loan:
            return marshal(loan, loan_fields), 200
        else:
            return {"message": "Loan not found"}, 404


class updateLoan(Resource):
    @jwt_required()
    def post(self, id):

        user_idd = get_jwt_identity()

        loan = Loan.query.get(id)
        if not loan:
            return {"message": "Loan not found"}, 404

        args = create_loan_args.parse_args()
        errors = []

        # Validaciones de campos individuales
        if not args["book_id"]:
            errors.append("Book is required")
        if not args["loan_date"]:
            errors.append("Loan date is required")
        if not args["return_date"]:
            errors.append("Return date is required")

        # Validación de existencia de usuario y libro
        user = User.query.get(user_idd)
        if not user:
            errors.append("Invalid user ID")

        book = Book.query.get(args["book_id"])
        if not book:
            errors.append("Invalid book ID")

        # Validación de fechas
        try:
            loan_date = datetime.strptime(args["loan_date"], "%Y-%m-%d")
            return_date = datetime.strptime(args["return_date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid date format. Please use YYYY-MM-DD.")

        if return_date <= loan_date:
            errors.append("Return date must be after loan date.")

        # Si hay errores, devuelve una respuesta con código 400
        if errors:
            return {"errors": errors}, 400

        # Actualiza los campos del préstamo
        loan.book_id = args["book_id"]
        loan.loan_date = loan_date
        loan.return_date = return_date

        # Guarda los cambios en la base de datos
        db.session.commit()

        return marshal(loan, loan_fields), 200


class deleteLoan(Resource):
    @jwt_required()
    def delete(self, id):
        session = db.session
        loan = session.get(Loan, id)
        if not loan:
            return {"message": "Loan not found"}, 404

        # Elimina el préstamo de la base de datos
        db.session.delete(loan)
        db.session.commit()

        return {"message": "Loan deleted successfully"}, 200
