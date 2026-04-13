def test_health_check_deve_retornar_status_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "walleto-api",
        "version": "1.0.0"
    }