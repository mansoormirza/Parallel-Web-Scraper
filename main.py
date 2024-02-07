import mysql.connector
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
from functools import partial
from jobs_parallel_scraping import create_jobs_table_parallel, save_to_mysql_parallel, scrape_page_parallel
from jobs_simple_scraping import create_jobs_table_simple, save_to_mysql_simple, scrape_pages_simple
from retrieve_data import display_table_data

if __name__ == '__main__':

    while True:
        print("\nChoose scraping type:")
        print("1. Simple Scraping")
        print("2. Parallel Scraping")
        print("3. Display Database Data")
        choice = input("Enter your choice (1, 2 or 3): ")

        if choice == "1":

            num_pages = int(input("Enter the number of pages to scrape: "))
            print("Put Some Skills to Filter Out (comma-separated):")
            skills_input = input('>')
            print("Filtering out Skills")
            skills_to_filter = [skill.strip() for skill in skills_input.split(',')]
            create_jobs_table_simple()
            start_time = time.time()
            job_listings = scrape_pages_simple(num_pages, skills_to_filter)
            save_to_mysql_simple(job_listings)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f'All pages scraped and saved in the table simple_jobs in database jobs!')
            print(f'Total time taken: {elapsed_time} seconds')
            # break  # Exit the loop if the code reaches here

        elif choice == "2":

            num_pages = int(input("Enter the number of pages to scrape: "))
            print("Put Some Skills to Filter Out (comma-separated):")
            skills_input = input('>')
            print("Filtering out Skills")
            skills_to_filter = [skill.strip() for skill in skills_input.split(',')]
            create_jobs_table_parallel()
            start_time = time.time()

            # Create a pool of worker processes
            with Pool() as pool:
                partial_scrape_page = partial(scrape_page_parallel, skills_to_filter=skills_to_filter)
                results = pool.map(partial_scrape_page, range(1, num_pages + 1))

            # Flatten the results list and include base URL data
            job_listings = [job for result in results for job in result]
            save_to_mysql_parallel(job_listings)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f'All pages scraped and saved in the table parallel_jobs in database jobs!')
            print(f'Total time taken: {elapsed_time} seconds')

        elif choice == "3":
            while True:
                print("\nChoose a table to display:")
                print("1. Simple Jobs (simple_jobs)")
                print("2. Parallel Jobs (parallel_jobs)")
                choice = input("Enter your choice (1 or 2): ")
                if choice == '1':
                    table_name = 'simple_jobs'
                    break 

                elif choice == '2':
                    table_name = 'parallel_jobs'
                    break 
                else:
                    print("\nInvalid choice\n")
                # Display data in the chosen table
            display_table_data(table_name)   
        else:
            print('\nWrong Option Selected, select the right option!\n')
