const crypto = require('crypto');
const rentals = require('../models/rental');
const { getBookById } = require('./book.service');
const { AppError } = require('../utils/AppError');

const rentBook = ({ bookId, userId }) => {
  if (bookId === undefined) {
    throw new AppError('bookId is required', 400);
  }

  const book = getBookById(bookId);
  if (book.stock < 1) {
    throw new AppError('Book is out of stock', 409);
  }

  book.stock -= 1;

  const rental = {
    id: crypto.randomUUID(),
    bookId: book.id,
    userId,
    rentedAt: new Date().toISOString(),
    returnedAt: null,
  };
  rentals.push(rental);
  return rental;
};

const returnBook = ({ rentalId, userId }) => {
  const rental = rentals.find((r) => r.id === rentalId);
  if (!rental) {
    throw new AppError('Rental not found', 404);
  }
  if (rental.userId !== userId) {
    throw new AppError('You can only return your own rentals', 403);
  }
  if (rental.returnedAt) {
    throw new AppError('Rental already returned', 409);
  }

  const book = getBookById(rental.bookId);
  book.stock += 1;
  rental.returnedAt = new Date().toISOString();
  return rental;
};

module.exports = { rentBook, returnBook };
