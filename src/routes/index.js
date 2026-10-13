const express = require('express');
const authRoutes = require('./auth.routes');
const bookRoutes = require('./book.routes');
const rentalRoutes = require('./rental.routes');
const { auth } = require('../middlewares/auth.middleware');

const router = express.Router();

router.use('/auth', authRoutes);
router.use('/books', auth, bookRoutes);
router.use('/rentals', auth, rentalRoutes);

module.exports = router;
