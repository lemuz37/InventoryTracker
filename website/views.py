from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import true
from .models import Devices, User
from . import db
import json
from datetime import datetime, timedelta

views = Blueprint('views', __name__)
DEVICE_LORD = "Trinity"

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    def duplicate_check():
        deviceQuery = Devices.query.filter_by(device=device, serialNumber=serialNumber).first()
        if deviceQuery:
            return true

    def check_date(date1, date2):
        if date1 > date2:
            return False
        else:
            return True

    devi=Devices.query.all()
    users=User.query.all()
    today = datetime.now()

    if request.method == 'POST':
        # For debugging POST requests
        # data = request.form
        # print(data)

        device = request.form.get('device')
        serialNumber = request.form.get('serialNumber')
        project = request.form.get('project')
        location = request.form.get('location')
        calStart = request.form.get('calStart')
        calEnd = request.form.get('calEnd')

        if device == "Choose Device":
            flash('Please select a device', category = 'error')
        elif not serialNumber:
            flash('Serial Number not entered', category='error')
        elif not location:
            flash('Location not entered', category='error')
        elif location == "Home":
            flash("Cannot take device home.", category='error')
        elif not calStart:
            flash('Calibration Start Date not entered', category='error')
        elif not calEnd:
            flash('Calibration End Date not entered', category='error')
        elif duplicate_check():
            flash('Device already exists in db', category='error')
        elif check_date(calStart, calEnd) == False:
            flash("End Date must be later than Start Date", category='error')
        else:
            if not project:
                project = "No Project"

            calStart = datetime.strptime(calStart, "%Y-%m-%d")
            calEnd = datetime.strptime(calEnd, "%Y-%m-%d")
            
            new_device = Devices(device=device, serialNumber=serialNumber, team=current_user.team,
                                project=project, location=location, calibrationStart=calStart, 
                                calibrationEnd=calEnd, user_name=current_user.user_name)
            db.session.add(new_device)
            db.session.commit()
            flash('Device added!', category='success')
    return render_template("home.html", user=current_user, devices=devi, users=users, today=today)



@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    devi=Devices.query.all()
    users=User.query.all()
    return render_template("users.html", user=current_user, devices=devi, users=users)

@views.route('/updateDevices', methods=['GET', 'POST'])
@login_required
def updateDevice():
    devi=Devices.query.all()
    users=User.query.all()

    if request.method == 'POST':
    # For debugging POST requests
        data = request.form
    #    print(data)

        updateDeviceIDs = data.getlist('update')
        team = data.getlist('team')
        project = data.getlist('project')
        location = data.getlist('location')
        calStart = data.getlist('calStart')
        calEnd = data.getlist('calEnd')

        if not updateDeviceIDs:
            return redirect(url_for('views.home'))
        else:
            for deviceID in updateDeviceIDs:
                device = Devices.query.get(deviceID)
                deviceIndex = int(deviceID) - 1

                if team[deviceIndex] == 'Select Team':
                    device.team = device.team
                else:
                    device.team = team[deviceIndex]

                if not project[deviceIndex]:
                    device.project = device.project
                else:
                    device.project = project[deviceIndex]

                if not location[deviceIndex]:
                    device.location = device.location
                else:
                    device.location = location[deviceIndex]

                if not calStart[deviceIndex]:
                    device.calibrationStart = device.calibrationStart
                else:
                    device.calibrationStart = datetime.strptime(calStart[deviceIndex], "%Y-%m-%d")

                if not calEnd[deviceIndex]:
                    device.calibrationEnd = device.calibrationEnd
                else:
                    device.calibrationEnd = datetime.strptime(calEnd[deviceIndex], "%Y-%m-%d")

                db.session.commit()
                
    return render_template("update_devices.html", user=current_user, devices=devi, users=users)

@views.route('/return-device', methods=['POST'])
def return_device():
    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)
    if device.user_name != DEVICE_LORD:
        device.user_name = DEVICE_LORD
        device.team = "System Test"
        db.session.commit()
        flash("Device returned!", category="success")
    return jsonify({})

@views.route('/check-out-device', methods=['POST'])
def checkout_device():
    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)
    if device.user_name != DEVICE_LORD:
        flash('Device is not available', category="error")
    else:
        device.user_name = current_user.user_name
        device.team = current_user.team
        db.session.commit()
        flash("Device checked out!", category="success")
    return jsonify({}) 