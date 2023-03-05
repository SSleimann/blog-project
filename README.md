# **B**log project

This project is a small social network where you can follow other users, post and view other users' posts.

## Usage

To use this project:

### Installation

* First you need to have a virtual environment, then you need to install django:

```shell
pip install django
```

* Create a .env file and add:
  
```shell
EMAIL_HOST_USER = yourmail@mail.com
EMAIL_HOST_PASSWORD = passwordmail
```

## Getting Started

* First clone the repository from Github and switch to the new directory:

```shell
git clone https://github.com/SSleimann/blog-project.git
cd blog-project
```

Activate the virtualenv for your project.

* Install project dependencies:

```shell
pip install -r requirements.txt
```

* Apply the migrations

```shell
python manage.py migrate
```

* Now you can run the server:

```shell
python manage.py runserver
```
