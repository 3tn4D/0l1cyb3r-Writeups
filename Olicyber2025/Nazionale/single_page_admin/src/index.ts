import assert from "assert";
import express from "express";
import dbPromise from "./database.js";
import type { Database } from "sqlite";
import crypto from "crypto";

function isString(value: unknown): value is string {
  return !!value && typeof value === "string";
}

declare global {
  namespace Express {
    interface Request {
      db: Database;
    }
  }
}

const app = express();

app.use(express.json());
app.set("view engine", "ejs");
app.use(express.static("static"));

app.use(async (req, res, next) => {
  try {
    req.db = await dbPromise;

    await req.db.run(`CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
	  username VARCHAR(255) UNIQUE NOT NULL,
	  password VARCHAR(255) NOT NULL,
	  is_admin BOOLEAN NOT NULL DEFAULT 0
    );`);

    await req.db.run(`CREATE TABLE IF NOT EXISTS token (
		token VARCHAR(255) PRIMARY KEY,
		user_id INT NOT NULL,
		FOREIGN KEY (user_id) REFERENCES users(id)
	);`);
    next();
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Database connection failed" });
  }
});

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/api/register", async (req, res) => {
  assert(isString(req.body.username), "Username is required");

  const password = crypto.randomUUID();
  try {
    await req.db.run(
      `INSERT INTO users (id, username, password) VALUES (NULL, ?, ?)`,
      [req.body.username, password],
    );

    const data = await req.db.get(`SELECT * FROM users WHERE username = ?`, [
      req.body.username,
    ]);

    const token = crypto.randomUUID();
    await req.db.run(`INSERT INTO token (token, user_id) VALUES (?, ?)`, [
      token,
      data.id,
    ]);

    res.send({
      password,
      token,
      is_admin: data.is_admin,
    });
    return;
  } catch (err) {
    if ((err as any).code === "SQLITE_CONSTRAINT") {
      res.status(400).json({ error: "Username already exists" });
      return;
    }
    res.status(500).json({ error: "Database error" });
    console.error(err);
    return;
  }
});

app.post("/api/login", async (req, res) => {
  assert(isString(req.body.username), "Username is required");
  assert(isString(req.body.password), "Password is required");

  try {
    const data = await req.db.get(
      `SELECT * FROM users WHERE username = ? AND password = ?`,
      [req.body.username, req.body.password],
    );

    if (!data) {
      res.status(401).json({ error: "Invalid username or password" });
      return;
    }

    const token = crypto.randomUUID();
    await req.db.run(`INSERT INTO token (token, user_id) VALUES (?, ?)`, [
      token,
      data.id,
    ]);

    res.send({
      token,
      is_admin: data.is_admin,
    });
    return;
  } catch (err) {
    res.status(500).json({ error: "Database error" });
    console.error(err);
    return;
  }
});

app.use((req, res, next) => {
  const authHeader = req.headers["authorization"];
  if (!authHeader) {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }
  const token = authHeader.split(" ")[1];
  if (!token) {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }
  if (!isString(token)) {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }
  req.db
    .get(`SELECT * FROM token WHERE token = ?`, [token])
    .then((data) => {
      if (!data) {
        res.status(401).json({ error: "Unauthorized" });
        return;
      }
      next();
    })
    .catch((err) => {
      res.status(500).json({ error: "Database error" });
      console.error(err);
    });
});

app.post("/api/admin", async (req, res) => {
  res.send({ message: process.env.FLAG || "flag{REDACTED}" });
});

app.listen(3000, "0.0.0.0", () => {
  console.log("Server is running on http://localhost:3000");
});
