from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from sqlalchemy import true
from .models import Device, User, Reservation
from . import db
import time
import json
import ast
import qrcode
import io
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_checked_out_devices = current_user.devices
    today = datetime.now()

    if request.method == 'POST' and request.form.__contains__("project_name_btn"):
        project_name = request.form.get('project_name')
        current_user.project = project_name
        for device in user_checked_out_devices:
            device.project = project_name
        db.session.commit()
    return render_template("home.html", user=current_user, devices=user_checked_out_devices, today=today)

# Check out device with qr code
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

    user_id = request.form.get('user_id')
    scan_data = request.form.get('scan_data')

    user = User.query.get(user_id)
    scan_data = string_to_dict(scan_data)

    if not scan_data:
        flash('Invalid input!', category='error')
    else:
        device = Device.query.get(scan_data.get("device_id"))

        # In case device gets deleted after qr_code creation
        if not device:
            flash("Device does not exist in database.", category="error")
            return jsonify({})

        device.checkout_time = datetime.now()
        device.user_id = user.id
        device.project = user.project
        device.checked_out = True
        db.session.commit()
        flash('Device assigned!', category='success')

    return redirect(request.referrer)

# Update device project from user home page
@views.route('/update_device_project', methods=['POST'])
def update_device_project():
    device_id = request.form.get('device_id')
    project = request.form.get("project_" + str(device_id))

    device = Device.query.get(device_id)

    if device is None:
        flash("Device not found!", category="error")
        return redirect(request.referrer)

    if not project:
        return redirect(request.referrer)
    
    device.project = project
    db.session.commit()
    flash("Device project updated!", category="success")
    return redirect(request.referrer)

# Update device location from user home page
@views.route('/update_device_location', methods=['POST'])
def update_device_location():
    device_id = request.form.get('device_id')
    location = request.form.get("location_" + str(device_id))

    device = Device.query.get(device_id)

    if device is None:
        flash("Device not found!", category="error")
        return redirect(request.referrer)

    if not location:
        return redirect(request.referrer)
    
    device.location = location
    db.session.commit()
    flash("Device project updated!", category="success")
    return redirect(request.referrer)

@views.route('/ecg_devices', methods=['GET'])
@login_required
def ecg_devices():
    ecg_devices = Device.query.filter(Device.device_category == "ECG").all()
    today = datetime.now()
    return render_template("device_templates/ecg_devices.html", user=current_user, devices=ecg_devices, today=today)


@views.route('/vital_devices', methods=['GET'])
@login_required
def vitals_devices():
    vitals_devices = Device.query.filter(
        Device.device_category == "Vitals").all()
    today = datetime.now()
    return render_template("device_templates/vitals_devices.html", user=current_user, devices=vitals_devices, today=today)


@views.route('/spirometer_devices', methods=['GET'])
@login_required
def spirometer_devices():
    spirometer_devices = Device.query.filter(
        Device.device_category == "Spirometer").all()
    today = datetime.now()
    return render_template("device_templates/spirometer_devices.html", user=current_user, devices=spirometer_devices, today=today)


@views.route('/calibration_syringes', methods=['GET'])
@login_required
def cal_syringe_devices():
    calibration_syringes = Device.query.filter(
        Device.device_category == "Calibration Syringe").all()
    today = datetime.now()
    return render_template("device_templates/calibration_syringes.html", user=current_user, devices=calibration_syringes, today=today)


@views.route('/simulator_devices', methods=['GET'])
@login_required
def simulator_devices():
    simulator_devices = Device.query.filter(
        Device.device_category == "Simulator").all()
    today = datetime.now()
    return render_template("device_templates/simulator_devices.html", user=current_user, devices=simulator_devices, today=today)


@views.route('/scale_devices', methods=['GET'])
@login_required
def scales_devices():
    scales_devices = Device.query.filter(
        Device.device_category == "Scales").all()
    today = datetime.now()
    radio_btn = "True"
    return render_template("device_templates/scales_devices.html", user=current_user, devices=scales_devices, today=today, btnradio=radio_btn)


@views.route('/eng_tools', methods=['GET'])
@login_required
def egn_tools():
    eng_tools = Device.query.filter(
        Device.device_category == "Engineering Tools").all()
    today = datetime.now()
    return render_template("device_templates/eng_tools.html", user=current_user, devices=eng_tools, today=today)

