from flask import Flask, render_template, request, jsonify
import pickle
import re
import logging
import json

app = Flask(__name__)

# Set up logging (optional but recommended)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Data embedded directly in the script
resources_db = {
    # Technical Domains
    "data analyst": {
        "courses": [
            {"name": "IBM Data Analyst", "link": "https://www.coursera.org/professional-certificates/ibm-data-analyst", "platform": "Coursera"},
            {"name": "Excel to MySQL: Analytic Techniques for Business Specialization", "link": "https://www.coursera.org/specializations/excel-mysql", "platform": "Coursera"},
            {"name": "Data Analysis with Python", "link": "https://www.udemy.com/course/data-analysis-with-pandas/", "platform": "Udemy"},
            {"name": "Data Analysis and Visualization Fundamentals", "link": "https://www.edx.org/certificates/professional-certificate/ibm-data-analysis-and-visualization-fundamentals", "platform": "edX"}
        ],
        "videos": [
            {"name": "Data Analyst Full Course", "link": "https://www.youtube.com/playlist?list=PLOWRNl6YgsT79ezWdEhOjvK4D-cQfr7ys", "platform": "YouTube"},
            {"name": "Introduction to Data Analysis", "link": "https://www.youtube.com/playlist?list=PLRueFtKLr0QN7MmQ8pdpQerOe_s8vGJG4", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Build Foundational Skills", "description": "Start with mathematics and statistics fundamentals. Learn Excel for data manipulation and basic analysis."},
            {"step": "Step 2: Learn Data Analysis Tools", "description": "Master SQL for database querying and Python (with Pandas, NumPy) for data analysis and manipulation."},
            {"step": "Step 3: Data Visualization", "description": "Focus on data visualization techniques using tools like Matplotlib, Seaborn (Python), or Tableau to effectively communicate insights."},
            {"step": "Step 4: Practice with Projects", "description": "Work on real-world data analysis projects to build a portfolio. Participate in Kaggle competitions or find datasets online."},
            {"step": "Step 5: Advanced Techniques & Specialization", "description": "Explore advanced statistical methods, machine learning basics, and consider specializing in areas like business intelligence or data warehousing."}
        ]
    },
    "software engineer": {
        "courses": [
            {"name": "Software Engineering Master Track", "link": "https://www.coursera.org/professional-certificates/devops-and-software-engineering", "platform": "Coursera"},
            {"name": "CS50's Introduction to Computer Science", "link": "https://www.edx.org/course/introduction-computer-science-harvardx-cs50x", "platform": "edX"},
            {"name": "Clean Code: Writing Code for Humans", "link": "https://www.udemy.com/course/writing-clean-code/", "platform": "Udemy"},
            {"name": "Full Stack Web Development", "link": "https://www.guvi.in/blog/best-full-stack-development-online-courses/", "platform": "Coursera"}
        ],
        "videos": [
            {"name": "Software Engineering Playlist", "link": "https://youtu.be/BDsCCtFl8WE", "platform": "YouTube"},
            {"name": "Clean Code Explained", "link": "https://youtu.be/7EmboKQH8lM", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Fundamentals of Programming", "description": "Start with a foundational programming language like Python, Java, or C++. Understand data structures and algorithms."},
            {"step": "Step 2: Learn Software Development Principles", "description": "Study software design patterns, SOLID principles, and understand different software development methodologies (Agile, Waterfall)."},
            {"step": "Step 3: Web Development Basics", "description": "Learn HTML, CSS, and JavaScript for frontend development. Explore backend technologies like Node.js, Python/Flask, or Java/Spring."},
            {"step": "Step 4: Version Control and Collaboration", "description": "Master Git for version control and learn collaborative coding practices. Contribute to open-source projects on platforms like GitHub."},
            {"step": "Step 5: Specialization and Advanced Topics", "description": "Choose a specialization like web development, mobile development, game development, or DevOps. Explore advanced topics like cloud computing, system design, and cybersecurity."}
        ]
    },
    "data scientist": {
        "courses": [
            {"name": "Data Science Specialization", "link": "https://www.coursera.org/specializations/jhu-data-science", "platform": "Coursera"},
            {"name": "Python for Data Science", "link": "https://cdss.berkeley.edu/dsus/academics/class-enrollment-info", "platform": "edX"},
            {"name": "Advanced Data Analysis", "link": "https://www.reddit.com/r/dataanalysis/comments/12lyue5/review_of_google_advanced_data_analysis/", "platform": "Udemy"}
        ],
        "videos": [
            {"name": "Data Science with Python", "link": "https://youtu.be/mkv5mxYu0Wk?si=OlXRgf-yO8mQwKOm", "platform": "YouTube"},
            {"name": "Statistics for Data Science", "link": "https://www.youtube.com/watch?v=xxpc-HPKN28", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Statistical Foundations", "description": "Develop a strong base in statistics and probability theory. Learn statistical modeling and inference techniques."},
            {"step": "Step 2: Programming for Data Science", "description": "Master Python and R programming languages. Focus on libraries like Pandas, NumPy, Scikit-learn, and TensorFlow/PyTorch."},
            {"step": "Step 3: Machine Learning Fundamentals", "description": "Learn core machine learning algorithms (regression, classification, clustering). Understand model evaluation and validation."},
            {"step": "Step 4: Data Wrangling and Visualization", "description": "Gain expertise in data cleaning, preprocessing, feature engineering, and data visualization using tools like Seaborn and Tableau."},
            {"step": "Step 5: Advanced Machine Learning & Specialization", "description": "Explore advanced machine learning topics like deep learning, natural language processing, or computer vision. Consider specializing in a domain like healthcare or finance."}
        ]
    },
     "aiml engineer": {
        "courses": [
            {"name": "Machine Learning Specialization", "link": "https://www.coursera.org/specializations/machine-learning", "platform": "Coursera"},
            {"name": "Deep Learning Specialization", "link": "https://www.coursera.org/specializations/deep-learning", "platform": "Coursera"},
            {"name": "AI for Everyone", "link": "https://www.coursera.org/learn/ai-for-everyone", "platform": "Coursera"}
        ],
        "videos": [
            {"name": "Machine Learning Fundamentals", "link": "https://www.uopeople.edu/blog/machine-learning-courses/", "platform": "Uopeople"},
            {"name": "Deep Learning Basics", "link": "https://www.youtube.com/watch?v=aircAruvnKk", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Mathematical and Programming Foundations", "description": "Strengthen your understanding of linear algebra, calculus, and probability. Master Python programming and essential libraries."},
            {"step": "Step 2: Machine Learning Core Concepts", "description": "Learn fundamental machine learning algorithms and concepts (supervised, unsupervised learning, model selection, evaluation)."},
            {"step": "Step 3: Deep Learning Techniques", "description": "Dive into neural networks, deep learning architectures (CNNs, RNNs), and frameworks like TensorFlow or PyTorch."},
            {"step": "Step 4: AI/ML Project Experience", "description": "Work on practical AI/ML projects to apply your knowledge and build a portfolio. Participate in hackathons and contribute to AI communities."},
            {"step": "Step 5: Specialization and Research", "description": "Specialize in areas like computer vision, NLP, reinforcement learning, or ethical AI. Stay updated with the latest research and advancements in the field."}
        ]
    },
    "ui/ux designer": {
        "courses": [
            {"name": "Google UX Design Professional Certificate", "link": "https://www.coursera.org/professional-certificates/google-ux-design", "platform": "Coursera"},
            {"name": "UI/UX Design Specialization", "link": "https://www.coursera.org/specializations/ui-ux-design", "platform": "Coursera"},
            {"name": "Adobe XD Masterclass", "link": "https://www.simplilearn.com/free-adobe-xd-course-skillup", "platform": "Simplilearn"}
        ],
        "videos": [
            {"name": "UI/UX Design Fundamentals", "link": "https://designlab.com/blog/best-ux-design-course-online", "platform": "DesignLab"},
            {"name": "Design Thinking Process", "link": "https://www.youtube.com/watch?v=_r0VX-aU_T8", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Design Principles and Fundamentals", "description": "Learn basic design principles (typography, color theory, layout). Understand user-centered design and design thinking."},
            {"step": "Step 2: UI/UX Design Tools", "description": "Master UI/UX design tools like Figma, Adobe XD, or Sketch. Practice creating wireframes, prototypes, and mockups."},
            {"step": "Step 3: User Research and Testing", "description": "Learn user research methodologies (user interviews, surveys, usability testing). Understand how to gather and analyze user feedback."},
            {"step": "Step 4: Portfolio Building", "description": "Create a strong portfolio showcasing your UI/UX design projects. Include case studies demonstrating your design process and problem-solving skills."},
            {"step": "Step 5: Advanced UX Topics & Specialization", "description": "Explore advanced UX topics like interaction design, information architecture, accessibility, and UX writing. Consider specializing in mobile UX, web UX, or specific industries."}
        ]

    },
    # Non-Tech Domains
    "digital marketer": {
        "courses": [
            {"name": "Digital Marketing Specialization", "link": "https://www.coursera.org/specializations/digital-marketing", "platform": "Coursera"},
            {"name": "Google Digital Marketing Certification", "link": "https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing", "platform": "Google"},
            {"name": "SEO for Beginners", "link": "https://www.coursera.org/learn/seo-fundamentals", "platform": "Coursesera"}
        ],
        "videos": [
            {"name": "Introduction to Digital Marketing", "link": "https://www.youtube.com/watch?v=DvwS7cV9GmQ", "platform": "YouTube"},
            {"name": "Content Marketing Strategy", "link": "https://academy.hubspot.com/courses/content-marketing", "platform": "HubSpot Academy"}
        ],
        "roadmap": [
            {"step": "Step 1: Digital Marketing Fundamentals", "description": "Understand core digital marketing concepts (SEO, SEM, content marketing, social media, email marketing)."},
            {"step": "Step 2: Learn Key Marketing Channels", "description": "Deepen your knowledge in specific channels like SEO (on-page, off-page, technical SEO), paid advertising (Google Ads, social media ads), and social media marketing."},
            {"step": "Step 3: Marketing Analytics and Tools", "description": "Master marketing analytics tools like Google Analytics to track campaign performance and make data-driven decisions. Learn about CRM and marketing automation tools."},
            {"step": "Step 4: Content Strategy and Creation", "description": "Develop content strategy skills and learn to create engaging content for different platforms (blog posts, social media content, videos)."},
            {"step": "Step 5: Specialization and Industry Trends", "description": "Specialize in areas like social media marketing, SEO, content marketing, or email marketing. Stay updated with the latest digital marketing trends and algorithm updates."}
        ]
    },
    "content writer": {
        "courses": [
            {"name": "Creative Writing Specialization", "link": "https://www.coursera.org/specializations/creative-writing", "platform": "Coursera"},
            {"name": "Writing for the Web", "link": "https://www.linkedin.com/learning/writing-for-the-web/welcome?u=229219690", "platform": "LinkedIN Learning"},
            {"name": "Copywriting for Beginners", "link": "https://www.udemy.com/course/copywriting-secrets/", "platform": "Udemy"}
        ],
        "videos": [
            {"name": "Content Writing Tips", "link": "https://youtu.be/8BdZ0dUu7VQ?si=iEpjVm92wnLDRnRT", "platform": "YouTube"},
            {"name": "How to Write Blog Posts", "link": "https://youtu.be/Q8rN3JKqUc8?si=xUJTLqwgB7gyb6LV", "platform": "YouTube"}
        ],
         "roadmap": [
            {"step": "Step 1: Writing Fundamentals and Grammar", "description": "Master grammar, punctuation, and sentence structure. Practice writing in different styles and tones."},
            {"step": "Step 2: Content Writing Techniques", "description": "Learn SEO writing, copywriting, storytelling, and content strategy basics. Understand how to write for different online platforms."},
            {"step": "Step 3: Content Creation Tools and Platforms", "description": "Become proficient with content management systems (CMS) like WordPress, writing tools, and SEO tools."},
            {"step": "Step 4: Build a Writing Portfolio", "description": "Create a portfolio of your writing samples. Write guest posts, contribute to blogs, or create a personal writing website."},
            {"step": "Step 5: Specialization and Niche Writing", "description": "Specialize in a niche like technical writing, SEO writing, copywriting, or content marketing. Develop expertise in a specific industry."}
        ]
    },
    "graphic designer": {
        "courses": [
            {"name": "Graphic Design Specialization", "link": "https://www.coursera.org/specializations/graphic-design", "platform": "Coursera"},
            {"name": "Adobe Photoshop for Beginners", "link": "https://www.udemy.com/course/adobe-photoshop-course/", "platform": "Udemy"},
            {"name": "Canva Design Basics", "link": "https://youtu.be/J0jE0OsF1zo?si=oWns6lUKPse1bS3-", "platform": "YouTube"}
        ],
        "videos": [
            {"name": "Graphic Design Basics", "link": "https://youtu.be/GQS7wPujL2k?si=sC9Ccf3TFpPDN7nD", "platform": "YouTube"},
            {"name": "Color Theory for Designers", "link": "https://youtu.be/7iY4QFqTlpE?si=upcYDDRGXgz4zyVb", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Design Principles and Visual Communication", "description": "Learn fundamental design principles (composition, typography, color theory, visual hierarchy). Understand visual communication concepts."},
            {"step": "Step 2: Graphic Design Software", "description": "Master graphic design software like Adobe Photoshop, Illustrator, and InDesign. Learn vector and raster graphics."},
            {"step": "Step 3: Design Projects and Portfolio Building", "description": "Work on various graphic design projects (logos, brochures, website layouts). Create a portfolio showcasing your design skills and style."},
            {"step": "Step 4: Branding and Visual Identity", "description": "Learn about branding principles, visual identity design, and how to create brand guidelines."},
            {"step": "Step 5: Specialization and Design Trends", "description": "Specialize in areas like branding, web design, print design, or motion graphics. Stay updated with current design trends and software updates."}
        ]
    },
     "financial analyst": {
        "courses": [
            {"name": "Financial Analyst Certification Program", "link": "https://www.khanacademy.org/economics-finance-domain/core-finance", "platform": "Khan Academy"},
            {"name": "Investment Management Specialization", "link": "https://www.coursera.org/specializations/investment-management", "platform": "Coursera"},
            {"name": "Excel for Finance", "link": "https://www.udemy.com/course/excel-for-finance-and-accounting/", "platform": "Udemy"}
        ],
        "videos": [
            {"name": "Introduction to Financial Analysis", "link": "https://youtu.be/Fi1wkUczuyk?si=d2Vt0N0dqxPG3W6z", "platform": "YouTube"},
            {"name": "Understanding Financial Statements", "link": "https://youtu.be/mnJDA3YXL9g?si=q0uuPW7fyyqEvmwM", "platform": "YouTube"}
        ],
         "roadmap": [
            {"step": "Step 1: Financial Accounting and Principles", "description": "Learn the fundamentals of financial accounting, financial statements (balance sheet, income statement, cash flow statement), and accounting principles."},
            {"step": "Step 2: Financial Modeling and Analysis", "description": "Master financial modeling techniques using Excel. Learn financial ratio analysis, forecasting, and valuation methods."},
            {"step": "Step 3: Investment Analysis and Portfolio Management", "description": "Study investment analysis, portfolio theory, asset valuation, and investment strategies. Understand different asset classes."},
            {"step": "Step 4: Industry Knowledge and Specialization", "description": "Gain industry-specific knowledge in areas like corporate finance, investment banking, asset management, or equity research."},
            {"step": "Step 5: Certification and Professional Development", "description": "Consider pursuing certifications like CFA (Chartered Financial Analyst) or CFP (Certified Financial Planner). Stay updated with financial market trends and regulations."}
        ]
    },
    "cybersecurity specialist": {
        "courses": [
            {"name": "Cybersecurity Specialization", "link": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst", "platform": "Coursera"},
            {"name": "Certified Ethical Hacker (CEH)", "link": "https://www.eccouncil.org/trainings/certified-ethical-hacker/", "platform": "EC-Council"}
        ],
        "videos": [
            {"name": "Introduction to Cybersecurity", "link": "https://youtu.be/z5nc9MDbvkw?si=H0XgtqET9NC-lgc9", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: IT Fundamentals and Networking", "description": "Build a strong foundation in IT fundamentals, computer networking, and operating systems (Windows, Linux)."},
            {"step": "Step 2: Cybersecurity Basics", "description": "Learn cybersecurity concepts, threats, vulnerabilities, and security principles. Understand different domains of cybersecurity."},
            {"step": "Step 3: Security Tools and Technologies", "description": "Become proficient with security tools like Wireshark, Nmap, Metasploit, and SIEM systems. Learn about firewalls, intrusion detection/prevention systems."},
            {"step": "Step 4: Ethical Hacking and Penetration Testing", "description": "Study ethical hacking methodologies and penetration testing techniques. Practice in virtual labs and capture-the-flag (CTF) challenges."},
            {"step": "Step 5: Specialization and Certifications", "description": "Specialize in areas like network security, application security, incident response, or threat intelligence. Pursue industry certifications like CompTIA Security+, CEH, or CISSP."}
        ]
    },
    "cybersecurity": {
        "courses": [
            {"name": "Cybersecurity Specialization", "link": "https://www.coursera.org/professional-certificates/ibm-cybersecurity-analyst", "platform": "Coursera"},
            {"name": "Certified Ethical Hacker (CEH)", "link": "https://www.eccouncil.org/trainings/certified-ethical-hacker/", "platform": "EC-Council"}
        ],
        "videos": [
            {"name": "Introduction to Cybersecurity", "link": "https://youtu.be/z5nc9MDbvkw?si=H0XgtqET9NC-lgc9", "platform": "YouTube"}
        ],
         "roadmap": [
            {"step": "Step 1: IT Fundamentals and Networking", "description": "Build a strong foundation in IT fundamentals, computer networking, and operating systems (Windows, Linux)."},
            {"step": "Step 2: Cybersecurity Basics", "description": "Learn cybersecurity concepts, threats, vulnerabilities, and security principles. Understand different domains of cybersecurity."},
            {"step": "Step 3: Security Tools and Technologies", "description": "Become proficient with security tools like Wireshark, Nmap, Metasploit, and SIEM systems. Learn about firewalls, intrusion detection/prevention systems."},
            {"step": "Step 4: Ethical Hacking and Penetration Testing", "description": "Study ethical hacking methodologies and penetration testing techniques. Practice in virtual labs and capture-the-flag (CTF) challenges."},
            {"step": "Step 5: Specialization and Certifications", "description": "Specialize in areas like network security, application security, incident response, or threat intelligence. Pursue industry certifications like CompTIA Security+, CEH, or CISSP."}
        ]
    },
    "cloud engineer": {
        "courses": [
            {"name": "Google Cloud Professional Cloud Architect", "link": "https://www.pluralsight.com/cloud-guru", "platform": "PLURALSIGHT"},
            {"name": "AWS Certified Solutions Architect", "link": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "platform": "AWS"}
        ],
        "videos": [
            {"name": "AWS Basics", "link": "https://youtu.be/k1RI5locZE4?si=HcRDvpe7rfDWwLMZ", "platform": "YouTube"}
        ],
          "roadmap": [
            {"step": "Step 1: IT Infrastructure and Networking", "description": "Understand IT infrastructure concepts (servers, storage, virtualization). Learn networking fundamentals (TCP/IP, DNS, routing)."},
            {"step": "Step 2: Cloud Computing Fundamentals", "description": "Learn about cloud computing models (IaaS, PaaS, SaaS), cloud service providers (AWS, Azure, GCP), and cloud deployment models."},
            {"step": "Step 3: Cloud Platform Skills (AWS, Azure, GCP)", "description": "Choose a cloud platform (AWS, Azure, or GCP) and gain hands-on experience with its services (compute, storage, networking, databases)."},
            {"step": "Step 4: DevOps and Automation", "description": "Learn DevOps practices, infrastructure as code (IaC) using tools like Terraform or CloudFormation, and automation using scripting and CI/CD pipelines."},
            {"step": "Step 5: Specialization and Certifications", "description": "Specialize in areas like cloud architecture, cloud security, DevOps, or serverless computing. Pursue cloud certifications from AWS, Azure, or GCP."}
        ]
    },
    "blockchain developer": {
        "courses": [
            {"name": "Blockchain Specialization", "link": "https://www.coursera.org/specializations/blockchain", "platform": "Coursera"},
            {"name": "Ethereum and Solidity", "link": "https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/", "platform": "Udemy"}
        ],
        "videos": [
            {"name": "Blockchain Basics", "link": "https://www.youtube.com/watch?v=SSo_EIwHSd4", "platform": "YouTube"}
        ],
        "roadmap": [
            {"step": "Step 1: Programming and Cryptography Basics", "description": "Strengthen your programming skills (especially in languages like JavaScript, Python, or Go). Learn cryptography fundamentals (hashing, encryption, digital signatures)."},
            {"step": "Step 2: Blockchain Fundamentals", "description": "Understand blockchain technology, distributed ledgers, consensus mechanisms, and smart contracts. Learn about different types of blockchains (public, private, consortium)."},
            {"step": "Step 3: Smart Contract Development", "description": "Learn smart contract development using Solidity (for Ethereum) or other relevant languages. Understand smart contract security and testing."},
            {"step": "Step 4: Blockchain Platforms and Tools", "description": "Gain experience with blockchain platforms like Ethereum, Hyperledger Fabric, or Corda. Explore blockchain development tools and frameworks."},
            {"step": "Step 5: Specialization and Decentralized Applications (DApps)", "description": "Specialize in areas like DApp development, DeFi (Decentralized Finance), NFTs (Non-Fungible Tokens), or blockchain security. Stay updated with blockchain innovations and trends."}
        ]
    }
}

job_openings = {
        "data analyst": [
        {"title": "Data Analyst", "link": "https://www.foundit.in/job/data-analyst-lynk-delhi-31205430?utm_campaign=google_jobs_apply", "company": "Energy Aspects"},
        {"title": "Senior Data Analyst", "link": "https://in.trabajo.org/job-3150-44553ee01fde049f939d8de7f0c0a902?utm_campaign=google_jobs_apply", "company": "Wipro"}
    ],
    "software engineer": [
        {"title": "Software Engineer", "link": "https://www.coursera.org/articles/software-engineer?form=MG0AV3", "company": "Acme Corp"},
        {"title": "Senior Software Engineer", "link": "https://www.theforage.com/blog/careers/software-engineering-resources?form=MG0AV3", "company": "Beta Co"}
    ],
    "data scientist": [
        {"title": "Data Scientist", "link": "https://www.coursera.org/specializations/jhu-data-science?form=MG0AV3", "company": "Gamma Inc"},
        {"title": "Senior Data Scientist", "link": "https://www.edx.org/certificates/professional-certificate/harvardx-data-science?form=MG0AV3", "company": "Delta Co"}
    ],
   "digital marketer": [
        {"title": "Digital Marketing Specialist", "link": "https://academy.hubspot.com/courses/digital-marketing?form=MG0AV3", "company": "MarketingPro"},
        {"title": "SEO Analyst", "link": "https://moz.com/beginners-guide-to-seo?form=MG0AV3", "company": "SearchTech"}
    ],
    "content writer": [
        {"title": "Content Writer", "link": "https://contentmarketinginstitute.com/articles/writing-examples-tools-tips/?form=MG0AV3", "company": "WriteWell"},
        {"title": "Copywriter", "link": "https://www.henryharvin.com/blog/content-writing-platforms/", "company": "AdText"}
    ],
    "graphic designer": [
        {"title": "Graphic Designer", "link": "https://www.timechamp.io/blogs/explore-the-top-10-freelance-graphic-design-websites/", "company": "DesignHub"},
        {"title": "Creative Visualizer", "link": "https://365datascience.com/trending/data-visualization-project-ideas/", "company": "VisualWorks"}
    ],
      "financial analyst": [
        {"title": "Financial Analyst", "link": "https://romeromentoring.com/financial-analyst-skills/", "company": "FinCorp"},
        {"title": "Investment Analyst", "link": "https://www.ollusa.edu/blog/financial-analyst-skills.html", "company": "InvestWell"}
    ],
    "cybersecurity specialist": [
        {"title": "Cybersecurity Analyst", "link": "https://www.infosectrain.com/courses/cybersecurity-analyst-training/", "company": "SecureTech"},
        {"title": "Penetration Tester", "link": "https://www.coursera.org/in/articles/how-to-become-a-penetration-tester", "company": "CyberProtect"}
    ],
     "cybersecurity": [
        {"title": "Cybersecurity Analyst", "link": "https://www.infosectrain.com/courses/cybersecurity-analyst-training/", "company": "SecureTech"},
        {"title": "Penetration Tester", "link": "https://www.coursera.org/in/articles/how-to-become-a-penetration-tester", "company": "CyberProtect"}
    ],
    "cloud engineer": [
        {"title": "Cloud Architect", "link": "https://www.coursera.org/articles/how-to-become-a-cloud-architect", "company": "Cloudify"},
        {"title": "DevOps Engineer", "link": "https://www.geeksforgeeks.org/devops-engineer-skills/", "company": "BuildTech"}
    ],
     "blockchain developer": [
        {"title": "Blockchain Engineer", "link": "https://www.gsdcouncil.org/blogs/blockchain-developer-skills", "company": "LedgerTech"},
        {"title": "Smart Contract Developer", "link": "https://www.techtarget.com/searchcio/tip/How-to-become-a-smart-contract-developer", "company": "CryptoHub"}
    ]
}

job_titles = set(job_openings.keys())

# Load the trained ML model if available (optional)
def load_model():
    try:
        with open('emails.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        logging.warning("No ML model found. Using basic logic.")
        return None

model = load_model()
# Load translations from JSON
try:
    with open('translations.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
except FileNotFoundError:
    logging.error("translations.json not found!")
    translations = {}

# Updated placeholder translation function
def translate_text(text, target_language):
    if target_language in translations and text in translations[target_language]:
        return translations[target_language][text]
    return text # Return original if translation not found


@app.route('/')
def index():
    """Render the main input page."""
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict resources based on user input."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        role = data.get('role', '').strip().lower()
        skills = [skill.strip().lower() for skill in data.get('skills', '').split(',') if skill.strip()] if data.get('skills') else []
        skill_gaps = data.get('skill_gaps', '').strip().lower()
        career_ambitions = data.get('career_ambitions', '').strip().lower()
        language = data.get('language', '').strip().lower()  # Get language from the request

        # Combine inputs to determine resources
        recommendations = {"courses": [], "videos": [], "jobs": [], "roadmap": []}
        # Combine inputs into one single string to search within resources_db
        combined_inputs_string = ' '.join(skills + [role, skill_gaps, career_ambitions]).strip()

        # Create regex patterns for all resource keys
        resource_patterns = {key: re.compile(r'\b' + re.escape(key) + r'\b') for key in resources_db}

        # Search resources based on input words/phrases
        for resource_key, pattern in resource_patterns.items():
            if pattern.search(combined_inputs_string):
                recommendations["courses"].extend(resources_db[resource_key]["courses"])
                recommendations["videos"].extend(resources_db[resource_key]["videos"])
                recommendations["roadmap"].extend(resources_db[resource_key]["roadmap"]) # Add roadmap

        # Search job openings based on exact matches of job titles
        job_title_patterns = {key: re.compile(r'\b' + re.escape(key) + r'\b') for key in job_titles}
        for job_title, pattern in job_title_patterns.items():
             if pattern.search(combined_inputs_string):
                 recommendations["jobs"].extend(job_openings[job_title])

        # Remove duplicates
        recommendations["courses"] = list({v["name"]: v for v in recommendations["courses"]}.values())
        recommendations["videos"] = list({v["name"]: v for v in recommendations["videos"]}.values())
        recommendations["jobs"] = list({v["title"]: v for v in recommendations["jobs"]}.values())
        recommendations["roadmap"] = list({v["step"]: v for v in recommendations["roadmap"]}.values()) # Remove duplicate roadmap steps

        # Translate content
        for course in recommendations["courses"]:
            course["name"] = translate_text(course["name"], language)
        for video in recommendations["videos"]:
            video["name"] = translate_text(video["name"], language)
        for job in recommendations["jobs"]:
            job["title"] = translate_text(job["title"], language)
        for step in recommendations["roadmap"]:
            step["step"] = translate_text(step["step"], language)
            step["description"]= translate_text(step["description"],language)


        # Example of how to use the language input (e.g., display message)
        if language:
            recommendations['message'] = f"{translate_text('Resources tailored for you in', language)} {language}!"
        else:
            recommendations['message'] = "ML model unavailable, using basic logic!"

        return jsonify(recommendations)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)