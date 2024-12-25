import csv
import os
from flask import render_template, current_app
from datetime import datetime, timedelta
import secrets
import string
import random

def render_page(template_name, page_title, **context):
    return render_template(
        template_name,
        page_title=page_title,
        website_name=current_app.config['WEBSITE_NAME'],
        year=current_app.config['YEAR'],
        **context
    )

def read_from_csv():
    reservations = []
    file_path = current_app.config['DATA_CSV']
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['reservation_date'] = datetime.strptime(row['reservation_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            reservations.append(row)
    return reservations

def write_to_csv(data):
    fieldnames = ['first_name', 'last_name', 'email', 'reservation_type', 'reservation_date', 'reservation_time', 'hash_key']
    file_path = current_app.config['DATA_CSV']
    file_exists = os.path.isfile(file_path)

    if file_exists:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != fieldnames:
                file_exists = False  # Mismatch in fields, clear the file

    # Ensure the date is in the correct format
    data['reservation_date'] = datetime.strptime(data['reservation_date'], '%Y-%m-%d').strftime('%Y-%m-%d')

    with open(file_path, mode='w' if not file_exists else 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(data)

def remove_old_records():
    file_path = current_app.config['DATA_CSV']
    if not os.path.isfile(file_path):
        return

    reservations = read_from_csv()
    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    updated_reservations = [r for r in reservations if datetime.strptime(r['reservation_date'], '%Y-%m-%d') >= two_weeks_ago]

    # Rewrite the CSV file with updated reservations
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['first_name', 'last_name', 'email', 'reservation_type', 'reservation_date', 'reservation_time', 'hash_key']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_reservations)

def generate_sample_data():
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones"]
    reservation_types = [rtype[0] for rtype in current_app.config['RESERVATION_TYPES']]
    times = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

    dummy_data = []
    for _ in range(6):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        dummy_data.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "reservation_type": random.choice(reservation_types),
            "reservation_date": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            "reservation_time": random.choice(times),
            "hash_key": ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        })

    for record in dummy_data:
        write_to_csv(record)

def update_csv(hash_key, updated_data):
    reservations = read_from_csv()
    updated_reservations = []
    for reservation in reservations:
        if reservation['hash_key'] == hash_key:
            reservation.update(updated_data)
        updated_reservations.append(reservation)

    file_path = current_app.config['DATA_CSV']
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['first_name', 'last_name', 'email', 'reservation_type', 'reservation_date', 'reservation_time', 'hash_key']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_reservations)

def delete_from_csv(hash_key):
    reservations = read_from_csv()
    updated_reservations = [r for r in reservations if r['hash_key'] != hash_key]

    file_path = current_app.config['DATA_CSV']
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['first_name', 'last_name', 'email', 'reservation_type', 'reservation_date', 'reservation_time', 'hash_key']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_reservations)

def get_reservation_by_hash_key(hash_key):
    file_path = current_app.config['DATA_CSV']
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['hash_key'] == hash_key:
                return row
    return None


def delete_reservation_by_hash_key(hash_key):
    file_path = current_app.config['DATA_CSV']
    updated_reservations = []
    deleted = False
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['hash_key'] != hash_key:
                updated_reservations.append(row)
            else:
                deleted = True

    if deleted:
        with open(file_path, mode='w', newline='') as file:
            fieldnames = ['first_name', 'last_name', 'email', 'reservation_type', 'reservation_date', 'reservation_time', 'hash_key']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_reservations)
    
    return deleted


