from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from sqlalchemy import true
from .models import Devices, User
from . import db
import time
import json
import ast
import qrcode
import io
from datetime import datetime

views = Blueprint('views', __name__)

# Home Page


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_checked_out_devices = Devices.query.filter(
        Devices.user_name.contains(current_user.user_name))
    today = datetime.now()

    if request.method == 'POST' and request.form.__contains__("project_name_btn"):
        # For debugging POST requests
        # data = request.form
        # print(data)
        project_name = request.form.get('project_name')
        current_user.project = project_name
        for device in user_checked_out_devices:
            device.project = project_name
        db.session.commit()
    return render_template("home.html", user=current_user, devices=user_checked_out_devices, today=today)

# ECG Devices Page


@views.route('/ecg_devices', methods=['GET'])
@login_required
def ecg_devices():
    ecg_devices = Devices.query.filter(Devices.device_category == "ECG").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/ecg_devices.html", user=current_user, devices=ecg_devices, today=today, btnradio=radio_btn)


@views.route('/vitals_devices', methods=['GET'])
@login_required
def vitals_devices():
    vitals_devices = Devices.query.filter(
        Devices.device_category == "Vitals").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/vitals_devices.html", user=current_user, devices=vitals_devices, today=today, btnradio=radio_btn)


@views.route('/spirometer_devices', methods=['GET'])
@login_required
def spirometer_devices():
    spirometer_devices = Devices.query.filter(
        Devices.device_category == "Spirometer").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/spirometer_devices.html", user=current_user, devices=spirometer_devices, today=today, btnradio=radio_btn)


@views.route('/cal_syringe_devices', methods=['GET'])
@login_required
def cal_syringe_devices():
    cal_syringe_devices = Devices.query.filter(
        Devices.device_category == "Calibration Syringe").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/cal_syringe_devices.html", user=current_user, devices=cal_syringe_devices, today=today, btnradio=radio_btn)


@views.route('/simulator_devices', methods=['GET'])
@login_required
def simulator_devices():
    simulator_devices = Devices.query.filter(
        Devices.device_category == "Simulator").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/simulator_devices.html", user=current_user, devices=simulator_devices, today=today, btnradio=radio_btn)


@views.route('/scales_devices', methods=['GET'])
@login_required
def scales_devices():
    scales_devices = Devices.query.filter(
        Devices.device_category == "Scales").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/scales_devices.html", user=current_user, devices=scales_devices, today=today, btnradio=radio_btn)


@views.route('/eng_tools', methods=['GET'])
@login_required
def egn_tools():
    eng_tools = Devices.query.filter(
        Devices.device_category == "Engineering Tools").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/eng_tools.html", user=current_user, devices=eng_tools, today=today, btnradio=radio_btn)


@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    devices = Devices.query.all()
    users = User.query.all()
    if request.method == 'POST':
        pass
    return render_template("users.html", user=current_user, devices=devices, users=users)


