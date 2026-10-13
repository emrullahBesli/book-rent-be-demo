# Test Dokümantasyonu

Bu belge Postman (veya curl) ile tekrarlanabilir yazılım test senaryolarını tanımlar. Ekran görüntüleri kanıt olarak bu senaryolara eklenmelidir; her senaryoda beklenen HTTP kodu ve gövde özeti yazılıdır.

**Önkoşul:** `npm start` çalışıyor, taban `http://localhost:3000/api/v1`.  
Sunucu restart edilirse token ve in-memory değişiklikler sıfırlanır; senaryolara login ile başlayın.

**Ortak header (login hariç):** `Authorization: Bearer <token>`

İşaretleme: **P** geçti, **K** kaldı (raporda doldurulur).

---

## T1 — Login başarılı

| | |
| --- | --- |
| Amaç | Geçerli kullanıcı token alır |
| Adımlar | `POST /auth/login` body: `{"username":"admin","password":"admin123"}` |
| Beklenen | `200`, `success: true`, `data.token` JWT (üç noktalı `header.payload.signature`), `data.user.id` = `1`, `data.user.username` = `admin`, şifre dönmez |
| Sonuç | P / K |

---

## T2 — Login hatalı şifre

| | |
| --- | --- |
| Amaç | Yanlış kimlik reddedilir |
| Adımlar | `POST /auth/login` `{"username":"admin","password":"yanlis"}` |
| Beklenen | `401`, `success: false`, `message`: `Invalid credentials`, `requestId` var |
| Sonuç | P / K |

---

## T3 — Login eksik alan

| | |
| --- | --- |
| Amaç | Doğrulama |
| Adımlar | `POST /auth/login` `{"username":"admin"}` |
| Beklenen | `400`, `message`: `username and password are required` |
| Sonuç | P / K |

---

## T4 — Token olmadan korumalı rota

| | |
| --- | --- |
| Amaç | Auth zorunluluğu |
| Adımlar | Header’sız `GET /books` |
| Beklenen | `401`, `message`: `Authorization token is required` |
| Sonuç | P / K |

---

## T5 — Kitap listesi pagination

| | |
| --- | --- |
| Amaç | Sayfalama meta verisi |
| Adımlar | Login → `GET /books?page=1&limit=2` |
| Beklenen | `200`, `data` uzunluğu 2, `page` 1, `limit` 2, `total` 4 (seed değişmediyse), `totalPages` 2 |
| Sonuç | P / K |

**Not:** Önce kitap eklendi/silindiyse `total` değişir. Seed ile test için sunucuyu yeniden başlatın.

---

## T6 — Kitap id ile getir

| | |
| --- | --- |
| Amaç | Tek kayıt |
| Adımlar | `GET /books/1` |
| Beklenen | `200`, `data.id` 1, `data.name` `"1984"` |
| Sonuç | P / K |

---

## T7 — Olmayan kitap

| | |
| --- | --- |
| Amaç | 404 |
| Adımlar | `GET /books/999` |
| Beklenen | `404`, `message`: `Book not found` |
| Sonuç | P / K |

---

## T8 — Kitap ekle

| | |
| --- | --- |
| Amaç | Create `201` |
| Adımlar | `POST /books` `{"name":"Simyacı","price":45,"stock":4}` |
| Beklenen | `201`, `data.name` `"Simyacı"`, `data.price` 45, `data.stock` 4, `data.id` sayı |
| Sonuç | P / K |

---

## T9 — Kitap ekle geçersiz gövde

| | |
| --- | --- |
| Amaç | 400 |
| Adımlar | `POST /books` `{"name":"","price":-1,"stock":4}` |
| Beklenen | `400`, `name is required` veya fiyat/stok mesajı (ilk başarısız doğrulama) |
| Sonuç | P / K |

---

## T10 — Kitap güncelle

| | |
| --- | --- |
| Amaç | PUT kısmi güncelleme |
| Adımlar | T8’deki `id` ile `PUT /books/:id` `{"stock":3}` |
| Beklenen | `200`, `data.stock` 3, diğer alanlar korunur |
| Sonuç | P / K |

---

## T11 — Kitap sil

