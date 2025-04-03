# Late Show API

This is a Flask-based API for tracking episodes, guests, and their appearances on the **Late Show**. The API allows managing episodes, guests, and their ratings through various endpoints.

## 📌 Features
- View all episodes and their details
- View all guests and their occupations
- Track guest appearances on specific episodes
- Rate guest appearances (1-5 scale)

---
## 🛠 Setup Instructions

### **1. Clone the Repository**
```sh
 git clone git@github.com:your-username/lateshow-firstname-lastname.git
 cd lateshow-firstname-lastname
```

### **2. Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Set Up the Database**
```sh
flask db upgrade  # Run migrations
python seed.py    # Seed the database with initial data
```

### **5. Start the Server**
```sh
flask run --port=5555
```

---
## 📌 API Endpoints

### **1. Get All Episodes**
```http
GET /episodes
```
#### ✅ Response
```json
[
  {"id": 1, "date": "1/11/99", "number": 1},
  {"id": 2, "date": "1/12/99", "number": 2}
]
```

### **2. Get Specific Episode**
```http
GET /episodes/:id
```
#### ✅ Response
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {"id": 1, "name": "Michael J. Fox", "occupation": "actor"}
    }
  ]
}
```

### **3. Get All Guests**
```http
GET /guests
```
#### ✅ Response
```json
[
  {"id": 1, "name": "Michael J. Fox", "occupation": "actor"},
  {"id": 2, "name": "Sandra Bernhard", "occupation": "Comedian"}
]
```

### **4. Create an Appearance**
```http
POST /appearances
```
#### 🔹 Request Body
```json
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}
```
#### ✅ Response
```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {"date": "1/12/99", "id": 2, "number": 2},
  "guest": {"id": 3, "name": "Tracey Ullman", "occupation": "television actress"}
}
```

---
## 📝 Validations
- The **rating** for an appearance must be between **1 and 5**.

---
## 🔥 Before Submitting
✔ **Run and test the API** in Postman
✔ **Ensure the database is seeded correctly**
✔ **Check your README formatting** with VS Code Markdown Preview (`Ctrl + Shift + V`)
✔ **Push your latest changes** to GitHub:
```sh
git add .
git commit -m "Final version"
git push origin main
```

---
## 📜 License
This project is for educational purposes only.

---
## 🚀 Author
**Jonas Kiwia**  
GitHub: [your-username]((https://github.com/JonasKiwia))

