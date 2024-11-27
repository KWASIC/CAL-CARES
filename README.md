# CALVIN CARES

CALVIN CARES is a modern, Django-based charity website designed to facilitate charitable activities and community engagement. The platform provides a user-friendly interface for managing donations, programs, and charitable initiatives.

## Features

- **Dynamic Content Management**
  - Mission statements and organizational goals
  - Featured charity programs
  - Help & Support services
  - Image and video content integration
  - Testimonials system

- **Responsive Design**
  - Mobile-first approach
  - Modern UI/UX
  - Bootstrap framework integration
  - Custom animations and transitions

- **Admin Interface**
  - User-friendly content management
  - Rich text editing with CKEditor
  - Image and video upload capabilities
  - Program and event management

## Technology Stack

- **Backend**
  - Python 3.10.0
  - Django 4.2.7
  - SQLite (Development)

- **Frontend**
  - HTML5/CSS3
  - JavaScript
  - Bootstrap
  - Font Awesome
  - CKEditor

- **Dependencies**
  - django-crispy-forms
  - crispy-bootstrap4
  - django-ckeditor
  - Pillow

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KWASIC/CAL-CARES.git
   cd CAL-CARES
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Website**
   - Main site: http://localhost:8000
   - Admin interface: http://localhost:8000/admin

## Project Structure

```
sadaka/
├── charity/                 # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View controllers
│   ├── admin.py            # Admin interface
│   └── urls.py             # URL routing
├── templates/              # HTML templates
│   └── charity/
├── static/                 # Static files
│   └── css/
├── media/                  # User-uploaded content
└── sadaka_project/         # Project settings
```

## Features in Detail

### Content Management
- Dynamic mission statements
- Program management with featured status
- Help & Support services with icons
- Image and video content integration
- Active/inactive status for testimonials

### User Interface
- Responsive navigation
- Modern carousel/slider
- Card-based content layout
- Hover effects and animations
- Mobile-friendly design

### Admin Features
- Rich text editing
- Image upload and management
- Video URL and file support
- Content ordering system
- Active/inactive content toggle

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original template design inspiration
- Bootstrap framework
- Django community
- All contributors and supporters