@views.route('/add_device', methods=['GET', 'POST'])
@login_required
def addDevice():
    def duplicate_check():
        deviceQuery = Devices.query.filter_by(
            device_category=device_category, serial_number=serial_number).first()
        if deviceQuery:
            return true

    device_table = Devices.query.all()
    user_table = User.query.all()
    today = datetime.now()

    if request.method == 'POST':
        # For debugging POST requests
        # data = request.form
        # print(data)

        device_category = request.form.get('device_category')
        device_name = request.form.get('device_name')
        model_number = request.form.get('model_number')
        serial_number = request.form.get('serial_number')
        location = request.form.get('location')
        calStart = request.form.get('calStart')
        calEnd = request.form.get('calEnd')

        if not calStart and not calEnd:
            calStart = str(datetime.min)[:-9]
            calEnd = str(datetime.min)[:-9]
            calibrated = False
        else:
            calibrated = True

        if device_category == "Select Device Category":
            flash('Please select a device category', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        if not device_name:
            flash('Please enter a device name', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        if not model_number:
            model_number = ""
        if not serial_number:
            flash('Serial Number not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        if not location:
            flash('Location not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        elif location.lower().__contains__("home"):
            flash("Cannot take device home.", category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        if not calStart:
            flash('Calibration Start Date not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        elif not calEnd:
            flash('Calibration End Date not entered', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        if duplicate_check():
            flash('Device already exists in db', category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)
        if calStart > calEnd:
            flash("End Date must be later than Start Date", category='error')
            return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)

        calStart = datetime.strptime(calStart, "%Y-%m-%d")
        calEnd = datetime.strptime(calEnd, "%Y-%m-%d")

        new_device = Devices(device_category=device_category, device_name=device_name,
                             model_number=model_number, serial_number=serial_number, team=current_user.team,
                             project="No Project", location=location, calibrated=calibrated, calibrationStart=calStart,
                             calibrationEnd=calEnd, user_name="Available")
        db.session.add(new_device)
        db.session.commit()
        flash('Device added!', category='success')

    return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)


@views.route('/update_devices', methods=['GET', 'POST'])
@login_required
def updateDevice():
    def duplicate_check(serial_number):
        deviceQuery = Devices.query.filter_by(device_category=device_category,
                                              serial_number=serial_number).first()
        if deviceQuery:
            return true

    devices = Devices.query.all()
    users = User.query.all()
    device_category = None
    btnradio = None

    if request.method == 'POST':
        # For debugging POST requests
        # data = request.form
        # print(data)

        if request.form.__contains__("device_category_selection"):
            device_category = request.form.get('device_category')
            btnradio = request.form.get('btnradio')

            if device_category == "Select Device Category":
                flash('Please select a device category', category='error')
            return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                   device_category=device_category, btnradio=btnradio)

        elif request.form.__contains__("update_devices"):
            data_dict = request.form.to_dict()
            # Pop first element in  dictionary
            (k := next(iter(data_dict)), data_dict.pop(k))
            # Pop last element in dictionary
            data_dict.popitem()[1]
            device_category = data_dict.popitem()[1]

            if current_user.admin == True:
                displayed_devices = int(len(data_dict)/8)
            else:
                displayed_devices = int(len(data_dict)/4)

            data_list = [0] * displayed_devices

            count = 0
            while displayed_devices > 0:
                if current_user.admin == True:
                    data_list[count] = list(data_dict.items())[
                        (count) * 8: (count + 1) * 8]
                else:
                    data_list[count] = list(data_dict.items())[
                        (count) * 4: (count + 1) * 4]
                count = count + 1
                displayed_devices = displayed_devices - 1

            if current_user.admin == True:
                for i in range(0, len(data_list)):
                    device_id_str = data_list[i][0][0].split('_')[-1:]
                    device_id = int(device_id_str[0])
                    device = Devices.query.get(device_id)
                    for j in range(0, 8):
                        data = data_list[i][j]
                        # Device Category
                        if j == 0:
                            if data[1] == "Select Device Category":
                                continue

                            else:
                                device.device_category = data[1]
                        # Device Name
                        if j == 1:
                            if not data[1]:
                                continue
                            else:
                                device.device_name = data[1]
                        # Model Number
                        if j == 2:
                            if not data[1]:
                                continue
                            else:
                                device.model_number = data[1]
                        # Serial Number
                        if j == 3:
                            if not data[1]:
                                continue
                            else:
                                if duplicate_check(data[1]):
                                    flash('Serial Number already exists in database.',
                                          category='error')
                                    return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                           device_category=device_category, btnradio=btnradio)
                                else:
                                    device.serial_number = data[1]
                        # calStart and cal End
                        if j == 4:
                            if not data[1] and not data_list[i][j + 1][1]:
                                continue
                            elif data[1] and not data_list[i][j + 1][1]:
                                flash('Calibration End Date not entered',
                                      category='error')
                                return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                       device_category=device_category, btnradio=btnradio)
                            elif not data[1] and data_list[i][j + 1][1]:
                                flash('Calibration Start Date not entered',
                                      category='error')
                                return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                       device_category=device_category, btnradio=btnradio)
                            elif data[1] > data_list[i][j + 1][1]:
                                flash("End Date must be later than Start Date",
                                      category='error')
                                return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                       device_category=device_category, btnradio=btnradio)
                            else:
                                device.calibrationStart = datetime.strptime(
                                    data[1], "%Y-%m-%d")
                                device.calibrationEnd = datetime.strptime(
                                    data_list[i][j + 1][1], "%Y-%m-%d")
                                device.calibrated = True
                        # Project
                        if j == 6:
                            if not data[1]:
                                continue
                            else:
                                device.project = data[1]
                        # Location
                        if j == 7:
                            if not data[1]:
                                continue
                            elif data[1].lower().__contains__("home"):
                                flash("Cannot take device home.",
                                      category='error')
                            else:
                                device.location = data[1]

            else:
                for i in range(0, len(data_list)):
                    device_id_str = data_list[i][0][0].split('_')[-1:]
                    device_id = int(device_id_str[0])
                    device = Devices.query.get(device_id)
                    for j in range(0, 4):
                        data = data_list[i][j]
                        # calStart & calEnd
                        if j == 0:
                            if not data[1] and not data_list[i][j + 1][1]:
                                continue
                            elif data[1] and not data_list[i][j + 1][1]:
                                flash('Calibration End Date not entered',
                                      category='error')
                                return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                       device_category=device_category, btnradio=btnradio)
                            elif not data[1] and data_list[i][j + 1][1]:
                                flash('Calibration Start Date not entered',
                                      category='error')
                                return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                       device_category=device_category, btnradio=btnradio)
                            elif data[1] > data_list[i][j + 1][1]:
                                flash("End Date must be later than Start Date",
                                      category='error')
                                return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                                                       device_category=device_category, btnradio=btnradio)
                            else:
                                device.calibrationStart = datetime.strptime(
                                    data[1], "%Y-%m-%d")
                                device.calibrationEnd = datetime.strptime(
                                    data_list[i][j + 1][1], "%Y-%m-%d")
                                device.calibrated = True
                        # Project
                        if j == 2:
                            if not data[1]:
                                continue
                            else:
                                device.project = data[1]
                        # Location
                        elif j == 3:
                            if not data[1]:
                                continue
                            elif data[1].lower().__contains__("home"):
                                flash("Cannot take device home.",
                                      category='error')
                            else:
                                device.location = data[1]

            db.session.commit()
            flash("Device(s) updated!", category="success")

    return render_template("update_devices.html", user=current_user, devices=devices, users=users,
                           device_category=device_category, btnradio=btnradio)


