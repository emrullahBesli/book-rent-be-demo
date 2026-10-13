const { asyncHandler } = require('../utils/asyncHandler');
const rentalService = require('../services/rental.service');

const rentBook = asyncHandler(async (req, res) => {
  const rental = rentalService.rentBook({
    bookId: req.body.bookId,
    userId: req.user.id,
  });
  res.status(201).json({ success: true, data: rental });
});

const returnBook = asyncHandler(async (req, res) => {
  const rental = rentalService.returnBook({
    rentalId: req.params.id,
    userId: req.user.id,
  });
  res.status(200).json({ success: true, data: rental });
});

module.exports = { rentBook, returnBook };
