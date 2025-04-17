# ResumeCraft - Professional Resume Builder

ResumeCraft is a free, open-source resume builder web application built with Django. It allows users to create professional resumes through a simple step-by-step wizard, choose from multiple templates, and export their resumes as PDF documents.

## Features

- **Step-by-step Resume Wizard**: Easily create a resume by filling in information section by section
- **Multiple Templates**: Choose from professional, modern resume templates
- **Live Preview**: See changes to your resume in real-time as you edit
- **PDF Export**: Download your resume as a beautifully formatted PDF
- **User Dashboard**: Save, edit, and manage multiple resume versions
- **Public Sharing**: Generate public links to share your resume with employers
- **Dark/Light Mode Support**: Templates support both light and dark modes

## Requirements

- Python 3.8+
- Django 5.2+
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/resumecraft.git
   cd resumecraft
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create initial resume templates:
   ```
   python manage.py loaddata resume_templates
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Usage

1. **Register/Login**: Create an account to save and manage your resumes
2. **Create a Resume**: Click "Create New Resume" button on the dashboard
3. **Fill in Details**: Complete each section of the resume form
4. **Choose a Template**: Select from available templates and customize appearance
5. **Preview & Export**: Preview your resume and download it as a PDF
6. **Share**: Generate a public link to share your resume with others (optional)

## Demo Accounts

For testing purposes, you can use the following demo account:
- Username: demo
- Password: resumecraft2023

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
