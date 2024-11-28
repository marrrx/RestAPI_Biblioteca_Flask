


#En este escenario, un usuario desea pedir un libro prestado; por lo que deberá de registrarse, loguearse y luego completar el registro para el prestamo, posteriormente el encargado de prestamos verificará dicho registro y otorgará el libro deseado por el usuario.


#  Aqui el usuario realiza su registro.
def test_user_register(client):
    user_data = {"name": "Juan", "email": "test@test.com", "password": "Holaaputa1."}
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201

#   Ahora se loguea, obteniendo su token para poder acceder a rutas protegidas y realizar dicho registro.
def test_user_login(client, new_user):
    user = {"email": new_user["email"], "password": new_user["password"]}
    response = client.post("/api/auth/login", json=user)
    assert response.status_code == 200
    assert "accessToken" in response.json

#   Aqui realiza su registro para el prestamo del libro.
def test_book_request(client, new_book, accessToken):
    loan_data = {
        "book_id": new_book["id"], 
        "loan_date": "2024-11-27",
        "return_date": "2024-12-04",
    }

    response = client.post(
        "/api/loan/create",
        json=loan_data,
        headers={"Authorization": f"Bearer {accessToken}"},
    )
    assert response.status_code == 201
    assert response.json["book_id"] == loan_data["book_id"]


#   Aqui el encargado de prestamos verifica el registro de prestamos verificando que se encuentre el usuario y el libro, otorgando así el libro.
def test_verify_loan(client, accessToken):
        response = client.get(
            "/api/loan",
            headers={"Authorization": f"Bearer {accessToken}"},
        )
        assert response.status_code == 200