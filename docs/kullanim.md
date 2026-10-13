# Kullanım Kılavuzu

Bu rehber, Book Rent API’yi bir istemci uygulamaya (web, mobil, Postman) nasıl bağlayacağınızı adım adım anlatır.

## 1. Sunucuyu ayağa kaldırın

Kurulum için [README](../README.md) dosyasına bakın. Kısa hali:

```bash
cd book-rent-api
npm install
npm start
```

Sağlık kontrolü: `POST http://localhost:3000/api/v1/auth/login` yanıt vermelidir. Tanımsız path `404` JSON döner; sunucu ayaktaysa bağlantı hatası almazsınız.

## 2. Kimlik doğrulama akışı

Login hariç her çağrı Bearer token ister.

```text
Login  →  token sakla  →  Authorization header  →  işlemler  →  Logout (token sil)
```

1. `POST /api/v1/auth/login` ile `username` ve `password` gönderin.
2. Yanıttaki `data.token` değerini bellekte (veya güvenli depoda) tutun. Şifreyi saklamayın.
3. Sonraki isteklerde:

   ```http
   Authorization: Bearer <data.token>
   ```

   Postman: Authorization sekmesi → Type: **Bearer Token** → Token kutusuna yapıştırın. Basic Auth kullanmayın.

4. Oturumu kapatmak için `POST /api/v1/auth/logout` çağırın, ardından yerel token’ı silin.

`data.token` JWT’dir (üç parça, nokta ile ayrılır). Logout token’ı bellek içi listeden siler; süre dolunca (`JWT_EXPIRES_IN`, varsayılan 8 saat) veya sunucu restart olunca da geçersiz olur. Yeniden login gerekir.

## 3. JSON istekleri

`POST` ve `PUT` gövdeleri JSON olmalıdır:

```http
Content-Type: application/json
```

Gövde 10 KB ile sınırlıdır (`express.json({ limit: '10kb' })`).

## 4. Frontend entegrasyon örneği (fetch)

```javascript
const API = 'http://localhost:3000/api/v1';

async function login(username, password) {
  const res = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  const json = await res.json();
  if (!json.success) throw new Error(json.message);
  return json.data.token;
}

async function listBooks(token, page = 1, limit = 10) {
  const res = await fetch(`${API}/books?page=${page}&limit=${limit}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

async function rentBook(token, bookId) {
  const res = await fetch(`${API}/rentals`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ bookId }),
  });
  return res.json();
}
```

CORS açıktır (`cors()`); tarayıcıdan `localhost` API’ye istek atılabilir.

## 5. Tipik ekran akışları

**Katalog**

1. Login
2. `GET /books?page=1&limit=10` ile listeleyin
3. Satıra tıklayınca `GET /books/:id`

**Yönetim (CRUD)**

1. Formdan `POST /books` (`name`, `price`, `stock`)
2. Düzenleme: `PUT /books/:id` (sadece değişen alanlar gönderilebilir)
3. Silme: `DELETE /books/:id`

**Kiralama**

1. Listede `stock > 0` olan kitabı seçin
2. `POST /rentals` `{ "bookId": 3 }`
3. Dönen `data.id` kiralama kimliğidir; iade için saklayın
4. `POST /rentals/:id/return`
5. Aynı kiralama tekrar iade edilirse `409` alınır
6. Stok 0 ise `409` `Book is out of stock`

## 6. Hata işleme

Tüm hatalar aynı şemadadır:

```json
{
  "success": false,
  "message": "...",
  "requestId": "..."
}
```

Önerilen istemci davranışı:

| HTTP | Ne yapın |
| ---- | -------- |
| `400` | Form alanlarını `message` ile işaretleyin |
| `401` | Token’ı silin, login ekranına yönlendirin |
| `403` | “Bu kiralama size ait değil” gösterin |
| `404` | Kayıt bulunamadı |
| `409` | Stok yok / zaten iade — kullanıcıya `message` gösterin |
| `5xx` | `requestId` ile loglayın |

`success === false` iken `data` beklemeyin.

## 7. Pagination

Liste yanıtı:

- `data`: o sayfadaki kitaplar
- `page`, `limit`, `total`, `totalPages`

Sonraki sayfa: `page + 1` ve `page <= totalPages`. `limit` en fazla 50’dir; daha büyük değer 50’ye çekilir.

## 8. Veri modeli (istemci)

**Book:** `id` (number), `name` (string), `price` (number), `stock` (number)

**Rental:** `id` (UUID string), `bookId`, `userId`, `rentedAt` (ISO), `returnedAt` (`null` veya ISO)

**User (login yanıtı):** `id`, `username` — şifre dönmez.

Bellek içi API olduğu için başka bir süreç/sunucu aynı veriyi paylaşmaz. Üretimde kalıcı depo yoktur; ödev/demo içindir.

## 9. Seed kitaplar (sunucu ilk açılış)

| id | name | price | stock |
| -- | ---- | ----- | ----- |
| 1 | 1984 | 40 | 3 |
| 2 | Hayvan Çiftliği | 35 | 2 |
| 3 | Suç ve Ceza | 55 | 1 |
| 4 | Sefiller | 70 | 0 |

Endpoint alanları için [API Dokümantasyonu](api.md), senaryolar için [Test Dokümantasyonu](test.md).