@views.route('/update_devices', methods=['GET', 'POST'])
@login_required
def updateDevice():
    def duplicate_check(serial_number):
        deviceQuery = Device.query.filter_by(device_category=device_category,
                                              serial_number=serial_number).first()
        if deviceQuery:
            return true

    devices = Device.query.all()
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
                    device = Device.query.get(device_id)
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
                    device = Device.query.get(device_id)
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

@views.route('/add_device', methods=['GET', 'POST'])
@login_required
def addDevice():
    def duplicate_check():
        deviceQuery = Device.query.filter_by(
            device_category=device_category, serial_number=serial_number).first()
        if deviceQuery:
            return True
        return False

    device_table = Device.query.all()
    user_table = User.query.all()
    today = datetime.now()

    if request.method == 'POST':

        device_name = request.form.get('device_name')
        device_category = request.form.get('device_category')
        model_number = request.form.get('model_number')
        serial_number = request.form.get('serial_number')
        device_owner = request.form.get('device_owner')
        location = request.form.get('location')
        calStart = request.form.get('cal_start')
        calEnd = request.form.get('cal_end')

        if not device_name:
            flash('Please enter a Device Name.', category='error')
            return redirect(request.referrer)
        if device_category == "Select Device Category":
            flash('Please select a Device Category.', category='error')
            return redirect(request.referrer)

        if not serial_number:
            flash('Please enter device Serial Number.', category='error')
            return redirect(request.referrer)
    
        if device_owner == "Select Team":
            flash('Please select an Owner.', category='error')
            return redirect(request.referrer)

        if location.lower().__contains__("home"):
            flash("Cannot take device home.", category='error')
            return redirect(request.referrer)
        
        if not calStart and not calEnd:
            calStart = str(datetime.min)[:-9]
            calEnd = str(datetime.min)[:-9]
            is_calibrated = False
        else:
            if not calStart:
                flash('Calibration Start Date not entered', category='error')
                return redirect(request.referrer)
            elif not calEnd:
                flash('Calibration End Date not entered', category='error')
                return redirect(request.referrer)
            if calStart > calEnd:
                flash("End Date must be later than Start Date", category='error')
                return redirect(request.referrer)
            is_calibrated = True
        
        if duplicate_check():
            flash('Device already exists in db', category='error')
            return redirect(request.referrer)

        calStart = datetime.strptime(calStart, "%Y-%m-%d")
        calEnd = datetime.strptime(calEnd, "%Y-%m-%d")

        new_device = Device(device_category=device_category, device_name=device_name,
                             model_number=model_number, serial_number=serial_number, owner=device_owner,
                             project="No Project", location=location, is_calibrated=is_calibrated, calibration_start=calStart,
                             calibration_end=calEnd)
        db.session.add(new_device)
        db.session.commit()
        flash('Device added!', category='success')

    return render_template("addDevice.html", user=current_user, devices=device_table, users=user_table, today=today)

@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    devices = Device.query.all()
    users = User.query.all()
    if request.method == 'POST':
        pass
    return render_template("users.html", user=current_user, devices=devices, users=users)

# ==============================================================================#
#                               Button Functions                                #
# ==============================================================================#


# Handle check out button click event
@views.route('/checkout_device', methods=['POST'])
def checkout_device():
    # For debugging POST requests
    # data = request.form
    # print(data)
    device_id = request.form.get('device_id')
    device = Device.query.get(device_id)
    now = datetime.now()

    if device.checked_out:
        flash('Device is not available', category="error")
        return redirect(request.referrer)
    
    if device.reservation and device.reservation.start_time < now and now < device.reservation.end_time:
        if current_user.team == device.reservation.user.team:
            device.checkout_time = now
            device.user_id = current_user.id
            device.project = current_user.project
            device.checked_out = True
            db.session.commit()
            flash("Device checked out!", category="success")
            return redirect(request.referrer)

        flash("The device " + device.device_name + " is currently reserved by " + device.reservation.user.team +" team. Please try checking it out at a later time, or check other available devices.", category="error")
        return redirect(request.referrer)
    
    device.checkout_time = now
    device.user_id = current_user.id
    device.project = current_user.project
    device.checked_out = True
    db.session.commit()
    flash("Device checked out!", category="success")
    return redirect(request.referrer)

@views.route('/return_device', methods=['POST'])
def return_device():
    device_id = request.form.get('device_id')
    device = Device.query.get(device_id)

    if device is None:
        flash("Device not found!", category="error")
        return redirect(request.referrer)

    device.user_id = None
    device.project = "No Project"
    device.checked_out = False
    device.checkout_time = None
    db.session.commit()
    flash("Device returned!", category="success")
    return redirect(request.referrer)

