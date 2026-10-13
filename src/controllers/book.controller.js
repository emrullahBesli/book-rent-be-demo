const { asyncHandler } = require('../utils/asyncHandler');
const bookService = require('../services/book.service');

const listBooks = asyncHandler(async (req, res) => {
  const result = bookService.listBooks({
    page: req.query.page,
    limit: req.query.limit,
  });
  res.status(200).json({ success: true, ...result });
});

const getBook = asyncHandler(async (req, res) => {
  const book = bookService.getBookById(req.params.id);
  res.status(200).json({ success: true, data: book });
});

const createBook = asyncHandler(async (req, res) => {
  const book = bookService.createBook(req.body);
  res.status(201).json({ success: true, data: book });
});

const updateBook = asyncHandler(async (req, res) => {
  const book = bookService.updateBook(req.params.id, req.body);
  res.status(200).json({ success: true, data: book });
});

const deleteBook = asyncHandler(async (req, res) => {
  bookService.deleteBook(req.params.id);
  res.status(200).json({ success: true, message: 'Book deleted' });
});

module.exports = {
  listBooks,
  getBook,
  createBook,
  updateBook,
  deleteBook,
};
