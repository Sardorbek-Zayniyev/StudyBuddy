
# StudyBuddy: Your Collaborative Learning Hub

StudyBuddy is a Django-based web application designed to empower students to learn together. It allows users to connect, share resources, and collaborate on various projects.

## Features
- **User Profiles**: Create personalized profiles and connect with other students.
- **Friendships**: Add classmates as friends and build a learning network.
- **Messaging**: Send direct messages to peers.
- **Groups**: Create or join study groups.
- **Notifications**: Get updates on messages, group activities, and events.
  
## Technologies and Libraries Used

- **Django**: Web framework for building the backend.
- **djangorestframework**: Toolkit for building APIs in Django.
- **django-cors-headers**: Middleware for handling Cross-Origin Resource Sharing (CORS).
- **Python**: Programming language used for development.
- **pillow**: Image processing library.
- **black**: Code formatter for Python.
- **click**: Python package for creating command-line interfaces.
- **mypy-extensions**: Type checking extensions for Python.
- **python-decouple**: For managing settings in a decoupled way.
- **sqlparse**: SQL parsing library.
- **packaging**: Tools for working with Python packages.
- **platformdirs**: For platform-specific directories.
  
## Installation

### Prerequisites:
- Python 3.x
- pip (Python package manager)

### Setup:
1. Clone the repository:
    ```bash
    git clone https://github.com/Sardorbek-Zayniyev/StudyBuddy.git
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

The app will be available at `http://127.0.0.1:8000/`.

## Contributing
Feel free to fork the repository, create a new branch, and submit pull requests. Please ensure that your code is well-tested before submitting.

## Contact
For any issues or feedback, please open an issue on this repository.
