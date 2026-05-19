# FINDER

Platform pencarian barang hilang kampus dengan arsitektur clean:

- **Web**: Django Template (`web/`)
- **Mobile API**: Django REST Framework (`api/v1/`)
- **Business logic**: service + selector (`apps/`)
- **Settings modular**: `config/settings/{base,development,production}.py`

## Struktur Inti

```text
apps/
  users/
  reports/
  chats/
  core/
api/v1/
  users/
  reports/
  chats/
web/
  views/
  templates/
config/settings/
requirements/
```

## Menjalankan Project

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
docker compose up -d postgres
python manage.py migrate
python manage.py runserver
```

## Seed Data Dummy

```bash
python manage.py seed_dummy_data --reset
```

Command ini membuat dummy user, report, chat, dan message untuk testing web/API.

## API Endpoints

Semua endpoint API tersedia di `/api/v1/`. Berikut adalah daftar lengkap endpoint yang tersedia:

### Authentication Users (`/api/v1/users/`)

| Method | Endpoint | Deskripsi | Auth | Status Code |
|--------|----------|-----------|------|-------------|
| POST | `register/` | Register user baru dengan email @umkt.ac.id | ❌ | 201 |
| POST | `login/` | Login dan dapatkan token | ❌ | 200 |
| POST | `logout/` | Logout (invalidate token) | ✅ | 204 |
| GET | `me/` | Get informasi user yang sedang login | ✅ | 200 |

### Reports CRUD (`/api/v1/reports/`)

| Method | Endpoint | Deskripsi | Auth | Query Params |
|--------|----------|-----------|------|--------------|
| GET | `` | List semua report dengan filter | ✅ | `status`, `location`, `q` |
| POST | `` | Create report baru | ✅ | - |
| GET | `{report_id}/` | Detail report spesifik | ✅ | - |
| PUT | `{report_id}/` | Update seluruh report (hanya owner) | ✅ | - |
| PATCH | `{report_id}/` | Update sebagian report (hanya owner) | ✅ | - |
| DELETE | `{report_id}/` | Delete report (hanya owner) | ✅ | - |

### Chats (`/api/v1/chats/`)

| Method | Endpoint | Deskripsi | Auth | Status Code |
|--------|----------|-----------|------|-------------|
| POST | `reports/{report_id}/rooms/` | Create atau dapatkan chat room untuk report | ✅ | 201/200 |
| GET | `rooms/{chatroom_id}/messages/` | Get messages (polling) | ✅ | 200 |
| POST | `rooms/{chatroom_id}/messages/` | Send message ke chat room | ✅ | 201 |

---

## Query Parameters & Filters

### Reports List (`GET /api/v1/reports/`)

| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| `status` | string | Filter by status: `LOST`, `FOUND`, `CLAIMED` |
| `location` | string | Filter by location (exact match) |
| `q` | string | Search di title dan description |

**Contoh:**
```
GET /api/v1/reports/?status=LOST&location=Kantin
GET /api/v1/reports/?q=laptop&status=LOST
```

---

## Request/Response Format

### Success Response

**Register / Login:**
```json
{
  "id": 1,
  "email": "user@umkt.ac.id",
  "name": "John Doe",
  "profile_picture": null,
  "token": "a1b2c3d4e5f6g7h8..."
}
```

**Reports List:**
```json
[
  {
    "id": 1,
    "title": "Laptop Hilang",
    "description": "Laptop MacBook Pro warna silver",
    "location": "Kantin",
    "status": "LOST",
    "image": null,
    "user": {"id": 1, "email": "user@umkt.ac.id", "name": "John Doe"},
    "created_at": "2026-05-19T12:00:00Z"
  }
]
```

**Chat Room:**
```json
{
  "id": 1,
  "report": 1,
  "user1": {"id": 1, "email": "user1@umkt.ac.id"},
  "user2": {"id": 2, "email": "user2@umkt.ac.id"},
  "created_at": "2026-05-19T12:00:00Z"
}
```

**Message:**
```json
{
  "id": 1,
  "chatroom": 1,
  "sender": {"id": 1, "email": "user@umkt.ac.id"},
  "message": "Apakah laptop sudah ketemu?",
  "created_at": "2026-05-19T12:05:00Z"
}
```

### Error Response

```json
{
  "detail": "Error message atau validation error"
}
```

**Contoh error:**
```json
{
  "detail": [
    "email: Email harus menggunakan domain @umkt.ac.id"
  ]
}
```

---

## Business Rules

### Chat Expiration
- **0-2 hari**: Bisa kirim & baca pesan
- **2-7 hari**: Hanya bisa baca (readonly)
- **>7 hari**: Chat otomatis dihapus

### Ownership & Access
- User hanya bisa **edit/delete** laporan miliknya
- Chat hanya bisa diakses oleh **2 participant** terkait
- Hanya user yang membuat laporan bisa **menerima chat**

### Email Validation
- Hanya email domain `@umkt.ac.id` yang diterima
- Validasi dilakukan di register, login, dan create account
- Format: `nama@umkt.ac.id`

---

## Testing dengan cURL

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@umkt.ac.id",
    "password": "securepass123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@umkt.ac.id",
    "password": "securepass123"
  }'
# Response: {"id": 1, "email": "...", "token": "abc123..."}
```

