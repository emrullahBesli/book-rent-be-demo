// server.js
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const app = require('./app');

const PORT = Number(process.env.PORT) || 3000;
const NODE_ENV = process.env.NODE_ENV || 'dev';

// Sunucu dinlemeye başlar
const server = app.listen(PORT, () => {
    console.log(`🚀 Sunucu ${PORT} portunda [${NODE_ENV}] modunda çalışıyor.`);
});

// Yakalanmamış Promise Reddetmelerini (Unhandled Rejections) Ele Alma
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION! 💥 Sunucu kapatılıyor...');
  console.error(err.name, err.message);
  
  // Mevcut isteklerin bitmesini bekleyip sunucuyu güvenle kapatır
  server.close(() => {
    process.exit(1);
  });
});

// Yakalanmamış İstisnaları (Uncaught Exceptions) Ele Alma
process.on('uncaughtException', (err) => {
  console.error('UNCAUGHT EXCEPTION! 💥 Sunucu kapatılıyor...');
  console.error(err.name, err.message);
  process.exit(1);
});