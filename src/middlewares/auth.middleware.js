const { AppError } = require('../utils/AppError');
const authService = require('../services/auth.service');

const extractToken = (req) => {
  const header = req.headers.authorization;
  if (!header || !header.startsWith('Bearer ')) {
    return null;
  }
  return header.slice(7);
};

const auth = (req, res, next) => {
  const token = extractToken(req);
  if (!token) {
    return next(new AppError('Authorization token is required', 401));
  }

  const user = authService.getUserByToken(token);
  if (!user) {
    return next(new AppError('Invalid or expired token', 401));
  }

  req.token = token;
  req.user = user;
  next();
};

module.exports = { auth };
