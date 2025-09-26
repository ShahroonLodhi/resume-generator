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

  // Function to safely get value from an element, returning empty string if null/undefined
  function safeGetValue(element, property = 'value') {
    return element ? (element[property] || '') : '';
  }

  // Function to safely set value on an element
  function safeSetValue(element, value, property = 'value') {
    if (element) {
      element[property] = value || '';
    }
  }

  // Function to populate personal info and skills - all optional
  function populatePersonalInfo(data) {
    safeSetValue(document.getElementById("name"), data.name);
    safeSetValue(document.getElementById("location"), data.location);
    safeSetValue(document.getElementById("phone"), data.phone);
    safeSetValue(document.getElementById("email"), data.email);
    safeSetValue(document.getElementById("linkedin"), data.linkedin);
    safeSetValue(document.getElementById("github"), data.github);

    // Handle skills safely
    const skillsData = data.skills || {};
    safeSetValue(document.getElementById("languages"), skillsData.languages);
    safeSetValue(document.getElementById("software"), skillsData.software);
  }

  // Generic function to clear non-template entries in a container
  function clearEntries(container) {
    if (container) {
      container.querySelectorAll(".field-entry:not(.template)").forEach((el) => el.remove());
    }
  }

  // Generic function to clone and fill an entry based on a template and data mapping
  function addEntries(container, templateSelector, dataArray, fillCallback) {
    if (!container) return;
    
    clearEntries(container);
    const template = container.querySelector(templateSelector);
    if (!template) return;
    
    // If no data provided, create one empty entry
    const arrayToProcess = (dataArray && dataArray.length > 0) ? dataArray : [{}];
    
    arrayToProcess.forEach((item) => {
      const newEntry = template.cloneNode(true);
      newEntry.style.display = "";
      newEntry.classList.remove("template");
      fillCallback(newEntry, item || {});
      container.appendChild(newEntry);
    });
  }

  // Fill functions for each repeatable section - all fields optional
  function fillEducation(entry, edu) {
    const institutionInput = entry.querySelector('input[name="institution[]"]');
    const locationInput = entry.querySelector('input[name="edu_location[]"]');
    const degreeInput = entry.querySelector('input[name="degree[]"]');
    const datesInput = entry.querySelector('input[name="edu_dates[]"]');
    const gpaInput = entry.querySelector('input[name="gpa[]"]');

    safeSetValue(institutionInput, edu.institution);
    safeSetValue(locationInput, edu.edu_location);
    safeSetValue(degreeInput, edu.degree);
    safeSetValue(datesInput, edu.edu_dates);
    safeSetValue(gpaInput, edu.gpa);
  }

  function fillExperience(entry, exp) {
    const companyInput = entry.querySelector('input[name="company[]"]');
    const locationInput = entry.querySelector('input[name="exp_location[]"]');
    const roleInput = entry.querySelector('input[name="role[]"]');
    const yearsInput = entry.querySelector('input[name="years[]"]');
    const detailsTextarea = entry.querySelector('textarea[name="exp_details[]"]');

    safeSetValue(companyInput, exp.company);
    safeSetValue(locationInput, exp.exp_location);
    safeSetValue(roleInput, exp.role);
    safeSetValue(yearsInput, exp.years);
    safeSetValue(detailsTextarea, exp.details);
  }

  function fillProject(entry, proj) {
    const nameInput = entry.querySelector('input[name="project_name[]"]');
    const techInput = entry.querySelector('input[name="technologies[]"]');
    const datesInput = entry.querySelector('input[name="proj_dates[]"]');
    const summaryTextarea = entry.querySelector('textarea[name="proj_summary[]"]');

    safeSetValue(nameInput, proj.project_name);
    safeSetValue(techInput, proj.technologies);
    safeSetValue(datesInput, proj.proj_dates);
    safeSetValue(summaryTextarea, proj.proj_summary);
  }

  // The main function to populate the entire form with sample data
  function populateForm(data) {
    // All sections are optional - handle missing data gracefully
    populatePersonalInfo(data || {});

    // Education - optional
    const educationContainer = document.querySelector('.repeatable-fields[data-section="education"]');
    addEntries(educationContainer, ".field-entry.template", data.education, fillEducation);

    // Experience - optional
    const experienceContainer = document.querySelector('.repeatable-fields[data-section="experience"]');
    addEntries(experienceContainer, ".field-entry.template", data.experience, fillExperience);

    // Projects - optional
    const projectsContainer = document.querySelector('.repeatable-fields[data-section="projects"]');
    addEntries(projectsContainer, ".field-entry.template", data.projects, fillProject);
  }

  // Attach event listener to Load Sample Data button - optional feature
  if (loadDataButton) {
    loadDataButton.addEventListener("click", () => {
      populateForm(sampleData);
    });
  }

  // Add button logic to clone template entries on demand - always available
  addButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const sectionName = button.getAttribute("data-add");
      const container = document.querySelector(`.repeatable-fields[data-section="${sectionName}"]`);
      
      if (!container) return;
      
      const template = container.querySelector(".field-entry.template");
      if (template) {
        const newEntry = template.cloneNode(true);
        newEntry.style.display = "";
        newEntry.classList.remove("template");

        // Clear input/textarea values to start fresh
        newEntry.querySelectorAll("input, textarea").forEach((input) => {
          input.value = "";
        });

        container.appendChild(newEntry);
      }
    });
  });

  // Remove entry functionality - allows removing even if fields are empty
  document.body.addEventListener('click', function (e) {
    if (e.target.classList.contains('remove-entry-button')) {
      const entry = e.target.closest('.field-entry');
      if (entry && !entry.classList.contains('template')) {
        entry.remove();
      }
    }
  });

  // Make all form fields optional by removing required attributes
  function makeFieldsOptional() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      // Remove any existing required attributes to make all fields optional
      form.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
        field.removeAttribute('required');
      });
      
      // Allow form submission even with empty fields
      form.addEventListener('submit', function(e) {
        // Remove any browser validation that might prevent submission
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
          input.setCustomValidity(''); // Clear any custom validation messages
        });
      });
    });
  }

  // Initialize optional field behavior
  makeFieldsOptional();

  // Re-apply optional field behavior when new entries are added
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        makeFieldsOptional();
      }
    });
  });

  // Start observing for dynamically added form elements
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});