# Button Functions

# Handle check out button click event
@views.route('/checkout_device', methods=['POST'])
def checkout_device():
    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)

    if device.user_name != "Available":
        flash('Device is not available', category="error")
    else:
        device.checkout_time = datetime.now()
        device.user_name = current_user.user_name
        device.team = current_user.team
        device.project = current_user.project
        db.session.commit()
        flash("Device checked out!", category="success")
    return jsonify(success=True)


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
    return jsonify(success=True)


@views.route('/update_device_project', methods=['POST'])
def update_device_project():
    form_data = request.form
    deviceID = form_data['deviceID']
    project = form_data['project']
    device = Devices.query.get(deviceID)
    if not project:
        return jsonify(success=True)
    else:
        device.project = project
        db.session.commit()
        flash("Device project updated!", category="success")
    return jsonify(success=True)


@views.route('/update_device_location', methods=['POST'])
def update_device_location():
    form_data = request.form
    deviceID = form_data['deviceID']
    location = form_data['location']
    device = Devices.query.get(deviceID)
    if not location:
        return jsonify(success=True)
    else:
        device.location = location
        db.session.commit()
        flash("Device location updated!", category="success")
    return jsonify(success=True)


@views.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():

    data = {
        "device_id": None,
        "device_category": None,
        "device_sn": None
    }

    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)

    data['device_id'] = device.id
    data['device_category'] = device.device_category
    data['device_sn'] = device.serial_number

    # Convert to string and generate QR code
    img = qrcode.make(str(data))

    # Save QR code to a BytesIO object
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    # Set the filename and send QR code as a downloadable file
    return send_file(byte_io,
                     download_name='qrcode.png',
                     as_attachment=True,
                     mimetype='image/png')


@views.route('/generate_user_qrcode', methods=['POST'])
def generate_user_qrcode():

    data = {
        "user_id": None,
        "user_email": None,
        "user_pw": None
    }

    userID = json.loads(request.data)
    userID = userID['userID']
    user = User.query.get(userID)

    data['user_id'] = user.id
    data['user_email'] = user.email
    data['user_pw'] = user.password

    # Convert to string and generate QR code
    img = qrcode.make(str(data))

    # Save QR code to a BytesIO object
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)

    # Set the filename and send QR code as a downloadable file
    return send_file(byte_io,
                     download_name='qrcode.png',
                     as_attachment=True,
                     mimetype='image/png')


