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
    # Personal information - all optional with safe defaults
    name = request.form.get('name', '').strip()
    location = request.form.get('location', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    linkedin = request.form.get('linkedin', '').strip()
    github = request.form.get('github', '').strip()

    # Education - all fields optional
    education = []
    institutions = request.form.getlist('institution[]')
    locations = request.form.getlist('edu_location[]')
    degrees = request.form.getlist('degree[]')
    dates = request.form.getlist('edu_dates[]')
    gpas = request.form.getlist('gpa[]')
    
    # Only add education entries that have at least one non-empty field
    for i in range(len(institutions)):
        entry = {
            'institution': institutions[i].strip() if i < len(institutions) else '',
            'location': locations[i].strip() if i < len(locations) else '',
            'degree': degrees[i].strip() if i < len(degrees) else '',
            'dates': dates[i].strip() if i < len(dates) else '',
            'gpa': gpas[i].strip() if i < len(gpas) else ''
        }
        # Add entry if any field has content
        if any(entry.values()):
            education.append(entry)

    # Experience - all fields optional
    experience = []
    roles = request.form.getlist('role[]')
    companies = request.form.getlist('company[]')
    exp_locations = request.form.getlist('exp_location[]')
    years = request.form.getlist('years[]')
    details_str = request.form.getlist('exp_details[]')
    
    # Determine the maximum length to handle mismatched arrays
    max_exp_length = max(len(roles), len(companies), len(exp_locations), len(years), len(details_str)) if any([roles, companies, exp_locations, years, details_str]) else 0
    
    for i in range(max_exp_length):
        role = roles[i].strip() if i < len(roles) else ''
        company = companies[i].strip() if i < len(companies) else ''
        exp_location = exp_locations[i].strip() if i < len(exp_locations) else ''
        year = years[i].strip() if i < len(years) else ''
        detail_text = details_str[i].strip() if i < len(details_str) else ''
        
        # Process details - split by newlines and filter empty lines
        details = [line.strip() for line in detail_text.split('\n') if line.strip()] if detail_text else []
        
        entry = {
            'role': role,
            'company': company,
            'location': exp_location,
            'years': year,
            'details': details
        }
        
        # Add entry if any field has content
        if role or company or exp_location or year or details:
            experience.append(entry)

    # Projects - all fields optional
    projects = []
    project_names = request.form.getlist('project_name[]')
    technologies_list = request.form.getlist('technologies[]')
    proj_dates_list = request.form.getlist('proj_dates[]')
    proj_summaries = request.form.getlist('proj_summary[]')
    
    max_proj_length = max(len(project_names), len(technologies_list), len(proj_dates_list), len(proj_summaries)) if any([project_names, technologies_list, proj_dates_list, proj_summaries]) else 0
    
    for i in range(max_proj_length):
        name_val = project_names[i].strip() if i < len(project_names) else ''
        tech_val = technologies_list[i].strip() if i < len(technologies_list) else ''
        dates_val = proj_dates_list[i].strip() if i < len(proj_dates_list) else ''
        summary_val = proj_summaries[i].strip() if i < len(proj_summaries) else ''
        
        entry = {
            'name': name_val,
            'technologies': tech_val,
            'dates': dates_val,
            'summary': summary_val
        }
        
        # Add entry if any field has content
        if any(entry.values()):
            projects.append(entry)

    # Skills - optional with safe handling
    skills = {}
    languages_input = request.form.get('languages', '').strip()
    if languages_input:
        languages_list = [s.strip() for s in languages_input.split(',') if s.strip()]
        if languages_list:
            skills['Languages'] = languages_list
    
    software_input = request.form.get('software', '').strip()
    if software_input:
        software_list = [s.strip() for s in software_input.split(',') if s.strip()]
        if software_list:
            skills['Software'] = software_list
    
    # Build complete data dictionary
    data = {
        'name': name,
        'location': location,
        'phone': phone,
        'email': email,
        'linkedin': linkedin,
        'github': github,
        'education': education,
        'experience': experience,
        'projects': projects,
        'skills': skills,
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
