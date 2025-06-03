const express = require('express');
const path = require('path');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Enhanced keyword validation
const validKeywords = new Set([
  'SECURELOCK123',
  'FULLSCREENLOCK',
  'RENDERLOCK2023'
]);

app.post('/validate-keyword', (req, res) => {
  const { keyword } = req.body;
  
  if (!keyword) {
    return res.status(400).json({ valid: false, message: 'Keyword required' });
  }
  
  const isValid = validKeywords.has(keyword.toUpperCase());
  return res.json({ 
    valid: isValid,
    message: isValid ? 'Access granted' : 'Invalid keyword'
  });
});

// Serve frontend
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));