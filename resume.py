from jinja2 import Template
import webbrowser
import os

print("Welcome to the Resume Generator!")
print("Type 'exit' or 'stop' at any prompt to quit.")

while True:
    # ===== PERSONAL INFO =====
    name = input("Full Name: ")
    if name == "":
        print("⚠ Name is required.")
        continue
    if name.lower() in ["exit", "stop"]:
        break
    
    phone = input("Phone Number: ")
    if phone == "":
        print("⚠ Phone number is required.")
        continue
    if phone.lower() in ["exit", "stop"]:
        break

    email = input("Email Address: ")
    if email == "":
        print("⚠ Email address is required.")
        continue
    if email.lower() in ["exit", "stop"]:
        break

    linkedin = input("LinkedIn Profile URL: ")
    if linkedin.lower() in ["exit", "stop"]:
        break

    github = input("GitHub Profile URL: ")
    if github.lower() in ["exit", "stop"]:
        break

    # ===== EDUCATION =====
    education = []
    print("\n--- Enter Education Details ---")
    while True:
        institution = input("Institution Name (or press Enter to stop): ")
        if institution.lower() in ["exit", "stop"]:
            exit()
        if not institution.strip():
            break
        location = input("Location: ")
        degree = input("Degree: ")
        dates = input("Dates (e.g., 2018-2022): ")
        gpa = input("GPA: ")
        education.append({
            "institution": institution, "location": location,
            "degree": degree, "dates": dates, "gpa": gpa
        })

    if not education:
        print("⚠ Education section is required.")
        continue

    # ===== EXPERIENCE =====
    experience = []
    print("\n--- Enter Experience Details ---")
    while True:
        role = input("Job Role (or press Enter to stop): ")
        if role.lower() in ["exit", "stop"]:
            exit()
        if not role.strip():
            break
        company = input("Company Name: ")
        years = input("Years (e.g., 2020-2024): ")
        experience.append({"role": role, "company": company, "years": years})

    if not experience:
        print("⚠ Experience section is required.")
        continue

    # ===== PROJECTS =====
    projects = []
    print("\n--- Enter Project Details (Optional) ---")
    while True:
        project_name = input("Project Name (or press Enter to stop): ")
        if project_name.lower() in ["exit", "stop"]:
            exit()
        if not project_name.strip():
            break
        technologies = input("Technologies Used: ")
        proj_dates = input("Dates: ")
        proj_summary = input("Project Summary: ")
        projects.append({
            "name": project_name,
            "technologies": technologies,
            "dates": proj_dates,
            "summary": proj_summary
        })

    # ===== SKILLS =====
    skills = input("Enter skills (comma separated): ").split(",")
    skills = [s.strip() for s in skills if s.strip()]

    if not skills:
        print("⚠ Skills section is required.")
        continue

    print("✅ Resume data collected successfully!")

    # ===== HTML TEMPLATE =====
    html_template = """
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{{ name }} - Resume</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }
            h1 { margin-bottom: 0; }
            .contact { font-size: 14px; color: #555; }
            h2 { border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 30px; }
            ul { list-style: none; padding: 0; }
        </style>
    </head>
    <body>
        <h1>{{ name }}</h1>
        <p class="contact">{{ phone }} | {{ email }} | <a href="{{ linkedin }}">LinkedIn</a> | <a href="{{ github }}">GitHub</a></p>

        <h2>Education</h2>
        <ul>
        {% for edu in education %}
            <li><strong>{{ edu.degree }}</strong>, {{ edu.institution }} - {{ edu.location }} ({{ edu.dates }}) — GPA: {{ edu.gpa }}</li>
        {% endfor %}
        </ul>

        <h2>Experience</h2>
        <ul>
        {% for job in experience %}
            <li><strong>{{ job.role }}</strong>, {{ job.company }} ({{ job.years }})</li>
        {% endfor %}
        </ul>

        {% if projects %}
        <h2>Projects</h2>
        <ul>
        {% for proj in projects %}
            <li><strong>{{ proj.name }}</strong> — {{ proj.technologies }} ({{ proj.dates }})<br>{{ proj.summary }}</li>
        {% endfor %}
        </ul>
        {% endif %}

        <h2>Skills</h2>
        <p>{{ skills | join(", ") }}</p>
    </body>
    </html>
    """

    # ===== LaTeX TEMPLATE =====
    # LaTeX Template
    latex_template = r"""
    \documentclass[a4paper,10pt]{article}
    \usepackage[margin=1in]{geometry}
    \usepackage{enumitem}
    \usepackage[hidelinks]{hyperref}

    \begin{document}

    \begin{center}
        {\LARGE \textbf{ {{ name }} }} \\
        {{ phone }} | {{ email }} | \href{ {{ linkedin }} }{LinkedIn} | \href{ {{ github }} }{GitHub}
    \end{center}

    \section*{Education}
    {% for edu in education %}
    \textbf{ {{ edu.degree }} } --- {{ edu.institution }} ({{ edu.location }}) \hfill {{ edu.dates }} \\
    GPA: {{ edu.gpa }} \\
    {% endfor %}

    \section*{Experience}
    {% for exp in experience %}
    \textbf{ {{ exp.role }} } --- {{ exp.company }} \hfill {{ exp.years }} \\
    {% endfor %}

    {% if projects %}
    \section*{Projects}
    {% for proj in projects %}
    \textbf{ {{ proj.name }} } --- {{ proj.technologies }} \hfill {{ proj.dates }} \\
    {{ proj.summary }} \\
    {% endfor %}
    {% endif %}

    \section*{Skills}
    \begin{itemize}[leftmargin=*]
    {% for skill in skills %}
        \item {{ skill }}
    {% endfor %}
    \end{itemize}

    \end{document}
    """


    # Render
    html_filled = Template(html_template).render(
        name=name, phone=phone, email=email, linkedin=linkedin, github=github,
        education=education, experience=experience, projects=projects, skills=skills
    )

    latex_filled = Template(latex_template).render(
        name=name, phone=phone, email=email, linkedin=linkedin, github=github,
        education=education, experience=experience, projects=projects, skills=skills
    )

    # Save
    with open("resume.html", "w", encoding="utf-8") as f:
        f.write(html_filled)
    with open("resume.tex", "w", encoding="utf-8") as f:
        f.write(latex_filled)

    print("💾 Files saved: resume.html and resume.tex")
    webbrowser.open("file://" + os.path.realpath("resume.html"))
    break
