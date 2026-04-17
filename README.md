# Registration App

Flask + SQLite registration web app for:
- Овог
- Нэр
- Утасны дугаар
- Имэйл

Features:
- Server-side email validation
- Success message after registration
- Admin page with registered records
- Excel export from admin page
- Clean minimal business-style UI

## Run in VS Code

### 1) Open terminal in the project folder

### 2) Create virtual environment
macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Start the app
```bash
python app.py
```

### 5) Open in browser
- Registration page: http://127.0.0.1:5000
- Admin page: http://127.0.0.1:5000/admin
- Excel download: button on admin page

## Email format example
Example valid emails:
- name@example.com
- user123@gmail.com

## Notes
- Database file name: `register.db`
- Table name: `register`
# firstTime
