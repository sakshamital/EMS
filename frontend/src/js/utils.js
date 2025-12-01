// --- Utility Functions ---

// 1. Format Date (e.g., "Mon, Oct 25, 2023")
function formatDate(dateString) {
    if (!dateString) return "N/A";
    const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// 2. Format DateTime (e.g., "Oct 25, 10:30 AM")
function formatDateTime(dateString) {
    if (!dateString) return "N/A";
    const options = { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// 3. Simple ID Selector Helper
function $(id) {
    return document.getElementById(id);
}

// 4. Show/Hide Element
function toggleVisibility(elementId, show) {
    const el = document.getElementById(elementId);
    if (show) {
        el.classList.remove('hidden');
    } else {
        el.classList.add('hidden');
    }
}