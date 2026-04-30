let selectedSlot = null;

function slotToTime(slot) {
    const times = ["9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"];
    return times[slot-1];
}

// Restrict appointment types based on doctor
const doctorTypeMap = {
    physician: [1, 2, 3, 4],
    surgeon: [5, 6],
    radiologist: [7, 8]
};

function filterAppointmentTypes() {
    const doctor = document.getElementById('doctorSelect').value;
    const typeSelect = document.getElementById('typeSelect');
    const allowed = doctorTypeMap[doctor];

    Array.from(typeSelect.options).forEach(opt => {
        const val = parseInt(opt.value);
        opt.style.display = allowed.includes(val) ? '' : 'none';
    });

    const currentVal = parseInt(typeSelect.value);
    if (!allowed.includes(currentVal)) {
        typeSelect.value = allowed[0];
        loadAvailableSlots();
    }
}

async function loadAvailableSlots() {
    const doctor = document.getElementById('doctorSelect').value;
    const choice = document.getElementById('typeSelect').value;
    if (!doctor || !choice) return;
    
    const response = await fetch(`/api/available_slots_with_duration/${doctor}/${choice}`);
    const data = await response.json();
    
    const container = document.getElementById('slotsContainer');
    if (data.slots.length === 0) {
        container.innerHTML = '<p class="error">No available slots</p>';
        return;
    }
    
    container.innerHTML = '<div style="width:100%; margin-bottom:10px;">Click to select:</div>';
    data.slots.forEach(slot => {
        const btn = document.createElement('button');
        btn.className = 'slot-btn';
        btn.textContent = slotToTime(slot);
        btn.onclick = () => {
            document.querySelectorAll('.slot-btn').forEach(b => b.style.border = 'none');
            btn.style.border = '3px solid #ffc107';
            selectedSlot = slot;
        };
        container.appendChild(btn);
    });
}

async function bookAppointment() {
    const name = document.getElementById('patientName').value;
    const contact = document.getElementById('contact').value;
    const choice = parseInt(document.getElementById('typeSelect').value);
    const reschedule = document.getElementById('reschedule').value;
    
    if (!name || !contact) {
        document.getElementById('bookMessage').innerHTML = '<div class="message error">Fill all fields</div>';
        return;
    }
    if (!selectedSlot) {
        document.getElementById('bookMessage').innerHTML = '<div class="message error">Select a time slot</div>';
        return;
    }
    
    const response = await fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, contact, choice, timeslot: selectedSlot, reschedule })
    });
    const data = await response.json();
    
    if (data.success) {
        document.getElementById('bookMessage').innerHTML = `<div class="message success">${data.message}</div>`;
        document.getElementById('patientName').value = '';
        document.getElementById('contact').value = '';
        selectedSlot = null;
        loadAvailableSlots();
    } else {
        document.getElementById('bookMessage').innerHTML = `<div class="message error">${data.message}</div>`;
    }
    setTimeout(() => { document.getElementById('bookMessage').innerHTML = ''; }, 3000);
}

async function viewAppointment() {
    const contact = document.getElementById('viewContact').value;
    if (!contact) {
        document.getElementById('viewResult').innerHTML = '<div class="message error">Enter contact number</div>';
        return;
    }
    
    const response = await fetch(`/api/view/${contact}`);
    const data = await response.json();
    
    if (data.found) {
        document.getElementById('viewResult').innerHTML = `
            <div class="message success">
                ✅ Appointment Found<br>
                <strong>Doctor:</strong> ${data.doctor}<br>
                <strong>Time:</strong> ${data.time}<br>
                <strong>Type:</strong> ${data.type}<br>
                <button onclick="cancelAppointment('${contact}')" style="background:#dc3545; margin-top:10px;">Cancel</button>
            </div>`;
    } else {
        document.getElementById('viewResult').innerHTML = `<div class="message error">${data.message}</div>`;
    }
}

async function cancelAppointment(contact) {
    const viewRes = await fetch(`/api/view/${contact}`);
    const viewData = await viewRes.json();
    if (!viewData.found) return;
    
    let choice = 1;
    const types = {'General Consultancy':1,'Blood Test/Vaccination':2,'ECG test':3,'Routine Checkup':4,'Minor surgery':5,'Major surgery':6,'X Ray':7,'Ultrasound':8};
    if (types[viewData.type]) choice = types[viewData.type];
    
    const response = await fetch('/api/cancel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contact, choice })
    });
    const data = await response.json();
    
    if (data.success) {
        document.getElementById('viewResult').innerHTML = `<div class="message success">${data.message}</div>`;
        document.getElementById('viewContact').value = '';
        loadAvailableSlots();
    }
}

// Event listeners
document.getElementById('doctorSelect').addEventListener('change', () => {
    selectedSlot = null; // 🔥 ONLY added line (fix)
    filterAppointmentTypes();
    loadAvailableSlots();
});

document.getElementById('typeSelect').addEventListener('change', loadAvailableSlots);

// Initialize
filterAppointmentTypes();
loadAvailableSlots();
