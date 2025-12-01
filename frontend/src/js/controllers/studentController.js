// Ensure user is Student
if (window.location.pathname.includes('dashboard') || window.location.pathname.includes('create-event')) {
    checkAuthRole('Student');
}

let currentEventId = null;

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('upcomingEventsSection')) {
        document.getElementById('navUserName').innerText = localStorage.getItem('name') || 'Student';
        loadUpcomingEvents();
        loadMyRegistrations(); // Auto-load registrations too
    }

    const createForm = document.getElementById('createEventForm');
    if (createForm) {
        createForm.addEventListener('submit', handleCreateEvent);
    }
});

// --- 1. Load Upcoming Events ---
async function loadUpcomingEvents() {
    const container = document.getElementById('upcomingEventsSection');
    try {
        const res = await fetch(`${API_URL.STUDENT}/events`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const events = await res.json();

        if (events.length === 0) {
            container.innerHTML = `<p class="col-span-full text-center text-gray-500 py-10">No upcoming events found.</p>`;
            return;
        }

        container.innerHTML = events.map(e => `
            <div class="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden flex flex-col h-full">
                <img src="${e.poster_url || 'https://via.placeholder.com/400x200'}" class="w-full h-40 object-cover">
                <div class="p-4 flex-1 flex flex-col">
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-bold text-lg text-gray-900 leading-tight">${e.name}</h3>
                        ${e.is_paid 
                            ? `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded font-bold">₹${e.fee}</span>`
                            : `<span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded font-bold">FREE</span>`
                        }
                    </div>
                    <p class="text-sm text-gray-500 mb-2">📅 ${new Date(e.date).toDateString()}</p>
                    <p class="text-sm text-gray-600 line-clamp-3 mb-4 flex-1">${e.description}</p>
                    <button onclick='openEventModal(${JSON.stringify(e).replace(/'/g, "&#39;")})' class="w-full mt-auto bg-green-50 text-green-700 border border-green-200 py-2 rounded hover:bg-green-100 font-semibold transition">
                        View Details
                    </button>
                </div>
            </div>
        `).join('');

    } catch (err) {
        container.innerHTML = `<p class="col-span-full text-center text-red-500">Error loading events</p>`;
    }
}

// --- 2. Handle Create Event ---
async function handleCreateEvent(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.innerText = "Submitting...";

    const data = {
        name: document.getElementById('eventName').value,
        date: document.getElementById('eventDate').value,
        registration_deadline: document.getElementById('regDeadline').value,
        description: document.getElementById('eventDesc').value,
        poster_url: document.getElementById('posterUrl').value,
        requirements: document.getElementById('eventReq').value,
        is_paid: document.getElementById('isPaid').checked,
        fee: document.getElementById('isPaid').checked ? parseInt(document.getElementById('eventFee').value) : 0
    };

    try {
        const res = await fetch(`${API_URL.STUDENT}/create-event`, {
            method: 'POST',
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}` 
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        
        if (res.ok) {
            alert('Event Proposed! Waiting for HOD approval.');
            window.location.href = 'dashboard.html';
        } else {
            alert('Error: ' + result.detail);
            btn.disabled = false;
            btn.innerText = "Submit Proposal";
        }
    } catch (err) {
        alert('Server Error');
        btn.disabled = false;
        btn.innerText = "Submit Proposal";
    }
}

// --- 3. Modal Logic ---
function openEventModal(event) {
    currentEventId = event._id;
    document.getElementById('modalTitle').innerText = event.name;
    document.getElementById('modalDate').innerText = `Date: ${new Date(event.date).toLocaleString()} | Deadline: ${new Date(event.registration_deadline).toLocaleDateString()}`;
    document.getElementById('modalDesc').innerText = event.description;
    document.getElementById('modalPoster').src = event.poster_url;
    
    const feeBadge = document.getElementById('modalFee');
    if (event.is_paid) {
        feeBadge.className = "bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded font-bold";
        feeBadge.innerText = `₹${event.fee}`;
    } else {
        feeBadge.className = "bg-green-100 text-green-800 text-xs px-2 py-1 rounded font-bold";
        feeBadge.innerText = "FREE";
    }

    document.getElementById('eventModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('eventModal').classList.add('hidden');
}

// --- 4. Register for Event (FIXED) ---
async function registerForEvent() {
    if(!currentEventId) return;
    if(!confirm("Confirm Registration?")) return;

    try {
        // Call the new backend endpoint
        const res = await fetch(`${API_URL.STUDENT}/register/${currentEventId}`, {
            method: 'POST',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });

        const data = await res.json();

        if (res.ok) {
            alert(`Success: ${data.message}`);
            closeModal();
            loadMyRegistrations(); // Refresh the "My Registrations" tab
        } else {
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("Server Error");
    }
}

// --- 5. My Registrations (FIXED) ---
async function loadMyRegistrations() {
    const tbody = document.getElementById('myRegistrationsTable');
    try {
        const res = await fetch(`${API_URL.STUDENT}/my-registrations`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const regs = await res.json();

        if (regs.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="px-6 py-4 text-center text-gray-400">No registrations yet</td></tr>`;
            return;
        }

        tbody.innerHTML = regs.map(r => `
            <tr class="bg-white border-b hover:bg-gray-50">
                <td class="px-6 py-4 font-medium text-gray-900">${r.event_name}</td>
                <td class="px-6 py-4">${new Date(r.event_date || r.registered_at).toLocaleDateString()}</td>
                <td class="px-6 py-4">
                    <span class="${r.status === 'Confirmed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'} text-xs font-medium px-2.5 py-0.5 rounded">
                        ${r.status}
                    </span>
                </td>
                <td class="px-6 py-4 text-center">
                    <button class="text-blue-600 hover:underline">View Ticket</button>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-red-500 py-4">Error loading data</td></tr>`;
    }
}

// --- 6. Tab Switcher ---
function switchTab(tabName) {
    const upcomingSec = document.getElementById('upcomingEventsSection');
    const myEventsSec = document.getElementById('myRegistrationsSection');
    const tabUpcoming = document.getElementById('tab-upcoming');
    const tabMyEvents = document.getElementById('tab-my-events');

    if (tabName === 'upcoming') {
        upcomingSec.classList.remove('hidden');
        myEventsSec.classList.add('hidden');
        tabUpcoming.classList.add('border-b-2', 'border-green-700', 'text-green-700', 'font-bold');
        tabUpcoming.classList.remove('text-gray-500');
        tabMyEvents.classList.remove('border-b-2', 'border-green-700', 'text-green-700', 'font-bold');
        tabMyEvents.classList.add('text-gray-500');
    } else {
        upcomingSec.classList.add('hidden');
        myEventsSec.classList.remove('hidden');
        tabMyEvents.classList.add('border-b-2', 'border-green-700', 'text-green-700', 'font-bold');
        tabMyEvents.classList.remove('text-gray-500');
        tabUpcoming.classList.remove('border-b-2', 'border-green-700', 'text-green-700', 'font-bold');
        tabUpcoming.classList.add('text-gray-500');
    }
}