# Railway Analytics System

A Flask-based Railway Analytics and Intelligent Route Search platform developed for railway data analysis, route exploration, and passenger enquiry support.

## Project Overview

The Railway Analytics System provides:

- Railway network analytics dashboard
- Smart route search between stations
- Train route exploration
- Data-driven railway insights
- User authentication system
- Interactive visualizations and reports

The application processes railway datasets and presents meaningful analytics through a clean web interface.

---

## Features

### Railway Network Analytics
- Total train statistics
- Major station analysis
- Longest route identification
- Average route distance insights
- Top traffic station visualization

### Smart Route Finder
- Source and destination station selection
- Route matching from railway dataset
- Train number display
- Number of stops calculation
- Estimated distance calculation

### User Management
- User Registration
- Secure Login
- Session Management
- Logout Functionality

### Data Processing
- Railway dataset cleaning
- Data preprocessing pipelines
- SQLite database integration

---

## Technology Stack

### Backend
- Python
- Flask
- SQLite

### Data Analysis
- Pandas
- NumPy
- Matplotlib

### Frontend
- HTML5
- CSS3
- Jinja2 Templates

### Database
- SQLite

---

## Project Structure

```text
Railway-Analytics-System/
│
├── app.py
├── README.md
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── trains.db
│
├── src/
│   ├── auth.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── database.py
│   └── visualizer.py
│
├── static/
│   ├── css/
│   └── images/
│
├── templates/
│   ├── home.html
│   ├── dashboard.html
│   ├── smart_search.html
│   ├── login.html
│   ├── register.html
│   └── enquiry.html
│
└── notebooks/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/railway-analytics-system.git

cd railway-analytics-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Database

The project uses SQLite database.

Main database:

```text
database/trains.db
```

Stores:

- Train information
- Station information
- Route details
- Analytics data

---

## Analytics Included

- Total trains available
- Station traffic analysis
- Route distance analysis
- Railway network statistics
- Route recommendation insights

---

## Future Enhancements

- Real-time train tracking
- Delay prediction using Machine Learning
- Passenger demand forecasting
- Interactive railway maps
- Live train status integration
- Advanced route optimization

---

## Screenshots

### Home Page
Railway Analytics System landing page with intelligent route exploration.

### Analytics Dashboard
Railway network insights and visualizations.

### Smart Route Search
Train search based on source and destination stations.

---

## Author

Anamika P Sudheesh

---

## License

This project is developed for educational and academic purposes.