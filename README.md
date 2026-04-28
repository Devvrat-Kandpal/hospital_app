# Hospital Schedule Management System

A web-based hospital scheduling system designed to manage next-day appointments efficiently. The system allows patients to book, view, and cancel appointments, automatically assigning them to the appropriate doctor based on appointment type. The backend is implemented in Python using linked lists, and the system is exposed through a web interface using Flask.

---

## Features

- Book appointments with automatic doctor allocation based on appointment type
- View appointment details using contact number as search parameter
- Cancel appointments with automatic slot recovery
- Automatic rescheduling for patients who opt in
- Admin view for monitoring all doctor schedules
- Doctor schedule viewing for individual practitioners

---

## Why Linked Lists?

Linked lists were chosen over arrays or database tables for the following reasons:

- **Dynamic sizing** – The schedule can expand or contract without pre-allocation
- **Efficient insertion and deletion** – No element shifting required, unlike arrays
- **Sequential access** – Schedules are naturally traversed in time order
- **Memory efficiency** – Nodes can be stored non-contiguously; removal leaves no empty gaps
- **Flexibility** – Appointment durations vary; linked lists accommodate variable-length bookings cleanly

For a scheduling system where appointments are frequently added, cancelled, and rescheduled, linked lists provide appropriate flexibility with minimal overhead.

---

## How It Works

### Schedule Structure

The system operates on a 12-hour workday (9:00 AM to 9:00 PM), divided into 24 time slots of 30 minutes each. Each slot is represented as a node in a linked list.

Three independent schedules are maintained:

| Schedule | Responsible Doctor | Appointment Types |
|----------|-------------------|-------------------|
| Physician | General Physician | Consultations, blood tests, ECG, routine checkups |
| General Surgeon | Surgeon | Minor surgery, major surgery |
| Radiologist | Radiologist | X-ray, ultrasound |

### Appointment Durations

Appointment types occupy different numbers of consecutive slots:

| Appointment Type | Duration | Slots Required |
|-----------------|----------|----------------|
| General Consultancy | 30 minutes | 1 |
| Blood Test / Vaccination | 30 minutes | 1 |
| X-Ray | 30 minutes | 1 |
| ECG Test | 1 hour | 2 |
| Routine Checkup | 1 hour | 2 |
| Minor Surgery | 1 hour | 2 |
| Ultrasound | 1 hour | 2 |
| Major Surgery | 3 hours | 6 |

The system verifies that the required number of consecutive slots is available before confirming a booking.

### Booking Flow

1. User provides name, contact number, appointment type, and preferred time slot
2. System determines appropriate doctor based on appointment type
3. Availability is checked for the requested slot and any subsequent slots required for the appointment duration
4. If available, the slot(s) are marked as booked and patient information is stored in the corresponding linked list nodes
5. Confirmation message is returned to the user

### Cancellation and Rescheduling

When an appointment is cancelled:
- The occupied time slots are marked as available
- The system scans subsequent appointments for patients who have opted into automatic rescheduling
- If a rescheduling-eligible appointment is found that can fit within the freed slots (based on its duration), it is moved to the earlier time
- The original slots occupied by the rescheduled appointment are marked available

This mechanism optimizes schedule utilization by filling gaps created by cancellations.

### Viewing Appointments

Users can retrieve appointment details by entering their contact number. The system searches all three doctor schedules sequentially and returns the appointment information if found.

### Admin Mode

Authorized hospital staff can access a password-protected view displaying all three doctor schedules. Admin users can also cancel any appointment manually if necessary.

### Doctor Mode

Individual doctors can view their own schedule and mark appointments as completed after patient consultation.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend Logic | Python | Linked list implementation, scheduling rules, booking logic |
| Web Server | Flask | HTTP request handling, route management, API endpoints |
| Frontend Structure | HTML | Page layout, forms, buttons, data containers |
| Frontend Styling | CSS | Visual design, responsive layout, color coding of time slots |
| Frontend Interactivity | JavaScript | API communication, dynamic UI updates, form validation |

### System Communication Flow

The four technologies interact as follows:

1. **HTML** presents the user interface (forms, buttons, displays)
2. **JavaScript** captures user actions and sends asynchronous HTTP requests to backend endpoints using the Fetch API
3. **Flask** routes requests to appropriate Python functions, which execute linked list operations
4. **Python** returns JSON responses to the frontend
5. **JavaScript** updates the DOM dynamically based on the response, eliminating full page reloads

This architecture provides a responsive user experience while maintaining clear separation of concerns.

---

## User Roles and Permissions

| Role | Permissions |
|------|-------------|
| Patient | Book appointment, view own appointment, cancel own appointment |
| Doctor | View assigned schedule, mark appointments as completed |
| Admin | View all doctor schedules, cancel any appointment (password protected) |

---

## Example Workflow

**Booking:**
1. Patient selects physician, appointment type (General Consultancy), and time slot (10:00 AM)
2. System verifies availability (1 slot required)
3. Slot is marked booked; patient information is stored
4. Confirmation is displayed

**Cancellation with Rescheduling:**
1. Patient cancels a 10:00 AM appointment (1 slot freed)
2. System scans later slots and finds a 2:00 PM patient who opted into rescheduling
3. The 2:00 PM patient is moved to 10:00 AM
4. The 2:00 PM slot is marked available for new bookings

---

## Installation and Execution

### Prerequisites

- Python 3.8 or higher
- Flask library

### Setup

```bash
pip install flask
