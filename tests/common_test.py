def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "Привіт, я твій додаток для контролю витрат!"


def test_not_found(test_client):
    response = test_client.get("/abc")
    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "Ми не змогли знайти це :("
