// Ensure user is Principal, else redirect
checkAuthRole('Principal');

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('navUserName').innerText = localStorage.getItem('name') || 'Principal';
    loadPendingHODs();
});

// --- 1. Load Pending HODs ---
async function loadPendingHODs() {
    const tbody = document.getElementById('hodTableBody');
    try {
        // FIX: Use API_URL.PRINCIPAL
        const res = await fetch(`${API_URL.PRINCIPAL}/hod/pending`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        if (!res.ok) throw new Error("Failed to fetch");

        const hods = await res.json();

        if (hods.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="px-6 py-4 text-center text-gray-400">No pending HOD requests</td></tr>`;
            return;
        }

        tbody.innerHTML = hods.map(h => `
            <tr class="bg-white border-b hover:bg-gray-50">
                <td class="px-6 py-4 font-medium text-gray-900">${h.name}</td>
                <td class="px-6 py-4">
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">${h.branch || 'General'}</span>
                </td>
                <td class="px-6 py-4 text-gray-500">${h.email}</td>
                <td class="px-6 py-4 text-center">
                    <button onclick="approveHOD('${h._id}')" class="font-medium text-green-600 hover:underline">Approve</button>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        console.error(err);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-red-500 py-4">Error loading data</td></tr>`;
    }
}

// --- 2. Approve HOD ---
async function approveHOD(id) {
    if (!confirm("Confirm approval for this HOD?")) return;

    try {
        // FIX: Use API_URL.PRINCIPAL
        const res = await fetch(`${API_URL.PRINCIPAL}/hod/approve/${id}`, {
            method: 'PATCH',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        if (res.ok) {
            alert("HOD Approved Successfully");
            loadPendingHODs();
        } else {
            const data = await res.json();
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("Server Error");
    }
}

// --- 3. Batch Progression ---
async function runBatchProgression() {
    const confirmMsg = "WARNING: This will move all students to the next year (1st->2nd, 2nd->3rd, etc.).\n\nAre you sure you want to proceed?";
    if (!confirm(confirmMsg)) return;

    try {
        // FIX: Use API_URL.PRINCIPAL
        const res = await fetch(`${API_URL.PRINCIPAL}/batch/progress`, {
            method: 'POST',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        const data = await res.json();
        if (res.ok) {
            alert(`Success: ${data.message}\nUpdated: ${data.details}`);
        } else {
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("Server Error during progression");
    }
}

// --- 4. Manual Student Override ---
async function overrideStudent() {
    const email = document.getElementById('overrideId').value;
    const newYear = document.getElementById('newYear').value;

    if (!email) return alert("Please enter a Student Email");

    try {
        // FIX: Use API_URL.PRINCIPAL
        const res = await fetch(`${API_URL.PRINCIPAL}/student/override`, {
            method: 'PATCH',
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}` 
            },
            body: JSON.stringify({ email: email, year: newYear })
        });

        const data = await res.json();
        if (res.ok) {
            alert("Student Profile Updated");
            document.getElementById('overrideId').value = '';
        } else {
            alert("Error: " + data.detail);
        }
    } catch (err) {
        alert("Server Error");
    }
}