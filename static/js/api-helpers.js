/**
 * API Helper Functions for AZone Project
 * ဒီ file ကို HTML ထဲမှာ include လုပ်ပြီး သုံးနိုင်တယ်
 */

// ============================================
// API Request Helper
// ============================================

/**
 * Make API request with error handling
 * @param {string} url - API endpoint
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} data - Request data (optional)
 * @returns {Promise<object>} Response data
 */
async function apiRequest(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin' // Include cookies for authentication
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || `HTTP ${response.status}: ${response.statusText}`);
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        return { 
            success: false, 
            error: error.message || 'Network error occurred'
        };
    }
}

// ============================================
// Leads API Helpers
// ============================================

/**
 * Get all leads
 * @param {object} filters - Filter options (search, service, status, page, per_page)
 * @returns {Promise<object>} Leads data
 */
async function getLeads(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.service) params.append('service', filters.service);
    if (filters.status) params.append('status', filters.status);
    if (filters.page) params.append('page', filters.page);
    if (filters.per_page) params.append('per_page', filters.per_page);
    
    const url = `/api/leads${params.toString() ? '?' + params.toString() : ''}`;
    return await apiRequest(url, 'GET');
}

/**
 * Create a new lead
 * @param {object} leadData - Lead data (name, email, phone, service, status)
 * @returns {Promise<object>} Created lead data
 */
async function createLead(leadData) {
    return await apiRequest('/api/leads', 'POST', leadData);
}

/**
 * Update a lead
 * @param {number} leadId - Lead ID
 * @param {object} leadData - Updated lead data
 * @returns {Promise<object>} Update result
 */
async function updateLead(leadId, leadData) {
    return await apiRequest(`/api/leads/${leadId}`, 'PUT', leadData);
}

/**
 * Delete a lead
 * @param {number} leadId - Lead ID
 * @returns {Promise<object>} Delete result
 */
async function deleteLead(leadId) {
    return await apiRequest(`/api/leads/${leadId}`, 'DELETE');
}

// ============================================
// Customers API Helpers
// ============================================

/**
 * Get all customers
 * @param {object} filters - Filter options
 * @returns {Promise<object>} Customers data
 */
async function getCustomers(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.status) params.append('status', filters.status);
    if (filters.package) params.append('package', filters.package);
    if (filters.page) params.append('page', filters.page);
    if (filters.per_page) params.append('per_page', filters.per_page);
    
    const url = `/api/customers${params.toString() ? '?' + params.toString() : ''}`;
    return await apiRequest(url, 'GET');
}

/**
 * Create a new customer
 * @param {object} customerData - Customer data
 * @returns {Promise<object>} Created customer data
 */
async function createCustomer(customerData) {
    return await apiRequest('/api/customers', 'POST', customerData);
}

/**
 * Update a customer
 * @param {number} customerId - Customer ID
 * @param {object} customerData - Updated customer data
 * @returns {Promise<object>} Update result
 */
async function updateCustomer(customerId, customerData) {
    return await apiRequest(`/api/customers/${customerId}`, 'PUT', customerData);
}

/**
 * Delete a customer
 * @param {number} customerId - Customer ID
 * @returns {Promise<object>} Delete result
 */
async function deleteCustomer(customerId) {
    return await apiRequest(`/api/customers/${customerId}`, 'DELETE');
}

// ============================================
// Projects API Helpers
// ============================================

/**
 * Get all projects
 * @param {object} filters - Filter options
 * @returns {Promise<object>} Projects data
 */
async function getProjects(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.status) params.append('status', filters.status);
    if (filters.service) params.append('service', filters.service);
    
    const url = `/api/projects${params.toString() ? '?' + params.toString() : ''}`;
    return await apiRequest(url, 'GET');
}

/**
 * Create a new project
 * @param {object} projectData - Project data
 * @returns {Promise<object>} Created project data
 */
async function createProject(projectData) {
    return await apiRequest('/api/projects', 'POST', projectData);
}

/**
 * Update project status
 * @param {number} projectId - Project ID
 * @param {string} status - New status (todo, in-progress, in-review, completed)
 * @returns {Promise<object>} Update result
 */
async function updateProjectStatus(projectId, status) {
    return await apiRequest(`/api/projects/${projectId}/status`, 'PUT', { status });
}

// ============================================
// Dashboard API Helpers
// ============================================

/**
 * Get dashboard statistics
 * @returns {Promise<object>} Dashboard stats
 */
async function getDashboardStats() {
    return await apiRequest('/api/dashboard/stats', 'GET');
}

/**
 * Get dashboard chart data
 * @param {string} period - Time period (7days, 30days, 90days, year)
 * @returns {Promise<object>} Chart data
 */
async function getDashboardChartData(period = '30days') {
    return await apiRequest(`/api/dashboard/chart?period=${period}`, 'GET');
}

// ============================================
// UI Helper Functions
// ============================================

/**
 * Show loading state
 * @param {string} elementId - Element ID to show loading
 */
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner"></div>';
        element.classList.add('loading');
    }
}

/**
 * Hide loading state
 * @param {string} elementId - Element ID to hide loading
 */
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('loading');
    }
}

/**
 * Show error message
 * @param {string} message - Error message
 * @param {string} containerId - Container ID to show error
 */
function showError(message, containerId = 'error-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-error">
                <i class="fas fa-exclamation-circle"></i>
                ${message}
            </div>
        `;
        container.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            container.style.display = 'none';
        }, 5000);
    }
}

/**
 * Show success message
 * @param {string} message - Success message
 * @param {string} containerId - Container ID to show success
 */
function showSuccess(message, containerId = 'success-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i>
                ${message}
            </div>
        `;
        container.style.display = 'block';
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            container.style.display = 'none';
        }, 3000);
    }
}

/**
 * Display data in table
 * @param {Array} data - Data array
 * @param {string} tableBodyId - Table body ID
 * @param {Function} rowRenderer - Function to render each row
 */
function displayTableData(data, tableBodyId, rowRenderer) {
    const tbody = document.getElementById(tableBodyId);
    if (!tbody) return;
    
    if (data.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="100%" class="text-center">
                    <div class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <p>No data found</p>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = data.map(rowRenderer).join('');
}

// ============================================
// Form Validation Helpers
// ============================================

/**
 * Validate email format
 * @param {string} email - Email address
 * @returns {boolean} Is valid email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone format
 * @param {string} phone - Phone number
 * @returns {boolean} Is valid phone
 */
function isValidPhone(phone) {
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 8;
}

/**
 * Validate required fields
 * @param {object} data - Form data
 * @param {Array} requiredFields - Required field names
 * @returns {object} Validation result
 */
function validateRequired(data, requiredFields) {
    const errors = [];
    
    for (const field of requiredFields) {
        if (!data[field] || data[field].toString().trim() === '') {
            errors.push(`${field} is required`);
        }
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        apiRequest,
        getLeads,
        createLead,
        updateLead,
        deleteLead,
        getCustomers,
        createCustomer,
        updateCustomer,
        deleteCustomer,
        getProjects,
        createProject,
        updateProjectStatus,
        getDashboardStats,
        getDashboardChartData,
        showLoading,
        hideLoading,
        showError,
        showSuccess,
        displayTableData,
        isValidEmail,
        isValidPhone,
        validateRequired
    };
}
