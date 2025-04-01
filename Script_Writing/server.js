const express = require("express");
const fs = require("fs").promises; // Using promises for cleaner async/await
const path = require("path");
const cors = require("cors");
const helmet = require("helmet"); // Security middleware
const rateLimit = require("express-rate-limit"); // Brute force protection
const morgan = require("morgan"); // Request logging
const { body, validationResult } = require("express-validator"); // Input validation

const app = express();
const PORT = process.env.PORT || 3000;
const TEXTS_FOLDER = path.join(__dirname, "Story 1", "texts");

// Security and middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:5500" // Adjust as needed
}));
app.use(helmet());
app.use(express.json({ limit: "10kb" })); // Prevent large payloads
app.use(morgan("dev"));

// Rate limiting (100 requests per 15 minutes)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use(limiter);

// Ensure texts directory exists
async function ensureTextsFolder() {
  try {
    await fs.mkdir(TEXTS_FOLDER, { recursive: true });
  } catch (err) {
    console.error("Could not create texts directory:", err);
  }
}

// Sanitize filename to prevent directory traversal
function sanitizeFilename(filename) {
  return filename.replace(/[^a-z0-9\-_.]/gi, "");
}

// Get all text files with metadata
app.get("/files", async (req, res) => {
  try {
    await ensureTextsFolder();
    const files = await fs.readdir(TEXTS_FOLDER);
    
    const textFiles = files.filter(file => file.endsWith(".txt"));
    const filesWithMetadata = await Promise.all(
      textFiles.map(async file => {
        const stats = await fs.stat(path.join(TEXTS_FOLDER, file));
        return {
          name: file,
          size: stats.size,
          lastModified: stats.mtime.toISOString(),
          created: stats.birthtime.toISOString()
        };
      })
    );
    
    res.json(filesWithMetadata);
  } catch (err) {
    console.error("Error listing files:", err);
    res.status(500).json({ error: "Failed to list files" });
  }
});

// Get file content
app.get("/file/:name", [
  // Validate filename
  (req, res, next) => {
    req.params.name = sanitizeFilename(req.params.name);
    if (!req.params.name.endsWith(".txt")) {
      return res.status(400).json({ error: "Only .txt files are supported" });
    }
    next();
  }
], async (req, res) => {
  try {
    const filePath = path.join(TEXTS_FOLDER, req.params.name);
    const content = await fs.readFile(filePath, "utf8");
    const stats = await fs.stat(filePath);
    
    res.json({ 
      content,
      metadata: {
        lastModified: stats.mtime.toISOString(),
        size: stats.size
      }
    });
  } catch (err) {
    if (err.code === "ENOENT") {
      return res.status(404).json({ error: "File not found" });
    }
    console.error("Error reading file:", err);
    res.status(500).json({ error: "Failed to read file" });
  }
});

// Save file content
app.post("/save", [
  // Input validation
  body("filename").isString().notEmpty(),
  body("content").isString()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const filename = sanitizeFilename(req.body.filename);
    if (!filename.endsWith(".txt")) {
      return res.status(400).json({ error: "Only .txt files are supported" });
    }

    const filePath = path.join(TEXTS_FOLDER, filename);
    await fs.writeFile(filePath, req.body.content, "utf8");
    
    // Get updated stats
    const stats = await fs.stat(filePath);
    
    res.json({ 
      success: true,
      metadata: {
        lastModified: stats.mtime.toISOString(),
        size: stats.size
      }
    });
  } catch (err) {
    console.error("Error saving file:", err);
    res.status(500).json({ error: "Failed to save file" });
  }
});

// Create new file
app.post("/files", [
  body("filename").isString().notEmpty()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    let filename = sanitizeFilename(req.body.filename);
    if (!filename.endsWith(".txt")) {
      filename += ".txt";
    }

    const filePath = path.join(TEXTS_FOLDER, filename);
    
    // Check if file exists
    try {
      await fs.access(filePath);
      return res.status(409).json({ error: "File already exists" });
    } catch (err) {
      if (err.code !== "ENOENT") throw err;
    }
    
    // Create empty file
    await fs.writeFile(filePath, "", "utf8");
    const stats = await fs.stat(filePath);
    
    res.status(201).json({
      success: true,
      filename,
      metadata: {
        lastModified: stats.mtime.toISOString(),
        size: stats.size
      }
    });
  } catch (err) {
    console.error("Error creating file:", err);
    res.status(500).json({ error: "Failed to create file" });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Unhandled error:", err);
  res.status(500).json({ error: "Internal server error" });
});

app.listen(PORT, async () => {
  await ensureTextsFolder();
  console.log(`Server running on port ${PORT}`);
  console.log(`Text files directory: ${TEXTS_FOLDER}`);
});