document.addEventListener('DOMContentLoaded', function () {
  const addButtons = document.querySelectorAll('.add-button');
  const loadDataButton = document.getElementById('load-sample-data');

  // Sample data object
  const sampleData = {
    name: "Jane Doe",
    location: "San Francisco, CA",
    phone: "(123) 456-7890",
    email: "jane.doe@example.com",
    linkedin: "https://linkedin.com/in/janedoe",
    github: "https://github.com/janedoe",
    education: [
      {
        institution: "University of California, Berkeley",
        edu_location: "Berkeley, CA",
        degree: "M.S. in Computer Science",
        edu_dates: "August 2021 -- May 2023",
        gpa: "3.95/4.00",
      },
      {
        institution: "Stanford University",
        edu_location: "Palo Alto, CA",
        degree: "B.S. in Electrical Engineering",
        edu_dates: "August 2017 -- May 2021",
        gpa: "3.80/4.00",
      },
    ],
    experience: [
      {
        company: "Google",
        exp_location: "Mountain View, CA",
        role: "Software Engineer",
        years: "June 2023 -- Present",
        details:
          "• Developed and maintained scalable backend services for Google Cloud Platform.\n• Collaborated with a team of 5 engineers to launch a new feature, increasing user engagement by 20%.\n• Optimized database queries, reducing response times by 30%.",
      },
      {
        company: "Meta",
        exp_location: "Menlo Park, CA",
        role: "Software Engineering Intern",
        years: "May 2022 -- August 2022",
        details:
          "• Implemented a new data pipeline using Python and Apache Spark to process large datasets.\n• Contributed to the development of a user-facing tool, improving the efficiency of A/B testing.\n• Wrote unit and integration tests to ensure code quality.",
      },
    ],
    projects: [
      {
        project_name: "Personal Portfolio Website",
        technologies: "HTML, CSS, JavaScript, React",
        proj_dates: "Spring 2023",
        proj_summary:
          "A responsive personal website to showcase my projects, skills, and resume. The site features a clean design and is optimized for both desktop and mobile devices.",
      },
    ],
    skills: {
      languages: "Python, JavaScript, C++, Java, SQL",
      software: "AWS, Docker, Git, Flask, Django, React, Node.js",
    },
  };

  // Function to populate personal info and skills
  function populatePersonalInfo(data) {
    document.getElementById("name").value = data.name || "";
    document.getElementById("location").value = data.location || "";
    document.getElementById("phone").value = data.phone || "";
    document.getElementById("email").value = data.email || "";
    document.getElementById("linkedin").value = data.linkedin || "";
    document.getElementById("github").value = data.github || "";

    document.getElementById("languages").value = data.skills.languages || "";
    document.getElementById("software").value = data.skills.software || "";
  }

  // Generic function to clear non-template entries in a container
  function clearEntries(container) {
    container.querySelectorAll(".field-entry:not(.template)").forEach((el) => el.remove());
  }

  // Generic function to clone and fill an entry based on a template and data mapping
  function addEntries(container, templateSelector, dataArray, fillCallback) {
    clearEntries(container);
    const template = container.querySelector(templateSelector);
    if (!template) return;
    dataArray.forEach((item) => {
      const newEntry = template.cloneNode(true);
      newEntry.style.display = "";
      newEntry.classList.remove("template");
      fillCallback(newEntry, item);
      container.appendChild(newEntry);
    });
  }

  // Fill functions for each repeatable section
  function fillEducation(entry, edu) {
    entry.querySelector('input[name="institution[]"]').value = edu.institution || "";
    entry.querySelector('input[name="edu_location[]"]').value = edu.edu_location || "";
    entry.querySelector('input[name="degree[]"]').value = edu.degree || "";
    entry.querySelector('input[name="edu_dates[]"]').value = edu.edu_dates || "";
    entry.querySelector('input[name="gpa[]"]').value = edu.gpa || "";
  }

  function fillExperience(entry, exp) {
    entry.querySelector('input[name="company[]"]').value = exp.company || "";
    entry.querySelector('input[name="exp_location[]"]').value = exp.exp_location || "";
    entry.querySelector('input[name="role[]"]').value = exp.role || "";
    entry.querySelector('input[name="years[]"]').value = exp.years || "";
    entry.querySelector('textarea[name="exp_details[]"]').value = exp.details || "";
  }

  function fillProject(entry, proj) {
    entry.querySelector('input[name="project_name[]"]').value = proj.project_name || "";
    entry.querySelector('input[name="technologies[]"]').value = proj.technologies || "";
    entry.querySelector('input[name="proj_dates[]"]').value = proj.proj_dates || "";
    entry.querySelector('textarea[name="proj_summary[]"]').value = proj.proj_summary || "";
  }

  // The main function to populate the entire form with sample data
  function populateForm(data) {
    populatePersonalInfo(data);

    // Education
    const educationContainer = document.querySelector('.repeatable-fields[data-section="education"]');
    addEntries(educationContainer, ".field-entry.template", data.education || [], fillEducation);

    // Experience
    const experienceContainer = document.querySelector('.repeatable-fields[data-section="experience"]');
    addEntries(experienceContainer, ".field-entry.template", data.experience || [], fillExperience);

    // Projects
    const projectsContainer = document.querySelector('.repeatable-fields[data-section="projects"]');
    addEntries(projectsContainer, ".field-entry.template", data.projects || [], fillProject);
  }

  // Attach event listener to Load Sample Data button
  if (loadDataButton) {
    loadDataButton.addEventListener("click", () => {
      populateForm(sampleData);
    });
  }

  // Add button logic to clone template entries on demand
  addButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const sectionName = button.getAttribute("data-add");
      const container = document.querySelector(`.repeatable-fields[data-section="${sectionName}"]`);
      const template = container.querySelector(".field-entry.template");
      if (template) {
        const newEntry = template.cloneNode(true);
        newEntry.style.display = "";
        newEntry.classList.remove("template");

        // Clear input/textarea values
        newEntry.querySelectorAll("input, textarea").forEach((input) => {
          input.value = "";
        });

        container.appendChild(newEntry);
      }
    });
  });




document.body.addEventListener('click', function (e) {
  if (e.target.classList.contains('remove-entry-button')) {
    const entry = e.target.closest('.field-entry');
    if (entry) {
      entry.remove();
    }
  }
});  
});