| | |
| --- | --- |
| Amaç | Delete |
| Adımlar | T8 kaydını `DELETE /books/:id` sonra `GET /books/:id` |
| Beklenen | Silme `200` `Book deleted`; GET `404` `Book not found` |
| Sonuç | P / K |

---

## T12 — Stok yokken kiralama

| | |
| --- | --- |
| Amaç | 409 stok kuralı |
| Adımlar | Seed’de `GET /books/4` (`Sefiller`, stock 0) → `POST /rentals` `{"bookId":4}` |
| Beklenen | `409`, `Book is out of stock` |
| Sonuç | P / K |

---

## T13 — Başarılı kiralama ve stok düşüşü

| | |
| --- | --- |
| Amaç | Stok azalır, rental oluşur |
| Adımlar | `GET /books/3` stoku not edin (seed: 1) → `POST /rentals` `{"bookId":3}` → tekrar `GET /books/3` |
| Beklenen | Kiralama `201`, `data.returnedAt` `null`, `data.userId` login kullanıcısı; kitap `stock` 1 azalır |
| Sonuç | P / K |

`data.id` değerini T14–T16 için saklayın.

---

## T14 — Aynı kitabı stok bitince tekrar kiralama

| | |
| --- | --- |
| Amaç | İkinci kiralama reddi |
| Adımlar | T13’ten sonra stok 0 ise `POST /rentals` `{"bookId":3}` |
| Beklenen | `409` `Book is out of stock` |
| Sonuç | P / K |

---

## T15 — İade ve stok artışı

| | |
| --- | --- |
| Amaç | Return stoku geri verir |
| Adımlar | `POST /rentals/<T13-id>/return` → `GET /books/3` |
| Beklenen | `200`, `returnedAt` ISO tarih; kitap stoku T13 öncesi değere döner |
| Sonuç | P / K |

---

## T16 — Çift iade

| | |
| --- | --- |
| Amaç | Idempotent olmayan iade |
| Adımlar | T15 sonrası aynı URL’ye tekrar `POST .../return` |
| Beklenen | `409` `Rental already returned` |
| Sonuç | P / K |

---

## T17 — Başkasının kiralama kaydını iade

| | |
| --- | --- |
| Amaç | 403 |
| Adımlar | `admin` ile kirala, `emrullah` / `123456` ile login, aynı `rental id` için iade |
| Beklenen | `403` `You can only return your own rentals` |
| Sonuç | P / K |

---

## T18 — Olmayan kiralama iadesi

| | |
| --- | --- |
| Amaç | 404 |
| Adımlar | `POST /rentals/00000000-0000-0000-0000-000000000000/return` |
| Beklenen | `404` `Rental not found` |
| Sonuç | P / K |

---

## T19 — Logout sonrası token iptali

| | |
| --- | --- |
| Amaç | Session silinir |
| Adımlar | Login → `POST /auth/logout` → aynı token ile `GET /books` |
| Beklenen | Logout `200` `Logged out`; liste `401` `Invalid or expired token` |
| Sonuç | P / K |

---

## T20 — Tanımsız rota

| | |
| --- | --- |
| Amaç | Global 404 |
| Adımlar | Token ile `GET /api/v1/unknown` |
| Beklenen | `404`, `message` `Route not found: GET /api/v1/unknown` içerir |
| Sonuç | P / K |

---

## T21 — `bookId` olmadan kiralama

| | |
| --- | --- |
| Amaç | 400 |
| Adımlar | `POST /rentals` `{}` |
| Beklenen | `400` `bookId is required` |
| Sonuç | P / K |

---

## Önerilen test sırası

T1 → T4 → T5 → T6 → T7 → T8 → T10 → T11 → T12 → T13 → T14 → T15 → T16 → T17 → T18 → T19 → T2 → T3 → T9 → T20 → T21

T13–T16 aynı oturum ve aynı kiralama id’sine bağlıdır.

## Kanıt (ekran görüntüsü)

Her senaryo için Postman’de şunları kaydedin:

1. URL, method, (varsa) body
2. Status kodu
3. Response JSON

Dosya adı önerisi: `T13-kirala-201.png`
