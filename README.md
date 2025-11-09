# WeMech: Your Comprehensive Automotive Solution

![WeMech Logo](https://img.shields.io/badge/WeMech-Automotive%20Solution-blue?style=for-the-badge)

A comprehensive web and desktop application designed to revolutionize the car ownership experience by providing maintenance tracking, parts sourcing, community support, and professional guidance all in one platform.

## 🚗 Overview

WeMech addresses the challenges faced by car owners in maintaining and repairing their vehicles by providing a centralized digital platform. The system eliminates the need for manual record-keeping and fragmented service searching, offering a streamlined solution for all automotive needs.

## 🎯 Problem Statement

Despite widespread car ownership, many drivers struggle with:
- Limited access to reliable automotive information and services
- Labor-intensive manual maintenance tracking using paper records
- Fragmented search processes for parts and solutions
- Lack of centralized platform for maintenance logs and professional guidance

## 💡 Solution

WeMech provides a comprehensive online platform featuring:
- **Car plate-based maintenance log retrieval**
- **Product pricing and listings platform**
- **Global community for problem-solving**
- **Professional guidance and resources**

## ✨ Features

### Core Functionality
- 🔐 **User Authentication**: Secure registration and login system
- 🚙 **Car Plate Recognition**: OCR-based license plate scanning for maintenance logs
- 📊 **Maintenance Tracking**: Historical service record management
- 🔍 **Smart Search**: AI-powered car and parts search functionality

### Advanced Features
- 🛒 **Parts Marketplace**: Comprehensive automotive parts catalog with pricing
- 👥 **Community Forum**: Global platform for sharing solutions and advice
- 📅 **Appointment Booking**: Online mechanic scheduling system
- 📚 **Solution Library**: Curated database of car problem solutions
- 📋 **Car Specifications**: Detailed vehicle information and specs
- ⭐ **Car Scoring System**: Vehicle condition assessment and valuation

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL
- **Data Processing**: Pandas, NLTK
- **OCR**: Tesseract (pytesseract)
- **Image Processing**: PIL (Python Imaging Library)

### Frontend
- **Templates**: Jinja2 (Flask templating)
- **Styling**: HTML/CSS
- **JavaScript**: For dynamic interactions

### Additional Technologies
- **CSV Processing**: For data management
- **Subprocess**: For external application integration
- **File Upload**: Flask file handling

## 📦 Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- Tesseract OCR Engine

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/wemech.git
   cd wemech
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask pandas nltk pytesseract pillow mysql-connector-python
   ```

3. **Install Tesseract OCR**
   - Windows: Download from [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. **Configure Tesseract path** (Windows)
   ```python
   # Update the path in app.py
   tess.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
   ```

5. **Setup MySQL Database**
   ```sql
   CREATE DATABASE wemech;
   USE wemech;
   
   CREATE TABLE maintenancelogs (
       log_id INT AUTO_INCREMENT PRIMARY KEY,
       plate_number VARCHAR(20),
       date_of_service DATE,
       type_of_service VARCHAR(100),
       service_provider VARCHAR(100)
   );
   ```

6. **Update database credentials**
   ```python
   # Update MySQL connection details in app.py
   connection = mysql.connector.connect(
       host="localhost",
       user="your_username",
       password="your_password",
       database="wemech"
   )
   ```

7. **Create required directories**
   ```bash
   mkdir uploads
   mkdir data
   ```

8. **Add CSV data files**
   - `data/dataset.csv` - Car database
   - `data/problems-solutions.csv` - Problems and solutions
   - `data/accounts.csv` - User accounts
   - `data/parts.csv` - Parts catalog

## 🚀 Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - Create an account or login with existing credentials

3. **Key Workflows**
   - **Maintenance Logs**: Upload car plate image → OCR processing → View logs
   - **Car Search**: Enter keywords and price filters → Browse results
   - **Parts Search**: Search by keywords → View parts and pricing
   - **Community**: Access forum for problem-solving and discussions
   - **Car Scoring**: Input car details → Get condition assessment

## 📊 Project Structure

```
wemech/
├── app.py                 # Main Flask application
├── data/                  # CSV data files
│   ├── dataset.csv
│   ├── problems-solutions.csv
│   ├── accounts.csv
│   └── parts.csv
├── templates/             # HTML templates
│   ├── index.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── autoaid.html
│   ├── carscore.html
│   ├── services.html
│   ├── community.html
│   ├── chat.html
│   ├── maintenance.html
│   └── filter.html
├── uploads/               # Uploaded files storage
├── static/                # CSS, JS, images
└── README.md
```

## 👥 Team

**Fundamentals of Software Engineering Project**

| Name | Role | Student ID |
|------|------|------------|
| Abdullah Bin Umar | Developer, Requirement Engineer |
| Safwan Hafeez | Lead, Developer, Architect |
| Ahmed Mujtaba | Developer, Tester |

## 📋 Development Roadmap

### Iteration 1: Core Functionality
- [x] User registration and authentication
- [x] Car plate-based maintenance log retrieval
- [x] Basic platform infrastructure

### Iteration 2: Enhanced Features
- [x] Product pricing and listings
- [x] Global community integration
- [x] Advanced search functionality

### Iteration 3: Optimization & Refinement
- [x] Online mechanic appointment system
- [x] Car problem solution library
- [x] Car information specifications
- [x] Car scoring system

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/home` | GET | Home dashboard |
| `/login` | GET/POST | User authentication |
| `/signup` | GET/POST | User registration |
| `/search` | POST | Car search functionality |
| `/search-problems` | POST | Problem search |
| `/carscorefunc` | POST | Car condition scoring |
| `/maintenancelog` | GET/POST | OCR-based log retrieval |
| `/filterParts` | POST | Parts catalog filtering |

## 🔒 Security Features

- Password validation and confirmation
- Email uniqueness verification
- Secure file upload handling
- SQL injection prevention
- Session management

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Tesseract OCR path configuration required for Windows
- CSV file paths need to be properly configured
- MySQL connection parameters need manual setup

## 📄 License

This project is part of an academic assignment for Fundamentals of Software Engineering course.

## 🤝 Support

For support and questions, please contact the development team or create an issue in the repository.

---

**Built with ❤️ by the Scalar Team**
