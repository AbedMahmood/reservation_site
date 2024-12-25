from flask import render_template, request, redirect, url_for, current_app
from datetime import datetime
import secrets
import string
from . import main_bp
from app.utils import render_page, write_to_csv

@main_bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        reservation_type = request.form['reservation_type']
        reservation_date = datetime.strptime(request.form['date'], '%Y-%m-%d')

        # Generate a 6-digit alphanumeric hash
        hash_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))

        # Prepare the data including the hash_key
        reservation_date = reservation_date.strftime('%Y-%m-%d')
        reservation_time = request.form['time']
        reservation_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "reservation_type": reservation_type,
            "reservation_date": reservation_date,
            "reservation_time": reservation_time,
            "hash_key": hash_key
        }

        write_to_csv(reservation_data)
        return render_page('components/confirm.html', 'Reservation Confirmed', reservation_data=reservation_data)
    
    reservation_types = current_app.config['RESERVATION_TYPES']
    return render_page('components/reserve.html', 'Make a Reservation', reservation_types=reservation_types)
