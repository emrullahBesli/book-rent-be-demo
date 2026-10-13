# API Dokümantasyonu

**Base URL:** `http://localhost:3000/api/v1`

Login dışındaki tüm isteklerde header zorunludur:

```http
Authorization: Bearer <token>
Content-Type: application/json
```

Başarılı yanıtlar `success: true` içerir. Hatalar:

```json
{
  "success": false,
  "message": "Hata açıklaması",
  "requestId": "uuid"
}
```

Her yanıtta `x-request-id` header’ı bulunur.

---

## 1. Login

Kullanıcı adı ve şifre ile oturum açar. `data.token` HS256 JWT’dir (`id`, `username`, `iat`, `exp`). Logout için aynı token bellek içi session’da da tutulur.

| | |
| --- | --- |
| Method | `POST` |
| URL | `http://localhost:3000/api/v1/auth/login` |
| Auth | Yok |

**Request body**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response `200`**

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImlhdCI6MTc0MjQwMDAwMCwiZXhwIjoxNzQyNDI4ODAwfQ.signature",
    "user": {
      "id": 1,
      "username": "admin"
    }
  }
}
```

**Hatalar**

| Durum | HTTP | `message` |
| ----- | ---- | --------- |
| `username` veya `password` yok | `400` | `username and password are required` |
| Yanlış bilgi | `401` | `Invalid credentials` |

---

## 2. Logout

Token’ı geçersiz kılar. Sonraki istekler aynı token ile `401` alır.

| | |
| --- | --- |
| Method | `POST` |
| URL | `http://localhost:3000/api/v1/auth/logout` |
| Auth | Bearer |

**Request body:** yok

**Response `200`**

```json
{
  "success": true,
  "message": "Logged out"
}
```

**Hatalar**

| Durum | HTTP | `message` |
| ----- | ---- | --------- |
| Header yok | `401` | `Authorization token is required` |
| Geçersiz token | `401` | `Invalid or expired token` |

---

## 3. Kitap listesi (pagination)

| | |
| --- | --- |
| Method | `GET` |
| URL | `http://localhost:3000/api/v1/books` |
| Auth | Bearer |

**Query parametreleri**

| Parametre | Varsayılan | Açıklama |
| --------- | ---------- | -------- |
| `page` | `1` | Sayfa numarası (≥ 1) |
| `limit` | `10` | Sayfa boyutu (max `50`) |

**Örnek URL:** `http://localhost:3000/api/v1/books?page=1&limit=2`

**Response `200`**

```json
{
  "success": true,
  "data": [
    { "id": 1, "name": "1984", "price": 40, "stock": 3 },
    { "id": 2, "name": "Hayvan Çiftliği", "price": 35, "stock": 2 }
  ],
  "page": 1,
  "limit": 2,
  "total": 4,
  "totalPages": 2
}
```

---

## 4. Kitap getir (id)

| | |
| --- | --- |
| Method | `GET` |
| URL | `http://localhost:3000/api/v1/books/:id` |
| Auth | Bearer |

**Örnek URL:** `http://localhost:3000/api/v1/books/1`

**Response `200`**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "1984",
    "price": 40,
    "stock": 3
  }
}
```

**Hatalar**

| Durum | HTTP | `message` |
| ----- | ---- | --------- |
| Kayıt yok | `404` | `Book not found` |

---

## 5. Kitap ekle

| | |
| --- | --- |
| Method | `POST` |
| URL | `http://localhost:3000/api/v1/books` |
| Auth | Bearer |

**Request body**

```json
{
  "name": "Simyacı",
  "price": 45,
  "stock": 4
}
```

| Alan | Tip | Zorunlu |
| ---- | --- | ------- |
| `name` | string (boş olamaz) | Evet |
| `price` | sayı ≥ 0 | Evet |
| `stock` | tam sayı ≥ 0 | Evet |

**Response `201`**

```json
{
  "success": true,
  "data": {
    "id": 5,
    "name": "Simyacı",
    "price": 45,
    "stock": 4
  }
}
```

**Hatalar**

