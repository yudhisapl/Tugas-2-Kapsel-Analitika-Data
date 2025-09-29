import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def make_user(username="userabc", email="user@example.com", role="staff", password="Aa1!aaaa"):
    resp = client.post("/users", json={
        "username": username,
        "email": email,
        "role": role,
        "password": password
    })
    assert resp.status_code == 201, resp.text
    return resp.json()

def test_create_user_success():
    data = make_user(username="userxyz", email="userxyz@example.com", role="staff", password="Abcdef1!")
    assert "id" in data
    assert data["username"] == "userxyz"
    assert "created_at" in data and "updated_at" in data
    assert "password" not in data

def test_validation_username_lowercase_and_length():
    # terlalu pendek
    resp = client.post("/users", json={
        "username": "abc",
        "email": "a@b.com",
        "role": "staff",
        "password": "Abcdef1!"
    })
    assert resp.status_code == 422

    # mengandung huruf kapital
    resp = client.post("/users", json={
        "username": "UserABC",
        "email": "a@b.com",
        "role": "staff",
        "password": "Abcdef1!"
    })
    assert resp.status_code == 422

def test_validation_password_rules():
    # tanpa uppercase
    resp = client.post("/users", json={
        "username": "userlow",
        "email": "u@e.com",
        "role": "staff",
        "password": "abcdef1!"
    })
    assert resp.status_code == 422

    # tanpa special (! atau @)
    resp = client.post("/users", json={
        "username": "userlow2",
        "email": "u2@e.com",
        "role": "staff",
        "password": "Abcdef12"
    })
    assert resp.status_code == 422

    # special tidak valid (#)
    resp = client.post("/users", json={
        "username": "userlow3",
        "email": "u3@e.com",
        "role": "staff",
        "password": "Abcdef1#"
    })
    assert resp.status_code == 422

def test_staff_can_read_self_but_not_others():
    u1 = make_user(username="staffaa", email="s1@e.com", role="staff", password="Aa1!good")
    u2 = make_user(username="staffbb", email="s2@e.com", role="staff", password="Aa1!good")

    # staff membaca dirinya sendiri -> OK
    r = client.get(f"/users/{u1['id']}", headers={"X-Role": "staff", "X-User-Id": u1["id"]})
    assert r.status_code == 200

    # staff membaca user lain -> forbidden
    r = client.get(f"/users/{u2['id']}", headers={"X-Role": "staff", "X-User-Id": u1["id"]})
    assert r.status_code == 403

def test_admin_can_list_update_and_delete():
    u = make_user(username="toadmin", email="adm@e.com", role="staff", password="Aa1!aaaa")

    # list all (admin)
    r = client.get("/users", headers={"X-Role": "admin", "X-User-Id": "admin"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert any(x["id"] == u["id"] for x in r.json())

    # update (admin)
    r = client.patch(
        f"/users/{u['id']}",
        json={"email": "new@e.com"},
        headers={"X-Role": "admin", "X-User-Id": "admin"}
    )
    assert r.status_code == 200
    updated = r.json()
    assert updated["email"] == "new@e.com"

    # delete (admin)
    r = client.delete(f"/users/{u['id']}", headers={"X-Role": "admin", "X-User-Id": "admin"})
    assert r.status_code == 204

    # cek sudah terhapus
    r = client.get(f"/users/{u['id']}", headers={"X-Role": "admin", "X-User-Id": "admin"})
    assert r.status_code == 404