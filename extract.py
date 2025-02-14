import csv
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import string
from tqdm import tqdm

fake = Faker()


def sanitize_text(text):
    """Removes newlines, extra spaces, and ensures proper formatting."""
    return text.replace('\n', ' ').replace('\r', ' ').replace(',', ' ').strip()


def generate_employee_data(num_employees=1000):
    with open("cleaned_employee_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "employee_id", "first_name", "last_name", "email", "phone_number", "address", "birthdate", 
            "hire_date", "job_title", "department", "salary", "password"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        
        writer.writeheader()

        for _ in tqdm(range(num_employees), desc="Generating Employee Data"):
            first_name = sanitize_text(fake.first_name())
            last_name = sanitize_text(fake.last_name())
            email = sanitize_text(fake.email())
            phone_number = sanitize_text(fake.phone_number())
            address = sanitize_text(fake.address())  # Clean address field
            birthdate = fake.date_of_birth(minimum_age=22, maximum_age=65)
            hire_date = fake.date_between(start_date=birthdate + timedelta(days=18*365), end_date="today")
            job_title = sanitize_text(fake.job())  # Remove any unwanted characters
            department = random.choice(["Sales", "Marketing", "Engineering", "HR", "Finance", "IT"])
            salary = random.randint(40000, 150000)
            employee_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            password = sanitize_text(fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True))
            
            writer.writerow({
                "employee_id": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "birthdate": birthdate.strftime('%Y-%m-%d'),
                "hire_date": hire_date.strftime('%Y-%m-%d'),
                "job_title": job_title,
                "department": department,
                "salary": salary,
                "password": password
            })

    df = pd.read_csv("cleaned_employee_data.csv", encoding="utf-8")  # Read to confirm structure
    return df


if __name__ == "__main__":
    num_employees = 1000
    df = generate_employee_data(num_employees)

    print(f"Generated {num_employees} cleaned employee records and saved to cleaned_employee_data.csv")
    print(df.head())
