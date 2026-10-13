const express = require('express');
const authController = require('../controllers/auth.controller');
const { auth } = require('../middlewares/auth.middleware');

const router = express.Router();

router.post('/login', authController.login);
router.post('/logout', auth, authController.logout);

module.exports = router;
