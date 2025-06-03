const express = require('express');
const path = require('path');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Simple keyword check
app.post('/check-keyword', (req, res) => {
  const { keyword } = req.body;
  const validKeywords = ['secret123', 'password', 'open'];
  
  if (validKeywords.includes(keyword.toLowerCase())) {
    res.json({ success: true });
  } else {
    res.json({ success: false });
  }
});

// Serve frontend
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));