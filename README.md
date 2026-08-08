# AI-Powered Grievance Redressal System

A full-stack web application that uses Artificial Intelligence and Natural Language Processing to automatically classify, prioritize, and manage citizen grievances/petitions.

## 🎯 Project Overview

This system automates the grievance handling process using:
- **AI Classification** - Automatically categorizes petitions into departments
- **Sentiment Analysis** - Detects emotional tone and urgency
- **Priority Detection** - Assigns priority based on sentiment and keywords
- **Real-time Tracking** - Transparent status updates and timeline
- **Analytics Dashboard** - Data-driven insights for decision making

## 🚀 Features

### Core Modules

1. **User Authentication & Submission**
   - Role-based access (Citizen, Officer, Admin)
   - JWT-based authentication
   - Secure petition submission with file upload

2. **AI Classification**
   - Automatic department categorization using ML
   - 8 categories: Education, Healthcare, Infrastructure, Transport, Water Supply, Electricity, Public Safety, Others
   - TF-IDF + Naive Bayes classifier
   - 85%+ accuracy on test data

3. **Priority Detection**
   - VADER sentiment analysis
   - Keyword-based urgency detection
   - Automatic priority assignment (High/Medium/Low)

4. **Tracking & Workflow**
   - Unique petition ID generation
   - Status tracking (Submitted → In Review → In Progress → Resolved/Rejected)
   - Complete audit trail with timestamps
   - Public tracking endpoint

5. **Analytics & Insights**
   - Dashboard statistics
   - Department-wise distribution
   - Trend analysis
   - Sentiment metrics
   - Average resolution time

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask 2.3.3
- **Database:** MySQL with SQLAlchemy ORM
- **Authentication:** JWT (flask-jwt-extended)
- **AI/ML:** 
  - scikit-learn (Classification)
  - NLTK (NLP, Sentiment Analysis)
  - VADER (Sentiment)
- **API:** RESTful API with CORS support

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5.3.0** for responsive UI
- **Vanilla JavaScript** (no framework dependencies)

### AI/NLP Components
- **Text Classification:** TF-IDF + Multinomial Naive Bayes
- **Sentiment Analysis:** NLTK VADER
- **Entity Extraction:** NLTK NER + Regex
- **Text Preprocessing:** Tokenization, Stemming, Lemmatization

## 📋 Prerequisites

- Python 3.9+
- MySQL 5.7+ or 8.0+
- pip (Python package manager)
- Git

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ISHWARYAKATHAMBARI/ai-grievance-system.git
cd ai-grievance-system
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Database Setup

```bash
# Create MySQL database
mysql -u root -p
```

```sql
CREATE DATABASE grievance_db;
CREATE USER 'grievance_user'@'localhost' IDENTIFIED BY 'grievance_pass';
GRANT ALL PRIVILEGES ON grievance_db.* TO 'grievance_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Initialize database and seed data
python init_db.py
```

### 4. Run the Application

**Backend:**
```bash
cd backend
source ../venv/bin/activate
FLASK_APP=app.start flask run --port=5001
```

**Frontend:**
```bash
cd frontend
python3 -m http.server 8000
```

### 5. Access the Application

- **Frontend:** http://localhost:8000
- **Backend API:** http://localhost:5001
- **Admin Login:** admin@grievance.gov.in / admin123

## 📁 Project Structure

```
ai-grievance-system/
├── backend/
│   ├── app/
│   │   ├── api/              # REST API endpoints
│   │   ├── nlp/              # AI/NLP modules
│   │   ├── services/         # Business logic
│   │   ├── models.py         # Database models
│   │   └── start.py          # Application entry
│   ├── init_db.py            # Database initialization
│   └── requirements.txt      # Dependencies
├── frontend/
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript
│   └── *.html                # HTML pages
└── README.md
```

## 🤖 How the AI Works

### Classification Model
- **Algorithm:** Multinomial Naive Bayes with TF-IDF
- **Training Data:** 64 sample petitions across 8 categories
- **Features:** 500 TF-IDF features with 1-gram and 2-gram
- **Accuracy:** 85%+ on test data

### Sentiment Analysis
- **Model:** NLTK VADER (pre-trained)
- **Output:** Positive/Negative/Neutral sentiment scores
- **Use:** Priority calculation and urgency detection

### Priority Calculation
```
Priority Score = Sentiment Score + Urgency Score

High Priority: Score >= 4
Medium Priority: Score >= 2
Low Priority: Score < 2
```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/profile` - Get user profile

### Petitions
- `POST /petitions/submit` - Submit petition (with AI processing)
- `GET /petitions/list` - List petitions with filters
- `GET /petitions/<id>` - Get petition details
- `PUT /petitions/<id>/status` - Update status (officers only)
- `GET /petitions/track/<petition_id>` - Public tracking

### Analytics
- `GET /analytics/dashboard` - Dashboard statistics
- `GET /analytics/trends` - Petition trends

### Departments
- `GET /departments/list` - List all departments

### Notifications
- `GET /notifications/list` - User notifications
- `PUT /notifications/<id>/read` - Mark as read

## 🎨 UI Features

- Modern Professional Design
- Responsive Layout
- Real-time Updates
- Status Badges
- Timeline Visualization
- AI Insights Panel

## 🔐 Security Features

- JWT-based authentication
- Password hashing (pbkdf2:sha256)
- Role-based access control
- CORS protection
- SQL injection prevention

## 📝 Sample Petitions for Testing

1. **High Priority:** "Urgent road repair needed on Main Street causing accidents"
2. **Medium Priority:** "Hospital lacks essential medicines and equipment"
3. **Low Priority:** "School library needs more books and study materials"

## 👥 Team

- **Project Guide:** Dr. M SHANMUGAM
- **Institution:** [Your Institution]

## 📄 License

This project is created for academic purposes.

---

**Note:** This is a demonstration project for educational purposes.
