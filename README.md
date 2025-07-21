# 🧩 Django ChatHub

[![Python Version](https://img.shields.io/badge/python-3.12+-blue)]()
[![Django Version](https://img.shields.io/badge/django-4.3-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)]()


A clean and minimal group chat app built using **Django**, **Tailwind CSS**, and **Alpine.js**. ChatHub provides user authentication, conversation creation, and message handling in a modern, responsive UI.

---

## 🚀 Features

- 🔐 Registration, login, and authentication  
- 📁 Create, edit, and delete conversations  
- 🖥️ Admin detection and message deletion  
- 🧭 Infinite scroll & smooth UX  
- ⚙️ Alpine.js components for UI interactions  
- 🧩 Modular code

---

## 🧰 Tech Stack

| Component   | Technology               |
| ----------- | ------------------------ |
| Backend     | Django 4.3               |
| Frontend    | Tailwind CSS, Alpine.js  |
| Templating  | Django Templates         |
| Database    | SQLite (default)         |
| Environment | Python 3.12+, Arch Linux |

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/DarshilNaliyapara/Django-ChatHub.git
   cd Django-ChatHub
   ```

2. **Create Virtual Environment with `uv`**

   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

6. **Visit the App**
   Open your browser and go to:
   👉 `http://127.0.0.1:8000`

---

## 📁 Project Structure

```
ChatHub/
├── base/               # Main chat app
│   ├── models.py       # Conversation & Message models
│   ├── views.py        # Logic for chat, login, register
│   ├── forms.py        # Django forms
│   ├── templates/      # HTML templates
│   └── static/         # Tailwind/JS assets
├── main/               # Project settings
├── requirements.txt    # Python packages
└── README.md
```

---

## 🙌 Author

**Darshil Naliyapara**
🔗 [GitHub Profile](https://github.com/DarshilNaliyapara)

---

## 📜 License

This project is licensed under the MIT License. Feel free to use and modify.

---

> Feel free to fork, star ⭐, and contribute to the project!
