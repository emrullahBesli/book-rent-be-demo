const express = require('express');
const rentalController = require('../controllers/rental.controller');

const router = express.Router();

router.post('/', rentalController.rentBook);
router.post('/:id/return', rentalController.returnBook);

module.exports = router;
