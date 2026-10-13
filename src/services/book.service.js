const books = require('../models/book');
const { AppError } = require('../utils/AppError');

let nextBookId = books.reduce((max, book) => Math.max(max, book.id), 0) + 1;

const parsePositiveInt = (value, fallback) => {
  const parsed = Number.parseInt(value, 10);
  if (Number.isNaN(parsed) || parsed < 1) {
    return fallback;
  }
  return parsed;
};

const listBooks = ({ page = 1, limit = 10 } = {}) => {
  const currentPage = parsePositiveInt(page, 1);
  let pageSize = parsePositiveInt(limit, 10);
  if (pageSize > 50) {
    pageSize = 50;
  }

  const total = books.length;
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const start = (currentPage - 1) * pageSize;
  const data = books.slice(start, start + pageSize);

  return {
    data,
    page: currentPage,
    limit: pageSize,
    total,
    totalPages,
  };
};

const getBookById = (id) => {
  const bookId = Number(id);
  const book = books.find((b) => b.id === bookId);
  if (!book) {
    throw new AppError('Book not found', 404);
  }
  return book;
};

const createBook = ({ name, price, stock }) => {
  if (!name || typeof name !== 'string' || !name.trim()) {
    throw new AppError('name is required', 400);
  }
  if (price === undefined || Number(price) < 0) {
    throw new AppError('price must be a non-negative number', 400);
  }
  if (stock === undefined || Number(stock) < 0) {
    throw new AppError('stock must be a non-negative integer', 400);
  }

  const book = {
    id: nextBookId++,
    name: name.trim(),
    price: Number(price),
    stock: Number.parseInt(stock, 10),
  };
  books.push(book);
  return book;
};

const updateBook = (id, { name, price, stock }) => {
  const book = getBookById(id);

  if (name !== undefined) {
    if (typeof name !== 'string' || !name.trim()) {
      throw new AppError('name cannot be empty', 400);
    }
    book.name = name.trim();
  }
  if (price !== undefined) {
    if (Number(price) < 0) {
      throw new AppError('price must be a non-negative number', 400);
    }
    book.price = Number(price);
  }
  if (stock !== undefined) {
    if (Number(stock) < 0) {
      throw new AppError('stock must be a non-negative integer', 400);
    }
    book.stock = Number.parseInt(stock, 10);
  }

  return book;
};

const deleteBook = (id) => {
  const book = getBookById(id);
  const index = books.findIndex((b) => b.id === book.id);
  books.splice(index, 1);
  return book;
};

module.exports = {
  listBooks,
  getBookById,
  createBook,
  updateBook,
  deleteBook,
};
