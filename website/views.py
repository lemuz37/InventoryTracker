from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import true
from .models import Devices, User
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    users = User.query.all()
    today = datetime.now()
    devices=Devices.query.all()
    return render_template("home.html", user=current_user, users=users,devices=devices, today=today)

@views.route('/devices', methods=['GET', 'POST'])
@login_required
def calibratedDevices():
    users = User.query.all()
    today = datetime.now()
    devices=Devices.query.all()
    device_category = None
    calibrated_devices = None

    if request.method == 'POST':
        # For debugging POST requests
        # data = request.form
        # print(data)
        device_category = request.form.get('device_category')
        calibrated_devices = request.form.get('calibrated_devices')

        if device_category == "Select Device Category":
            flash('Please select a device category', category = 'error')

    return render_template("devices.html", user=current_user, users=users,devices=devices, today=today, 
                           device_category=device_category, calibrated_devices=calibrated_devices)


@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    devices=Devices.query.all()
    users=User.query.all()
    return render_template("users.html", user=current_user, devices=devices, users=users)

@views.route('/add_device', methods=['GET', 'POST'])
@login_required
def addDevice():
    def duplicate_check():
        deviceQuery = Devices.query.filter_by(device_category=device_category, serial_number=serial_number).first()
        if deviceQuery:
            return true

    devi=Devices.query.all()
    users=User.query.all()
    today = datetime.now()

    if request.method == 'POST':
        # For debugging POST requests
        data = request.form
        print(data)

        device_category = request.form.get('device_category')
        device_name = request.form.get('device_name')
        serial_number = request.form.get('serial_number')
        project = request.form.get('project')
        location = request.form.get('location')
        calStart = request.form.get('calStart')
        calEnd = request.form.get('calEnd')

        if not calStart and not calEnd:
            calStart = str(datetime.min)[:-9]
            calEnd = str(datetime.min)[:-9]
            calibrated = False
        else: calibrated = True

        if device_category == "Select Device Category":
            flash('Please select a device category', category = 'error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if not device_name:
            flash('Please enter a device name', category = 'error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if not serial_number:
            flash('Serial Number not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if not location:
            flash('Location not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        elif location.lower().__contains__("home"):
            flash("Cannot take device home.", category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if not calStart:
            flash('Calibration Start Date not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        elif not calEnd:
            flash('Calibration End Date not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if duplicate_check():
            flash('Device already exists in db', category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if calStart > calEnd:
            flash("End Date must be later than Start Date", category='error')
            return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)
        if not project:
            project = "No Project"

        calStart = datetime.strptime(calStart, "%Y-%m-%d")
        calEnd = datetime.strptime(calEnd, "%Y-%m-%d")
        
        new_device = Devices(device_category=device_category, device_name=device_name, 
                            serial_number=serial_number, team=current_user.team,
                            project=project, location=location, calibrated=calibrated, calibrationStart=calStart, 
                            calibrationEnd=calEnd, user_name=current_user.user_name)
        db.session.add(new_device)
        db.session.commit()
        flash('Device added!', category='success')
    
    return render_template("addDevice.html", user=current_user, devices=devi, users=users, today=today)

@views.route('/update_devices', methods=['GET', 'POST'])
@login_required
def updateDevice():
    devices=Devices.query.all()
    users=User.query.all()
    device_category = None
    calibrated_devices = None

    if request.method == 'POST':
    # For debugging POST requests
        # data = request.form
        # print(data)

        if request.form.__contains__("device_category_selection"):
            device_category = request.form.get('device_category')
            calibrated_devices = request.form.get('calibrated_devices')
            if device_category == "Select Device Category":
                flash('Please select a device category', category = 'error')
            return render_template("update_devices.html", user=current_user, devices=devices, users=users, 
                                   device_category=device_category, calibrated_devices=calibrated_devices)
        
        elif request.form.__contains__("update_devices"):

            requested_device_updates = request.form.getlist('update')
            team = request.form.getlist('team')
            project = request.form.getlist('project')
            location = request.form.getlist('location')
            calStart = request.form.getlist('calStart')
            calEnd = request.form.getlist('calEnd')

            if not requested_device_updates:
                return redirect(url_for('views.home'))
            else:
                for device_to_update in requested_device_updates:
                    device_to_update = list(device_to_update.split(","))
                    device = Devices.query.get(device_to_update[0])
                    device_row = int(device_to_update[1])

                    if team[device_row] == 'Select Team':
                        device.team = device.team
                    else:
                        device.team = team[device_row]

                    if not project[device_row]:
                        device.project = device.project
                    else:
                        device.project = project[device_row]

                    if not location[device_row]:
                        device.location = device.location
                    else:
                        device.location = location[device_row]

                    if not calStart[device_row] and not calEnd[device_row]:
                        device.calibrationStart = device.calibrationStart
                        device.calibrationEnd = device.calibrationEnd
                    else:
                        if not calStart[device_row]:
                            flash('Calibration Start Date not entered', category='error')
                            return render_template("update_devices.html", user=current_user, devices=devices, users=users, 
                                                   device_category=device_category, calibrated_devices=calibrated_devices)
                        elif not calEnd[device_row]:
                            flash('Calibration End Date not entered', category='error')
                            return render_template("update_devices.html", user=current_user, devices=devices, users=users, 
                                                   device_category=device_category, calibrated_devices=calibrated_devices)
                        elif calStart[device_row] > calEnd[device_row]:
                            flash("End Date must be later than Start Date", category='error')
                            return render_template("update_devices.html", user=current_user, devices=devices, users=users, 
                                                   device_category=device_category, calibrated_devices=calibrated_devices)
                        else:
                            device.calibrationStart = datetime.strptime(calStart[device_row], "%Y-%m-%d")
                            device.calibrationEnd = datetime.strptime(calEnd[device_row], "%Y-%m-%d")
                            device.calibrated = True
                    
                    db.session.commit()
                flash("Device(s) updated!", category="success")
    return render_template("update_devices.html", user=current_user, devices=devices, users=users, 
                           device_category=device_category, calibrated_devices=calibrated_devices)

@views.route('/return_device', methods=['POST'])
def return_device():
    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)
    device.user_name = "Available"
    device.team = "System Test"
    device.project = "No Project"
    db.session.commit()
    flash("Device returned!", category="success")
    return jsonify({})

@views.route('/check_out_device', methods=['POST'])
def checkout_device():
    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)
    if device.user_name != "Available":
        flash('Device is not available', category="error")
    else:
        device.user_name = current_user.user_name
        device.team = current_user.team
        db.session.commit()
        flash("Device checked out!", category="success")
    return jsonify({}) 