from DB.Extension import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)

    # Relación uno a muchos loans
    loans = db.relationship("Loan", backref="user", lazy=True)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, password={self.password})"


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)

    # Relación uno a muchos books
    books = db.relationship("Book", backref="category", lazy=True)

    def __repr__(self):
        return f"Category(name={self.name})"


class Book(db.Model):
    __tablename__ = "books"  # Nombre de la tabla "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False
    )  # Referencia correcta a la tabla "categories"
    description = db.Column(db.String(120), unique=False, nullable=False)
    publication_date = db.Column(db.String(120), unique=False, nullable=False)
    # Relación uno a muchos loans
    loans = db.relationship("Loan", backref="book", lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, category={self.category.name}, year={self.year})"


class Loan(db.Model):
    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # Corregir referencia
    book_id = db.Column(
        db.Integer, db.ForeignKey("books.id"), nullable=False
    )  # Corregir referencia a "books"
    loan_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Loan(user_id={self.user_id}, book_id={self.book_id}, loan_date={self.loan_date}, return_date={self.return_date})"
