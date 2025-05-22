# Write Another One

**Write Another One** is a Django-based web platform designed to help writers craft, organize, and publish fictional stories. It provides a structured environment for developing narratives, managing characters, and building immersive worlds.

Live site: [www.writeanotherone.com](https://www.writeanotherone.com)

---

## Features

- **Story Management**: Create and edit stories with a user-friendly interface.
- **Project Organization**: Keep your writing projects organized and accessible.
- **User Authentication**: Secure login and registration system for personalized experiences.

---

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default, can be configured)
- **Deployment**: Hosted on PythonAnywhere

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Francisco-Pages/write_another_one-repo.git
cd write_another_one-repo
```
2. **Create a virtual environment and activate it:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. **Install dependencies:**
```bash
pip install -r requirements.txt
```
4.	**Apply migrations:**
```bash
python manage.py migrate
```
5.	**Run the development server:**
```bash
python manage.py runserver
```
6.	**Access the application:**
Open your browser and navigate to http://127.0.0.1:8000/

⸻

Project Structure

write_another_one-repo/
├── author_app/        # Handles author-related functionalities
├── story_app/         # Manages stories and related content
├── templates/         # HTML templates for rendering pages
├── static/            # Static files (CSS, JS, images)
├── media/             # Uploaded media files
├── wao_project/       # Project configuration and settings
├── manage.py          # Django's command-line utility
└── requirements.txt   # Python dependencies


⸻

Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

⸻

License

This project is licensed under the MIT License.

⸻

Contact

For questions or feedback, reach out via the GitHub repository.