@views.route('/reserve_device', methods=['POST'])
def reserve_device():
    # For debugging POST requests
    # data = request.form
    # print(data)
    device_id = request.form.get('device_id')
    reservation_start = datetime.strptime(request.form.get('reservation_start_date'), "%Y-%m-%d")
    reservation_end = datetime.strptime(request.form.get('reservation_end_date'), "%Y-%m-%d")
    project = request.form.get('project')

    device = Device.query.get(device_id)

    if device is None:
        flash("Device not found!", category="error")
        return redirect(request.referrer)

    if reservation_end < reservation_start:
            flash('Error: The end date cannot be earlier than the start date.', category="error")
            return redirect(request.referrer)
    
    if device.reservation:
        flash('Device is not available for reservation.', category="error")
        return redirect(request.referrer)
    
    new_reservation = Reservation(
        start_time=reservation_start,
        end_time=reservation_end,
        user_id=current_user.id,
        device_id=device.id,
        project=project
    )
    db.session.add(new_reservation)
    
    if project:
        db.session.commit()
        flash("Device reserved for project " + project, category="success")
        return redirect(request.referrer)

    db.session.commit()
    flash("Device reserved!", category="success")
    return redirect(request.referrer)

@views.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():

    data = {
        "device_id": None,
        "device_category": None,
        "device_sn": None
    }

    device_id = request.form.get('device_id')
    device = Device.query.get(device_id)

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


@views.route('/generate_user_qr_code', methods=['POST'])
def generate_user_qr_code():

    data = {
        "user_id": None,
        "user_email": None,
        "user_pw": None
    }

    user_id = request.form.get('user_id')
    user = User.query.get(int(user_id))

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
    device_id = request.form.get('device_id')
    device = Device.query.get(device_id)
    db.session.delete(device)
    db.session.commit()
    flash('Another one bites the dust.', category="success")
    return redirect(request.referrer)


@views.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    if int(user_id) == current_user.id:
        flash("You cannot delete yourself.", category="error")
        return redirect(request.referrer)

    user = User.query.get(int(user_id))
    if user.devices:
        for device in user.devices:
            device.user_id = None
            device.project = "No Project"
            device.checked_out = False
            device.checkout_time = None
    db.session.delete(user)
    db.session.commit()
    flash('Another one bites the dust.', category="success")
    return redirect(request.referrer)

@views.route('/assign_device', methods=['POST'])
def user_assign_device():
    user_id = request.form.get('user_id')
    device_category = request.form.get('device_category_' + user_id)
    serial_number = request.form.get("serial_number_" + user_id)
    user = User.query.filter_by(id=int(user_id)).first()

    device = Device.query.filter_by(device_category=device_category,
                                     serial_number=serial_number).first()

    if not device:
        flash("Device does not exist in database.", category="error")
        return redirect(request.referrer)
    elif device.checked_out or device.reservation:
        flash("Device is not available.", category="error")
        return redirect(request.referrer)
    else:
        device.user_id = user.id
        device.project = user.project
        device.checked_out = True
        device.checkout_time = datetime.now()
        db.session.commit()
        flash('Device assigned!', category='success')
    return redirect(request.referrer)

@views.route('/edit_user', methods=['POST'])
def edit_user():
    user_id = request.form.get('user_id')
    user = User.query.get(int(user_id))

    first_name = request.form.get("first_name_" + user_id).lower()
    last_name = request.form.get("last_name_" + user_id).lower()
    project = request.form.get("project_" + user_id)
    team = request.form.get("team")
    admin = request.form.get("admin_" + user_id)

    if not first_name and not last_name:
        pass
    else:
        if first_name:
            user.first_name = first_name.title()
        if last_name:
            user.last_name = last_name.title()
        user.user_name = first_name.title()[0] + last_name.title()
    if not project:
        pass
    else:
        user.project = project

    if team == "Select Team":
        pass
    else:
        user.team = team

    if admin == "on":
        user.admin = True
    else:
        user.admin = False
        if int(user_id) == current_user.id:
            db.session.commit()
            flash('User edited!', category='success')
            return redirect(url_for('auth.logout'))

    db.session.commit()
    flash('User edited!', category='success')
    return redirect(request.referrer)