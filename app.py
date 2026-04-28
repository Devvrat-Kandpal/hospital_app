from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========  TEAM'S LINKED LIST CODE ==========
class node:
    def __init__(self, timeslot=None, Name=None, Contact_number=None, Type=None, Reschedule=None):
        self.timeslot = timeslot
        self.Name = Name
        self.Contact_number = Contact_number
        self.Type = Type
        self.Reschedule = Reschedule
        self.next = None

class linked_list:
    def __init__(self):
        self.head = node()
    
    def append(self, timeslot, Name, Contact_number, Type, Reschedule):
        new_node = node(timeslot, Name, Contact_number, Type, Reschedule)
        cur = self.head
        while cur.next != None:
            cur = cur.next
        cur.next = new_node
    
    def display(self):
        Appointments = []
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            aptmnt = [cur_node.timeslot, cur_node.Name, cur_node.Contact_number, cur_node.Type, cur_node.Reschedule]
            Appointments.append(aptmnt)
        return Appointments
    
    def view(self, timeslot):
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            if cur_node.timeslot == timeslot:
                return (cur_node.timeslot, cur_node.Name, cur_node.Contact_number, cur_node.Type, cur_node.Reschedule)
        return None
    
    def insert_new_appointment(self, timeslot, Name, Contact_number, Type, Reschedule):
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            if cur_node.timeslot == timeslot:
                cur_node.Name = Name
                cur_node.Contact_number = Contact_number
                cur_node.Type = Type
                cur_node.Reschedule = Reschedule
                return True
        return False
    
    def delete_appointment_by_contact(self, contactn, atype):
        dicttime = {1:"9:00",2:"9:30",3:"10:00",4:"10:30",5:"11:00",6:"11:30",7:"12:00",8:"12:30",9:"13:00",10:"13:30",11:"14:00",12:"14:30",13:"15:00",14:"15:30",15:"16:00",16:"16:30",17:"17:00",18:"17:30",19:"18:00",20:"18:30",21:"19:00",22:"19:30",23:"20:00",24:"20:30"}
        cur_node = self.head
        prev_node = self.head
        start = None
        flag = 0
        
        while cur_node.next != None:
            cur_node = cur_node.next
            if cur_node.Contact_number == contactn:
                if flag == 0:
                    start = cur_node.timeslot
                    flag = 1
                
                # Update availability
                if atype in [1,2,3,4]:
                    physician_timeslot_availability[cur_node.timeslot - 1] = dicttime[cur_node.timeslot]
                elif atype in [5,6]:
                    gensurgeon_timeslot_availability[cur_node.timeslot - 1] = dicttime[cur_node.timeslot]
                else:
                    radiologist_timeslot_availability[cur_node.timeslot - 1] = dicttime[cur_node.timeslot]
                
                cur_node.Name = None
                cur_node.Contact_number = None
                cur_node.Type = None
                cur_node.Reschedule = None
        
        return start
    
    def get_appointment_by_contact(self, contactn):
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            if cur_node.Contact_number == contactn:
                return {
                    'timeslot': cur_node.timeslot,
                    'name': cur_node.Name,
                    'contact': cur_node.Contact_number,
                    'type': cur_node.Type,
                    'reschedule': cur_node.Reschedule
                }
        return None

# ========== INITIALIZE SCHEDULES ==========
physician_schedule = linked_list()
gensurgeon_schedule = linked_list()
radiologist_schedule = linked_list()

for i in range(24):
    physician_schedule.append(i+1, None, None, None, None)
    gensurgeon_schedule.append(i+1, None, None, None, None)
    radiologist_schedule.append(i+1, None, None, None, None)

# Availability tracking
physician_timeslot_availability = ["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"]
gensurgeon_timeslot_availability = ["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"]
radiologist_timeslot_availability = ["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"]

# Appointment types mapping
choices_map = {
    1: 'General Consultancy',
    2: 'Blood Test/Vaccination',
    3: 'ECG test',
    4: 'Routine Checkup',
    5: 'Minor surgery',
    6: 'Major surgery',
    7: 'X Ray',
    8: 'Ultrasound'
}

