from flask import Flask, render_template, request, send_file, session, redirect, url_for
from jinja2 import Template
import os
import io
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Define a dictionary to map template names to file paths
TEMPLATE_FILES = {
    "professional": {
        "html": "resume_templates/professional_html_template.html",
        "latex": "resume_templates/professional_latex_template.tex"
    },
    "modern": {
        "html": "resume_templates/modern_html_template.html",
        "latex": "resume_templates/modern_latex_template.tex"
    }
}

def _get_template_content(template_choice):
    """Helper function to get template content based on choice."""
    try:
        html_template_path = TEMPLATE_FILES[template_choice]["html"]
        latex_template_path = TEMPLATE_FILES[template_choice]["latex"]
        
        with open(html_template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        with open(latex_template_path, "r", encoding="utf-8") as f:
            latex_content = f.read()
        return html_content, latex_content
    except (KeyError, FileNotFoundError):
        return None, None

@app.route('/')
def index():
    """Renders the main input form, pre-populating with session data if available."""
    data = session.get('resume_data', {})
    return render_template('index.html', data=data)

@app.route('/generate', methods=['POST'])
def generate_resume():
    """Processes form data and generates the resume based on initial template choice."""
    name = request.form.get('name')
    location = request.form.get('location')
    phone = request.form.get('phone')
    email = request.form.get('email')
    linkedin = request.form.get('linkedin')
    github = request.form.get('github')

    education = []
    institutions = request.form.getlist('institution[]')
    locations = request.form.getlist('edu_location[]')
    degrees = request.form.getlist('degree[]')
    dates = request.form.getlist('edu_dates[]')
    gpas = request.form.getlist('gpa[]')
    for i in range(len(institutions)):
        if institutions[i].strip():
            education.append({
                'institution': institutions[i],
                'location': locations[i],
                'degree': degrees[i],
                'dates': dates[i],
                'gpa': gpas[i]
            })

    experience = []
    roles = request.form.getlist('role[]')
    companies = request.form.getlist('company[]')
    exp_locations = request.form.getlist('exp_location[]')
    years = request.form.getlist('years[]')
    details_str = request.form.getlist('exp_details[]')
    for i in range(len(roles)):
        if roles[i].strip():
            details = [line.strip() for line in details_str[i].split('\n') if line.strip()]
            experience.append({
                'role': roles[i],
                'company': companies[i],
                'location': exp_locations[i],
                'years': years[i],
                'details': details
            })

    projects = []
    project_names = request.form.getlist('project_name[]')
    technologies_list = request.form.getlist('technologies[]')
    proj_dates_list = request.form.getlist('proj_dates[]')
    proj_summaries = request.form.getlist('proj_summary[]')
    for i in range(len(project_names)):
        if project_names[i].strip():
            projects.append({
                'name': project_names[i],
                'technologies': technologies_list[i],
                'dates': proj_dates_list[i],
                'summary': proj_summaries[i]
            })

    skills = {}
    languages_list = [s.strip() for s in request.form.get('languages', '').split(',') if s.strip()]
    if languages_list:
        skills['Languages'] = languages_list
    software_list = [s.strip() for s in request.form.get('software', '').split(',') if s.strip()]
    if software_list:
        skills['Software'] = software_list
    
    data = {
        'name': name, 'location': location, 'phone': phone, 'email': email,
        'linkedin': linkedin, 'github': github, 'education': education,
        'experience': experience, 'projects': projects, 'skills': skills,
        'template_choice': request.form.get('template_choice', 'professional')
    }

    # Store the entire data dictionary in the session
    session['resume_data'] = data

    html_template, latex_template = _get_template_content(data['template_choice'])
    if not html_template:
        return "Template files not found. Please check your file paths.", 404

    html_filled = Template(html_template).render(data)
    latex_filled = Template(latex_template).render(data)

    return render_template('resume_preview.html', html_content=html_filled, latex_content=latex_filled, data=data)

@app.route('/update_template', methods=['POST'])
def update_template():
    """Handles template changes from the preview page by using session data."""
    # Retrieve the stored data from the session
    data = session.get('resume_data')
    if not data:
        return redirect(url_for('index'))

    # Update the template choice from the form submission
    template_choice = request.form.get('template_choice', 'professional')
    data['template_choice'] = template_choice
    
    # Store the updated data back in the session
    session['resume_data'] = data

    html_template, latex_template = _get_template_content(template_choice)
    if not html_template:
        return "Template files not found. Please check your file paths.", 404
        
    html_filled = Template(html_template).render(data)
    latex_filled = Template(latex_template).render(data)

    return render_template('resume_preview.html', html_content=html_filled, latex_content=latex_filled, data=data)


@app.route('/download/<file_type>')
def download(file_type):
    """Handles file downloads from the session data."""
    data = session.get('resume_data')
    if not data:
        return "No resume data found.", 404
    
    template_choice = data.get('template_choice', 'professional')

    html_template, latex_template = _get_template_content(template_choice)
    if not html_template:
        return "Template files not found. Please check your file paths.", 404

    if file_type == 'html':
        html_filled = Template(html_template).render(data)
        return send_file(
            io.BytesIO(html_filled.encode()),
            mimetype='text/html',
            as_attachment=True,
            download_name=f'resume_{template_choice}.html'
        )
    elif file_type == 'tex':
        latex_filled = Template(latex_template).render(data)
        return send_file(
            io.BytesIO(latex_filled.encode()),
            mimetype='application/x-tex',
            as_attachment=True,
            download_name=f'resume_{template_choice}.tex'
        )
    return "Invalid file type.", 400

if __name__ == '__main__':
    app.run(debug=True)
