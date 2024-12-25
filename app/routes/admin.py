from flask import request, current_app, redirect, url_for, render_template, flash
from . import main_bp
from app.utils import render_page, read_from_csv, write_to_csv, generate_sample_data, update_csv, delete_from_csv, get_reservation_by_hash_key, delete_reservation_by_hash_key
import os
from datetime import datetime

@main_bp.route('/admin', methods=['GET'])
def admin():
    file_path = current_app.config['DATA_CSV']
    if not os.path.isfile(file_path):
        generate_sample_data()
    else:
        reservations = read_from_csv()
        if len(reservations) < 3:
            generate_sample_data()

    reservations = read_from_csv()
    # Sort reservations by upcoming reservation date
    reservations.sort(key=lambda r: datetime.strptime(r['reservation_date'], '%Y-%m-%d'))

    return render_page(
        'components/admin.html',
        'Upcoming Reservations',
        reservations=reservations
    )

@main_bp.route('/admin/update/<hash_key>', methods=['POST'])
def update_reservation(hash_key):
    updated_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'reservation_type': request.form['reservation_type'],
        'reservation_date': request.form['reservation_date'],
        'reservation_time': request.form['reservation_time']
    }
    update_csv(hash_key, updated_data)
    return redirect(url_for('main_bp.admin'))

@main_bp.route('/admin/delete/<hash_key>', methods=['POST'])
def delete_reservation_action(hash_key):
    if delete_reservation_by_hash_key(hash_key):
        flash('Reservation deleted successfully.', 'success')
    else:
        flash('Reservation not found.', 'error')
    return redirect(url_for('main_bp.admin'))

@main_bp.route('/admin/edit/<hash_key>', methods=['GET', 'POST'])
def edit_reservation(hash_key):
    if request.method == 'POST':
        try:
            updated_data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'reservation_type': request.form['reservation_type'],
                'reservation_date': request.form['reservation_date'],
                'reservation_time': request.form['reservation_time']
            }
            update_csv(hash_key, updated_data)
            return redirect(url_for('main_bp.admin'))
        except Exception:
            return render_template('error.html', error_message="An error occurred while updating the reservation."), 500
    
    reservations = read_from_csv()
    reservation = next((r for r in reservations if r['hash_key'] == hash_key), None)
    if reservation is None:
        return redirect(url_for('main_bp.admin'))

    reservation_types = current_app.config['RESERVATION_TYPES']
    return render_template('components/edit_reservation.html', reservation=reservation, reservation_types=reservation_types)

@main_bp.route('/admin/confirm_delete/<hash_key>', methods=['GET'])
def confirm_delete_reservation(hash_key):
    reservation = get_reservation_by_hash_key(hash_key)
    if reservation:
        return render_template('components/delete_reservation.html', reservation=reservation)
    flash('Reservation not found.', 'error')
    return redirect(url_for('main_bp.admin'))
