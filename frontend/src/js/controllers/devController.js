// Check if user is Developer, else redirect
checkAuthRole('Developer');

document.addEventListener('DOMContentLoaded', () => {
    // Set User Name in Navbar
    document.getElementById('navUserName').innerText = localStorage.getItem('name') || 'Developer';

    // Initial Data Load
    loadColleges();
    loadPendingPrincipals();

    // Form Listener
    document.getElementById('createCollegeForm').addEventListener('submit', handleCreateCollege);
});

// --- 1. Load Colleges ---
async function loadColleges() {
    const tableBody = document.getElementById('collegeListTable');
    try {
        // FIX: Use API_URL.DEVELOPER instead of API_URL
        const res = await fetch(`${API_URL.DEVELOPER}/colleges`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const colleges = await res.json();

        if (!res.ok) throw new Error(colleges.detail || "Failed to load");

        tableBody.innerHTML = colleges.map(col => `
            <tr class="bg-white border-b hover:bg-gray-50">
                <td class="px-4 py-2 font-medium text-gray-900">${col.code}</td>
                <td class="px-4 py-2">${col.name}</td>
                <td class="px-4 py-2">${col.district}</td>
                <td class="px-4 py-2 text-xs text-gray-500">${col.principal_id || '<span class="text-red-500">Unassigned</span>'}</td>
            </tr>
        `).join('');
        
        populateModalDropdown(colleges);

    } catch (err) {
        console.error(err);
        tableBody.innerHTML = `<tr><td colspan="4" class="text-center text-red-500 py-2">Error loading data</td></tr>`;
    }
}

// --- 2. Create College ---
async function handleCreateCollege(e) {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('colName').value,
        code: document.getElementById('colCode').value,
        district: document.getElementById('colDistrict').value
    };

    try {
        // FIX: Use API_URL.DEVELOPER
        const res = await fetch(`${API_URL.DEVELOPER}/college`, {
            method: 'POST',
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}` 
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        
        if (res.ok) {
            alert('College Created Successfully!');
            document.getElementById('createCollegeForm').reset();
           // --- 1. Load Colleges (Updated) ---
async function loadColleges() {
    const tableBody = document.getElementById('collegeListTable');
    try {
        const res = await fetch(`${API_URL.DEVELOPER}/colleges`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        const colleges = await res.json();

        if (!res.ok) throw new Error(colleges.detail || "Failed to load");

        tableBody.innerHTML = colleges.map(col => `
            <tr class="bg-white border-b hover:bg-gray-50">
                <td class="px-4 py-2 font-medium text-gray-900">${col.code}</td>
                <td class="px-4 py-2">${col.name}</td>
                <td class="px-4 py-2">${col.district}</td>
                <td class="px-4 py-2 text-xs text-gray-500">${col.principal_id || '<span class="text-red-500">Unassigned</span>'}</td>
                <td class="px-4 py-2 text-center">
                    <button onclick="deleteCollege('${col._id}')" class="bg-red-100 text-red-600 hover:bg-red-200 px-3 py-1 rounded text-xs font-bold transition">
                        Delete
                    </button>
                </td>
            </tr>
        `).join('');
        
        populateModalDropdown(colleges);

    } catch (err) {
        console.error(err);
        tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-red-500 py-2">Error loading data</td></tr>`;
    }
}

// --- 5. Delete College (New Function) ---
async function deleteCollege(id) {
    if (!confirm("Are you sure you want to delete this college? This cannot be undone.")) return;

    try {
        const res = await fetch(`${API_URL.DEVELOPER}/college/${id}`, {
            method: 'DELETE',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });

        const result = await res.json();

        if (res.ok) {
            alert("College Deleted Successfully");
            loadColleges(); // Refresh the list
        } else {
            alert("Error: " + result.detail);
        }
    } catch (err) {
        alert("Server Error");
    }
}
        } else {
            alert('Error: ' + result.detail);
        }
    } catch (err) {
        alert('Server Error');
    }
}

// --- 3. Load Pending Principals ---
async function loadPendingPrincipals() {
    const tableBody = document.getElementById('pendingPrincipalsTable');
    try {
        // FIX: Use API_URL.DEVELOPER
        const res = await fetch(`${API_URL.DEVELOPER}/principals/pending`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        if (!res.ok) throw new Error("Failed");
        
        const users = await res.json();

        if (users.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="3" class="px-4 py-2 text-center text-gray-500">No pending requests</td></tr>`;
            return;
        }

        tableBody.innerHTML = users.map(user => `
            <tr class="bg-white border-b">
                <td class="px-4 py-2 font-medium">${user.name}</td>
                <td class="px-4 py-2">${user.email}</td>
                <td class="px-4 py-2">
                    <button onclick="openApprovalModal('${user._id}')" class="bg-green-100 text-green-700 px-3 py-1 rounded text-xs hover:bg-green-200">
                        Approve
                    </button>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="3" class="text-center text-sm text-gray-400 py-2">No pending requests</td></tr>`;
    }
}

// --- 4. Modal & Approval Logic ---
function populateModalDropdown(colleges) {
    const select = document.getElementById('modalCollegeSelect');
    const available = colleges.filter(c => !c.principal_id);
    
    if (available.length === 0) {
        select.innerHTML = '<option disabled>No available colleges</option>';
        return;
    }

    select.innerHTML = available.map(c => `
        <option value="${c._id}">${c.name} (${c.code})</option>
    `).join('');
}

function openApprovalModal(userId) {
    document.getElementById('modalPrincipalId').value = userId;
    document.getElementById('approvalModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('approvalModal').classList.add('hidden');
}

async function confirmApproval() {
    const userId = document.getElementById('modalPrincipalId').value;
    const collegeId = document.getElementById('modalCollegeSelect').value;

    if (!collegeId) {
        alert("Please select a college");
        return;
    }

    try {
        // FIX: Use API_URL.DEVELOPER and proper query parameter
        const res = await fetch(`${API_URL.DEVELOPER}/approve/principal/${userId}?college_id=${collegeId}`, {
            method: 'PATCH',
            headers: { "Authorization": `Bearer ${getToken()}` }
        });

        const result = await res.json();
        
        if (res.ok) {
            alert('Principal Approved!');
            closeModal();
            loadPendingPrincipals();
            loadColleges();
        } else {
            alert('Error: ' + result.detail);
        }
    } catch (err) {
        alert('Approval failed');
    }
}