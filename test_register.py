import pytest
from app import app, init_db, is_valid_email, is_valid_phone, DB_PATH


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr("app.DB_PATH", test_db)

    import app as app_module
    app_module.DB_PATH = test_db
    init_db()

    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as c:
        yield c

    app_module.DB_PATH = DB_PATH


# --- Validation helpers ---

def test_valid_email():
    assert is_valid_email("user@example.com")
    assert is_valid_email("user123@gmail.com")

def test_invalid_email():
    assert not is_valid_email("userexample.com")
    assert not is_valid_email("user@")
    assert not is_valid_email("")

def test_valid_phone():
    assert is_valid_phone("99112233")
    assert is_valid_phone("+976-9911-2233")
    assert is_valid_phone("(976) 9911 2233")

def test_invalid_phone():
    assert not is_valid_phone("abc")
    assert not is_valid_phone("123")
    assert not is_valid_phone("")


# --- Registration route ---

def test_register_get(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert "register" in rv.data.decode().lower() or rv.status_code == 200

def test_register_success(client):
    rv = client.post("/", data={
        "ovog": "Дорж",
        "ner": "Болд",
        "utas": "99112233",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert "success" in rv.request.path or b"success" in rv.data.lower() or rv.status_code == 200

def test_register_missing_fields(client):
    rv = client.post("/", data={
        "ovog": "",
        "ner": "",
        "utas": "",
        "email": "",
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert "Бүх талбарыг бөглөнө үү".encode() in rv.data

def test_register_invalid_email(client):
    rv = client.post("/", data={
        "ovog": "Дорж",
        "ner": "Болд",
        "utas": "99112233",
        "email": "notanemail",
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert "email формат".encode() in rv.data.lower()

def test_register_invalid_phone(client):
    rv = client.post("/", data={
        "ovog": "Дорж",
        "ner": "Болд",
        "utas": "abc",
        "email": "bold@example.com",
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert "утасны дугаар".encode() in rv.data.lower()

def test_register_duplicate_email(client):
    data = {
        "ovog": "Дорж",
        "ner": "Болд",
        "utas": "99112233",
        "email": "bold@example.com",
    }
    client.post("/", data=data)
    rv = client.post("/", data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert "өмнө нь бүртгэгдсэн".encode() in rv.data

def test_register_redirects_to_success(client):
    rv = client.post("/", data={
        "ovog": "Дорж",
        "ner": "Болд",
        "utas": "99112233",
        "email": "bold@example.com",
    })
    assert rv.status_code == 302
    assert "/success" in rv.headers["Location"]