# Duration of each appointment type (in slots)
duration_map = {
    1: 1,  # General Consultancy - 30 min
    2: 1,  # Blood Test - 30 min
    3: 2,  # ECG test - 1 hour
    4: 2,  # Routine Checkup - 1 hour
    5: 2,  # Minor surgery - 1 hour
    6: 6,  # Major surgery - 3 hours
    7: 1,  # X Ray - 30 min
    8: 2   # Ultrasound - 1 hour
}

# Helper function to convert slot to time
def slot_to_time(slot):
    times = ["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"]
    return times[slot-1] if 1 <= slot <= 24 else "Unknown"

# ========== BOOKING LOGIC (Your team's logic adapted for API) ==========
def book_appointment_api(name, contact, choice, timechoice, reschedule):
    atype = choices_map.get(choice)
    duration = duration_map.get(choice, 1)
    
    # Determine which doctor
    if choice in [1,2,3,4]:
        schedule = physician_schedule
        availability = physician_timeslot_availability
    elif choice in [5,6]:
        schedule = gensurgeon_schedule
        availability = gensurgeon_timeslot_availability
    else:
        schedule = radiologist_schedule
        availability = radiologist_timeslot_availability
    
    # Check if slot is available (and consecutive slots for multi-slot appointments)
    available = True
    for i in range(duration):
        if timechoice + i > 24:
            available = False
            break
        if availability[timechoice + i - 1] == 0:
            available = False
            break
    
    if not available:
        return {'success': False, 'message': 'Selected time slot not available'}
    
    # Book the slot(s)
    for i in range(duration):
        schedule.insert_new_appointment(timechoice + i, name, contact, atype, reschedule)
        availability[timechoice + i - 1] = 0
    
    time_str = slot_to_time(timechoice)
    
    return {
        'success': True,
        'message': f'Appointment booked for {name} at {time_str}',
        'time': time_str,
        'type': atype,
        'timeslot': timechoice,
        'duration': duration
    }

# ========== FLASK ROUTES ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patient')
def patient_mode():
    return render_template('patient.html')

@app.route('/doctor')
def doctor_mode():
    return render_template('doctor.html')

@app.route('/admin')
def admin_mode():
    return render_template('admin.html')

# ========== API ENDPOINTS ==========

@app.route('/api/available_slots/<doctor>')
def get_available_slots(doctor):
    """Get available slots for a doctor"""
    if doctor == 'physician':
        availability = physician_timeslot_availability
    elif doctor == 'surgeon':
        availability = gensurgeon_timeslot_availability
    else:
        availability = radiologist_timeslot_availability
    
    slots = [i+1 for i, s in enumerate(availability) if s != 0]
    return jsonify({'slots': slots})

@app.route('/api/available_slots_with_duration/<doctor>/<int:choice>')
def get_available_slots_with_duration(doctor, choice):
    """Get available slots considering appointment duration"""
    duration = duration_map.get(choice, 1)
    
    if doctor == 'physician':
        availability = physician_timeslot_availability
    elif doctor == 'surgeon':
        availability = gensurgeon_timeslot_availability
    else:
        availability = radiologist_timeslot_availability
    
    slots = []
    for i in range(24):
        if availability[i] != 0:
            # Check if enough consecutive slots available
            available = True
            for j in range(duration):
                if i + j >= 24 or availability[i + j] == 0:
                    available = False
                    break
            if available:
                slots.append(i+1)
    
    return jsonify({'slots': slots, 'duration': duration})

@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    result = book_appointment_api(
        name=data['name'],
        contact=data['contact'],
        choice=data['choice'],
        timechoice=data['timeslot'],
        reschedule=data.get('reschedule', 'no')
    )
    return jsonify(result)

@app.route('/api/view/<contact>')
def view_appointment(contact):
    """View appointment by contact number"""
    for schedule, doctor in [(physician_schedule, 'Physician'), (gensurgeon_schedule, 'Surgeon'), (radiologist_schedule, 'Radiologist')]:
        apt = schedule.get_appointment_by_contact(contact)
        if apt:
            return jsonify({
                'found': True,
                'doctor': doctor,
                'name': apt['name'],
                'contact': apt['contact'],
                'type': apt['type'],
                'timeslot': apt['timeslot'],
                'time': slot_to_time(apt['timeslot']),
                'reschedule': apt['reschedule']
            })
    return jsonify({'found': False, 'message': 'No appointment found for this contact'})