### 3. Get Current User (dengan token)
```bash
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Token abc123..."
```

### 4. List Reports
```bash
# Semua reports
curl -X GET http://localhost:8000/api/v1/reports/ \
  -H "Authorization: Token abc123..."

# Filter by status
curl -X GET "http://localhost:8000/api/v1/reports/?status=LOST" \
  -H "Authorization: Token abc123..."

# Search dengan keyword
curl -X GET "http://localhost:8000/api/v1/reports/?q=laptop" \
  -H "Authorization: Token abc123..."

# Filter multiple params
curl -X GET "http://localhost:8000/api/v1/reports/?status=LOST&location=Kantin&q=macbook" \
  -H "Authorization: Token abc123..."
```

### 5. Create Report
```bash
curl -X POST http://localhost:8000/api/v1/reports/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Laptop Hilang",
    "description": "MacBook Pro 14 inch, warna silver",
    "location": "Kantin Utama",
    "status": "LOST"
  }'
```

### 6. Get Report Detail
```bash
curl -X GET http://localhost:8000/api/v1/reports/1/ \
  -H "Authorization: Token abc123..."
```

### 7. Update Report
```bash
# Full update (PUT)
curl -X PUT http://localhost:8000/api/v1/reports/1/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Laptop Ketemu",
    "description": "...",
    "location": "...",
    "status": "FOUND"
  }'

# Partial update (PATCH)
curl -X PATCH http://localhost:8000/api/v1/reports/1/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{"status": "CLAIMED"}'
```

### 8. Delete Report
```bash
curl -X DELETE http://localhost:8000/api/v1/reports/1/ \
  -H "Authorization: Token abc123..."
```

### 9. Create Chat Room
```bash
curl -X POST http://localhost:8000/api/v1/chats/reports/1/rooms/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json"
# Return: 201 jika baru, 200 jika sudah ada
```

### 10. Get Chat Messages (Polling)
```bash
curl -X GET http://localhost:8000/api/v1/chats/rooms/1/messages/ \
  -H "Authorization: Token abc123..."
```

### 11. Send Message
```bash
curl -X POST http://localhost:8000/api/v1/chats/rooms/1/messages/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{"message": "Apakah laptop sudah ketemu?"}'
```

### 12. Logout
```bash
curl -X POST http://localhost:8000/api/v1/users/logout/ \
  -H "Authorization: Token abc123..."
# Response: 204 No Content
```

---

## Status Codes

| Code | Arti | Contoh |
|------|------|--------|
| 200 | OK | Login berhasil, get data berhasil |
| 201 | Created | Register, create report, send message |
| 204 | No Content | Logout, delete berhasil |
| 400 | Bad Request | Validasi gagal (email format salah) |
| 401 | Unauthorized | Token tidak valid/expired |
| 403 | Forbidden | User bukan owner (edit/delete bukan milik) |
| 404 | Not Found | Report/chat tidak ditemukan |
| 500 | Server Error | Error di server |
