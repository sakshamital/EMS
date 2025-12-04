checkAuthRole('Teacher');

document.addEventListener('DOMContentLoaded', () => {
    loadMyStudents();
});

async function loadMyStudents() {
    const tbody = document.getElementById('studentTable');
    const classInfo = document.getElementById('classInfo');
    
    try {
        // We assume we added a Teacher endpoint to config.js: 
        // TEACHER: `${API_BASE_URL}/teacher`
        const res = await fetch(`${API_URL.TEACHER}/my-students`, {
            headers: { "Authorization": `Bearer ${getToken()}` }
        });
        
        const students = await res.json();
        
        if (students.length > 0) {
            // Display the class details from the first student (or user profile)
            const s = students[0];
            classInfo.innerText = `${s.branch} | ${s.year} | Section ${s.section}`;
        } else {
            classInfo.innerText = "No students found in your assigned class.";
            tbody.innerHTML = `<tr><td colspan="4" class="p-4 text-center">Class is empty.</td></tr>`;
            return;
        }

        tbody.innerHTML = students.map(s => `
            <tr class="border-b hover:bg-gray-50">
                <td class="p-3 font-bold text-gray-700">${s.college_id_number || 'N/A'}</td>
                <td class="p-3">
                    <div class="font-medium">${s.name}</div>
                    <div class="text-xs text-gray-500">${s.email}</div>
                </td>
                <td class="p-3">${s.phone}</td>
                <td class="p-3">
                    <span class="px-2 py-1 rounded text-xs font-bold ${s.approval_status === 'Approved' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}">
                        ${s.approval_status}
                    </span>
                </td>
            </tr>
        `).join('');

    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-red-500">Error loading data</td></tr>`;
    }
}