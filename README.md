
# LinkedIn Job Scraper

### 🚀 **About the Project**

This project is a Python application that uses Selenium and WebDriver to extract job postings from LinkedIn. Users can specify the type of jobs they want to extract, and the program will collect information such as the job title, company name, location, job type, seniority, number of applicants, and the posting URL. The extracted data is stored in a SQL Server database for further analysis.

---

### ⚙️ **Features**

- Automated login to LinkedIn.
- Simulated human-like behavior to avoid detection by LinkedIn's anti-bot measures.
- Extraction of detailed job information, including:
  - Job title
  - Company name
  - Location
  - Employment type
  - Seniority level
  - Number of applicants
  - Posting URL
- Data storage in a SQL Server database.

---

### 🛠️ **Technologies Used**

- **Python**
  - Libraries: `selenium`, `pandas`, `sqlalchemy`, `logging`
- **Database**
  - SQL Server (with ODBC Driver 17)
- **Web Scraping**
  - Selenium WebDriver for dynamic content extraction.

---

### 📄 **Workflow**

1. **Login to LinkedIn:**
   - Automates login to LinkedIn using provided credentials.
   - Simulates human-like delays to avoid detection.

2. **Navigate to Job Listings:**
   - Accesses a specified LinkedIn job search page.

3. **Extract Job Information:**
   - Scrapes job details such as title, company, location, seniority, and more.
   - Ensures duplicate jobs are not added to the database.

4. **Store Data:**
   - Saves extracted job details to a SQL Server database.

---

### 🧩 **How to Run**

#### Prerequisites
- Python 3.8 or higher
- Chrome browser and ChromeDriver installed
- SQL Server database configured
- LinkedIn account with valid credentials
- Required dependencies installed:

```bash
pip install selenium pandas sqlalchemy
```

#### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/YourUsername/linkedin_job_scraper.git
   cd linkedin_job_scraper
   ```

2. Set up your database:
   - Create a database in SQL Server.
   - Update the connection string in the script:
     ```python
     db_host = "your_database_host"
     db_name = "your_database_name"
     table_name = "your_table_name"
     ```

3. Configure the script:
   - Set your LinkedIn credentials in the script:
     ```python
     email_usuario = "your_email"
     senha_usuario = "your_password"
     ```
   - Update the path to ChromeDriver:
     ```python
     driver_path = "path_to_chromedriver"
     ```

4. Run the script:
   ```bash
   python main.py
   ```

---

### 📊 **Project Demonstration**

Example of extracted data:

| Title                | Company         | Location         | Type      | Seniority     | Applicants | URL                            | Extraction Date |
|----------------------|-----------------|------------------|-----------|---------------|------------|--------------------------------|-----------------|
| Data Analyst         | Example Corp   | Remote           | Full-time | Mid-level     | 50+        | [Link](#)                      | 2024-12-05      |
| Business Consultant  | Another Corp   | New York, NY     | Part-time | Senior-level  | 20-50      | [Link](#)                      | 2024-12-05      |

---

### 📝 **What You Can Learn from This Project**

- **Web Automation with Selenium:**
  - Logging in and navigating dynamically loaded pages.
- **Data Extraction Techniques:**
  - Using CSS selectors and XPath to target web elements.
- **Database Integration:**
  - Storing scraped data in a structured format for further analysis.
- **Error Handling:**
  - Managing timeouts, missing elements, and stale references.

---

### 🔧 **Potential Improvements**

- Add support for extracting jobs from multiple pages or different LinkedIn job searches.
- Implement a more sophisticated method to avoid detection (e.g., rotating proxies).
- Create a user interface to make job selection easier.
- Integrate the database with a dashboarding tool like Power BI or Tableau.

---

### 📬 **Contact**

Feel free to reach out if you have any questions or suggestions:

- **GitHub:** [OscarFantozzi](https://github.com/OscarFantozzi)
- **LinkedIn:** [Oscar Fantozzi](https://linkedin.com/in/oscarfantozzi)

