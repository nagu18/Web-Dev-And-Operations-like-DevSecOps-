Here is your complete README.md for the Django Code Sharing App — covering every step from setup to deployment. You can copy and paste this directly into your project.

⸻


# 💬 Django Code Sharing App

A simple Django project where users can:

- 🔐 Register, login, and logout
- 🧑‍💻 Post code snippets
- 🗂 View their previously shared code
- 🟢 See a cool username badge and logout option

---

## 🚀 Features

- Django authentication (register/login/logout)
- Store user-submitted code in a database
- Display personalized dashboard
- Styled UI with a circular username badge and monospace code blocks

---

## 📁 Project Structure

code_chat/
│
├── data/
│   ├── migrations/
│   ├── templates/
│   │   └── data/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── home.html     👈 Main UI
│   ├── init.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             👈 CodePost model here
│   ├── urls.py               👈 App-level routes
│   └── views.py              👈 Main logic here
│
├── code_chat/
│   ├── init.py
│   ├── settings.py           👈 Configuration
│   ├── urls.py               👈 Root-level routing
│   └── wsgi.py
│
├── db.sqlite3
└── manage.py

---

## ⚙️ Step-by-Step Setup

### ✅ 1. Install Django

```bash
pip install django


⸻

✅ 2. Create Django Project & App

django-admin startproject code_chat
cd code_chat
python manage.py startapp data


⸻

✅ 3. Register the App in settings.py

Edit code_chat/settings.py:

INSTALLED_APPS = [
    ...
    'data',  # your app
]

# Static & login settings
STATIC_URL = 'static/'
LOGIN_URL = 'login'


⸻

✅ 4. Setup URLs

In code_chat/urls.py:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data.urls')),
]

In data/urls.py:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]


⸻

🧠 CodePost Model

Create data/models.py:

from django.db import models
from django.contrib.auth.models import User

class CodePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


⸻

✅ 5. Migrate the Database

python manage.py makemigrations
python manage.py migrate


⸻

✅ 6. Create Superuser (optional)

python manage.py createsuperuser


⸻

✅ 7. Add Views in data/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CodePost

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'User registered successfully')
            return redirect('login')
    return render(request, 'data/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'data/login.html')

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            CodePost.objects.create(user=request.user, code=code)
    posts = CodePost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'data/home.html', {'posts': posts})

def user_logout(request):
    logout(request)
    return redirect('login')


⸻

✅ 8. Templates

📄 templates/data/login.html

<h1>Login</h1>
<form method="POST">{% csrf_token %}
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>
<a href="{% url 'register' %}">Register</a>


⸻

📄 templates/data/register.html

<h1>Register</h1>
<form method="POST">{% csrf_token %}
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Register</button>
</form>
<a href="{% url 'login' %}">Already have an account? Login</a>


⸻

📄 templates/data/home.html

<!DOCTYPE html>
<html>
<head>
    <title>Code Share</title>
    <style>
        body {
            font-family: monospace; background: #f9f9f9; margin: 0;
        }
        .header {
            background: #1e1e2f; color: white;
            padding: 20px; display: flex; justify-content: space-between; align-items: center;
        }
        .user-circle {
            width: 50px; height: 50px; background: #4CAF50;
            border-radius: 50%; display: flex; justify-content: center; align-items: center;
            font-weight: bold; font-size: 14px; color: white; text-transform: uppercase;
        }
        .logout {
            color: white; text-decoration: none; font-weight: bold;
        }
        .container {
            max-width: 700px; margin: 30px auto; background: white; padding: 20px; border-radius: 8px;
        }
        textarea {
            width: 100%; height: 120px; margin-bottom: 10px; font-family: monospace; padding: 10px;
        }
        .code-block {
            background: #272822; color: #f8f8f2;
            padding: 10px; border-radius: 5px; margin-top: 20px; white-space: pre-wrap;
        }
        .meta {
            font-size: 12px; color: #555; margin-top: 5px;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="user-circle">{{ request.user.username|first }}</div>
        <a href="{% url 'logout' %}" class="logout">Logout</a>
    </div>

    <div class="container">
        <h2>Welcome, {{ request.user.username|title }}</h2>
        <form method="POST">
            {% csrf_token %}
            <textarea name="code" placeholder="Paste your code..."></textarea><br>
            <button type="submit">Submit</button>
        </form>

        <hr>

        <h3>Your Code Snippets:</h3>
        {% for post in posts %}
            <div class="code-block">{{ post.code }}</div>
            <div class="meta">Submitted at {{ post.created_at }}</div>
        {% empty %}
            <p>No code submitted yet.</p>
        {% endfor %}
    </div>
</body>
</html>


⸻

🏁 Run the Server

python manage.py runserver

Visit: http://127.0.0.1:8000

⸻

🎯 Done!

You now have a fully working Django app that supports:
	•	Register/Login/Logout
	•	Code sharing with storage
	•	Profile badge with logout
	•	Code-only personal dashboard

⸻

Need enhancements? Add syntax highlighting, public walls, like buttons, or even code execution support!

Let me know if you want me to export this to a real `README.md` file or zip the whole project folder!