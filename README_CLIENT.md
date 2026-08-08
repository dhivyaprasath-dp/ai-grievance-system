# AI Grievance System - Quick Start Guide

Welcome! This guide will help you set up and run the AI-Powered Grievance System on your computer.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:
1. **Python 3.9 or higher** (Download from [python.org](https://www.python.org/downloads/))
2. **MySQL Server** (Download from [mysql.com](https://dev.mysql.com/downloads/mysql/))

## 🚀 How to Run (Mac/Linux)

1. Open your terminal.
2. Navigate to this project folder.
3. Run the start script:
   ```bash
   ./start_project.sh
   ```
   
   *This script will automatically:*
   - Create a virtual environment
   - Install all required libraries
   - Setup the database
   - Start both the Backend and Frontend servers

4. Once running, open your browser and go to:
   👉 **http://localhost:8000**

## 🔑 Login Credentials

- **Admin Email:** `admin@grievance.gov.in`
- **Password:** `admin123`

## 🛑 How to Stop

Press `CTRL+C` in the terminal window where the script is running.

## ❓ Troubleshooting

**Database Connection Error?**
If you see a database error, you might need to update the database password.
1. Open `backend/.env` file in a text editor.
2. Change `DB_PASS=` to your MySQL root password (e.g., `DB_PASS=yourpassword`).
3. Run `./start_project.sh` again.

**Python not found?**
Ensure Python is added to your system PATH. Try running `python3 --version` in your terminal to verify.

---
*Developed for AI Grievance System Project*
