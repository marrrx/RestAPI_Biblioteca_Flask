from flask_jwt_extended import create_access_token
from DB.Extension import db
from DB.Models import Category


def test_create_book_success(client, app):
    # Crear una categoría para asignarla al libro
    with app.app_context():
        category = Category(name="Fiction")
        db.session.add(category)
        db.session.commit()
        access_token = create_access_token(identity={"user_id": 1})

    # Crear un token JWT válido
    headers = {"Authorization": f"Bearer {access_token}"}

    # Datos válidos del libro
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category_id": 1,  # ID de la categoría creada
        "description": "A novel set in the 1920s.",
        "publication_date": "1925-04-10",
    }

    # Enviar solicitud POST para crear un libro
    response = client.post("/api/book/create", json=book_data, headers=headers)

    # Verificaciones
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]