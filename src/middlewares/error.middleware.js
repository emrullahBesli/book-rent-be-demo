const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal server error';

  console.error(`[${req.requestId || '-'}] ${statusCode} ${message}`);
  if (statusCode >= 500) {
    console.error(err.stack);
  }

  res.status(statusCode).json({
    success: false,
    message,
    requestId: req.requestId,
  });
};

module.exports = { errorHandler };
