# FINDER API Documentation

> **Base URL**: `http://localhost:8000/api/v1/`
>
> **API Version**: `v1`

---

## Table of Contents

- [Authentication](#authentication)
- [Error Format](#error-format)
- [Endpoints](#endpoints)
  - [Users](#1-users)
    - [POST /users/google/login/](#11-google-login)
    - [GET /users/me/](#12-get-current-user)
    - [POST /users/logout/](#13-logout)
  - [Reports](#2-reports)
    - [GET /reports/](#21-list-reports)
    - [POST /reports/](#22-create-report)
    - [GET /reports/:id/](#23-get-report-detail)
    - [PUT /reports/:id/](#24-update-report-full)
    - [PATCH /reports/:id/](#25-update-report-partial)
    - [DELETE /reports/:id/](#26-delete-report)
  - [Chats](#3-chats)
    - [GET /chats/rooms/](#31-list-chat-rooms)
    - [POST /chats/reports/:report_id/rooms/](#32-create-chatroom)
    - [GET /chats/rooms/:chatroom_id/messages/](#33-list-messages)
    - [POST /chats/rooms/:chatroom_id/messages/](#34-send-message)
- [Enumerations](#enumerations)

---

## Authentication

This API uses **Token Authentication**. Include the token in the `Authorization` header:

```
Authorization: Token <your_token>
```

Tokens are obtained via the [Google Login](#11-google-login) endpoint. Session-based authentication is also supported for browser clients.

### Permission Levels

| Icon | Meaning |
|------|---------|
| 🔓 | **Public** — No authentication required |
| 🔒 | **Authenticated** — Token required |
| 🔓🔒 | **Read Public / Write Authenticated** — `GET` is public, other methods require token |

---

## Error Format

All error responses follow this structure:

```json
{
    "detail": "Error message string."
}
```

For validation errors:

```json
{
    "field_name": [
        "Validation error message."
    ]
}
```

### Common Error Codes

| Status Code | Meaning |
|-------------|---------|
| `400` | Bad Request — Validation error or invalid input |
| `401` | Unauthorized — Missing or invalid token |
| `403` | Forbidden — You don't have permission for this action |
| `404` | Not Found — Resource does not exist |
| `405` | Method Not Allowed |

---

## Endpoints

---

### 1. Users

---

#### 1.1 Google Login

Authenticate using a Google OAuth2 ID Token. If the user does not exist, a new account will be created automatically. Only `@umkt.ac.id` email domains are accepted.

| | |
|---|---|
| **URL** | `POST /api/v1/users/google/login/` |
| **Auth** | 🔓 Public |
| **Content-Type** | `application/json` |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id_token` | `string` | ✅ | Google OAuth2 ID Token |

**Request Example**

```json
{
    "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response** — `200 OK`

```json
{
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": null
    }
}
```

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `400` | Empty `id_token` | `{"id_token": ["id_token wajib diisi."]}` |
| `400` | Invalid Google token | `["ID token Google tidak valid."]` |
| `400` | Non-`@umkt.ac.id` domain | `["Akun Google harus berasal dari domain umkt.ac.id."]` |
| `400` | Unverified email | `["Email Google belum terverifikasi."]` |
| `400` | OAuth not configured | `["Google OAuth belum dikonfigurasi di server."]` |

---

#### 1.2 Get Current User

Retrieve the profile of the currently authenticated user.

| | |
|---|---|
| **URL** | `GET /api/v1/users/me/` |
| **Auth** | 🔒 Authenticated |

**Request Headers**

```
Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

**Response** — `200 OK`

```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "2411102441250@umkt.ac.id",
    "name": "John Doe",
    "profile_picture": null,
    "statistics": {
        "lost": 2,
        "found": 1,
        "claimed": 3
    }
}
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `uuid` | Unique user identifier |
| `email` | `string` | User's campus email |
| `name` | `string` | Display name |
| `profile_picture` | `string \| null` | URL to profile picture |
| `statistics` | `object` | User's report statistics |
| `statistics.lost` | `int` | Total LOST reports |
| `statistics.found` | `int` | Total FOUND reports |
| `statistics.claimed` | `int` | Total CLAIMED reports |

**Error Responses**

| Status | Condition |
|--------|-----------|
| `401` | Missing or invalid token |

---

#### 1.3 Logout

Logout the current user by deleting their authentication token.

| | |
|---|---|
| **URL** | `POST /api/v1/users/logout/` |
| **Auth** | 🔒 Authenticated |

**Request Headers**

```
Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

**Response** — `204 No Content`

_(Empty body)_

**Error Responses**

| Status | Condition |
|--------|-----------|
| `401` | Missing or invalid token |

---

### 2. Reports

---

#### 2.1 List Reports

Retrieve a list of all reports. Supports optional filters via query parameters.

| | |
|---|---|
| **URL** | `GET /api/v1/reports/` |
| **Auth** | 🔓🔒 Read Public / Write Authenticated |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | `string` | ❌ | Filter by status: `LOST`, `FOUND`, or `CLAIMED` |
| `location` | `string` | ❌ | Filter by location (case-insensitive, partial match) |
| `q` | `string` | ❌ | Search keyword in `title`, `description`, and `location` |

**Request Examples**

```
GET /api/v1/reports/
GET /api/v1/reports/?status=LOST
GET /api/v1/reports/?location=Gedung+B
GET /api/v1/reports/?q=laptop&status=FOUND
```

**Response** — `200 OK`

> **Note**: If the request is made **without authentication**, the `user` field will be `null` to protect reporter privacy.

```json
[
    {
        "id": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "2411102441250@umkt.ac.id",
            "name": "John Doe",
            "profile_picture": "https://lh3.googleusercontent.com/a/example"
        ,
        "title": "Lost my laptop",
        "description": "Black ThinkPad X1 Carbon",
        "location": "Gedung B",
        "image": "https://hgbacpslssmgpniobtys.supabase.co/storage/v1/object/public/images2/example.jpg",
        "status": "LOST",
        "created_at": "2026-06-07T08:27:07.256643+07:00"
    }
]
```

**Response (Anonymous / Not Logged In)**

```json
[
    {
        "id": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
        "user": null,
        "title": "Lost my laptop",
        "description": "Black ThinkPad X1 Carbon",
        "location": "Gedung B",
        "image": "https://hgbacpslssmgpniobtys.supabase.co/storage/v1/object/public/images2/example.jpg",
        "status": "LOST",
        "created_at": "2026-06-07T08:27:07.256643+07:00"
    }
]
```

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `uuid` | Unique report identifier |
| `user` | `object \| null` | Report owner info (`null` if not authenticated) |
| `user.id` | `uuid` | Owner's user ID |
| `user.email` | `string` | Owner's email |
| `user.name` | `string` | Owner's display name |
| `user.profile_picture` | `string \| null` | Owner's profile picture URL |
| `title` | `string` | Report title (max 180 chars) |
| `description` | `string` | Detailed description |
| `location` | `string` | Location of lost/found item (max 255 chars) |
| `image` | `string \| null` | URL to uploaded image on Supabase Storage |
| `status` | `string` | Report status: `LOST`, `FOUND`, or `CLAIMED` |
| `created_at` | `datetime` | ISO 8601 timestamp |

---

#### 2.2 Create Report

Create a new lost/found report. Requires authentication.

| | |
|---|---|
| **URL** | `POST /api/v1/reports/` |
| **Auth** | 🔒 Authenticated |
| **Content-Type** | `multipart/form-data` |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | ✅ | Report title (max 180 characters) |
| `description` | `string` | ✅ | Detailed description |
| `location` | `string` | ✅ | Location of the item (max 255 characters) |
| `image` | `file` | ❌ | Image file (JPG, JPEG, or PNG, max 5MB) |
| `status` | `string` | ❌ | Report status. Default: `LOST`. Options: `LOST`, `FOUND`, `CLAIMED` |

**Request Example (cURL)**

```bash
curl -X POST http://localhost:8000/api/v1/reports/ \
  -H "Authorization: Token a1b2c3d4..." \
  -F "title=Lost my laptop" \
  -F "description=Black ThinkPad X1 Carbon" \
  -F "location=Gedung B" \
  -F "image=@/path/to/photo.jpg"
```

**Response** — `201 Created`

```json
{
    "id": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "title": "Lost my laptop",
    "description": "Black ThinkPad X1 Carbon",
    "location": "Gedung B",
    "image": "https://hgbacpslssmgpniobtys.supabase.co/storage/v1/object/public/images2/uuid.jpg",
    "status": "LOST",
    "created_at": "2026-06-07T08:27:07.256643+07:00"
}
```

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `400` | Missing required field | `{"title": ["This field is required."]}` |
| `400` | Image exceeds 5MB | `{"image": ["Ukuran file gambar tidak boleh melebihi 5MB."]}` |
| `400` | Invalid image format | `{"image": ["Format gambar harus berupa JPG, JPEG, atau PNG."]}` |
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |

---

#### 2.3 Get Report Detail

Retrieve a single report by its UUID.

| | |
|---|---|
| **URL** | `GET /api/v1/reports/<uuid:report_id>/` |
| **Auth** | 🔓🔒 Read Public / Write Authenticated |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | `uuid` | The UUID of the report |

**Request Example**

```
GET /api/v1/reports/c40314c2-85cd-4eb4-b526-688257e7c9f9/
```

**Response** — `200 OK`

```json
{
    "id": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "title": "Lost my laptop",
    "description": "Black ThinkPad X1 Carbon",
    "location": "Gedung B",
    "image": "https://hgbacpslssmgpniobtys.supabase.co/storage/v1/object/public/images2/example.jpg",
    "status": "LOST",
    "created_at": "2026-06-07T08:27:07.256643+07:00"
}
```

> **Note**: `user` will be `null` when the request is made without authentication.

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `404` | Report not found | `{"detail": "Laporan tidak ditemukan."}` |

---

#### 2.4 Update Report (Full)

Fully update a report. All writable fields must be provided. Only the **report owner** can perform this action.

| | |
|---|---|
| **URL** | `PUT /api/v1/reports/<uuid:report_id>/` |
| **Auth** | 🔒 Authenticated (owner only) |
| **Content-Type** | `multipart/form-data` |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | `uuid` | The UUID of the report |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | ✅ | Report title (max 180 characters) |
| `description` | `string` | ✅ | Detailed description |
| `location` | `string` | ✅ | Location of the item (max 255 characters) |
| `image` | `file` | ❌ | New image file (JPG, JPEG, or PNG, max 5MB) |
| `status` | `string` | ❌ | Report status: `LOST`, `FOUND`, or `CLAIMED` |

**Response** — `200 OK`

```json
{
    "id": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "title": "Updated Title",
    "description": "Updated description",
    "location": "Gedung C",
    "image": "https://hgbacpslssmgpniobtys.supabase.co/storage/v1/object/public/images2/new-uuid.jpg",
    "status": "FOUND",
    "created_at": "2026-06-07T08:27:07.256643+07:00"
}
```

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `400` | Validation error | `{"title": ["This field is required."]}` |
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Not the owner | `{"detail": "Hanya pemilik laporan yang bisa mengubah data."}` |
| `404` | Report not found | `{"detail": "Laporan tidak ditemukan."}` |

---

#### 2.5 Update Report (Partial)

Partially update a report. Only the provided fields will be updated. Only the **report owner** can perform this action.

| | |
|---|---|
| **URL** | `PATCH /api/v1/reports/<uuid:report_id>/` |
| **Auth** | 🔒 Authenticated (owner only) |
| **Content-Type** | `multipart/form-data` or `application/json` |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | `uuid` | The UUID of the report |

**Request Body** _(all fields optional)_

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | ❌ | Report title (max 180 characters) |
| `description` | `string` | ❌ | Detailed description |
| `location` | `string` | ❌ | Location of the item (max 255 characters) |
| `image` | `file` | ❌ | New image file (JPG, JPEG, or PNG, max 5MB) |
| `status` | `string` | ❌ | Report status: `LOST`, `FOUND`, or `CLAIMED` |

**Request Example (JSON)**

```json
{
    "status": "CLAIMED"
}
```

**Response** — `200 OK`

```json
{
    "id": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
    "user": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "title": "Lost my laptop",
    "description": "Black ThinkPad X1 Carbon",
    "location": "Gedung B",
    "image": "https://hgbacpslssmgpniobtys.supabase.co/storage/v1/object/public/images2/example.jpg",
    "status": "CLAIMED",
    "created_at": "2026-06-07T08:27:07.256643+07:00"
}
```

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Not the owner | `{"detail": "Hanya pemilik laporan yang bisa mengubah data."}` |
| `404` | Report not found | `{"detail": "Laporan tidak ditemukan."}` |

---

#### 2.6 Delete Report

Delete a report. Only the **report owner** can perform this action.

| | |
|---|---|
| **URL** | `DELETE /api/v1/reports/<uuid:report_id>/` |
| **Auth** | 🔒 Authenticated (owner only) |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | `uuid` | The UUID of the report |

**Response** — `204 No Content`

_(Empty body)_

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Not the owner | `{"detail": "Hanya pemilik laporan yang bisa mengubah data."}` |
| `404` | Report not found | `{"detail": "Laporan tidak ditemukan."}` |

---

### 3. Chats

The chat system allows users to communicate about reports. Key business rules:

- **Only non-owners** can initiate a chat on a report (the report owner cannot chat with themselves).
- **Chat room expiration**: Chat rooms are automatically deleted after **7 days**.
- **Read-only after 2 days**: Messages can only be sent within the first **2 days** after the chat room is created. After that, the chat becomes read-only.
- **Participant-only access**: Only `user1` (report owner) and `user2` (initiator) can access a chat room.

---

#### 3.1 List Chat Rooms

Retrieve all chat rooms for the currently authenticated user. The rooms are ordered by the most recent message (`last_message_at`) descending, or by creation date if no messages exist. The response includes the `last_message` if available.

| | |
|---|---|
| **URL** | `GET /api/v1/chats/rooms/` |
| **Auth** | 🔒 Authenticated |

**Response** — `200 OK`

```json
[
    {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "report": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
        "user1": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "2411102441250@umkt.ac.id",
            "name": "John Doe",
            "profile_picture": "https://lh3.googleusercontent.com/a/example"
        },
        "user2": {
            "id": "660f9500-f39c-52e5-b827-557766550001",
            "email": "2411102441251@umkt.ac.id",
            "name": "Jane Smith",
            "profile_picture": "https://lh3.googleusercontent.com/a/example"
        },
        "created_at": "2026-06-07T10:00:00.000000+07:00",
        "last_message": {
            "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
            "chatroom": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "sender": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "2411102441250@umkt.ac.id",
                "name": "John Doe",
                "profile_picture": "https://lh3.googleusercontent.com/a/example"
            },
            "message": "Halo, saya menemukan laptop Anda.",
            "created_at": "2026-06-07T10:05:00.000000+07:00"
        }
    }
]
```

**Response Fields (per chat room)**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `uuid` | Unique chat room identifier |
| `report` | `uuid` | ID of the associated report |
| `user1` | `object` | Report owner info |
| `user1.profile_picture` | `string \| null` | Owner's profile picture URL |
| `user2` | `object` | Chat initiator info |
| `user2.profile_picture` | `string \| null` | Initiator's profile picture URL |
| `created_at` | `datetime` | ISO 8601 timestamp |
| `last_message` | `object \| null` | The most recent message object, if any |
| `last_message.message` | `string` | Content of the last message |

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |

---

#### 3.2 Create ChatRoom

Create or retrieve a chat room for a specific report. If a chat room already exists between the authenticated user and the report owner, the existing room is returned.

| | |
|---|---|
| **URL** | `POST /api/v1/chats/reports/<uuid:report_id>/rooms/` |
| **Auth** | 🔒 Authenticated |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `report_id` | `uuid` | The UUID of the report to chat about |

**Request Body**

_(No body required)_

**Response — `201 Created`** _(new chat room created)_

```json
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "report": "c40314c2-85cd-4eb4-b526-688257e7c9f9",
    "user1": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "user2": {
        "id": "660f9500-f39c-52e5-b827-557766550001",
        "email": "2411102441251@umkt.ac.id",
        "name": "Jane Smith",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "created_at": "2026-06-07T10:00:00.000000+07:00"
}
```

**Response — `200 OK`** _(existing chat room returned)_

_(Same structure as above)_

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `uuid` | Unique chat room identifier |
| `report` | `uuid` | ID of the associated report |
| `user1` | `object` | Report owner info |
| `user1.id` | `uuid` | Owner's user ID |
| `user1.email` | `string` | Owner's email |
| `user1.name` | `string` | Owner's display name |
| `user1.profile_picture` | `string \| null` | Owner's profile picture URL |
| `user2` | `object` | Chat initiator info |
| `user2.id` | `uuid` | Initiator's user ID |
| `user2.email` | `string` | Initiator's email |
| `user2.name` | `string` | Initiator's display name |
| `user2.profile_picture` | `string \| null` | Initiator's profile picture URL |
| `created_at` | `datetime` | ISO 8601 timestamp |

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `400` | Owner tries to chat with self | `["Pemilik laporan tidak bisa chat dengan dirinya sendiri."]` |
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |
| `404` | Report not found | `{"detail": "Laporan tidak ditemukan."}` |

---

#### 3.3 List Messages

Retrieve all messages in a chat room. Only participants can access messages.

| | |
|---|---|
| **URL** | `GET /api/v1/chats/rooms/<uuid:chatroom_id>/messages/` |
| **Auth** | 🔒 Authenticated (participant only) |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `chatroom_id` | `uuid` | The ID of the chat room |

**Response** — `200 OK`

```json
[
    {
        "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
        "chatroom": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "sender": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "2411102441250@umkt.ac.id",
            "name": "John Doe",
            "profile_picture": "https://lh3.googleusercontent.com/a/example"
        ,
        "message": "Halo, saya menemukan laptop Anda.",
        "created_at": "2026-06-07T10:05:00.000000+07:00"
    },
    {
        "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "chatroom": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "sender": {
            "id": "660f9500-f39c-52e5-b827-557766550001",
            "email": "2411102441251@umkt.ac.id",
            "name": "Jane Smith",
            "profile_picture": "https://lh3.googleusercontent.com/a/example"
        ,
        "message": "Terima kasih! Bisa ketemu dimana?",
        "created_at": "2026-06-07T10:06:00.000000+07:00"
    }
]
```

**Response Fields (per message)**

| Field | Type | Description |
|-------|------|-------------|
| `id` | `uuid` | Unique message identifier |
| `chatroom` | `uuid` | ID of the chat room |
| `sender` | `object` | Sender info |
| `sender.id` | `uuid` | Sender's user ID |
| `sender.email` | `string` | Sender's email |
| `sender.name` | `string` | Sender's display name |
| `sender.profile_picture` | `string \| null` | Sender's profile picture URL |
| `message` | `string` | Message content |
| `created_at` | `datetime` | ISO 8601 timestamp |

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `400` | Chat expired and deleted | `["Chat sudah kedaluwarsa dan dihapus."]` |
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Not a participant | `{"detail": "Hanya participant chat yang bisa mengakses chat."}` |
| `404` | Chat room not found | `{"detail": "Chat tidak ditemukan atau sudah kedaluwarsa."}` |

---

#### 3.4 Send Message

Send a new message in a chat room. Only participants can send messages, and only within the first 2 days of the chat room's creation.

| | |
|---|---|
| **URL** | `POST /api/v1/chats/rooms/<uuid:chatroom_id>/messages/` |
| **Auth** | 🔒 Authenticated (participant only) |
| **Content-Type** | `application/json` |

**Path Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `chatroom_id` | `uuid` | The ID of the chat room |

**Request Body**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | `string` | ✅ | The message content (cannot be empty or whitespace-only) |

**Request Example**

```json
{
    "message": "Halo, saya menemukan laptop Anda."
}
```

**Response** — `201 Created`

```json
{
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "chatroom": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "sender": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "2411102441250@umkt.ac.id",
        "name": "John Doe",
        "profile_picture": "https://lh3.googleusercontent.com/a/example"
    ,
    "message": "Halo, saya menemukan laptop Anda.",
    "created_at": "2026-06-07T10:05:00.000000+07:00"
}
```

**Error Responses**

| Status | Condition | Example |
|--------|-----------|---------|
| `400` | Empty message | `["Pesan tidak boleh kosong."]` |
| `400` | Chat expired and deleted | `["Chat sudah kedaluwarsa dan dihapus."]` |
| `400` | Chat is read-only (>2 days) | `{"detail": "Chat sudah readonly setelah 2 hari."}` |
| `401` | Not authenticated | `{"detail": "Authentication credentials were not provided."}` |
| `403` | Not a participant | `{"detail": "Hanya participant chat yang bisa mengakses chat."}` |
| `404` | Chat room not found | `{"detail": "Chat tidak ditemukan atau sudah kedaluwarsa."}` |

---

## Enumerations

### ReportStatus

| Value | Display Name (ID) | Description |
|-------|-------------------|-------------|
| `LOST` | Hilang | Item is lost |
| `FOUND` | Menemukan | Item has been found |
| `CLAIMED` | Selesai | Item has been returned to owner |

---

## Quick Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/v1/users/google/login/` | 🔓 | Login with Google |
| `GET` | `/api/v1/users/me/` | 🔒 | Get current user profile |
| `POST` | `/api/v1/users/logout/` | 🔒 | Logout (delete token) |
| `GET` | `/api/v1/reports/` | 🔓 | List all reports |
| `POST` | `/api/v1/reports/` | 🔒 | Create a new report |
| `GET` | `/api/v1/reports/:id/` | 🔓 | Get report detail |
| `PUT` | `/api/v1/reports/:id/` | 🔒 | Full update report (owner) |
| `PATCH` | `/api/v1/reports/:id/` | 🔒 | Partial update report (owner) |
| `DELETE` | `/api/v1/reports/:id/` | 🔒 | Delete report (owner) |
| `GET` | `/api/v1/chats/rooms/` | 🔒 | List all chat rooms |
| `POST` | `/api/v1/chats/reports/:id/rooms/` | 🔒 | Create/get chat room |
| `GET` | `/api/v1/chats/rooms/:id/messages/` | 🔒 | List chat messages |
| `POST` | `/api/v1/chats/rooms/:id/messages/` | 🔒 | Send a message |