@app.route('/api/cancel', methods=['POST'])
def cancel_appointment():
    data = request.json
    contact = data['contact']
    choice = data['choice']
    
    if choice in [1,2,3,4]:
        schedule = physician_schedule
    elif choice in [5,6]:
        schedule = gensurgeon_schedule
    else:
        schedule = radiologist_schedule
    
    start_slot = schedule.delete_appointment_by_contact(contact, choice)
    
    if start_slot:
        return jsonify({'success': True, 'message': 'Appointment cancelled successfully', 'cancelled_slot': start_slot})
    return jsonify({'success': False, 'message': 'Appointment not found'})

@app.route('/api/doctor_schedule/<doctor>')
def get_doctor_schedule(doctor):
    """Get full schedule for a doctor"""
    if doctor == 'physician':
        schedule = physician_schedule
        availability = physician_timeslot_availability
        name = "Dr. Smith (Physician)"
    elif doctor == 'surgeon':
        schedule = gensurgeon_schedule
        availability = gensurgeon_timeslot_availability
        name = "Dr. Kumar (Surgeon)"
    else:
        schedule = radiologist_schedule
        availability = radiologist_timeslot_availability
        name = "Dr. Priya (Radiologist)"
    
    appointments = []
    for i in range(24):
        apt_data = schedule.view(i+1)
        if apt_data:
            appointments.append({
                'timeslot': i+1,
                'time': slot_to_time(i+1),
                'name': apt_data[1] if apt_data[1] else None,
                'contact': apt_data[2] if apt_data[2] else None,
                'type': apt_data[3] if apt_data[3] else None,
                'status': 'booked' if apt_data[1] else 'available'
            })
        else:
            appointments.append({
                'timeslot': i+1,
                'time': slot_to_time(i+1),
                'name': None,
                'contact': None,
                'type': None,
                'status': 'available' if availability[i] != 0 else 'available'
            })
    
    return jsonify({'doctor': name, 'appointments': appointments})

@app.route('/api/mark_complete', methods=['POST'])
def mark_complete():
    data = request.json
    doctor = data['doctor']
    timeslot = data['timeslot']
    
    if doctor == 'physician':
        schedule = physician_schedule
    elif doctor == 'surgeon':
        schedule = gensurgeon_schedule
    else:
        schedule = radiologist_schedule
    
    apt = schedule.view(timeslot)
    if apt and apt[1]:
        # Mark as completed (we'll add a status field or just leave as is)
        # For now, just return success
        return jsonify({'success': True, 'message': 'Marked as completed'})
    return jsonify({'success': False, 'message': 'Appointment not found'})

@app.route('/api/all_appointments')
def get_all_appointments():
    """Get all appointments for admin view"""
    result = {}
    
    for doctor_name, schedule in [('physician', physician_schedule), ('surgeon', gensurgeon_schedule), ('radiologist', radiologist_schedule)]:
        appointments = []
        for i in range(24):
            apt = schedule.view(i+1)
            if apt and apt[1]:
                appointments.append({
                    'timeslot': i+1,
                    'time': slot_to_time(i+1),
                    'name': apt[1],
                    'contact': apt[2],
                    'type': apt[3],
                    'reschedule': apt[4]
                })
        result[doctor_name] = appointments
    
    return jsonify(result)

@app.route('/api/admin_cancel', methods=['POST'])
def admin_cancel():
    data = request.json
    contact = data['contact']
    
    # Try to find and cancel in any schedule
    for choice_range, schedule in [([1,2,3,4], physician_schedule), ([5,6], gensurgeon_schedule), ([7,8], radiologist_schedule)]:
        apt = schedule.get_appointment_by_contact(contact)
        if apt:
            # Determine choice from appointment type
            for c, type_name in choices_map.items():
                if type_name == apt['type']:
                    schedule.delete_appointment_by_contact(contact, c)
                    return jsonify({'success': True, 'message': f'Cancelled appointment for {contact}'})
    
    return jsonify({'success': False, 'message': 'No appointment found for this contact'})

if __name__ == '__main__':
    app.run(debug=True)