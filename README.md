# Midnight-Times
A news portal where user can register themselves and search for news. The project is built using Python, Django, VueJs, Quasar, and Javascript.

## Getting Started

Follow these steps to set up the project on your local machine.

### 1. Clone the repository

Clone the repository using the following command:

```bash
> git clone git@github.com:Yash-Pukale/Midnight-Times.git
```

### 2. Navigate to the project directory

```bash
> cd Midnight-Times
```

### 3. Setup a virtual environment
```bash
> python3 -m venv venv
> source venv/bin/activate
```

### 4. Install the required packages
```bash
> pip install -r requirements.txt
```

### 5. Set up the Django App
```bash
> cd django-app
> python manage.py migrate
> python manage.py createsuperuser
> python manage.py runserver
```
Note: Remember the credentials used to create the superuser. We will be using the same credentials to login into the system.
Make sure the app runs on port 8000.

### 5. Set up the Frontend App(VueJs + Quasar Framework)
```bash
> cd quasar-app
> npm install
```
This will install the necessary node modules required to run the application.

### 6. Creating Environment File
```bash
> touch .env
```

Add the below line to the file, this will treat APP_BASE_URL as environment variable

```
APP_BASE_URL=http://127.0.0.1:8000/
```

### 7. Run the Frontend App
```bash
> quasar dev
```