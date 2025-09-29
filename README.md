# Tugas 2 : Pengembangan CRUD API untuk Users Module dengan Validasi Data

## Struktur Folder
```
modules/
└── items/
├── routes/
│ ├── createUser.py
│ ├── readUser.py
│ ├── updateUser.py
│ └── deleteUser.py
├── schema/
│ └── schemas.py
└── tests/
└── test_user.py
.gitignore
main.py
README.MD
```
---

## Persiapan *Environment*

1. **Clone repository (atau download ZIP)**
   ```bash
   git clone https://github.com/<USERNAME>/<REPO>.git

2. **Buat dan aktifkan virtual environment**
    ### Windows PowerShell
    python -m venv .venv
    .venv\Scripts\activate

3. **Menjalankan Server**
    fastapi dev main.py

4. **Akses dokumentasi**
    - Swagger UI → http://127.0.0.1:8000/docs
    - ReDoc → http://127.0.0.1:8000/redoc

## Aturan Akses (Tanpa JWT)

Gunakan header HTTP berikut:

- `X-Role`: `admin` atau `staff`
- `X-User-Id`: id user (untuk staff mengakses data dirinya sendiri)

### Tabel Akses Endpoint

| Endpoint          | Akses                        |
|-------------------|------------------------------|
| `POST /users`     | Public (tanpa header)        |
| `GET /users`      | Admin only                   |
| `GET /users/{id}` | Admin atau staff (hanya self)|
| `PATCH /users/{id}` | Admin only                 |
| `DELETE /users/{id}` | Admin only                |
