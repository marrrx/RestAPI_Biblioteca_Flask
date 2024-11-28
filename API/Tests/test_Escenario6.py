

#   Un usuario decide devolver el libro, por lo que el encargado deberá eliminar el registro de dicho prestamo.



#    El encargado busca el registro con el id que se le otorgo al usuario cuando realizo su registro.
def test_search_loan(client, new_loan, accessToken):
    loan_id = new_loan["id"]
    response = client.get(
        f"/api/loan/{loan_id}", headers={"Authorization": f"Bearer {accessToken}"}
    )
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "book_id": 1,
        "user_id": 1,
        "loan_date": "2024-11-27 00:00:00",
        "return_date": "2024-12-04 00:00:00",
    }

#    Una vez encontrado procede a eliminarlo.
def test_delete_loan(client, new_loan, accessToken):
    loan_id = new_loan["id"]
    response = client.delete(
        f"/api/loan/delete/{loan_id}", headers={"Authorization": f"Bearer {accessToken}"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Loan deleted successfully"}
