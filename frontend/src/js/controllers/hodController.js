// Ensure user is HOD
checkAuthRole('HOD');

let currentEventId = null;

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('navUserName').innerText = localStorage.getItem('name') || 'HOD';
    loadPendingStudents();
    loadPendingEvents();
});

// --- 1. Load Pending Students ---
async function loadPendingStudents() {
    const tbody = document.getElementById('studentTableBody');
    try {
        // FIX: Use API_URL.ADMIN
        const res = await fetch(`${API_URL.ADMIN}/students/pending`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        if (!res.ok) throw new Error("Failed to fetch");

        const students = await res.json();

        if (students.length === 0) {
            tbody.innerHTML = `<tr><td colspan="3" class="px-4 py-4 text-center text-gray-400">No pending students</td></tr>`;
            return;
        }

        tbody.innerHTML = students.map(s => `
            <tr class="border-b hover:bg-gray-50">
                <td class="px-4 py-3">
                    <div class="font-medium text-gray-900">${s.name}</div>
                    <div class="text-xs text-gray-500">${s.email}</div>
                </td>
                <td class="px-4 py-3 text-sm">
                    <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${s.branch || 'N/A'}</span>
                    <span class="ml-1 text-gray-500">${s.year || ''}</span>
                </td>
                <td class="px-4 py-3 text-center">
                    <button onclick="approveStudent('${s._id}')" class="bg-green-600 text-white p-1.5 rounded hover:bg-green-700" title="Approve">
                        ✔️
                    </button>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="3" class="text-center text-red-500 py-4">Error loading data</td></tr>`;
    }
}

async function approveStudent(id) {
    if (!confirm("Approve this student?")) return;

    try {
        // FIX: Use API_URL.ADMIN
        const res = await fetch(`${API_URL.ADMIN}/students/approve/${id}`, {
            method: 'PATCH',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        if (res.ok) {
            loadPendingStudents(); 
        } else {
            alert("Failed to approve");
        }
    } catch (err) {
        alert("Server Error");
    }
}

// --- 2. Load Pending Events ---
async function loadPendingEvents() {
    const container = document.getElementById('eventListContainer');
    try {
        // FIX: Use API_URL.ADMIN
        const res = await fetch(`${API_URL.ADMIN}/events/pending`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        if (!res.ok) throw new Error("Failed to fetch");

        const events = await res.json();

        if (events.length === 0) {
            container.innerHTML = `<p class="text-center text-gray-400 py-4">No pending events</p>`;
            return;
        }

        container.innerHTML = events.map(e => `
            <div class="border rounded-lg p-4 hover:shadow-md transition bg-white">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-gray-800">${e.name}</h3>
                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Pending</span>
                </div>
                <p class="text-sm text-gray-600 mb-3 line-clamp-2">${e.description}</p>
                <div class="flex justify-between items-center text-xs text-gray-500">
                    <span>📅 ${new Date(e.date).toLocaleDateString()}</span>
                    <button onclick='openEventModal(${JSON.stringify(e).replace(/'/g, "&#39;")})' class="text-indigo-600 hover:text-indigo-800 font-medium">
                        View & Action &rarr;
                    </button>
                </div>
            </div>
        `).join('');

    } catch (err) {
        container.innerHTML = `<p class="text-center text-red-500">Error loading events</p>`;
    }
}

// --- 3. Modal Actions ---
function openEventModal(event) {
    currentEventId = event._id;
    document.getElementById('modalEventName').innerText = event.name;
    document.getElementById('modalEventDate').innerText = `Date: ${new Date(event.date).toDateString()}`;
    document.getElementById('modalEventDesc').innerText = event.description;
    document.getElementById('modalEventReq').innerText = event.requirements || "No special requirements";
    
    document.getElementById('eventModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('eventModal').classList.add('hidden');
    currentEventId = null;
}

async function updateEventStatus(status) {
    if (!currentEventId) return;

    try {
        // FIX: Use API_URL.ADMIN
        const res = await fetch(`${API_URL.ADMIN}/events/status/${currentEventId}?status=${status}`, {
            method: 'PATCH',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        if (res.ok) {
            alert(`Event ${status}!`);
            closeModal();
            loadPendingEvents();
        } else {
            alert("Action failed");
        }
    } catch (err) {
        alert("Server Error");
    }
}

// --- 4. HOD Direct Event Creation (New Feature) ---
function openCreateModal() {
    // Reusing the Student logic for UI simplicity, or you can add a separate modal here.
    // For now, let's just use a simple prompt flow or redirect.
    // Ideally, HOD should have a "create-event.html" similar to students.
    window.location.href = '../student/create-event.html'; // Reuse the form
    // Note: The form needs logic to detect if user is HOD and call the ADMIN API.
}