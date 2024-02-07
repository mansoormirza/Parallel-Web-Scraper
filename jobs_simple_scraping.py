import mysql.connector
import requests
from bs4 import BeautifulSoup
import time

# Function to create the 'jobs' table in MySQL
def create_jobs_table_simple():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='jobs'
    )

    cursor = conn.cursor()

    # Define the SQL query to create the 'jobs' table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS simple_jobs (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Company_Name VARCHAR(255),
        Required_Skills LONGTEXT,
        More_Info LONGTEXT
    )
    """

    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Function to save job listings to MySQL
def save_to_mysql_simple(job_listings):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='jobs'
    )

    cursor = conn.cursor()

    for job in job_listings:
        company_name = job['Company Name']
        required_skills = job['Required Skills']
        more_info = job['More Info']

        # Define the SQL insert query to save the data in the 'jobs' table
        insert_query = "INSERT INTO simple_jobs (company_name, required_skills, more_info) VALUES (%s, %s, %s)"
        values = (company_name, required_skills, more_info)

        cursor.execute(insert_query, values)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

# Function to find jobs
def find_jobs(url, skills_to_filter):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    job_listings = []
    
    for job in jobs:
        job_date = job.find('span', class_='sim-posted').span.text
        if 'few' in job_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            skills = job.find('span', class_='srp-skills').text.strip()
            more_info = job.header.h2.a['href']

            skills_matched = [skill for skill in skills_to_filter if skill.lower() in skills.lower()]

            if not skills_matched:
                job_listings.append({
                    'Company Name': company_name,
                    'Required Skills': skills,
                    'More Info': more_info
                })

    return job_listings

# Function to scrape all pages
def scrape_pages_simple(num_pages, skills_to_filter):
    job_listings = []
    for page_number in range(1, num_pages + 1):
        base_url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='
        page_url = f'{base_url}&sequence={page_number}&startPage=1'
        print(f'Scraping page {page_number}')
        job_listings.extend(find_jobs(page_url, skills_to_filter))
    return job_listings


