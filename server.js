import express from "express";
import mysql from "mysql2";
import cors from "cors";
import dotenv from "dotenv";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

const app = express();

app.use(cors());
app.use(express.json());

// Crear conexión a la base de datos
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// Test database connection
pool.getConnection((err, connection) => {
  if (err) {
    console.error("Error connecting to the database:", err);
    return;
  }
  console.log("Successfully connected to database");
  connection.release();
});

// Ruta para guardar el formulario
app.post("/api/submit-form", async (req, res) => {
  let connection;
  try {
    const {
      startupName,
      country,
      city,
      university,
      sdg,
      hpHistory,
      leadSource,
      teamMembers,
    } = req.body;

    console.log("Received form data:", {
      startupName,
      country,
      city,
      university,
      sdg,
      hpHistory,
      leadSource,
      teamMembers,
    });

    // Iniciar transacción
    connection = await pool.promise().getConnection();
    await connection.beginTransaction();
    console.log("Transaction started");

    try {
      // Insertar equipo
      const [teamResult] = await connection.query(
        "INSERT INTO teams (startup_name, country, city, university, sdg, hp_history, lead_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
          startupName,
          country,
          city,
          university,
          sdg,
          JSON.stringify(hpHistory),
          leadSource,
        ]
      );
      console.log("Team inserted with ID:", teamResult.insertId);

      const teamId = teamResult.insertId;

      // Insertar miembros del equipo
      for (const member of teamMembers) {
        console.log("Inserting team member:", member);
        const [result] = await connection.query(
          "INSERT INTO team_members (team_id, member_type, first_name, last_name, email, phone, country, city, university, is_different_university) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
          [
            teamId,
            member.type,
            member.firstName,
            member.lastName,
            member.email,
            member.phone,
            member.country,
            member.city,
            member.university,
            member.isDifferentUniversity,
          ]
        );
        console.log("Team member inserted with ID:", result.insertId);
      }

      await connection.commit();
      console.log("Transaction committed successfully");
      res.json({ success: true, message: "Form submitted successfully" });
    } catch (error) {
      console.error("Error during database operations:", error);
      if (connection) {
        await connection.rollback();
        console.log("Transaction rolled back");
      }
      throw error;
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    res.status(500).json({
      success: false,
      message: "Error submitting form",
      error: error.message,
    });
  } finally {
    if (connection) {
      connection.release();
      console.log("Database connection released");
    }
  }
});

// Add error handling for the server
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: "Something broke!",
    error: err.message,
  });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
