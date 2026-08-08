# AI-Powered Grievance Redressal System - Project Report

## 1. Project Overview & Novelty

### 1.1 Introduction
The **AI-Powered Grievance Redressal System** is a next-generation e-governance solution designed to revolutionize how citizen complaints are handled. Unlike traditional systems that rely on manual data entry and sorting, this platform leverages **Artificial Intelligence (AI)** and **Natural Language Processing (NLP)** to automate the entire lifecycle of a grievance—from submission to resolution.

### 1.2 The Novelty (Innovation)
The core innovation of this project lies in its **intelligent automation pipeline**. Traditional systems are passive; they simply store data. This system is active; it "reads" and "understands" the grievance.

Key novel features include:
*   **Zero-Touch Classification:** The system automatically understands the content of a complaint (e.g., "potholes on main road") and routes it to the correct department (e.g., "Infrastructure") without human intervention.
*   **Smart Priority Detection:** It doesn't just look at *what* the problem is, but *how urgent* it is. By analyzing the emotional tone (sentiment) and scanning for urgency keywords (e.g., "danger", "life-threatening"), it automatically flags critical issues for immediate attention.
*   **Emotional Intelligence:** The system detects the sentiment of the citizen (Angry, Distressed, Hopeful), allowing officials to gauge public mood and respond with appropriate empathy.

---

## 2. Technology Stack

This project is built on a robust, scalable, and modern full-stack architecture.

### 2.1 Frontend (User Interface)
*   **Core Technologies:** HTML5, CSS3, JavaScript (ES6+)
*   **Framework:** Vanilla JavaScript (Lightweight, no heavy framework overhead)
*   **Styling:** Bootstrap 5.3.0 (Responsive, mobile-first design)
*   **Features:**
    *   Real-time dashboard with charts (Chart.js)
    *   Asynchronous data fetching (Fetch API)
    *   Dynamic DOM manipulation for live status updates

### 2.2 Backend (Server & Logic)
*   **Language:** Python 3.9+
*   **Web Framework:** Flask 2.3.3 (Microframework for high performance)
*   **ORM:** SQLAlchemy (Database abstraction layer)
*   **Authentication:** JWT (JSON Web Tokens) for secure, stateless authentication
*   **API Architecture:** RESTful API with CORS support

### 2.3 Database
*   **System:** MySQL (Relational Database Management System)
*   **Schema:** Normalized schema with tables for Users, Petitions, Departments, and Notifications.

### 2.4 AI & Machine Learning Libraries
*   **scikit-learn:** For building and running the classification models.
*   **NLTK (Natural Language Toolkit):** For advanced text processing, tokenization, and VADER sentiment analysis.
*   **NumPy:** For numerical computations and probability calculations.

---

## 3. Deep Dive: AI Concepts & Implementation

The "brain" of the system resides in the `backend/app/nlp` module. Here is a technical breakdown of the AI concepts used:

### 3.1 Text Preprocessing Pipeline
Before any analysis, raw text is cleaned to ensure high accuracy.
*   **Cleaning:** Removal of URLs, emails, special characters, and numbers.
*   **Normalization:** Converting all text to lowercase.
*   **Tokenization:** Breaking text into individual words (tokens) using `nltk.word_tokenize`.
*   **Stopword Removal:** Filtering out common words (and, the, is) that carry little meaning.
*   **Lemmatization:** Reducing words to their base form (e.g., "running" -> "run") using WordNet Lemmatizer to standardize the input.

### 3.2 Automated Department Classification
*   **Algorithm:** **Multinomial Naive Bayes**. This probabilistic classifier is highly effective for text categorization tasks.
*   **Feature Extraction:** **TF-IDF (Term Frequency-Inverse Document Frequency)** Vectorizer.
    *   It converts text into numerical vectors.
    *   It weighs words based on how unique they are to a specific category (e.g., "leakage" is strong for Water Supply, but "salary" is not).
    *   **N-grams:** Uses both unigrams (single words) and bigrams (pairs of words) to capture context (e.g., "not working").
*   **Training:** The model is trained on a curated dataset of grievance examples across 8 categories (Education, Healthcare, Infrastructure, etc.).

### 3.3 Sentiment Analysis & Emotional Intelligence
*   **Model:** **VADER (Valence Aware Dictionary and sEntiment Reasoner)**.
*   **Mechanism:** VADER is a lexicon and rule-based sentiment analysis tool specifically tuned for social media and short texts. It doesn't just count positive/negative words; it understands:
    *   **Intensity:** "extremely bad" is more negative than "bad".
    *   **Negation:** "not good" is negative.
    *   **Punctuation:** "Bad!!!" is more intense than "Bad".
*   **Output:** A compound score ranging from -1 (Most Negative) to +1 (Most Positive).

### 3.4 Intelligent Priority Detection
The system calculates a **Priority Score** using a hybrid logic:
1.  **Sentiment Score:** Highly negative sentiment (indicating anger or distress) increases priority.
2.  **Urgency Keywords:** The system scans for predefined keywords:
    *   *Critical:* "emergency", "danger", "fatal" (+3 points)
    *   *High:* "urgent", "serious", "immediately" (+2 points)
    *   *Medium:* "needed", "request" (+1 point)
3.  **Final Calculation:**
    *   `Priority Score = Sentiment Impact + Urgency Score`
    *   **High Priority:** Score ≥ 4
    *   **Medium Priority:** Score ≥ 2
    *   **Low Priority:** Score < 2

### 3.5 Entity Extraction
*   **Purpose:** To automatically identify key details like locations, dates, and organizations mentioned in the complaint.
*   **Technique:** Uses Named Entity Recognition (NER) to parse specific proper nouns, helping officers quickly identify *where* the problem is occurring without reading the full text.

---

## 4. Conclusion
The AI-Powered Grievance Redressal System represents a significant leap forward in public administration technology. By combining modern web frameworks with sophisticated NLP techniques, it ensures that every citizen's voice is heard, understood, and acted upon with speed and precision.
