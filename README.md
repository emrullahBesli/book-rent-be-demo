# Book Rent API

In-memory kitap kiralama REST API’si. Veritabanı yoktur; kullanıcılar, kitaplar ve kiralamalar uygulama belleğinde tutulur. Sunucu yeniden başlatılınca veriler seed haline döner.

## Gereksinimler

- Node.js 18 veya üzeri
- npm

## Kurulum

```bash
git clone <repo-url>
cd book-rent-api
npm install
```

## Ortam değişkenleri

Kök dizinde `.env` dosyası oluşturun (`.env` git’e eklenmez):

```env
PORT=3000
NODE_ENV=dev
JWT_SECRET=book-rent-dev-secret
JWT_EXPIRES_IN=8h
```

| Değişken        | Açıklama                         | Varsayılan              |
| --------------- | -------------------------------- | ----------------------- |
| `PORT`          | HTTP dinleme portu               | `3000`                  |
| `NODE_ENV`      | Ortam adı (log mesajı)           | `dev`                   |
| `JWT_SECRET`    | JWT imza anahtarı                | `book-rent-dev-secret`  |
| `JWT_EXPIRES_IN`| Token süresi (`jsonwebtoken`)    | `8h`                    |

## Çalıştırma

```bash
npm start
```

Başarılı çıktı:

```text
🚀 Sunucu 3000 portunda [dev] modunda çalışıyor.
```

API tabanı: `http://localhost:3000/api/v1`

## Demo kullanıcılar

| Kullanıcı  | Şifre     |
| ---------- | --------- |
| `admin`    | `admin123`|
| `emrullah` | `123456`  |

## Hızlı deneme

```bash
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

Login hariç tüm endpoint’ler `Authorization: Bearer <token>` ister.

## Proje yapısı

```text
src/
  app.js            Express uygulaması, middleware sırası
  server.js         Port dinleme, process hata yakalama
  controllers/      HTTP istek/yanıt
  services/         İş kuralları (in-memory)
  models/           Seed veriler
  routes/           Rota tanımları
  middlewares/      auth, log, 404, error
  utils/            AppError, asyncHandler
```

## Dokümantasyon

- [Proje Tanıtım Dokümanı (PDF)](docs/proje-tanitim.pdf) — amaç, senaryo, sistem özeti
- [API Dokümantasyonu](docs/api.md) — endpoint’ler, request/response örnekleri
- [Kullanım Kılavuzu](docs/kullanim.md) — entegrasyon adımları
- [Test Dokümantasyonu](docs/test.md) — yazılı test senaryoları
