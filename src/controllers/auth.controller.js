const { asyncHandler } = require('../utils/asyncHandler');
const authService = require('../services/auth.service');

const login = asyncHandler(async (req, res) => {
  const result = authService.login(req.body);
  res.status(200).json({ success: true, data: result });
});

const logout = asyncHandler(async (req, res) => {
  authService.logout(req.token);
  res.status(200).json({ success: true, message: 'Logged out' });
});

module.exports = { login, logout };