| Durum | HTTP | `message` |
| ----- | ---- | --------- |
| İsim yok | `400` | `name is required` |
| Geçersiz fiyat | `400` | `price must be a non-negative number` |
| Geçersiz stok | `400` | `stock must be a non-negative integer` |

---

## 6. Kitap güncelle

Kısmi güncelleme: gönderilen alanlar değişir.

| | |
| --- | --- |
| Method | `PUT` |
| URL | `http://localhost:3000/api/v1/books/:id` |
| Auth | Bearer |

**Örnek URL:** `http://localhost:3000/api/v1/books/1`

**Request body**

```json
{
  "name": "1984",
  "price": 42,
  "stock": 5
}
```

**Response `200`**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "1984",
    "price": 42,
    "stock": 5
  }
}
```

**Hatalar:** kitap yoksa `404` (`Book not found`); geçersiz alanlarda `400`.

---

## 7. Kitap sil

| | |
| --- | --- |
| Method | `DELETE` |
| URL | `http://localhost:3000/api/v1/books/:id` |
| Auth | Bearer |

**Örnek URL:** `http://localhost:3000/api/v1/books/2`

**Response `200`**

```json
{
  "success": true,
  "message": "Book deleted"
}
```

**Hatalar:** `404` `Book not found`

---

## 8. Kitap kirala

Giriş yapan kullanıcı adına kiralama kaydı oluşturur. Kitap stoğu 1 azalır.

| | |
| --- | --- |
| Method | `POST` |
| URL | `http://localhost:3000/api/v1/rentals` |
| Auth | Bearer |

**Request body**

```json
{
  "bookId": 3
}
```

**Response `201`**

```json
{
  "success": true,
  "data": {
    "id": "886f9873-60b2-42fe-9c9c-7a0f00122334",
    "bookId": 3,
    "userId": 1,
    "rentedAt": "2026-09-17T14:23:53.940Z",
    "returnedAt": null
  }
}
```

**Hatalar**

| Durum | HTTP | `message` |
| ----- | ---- | --------- |
| `bookId` yok | `400` | `bookId is required` |
| Kitap yok | `404` | `Book not found` |
| Stok 0 | `409` | `Book is out of stock` |

Seed’de `Sefiller` (`id: 4`) stoğu 0’dır; kiralama `409` döner.

---

## 9. Kitap iade

Yalnızca kiralayan kullanıcı iade edebilir. Stok 1 artar, `returnedAt` set edilir.

| | |
| --- | --- |
| Method | `POST` |
| URL | `http://localhost:3000/api/v1/rentals/:id/return` |
| Auth | Bearer |

**Örnek URL:** `http://localhost:3000/api/v1/rentals/886f9873-60b2-42fe-9c9c-7a0f00122334/return`

**Request body:** yok

**Response `200`**

```json
{
  "success": true,
  "data": {
    "id": "886f9873-60b2-42fe-9c9c-7a0f00122334",
    "bookId": 3,
    "userId": 1,
    "rentedAt": "2026-09-17T14:23:53.940Z",
    "returnedAt": "2026-09-17T14:23:53.962Z"
  }
}
```

**Hatalar**

| Durum | HTTP | `message` |
| ----- | ---- | --------- |
| Kiralama yok | `404` | `Rental not found` |
| Başka kullanıcının kaydı | `403` | `You can only return your own rentals` |
| Zaten iade edilmiş | `409` | `Rental already returned` |

---

## Tanımsız rota

| | |
| --- | --- |
| Method | herhangi |
| URL | tanımlı olmayan path |

**Response `404`**

```json
{
  "success": false,
  "message": "Route not found: GET /api/v1/unknown",
  "requestId": "aa31e65d-7aef-4035-8690-c583c4714325"
}
```

---

## HTTP durum özeti

| Kod | Anlam |
| --- | ----- |
| `200` | Başarılı okuma / güncelleme / silme / logout / iade |
| `201` | Oluşturma (kitap, kiralama) |
| `400` | Doğrulama hatası |
| `401` | Token yok / geçersiz / yanlış şifre |
| `403` | Başkasının kiralama kaydına iade |
| `404` | Kaynak veya rota yok |
| `409` | Stok yok veya tekrar iade |
