# **B**log project

This project is a small social network where you can follow other users, post and view other users' posts.

## Usage

To use this project:

### Installation

* First you need to have a virtual environment, then you need to install django:

```bash
pip install django
```

## Getting Started

* First clone the repository from Github and switch to the new directory:
<https://github.com/SSleimann/blog-project.git>

```bash
git clone https://github.com/SSleimann/blog-project.git
cd blog-project
```

Activate the virtualenv for your project.

* Install project dependencies:

```bash
pip install -r requirements.txt
```

* Apply the migrations

```bash
python manage.py migrate
```

* Now you can run the server:

```bash
python manage.py runserver
```
