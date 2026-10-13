// app.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const routes = require('./routes');
const { requestId } = require('./middlewares/requestId.middleware');
const { notFound } = require('./middlewares/notFound.middleware');
const { errorHandler } = require('./middlewares/error.middleware');

const app = express();

// --- 1. Temel ve Güvenlik Ara Yazılımları (Middlewares) ---
app.use(helmet()); // HTTP başlıklarını güvenli hale getirir
app.use(cors()); // CORS politikalarını yönetir
app.use(express.json({ limit: '10kb' })); // JSON gövde boyutunu sınırlandırır
app.use(express.urlencoded({ extended: true }));
app.use(requestId);
app.use(morgan('dev')); // HTTP istek loglayıcı

// --- 2. API Rotaları ---
app.use('/api/v1', routes);

// --- 3. Tanımsız Rota ve Hata Yönetimi ---
app.use(notFound);      // Bulunamayan rotalar (404)
app.use(errorHandler);  // Merkezi global hata yakalayıcı

module.exports = app;