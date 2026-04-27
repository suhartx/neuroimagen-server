def test_rejects_invalid_extension(client):
    response = client.post(
        "/studies/upload",
        files={"file": ("study.exe", b"123", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "extensión de archivo no permitida"