@views.route('/delete_device', methods=['POST'])
def delete_device():
    deviceID = json.loads(request.data)
    deviceID = deviceID['deviceID']
    device = Devices.query.get(deviceID)
    db.session.delete(device)
    db.session.commit()
    return jsonify({})


@views.route('/delete_user', methods=['POST'])
def delete_user():
    userID = json.loads(request.data)
    userID = userID['userID']
    if userID == current_user.id:
        flash("You cannot delete yourself.", category="error")
        return jsonify({})

    user = User.query.get(userID)
    user_checked_out_devices = Devices.query.filter(
        Devices.user_name.contains(user.user_name))
    for device in user_checked_out_devices:
        device.user_name = "Available"
        device.team = "System Test"
        device.project = "No Project"
    db.session.delete(user)
    db.session.commit()
    return jsonify({})


@views.route('/assign_device', methods=['POST'])
def user_assign_device():
    data = json.loads(request.data)
    userID = data.get("userId")
    device_category = data.get("deviceCategory")
    serial_number = data.get("serialNumber")
    user = User.query.filter_by(id=int(userID)).first()

    device = Devices.query.filter_by(device_category=device_category,
                                     serial_number=serial_number).first()

    if not device:
        flash("Device does not exist in database.", category="error")
        return jsonify({})
    elif device.user_name != "Available":
        flash("Device is not available.", category="error")
        return jsonify({})
    else:
        device.checkout_time = datetime.now()
        device.user_name = user.user_name
        db.session.commit()
        flash('Device assigned!', category='success')
    return jsonify({})


@views.route('/editUser', methods=['POST'])
def editUser():
    data = json.loads(request.data)
    userID = data.get("userId")
    user_name = data.get("user_name")
    project = data.get("project")
    email = data.get("email").lower()
    team = data.get("team")
    admin = data.get("admin")

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists', category='error')
        return jsonify({})

    else:
        user = User.query.filter_by(id=int(userID)).first()
        user_checked_out_devices = Devices.query.filter(
            Devices.user_name.contains(user.user_name))
        if not user_name:
            pass
        else:
            user.user_name = user_name
            for device in user_checked_out_devices:
                device.user_name = user_name
        if not project:
            pass
        else:
            user.project = project
            for device in user_checked_out_devices:
                device.project = project
        if not email:
            pass
        else:
            user.email = email
        if team == "Select Team":
            pass
        else:
            user.team = team
            for device in user_checked_out_devices:
                device.team = team
        if admin:
            user.admin = admin
        else:
            user.admin = admin
            if userID == current_user.id:
                db.session.commit()
                flash('User edited!', category='success')
                return redirect(url_for('auth.logout'))

        db.session.commit()
        flash('User edited!', category='success')
    return jsonify({})


@views.route('/assign_device_w_qr_code', methods=['POST'])
def assign_device_w_qr_code():
    def is_valid_dict_string(s):
        """Check if string is a valid Python dict string."""
        try:
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                return True
        except (ValueError, SyntaxError):
            return False
        return False

    def string_to_dict(s):
        """Convert string to dict and check for required keys."""
        if is_valid_dict_string(s):
            d = ast.literal_eval(s)
            required_keys = ["device_id", "device_category", "device_sn"]
            if all(key in d for key in required_keys):
                return d
        return None

    data_dict = request.form.to_dict()
    user = User.query.filter_by(id=int(data_dict.get("userId"))).first()

    scan_data = string_to_dict(data_dict.get("scan_data"))

    if not scan_data:
        flash('Invalid input!', category='error')
    else:
        device = Devices.query.filter_by(
            id=int(scan_data.get("device_id"))).first()

        # In case device gets deleted after qr_code creation
        if not device:
            flash("Device does not exist in database.", category="error")
            return jsonify({})

        device.checkout_time = datetime.now()
        device.user_name = user.user_name
        db.session.commit()
        flash('Device assigned!', category='success')

    return redirect(url_for('views.home'))
