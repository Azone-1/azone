// Admin Dashboard JavaScript - Leads & Contacts Feature

// Leads Data Storage
let leads = JSON.parse(localStorage.getItem('aZoneLeads')) || [];
let currentSort = { column: null, direction: 'asc' };
let filteredLeads = [];

// Customers Data Storage
let customers = JSON.parse(localStorage.getItem('aZoneCustomers')) || [];
let customerSort = { column: null, direction: 'asc' };
let filteredCustomers = [];

// Projects Data Storage
let projects = JSON.parse(localStorage.getItem('aZoneProjects')) || [];
let filteredProjects = [];

// Sample Customer Data (if no customers exist) - Converted from Leads
const sampleCustomers = [
    {
        id: 'CUST-001',
        name: 'James Thompson',
        email: 'james.thompson@techcorp.com',
        phone: '+1 (415) 555-0123',
        package: 'Bot Reply Packages',
        joinDate: '2024-01-05',
        status: 'Active',
        originalLeadId: '1'
    },
    {
        id: 'CUST-002',
        name: 'Maria Rodriguez',
        email: 'maria.rodriguez@marketingpro.io',
        phone: '+1 (212) 555-0456',
        package: 'Content Packs',
        joinDate: '2024-01-12',
        status: 'Trial',
        originalLeadId: '2'
    },
    {
        id: 'CUST-003',
        name: 'Robert Chen',
        email: 'robert.chen@startupxyz.com',
        phone: '+1 (310) 555-0789',
        package: 'Content Packs',
        joinDate: '2024-01-15',
        status: 'Active',
        originalLeadId: '3'
    },
    {
        id: 'CUST-004',
        name: 'Sarah Williams',
        email: 'sarah.williams@mediagroup.net',
        phone: '+1 (617) 555-0234',
        package: 'Video Packs',
        joinDate: '2024-01-18',
        status: 'Suspended',
        originalLeadId: '4'
    },
    {
        id: 'CUST-005',
        name: 'Michael Anderson',
        email: 'michael.anderson@innovateai.com',
        phone: '+1 (206) 555-0567',
        package: 'AI Tools & Automation',
        joinDate: '2024-01-20',
        status: 'Active',
        originalLeadId: '5'
    },
    {
        id: 'CUST-006',
        name: 'Jennifer Martinez',
        email: 'jennifer.martinez@digitalpro.com',
        phone: '+1 (312) 555-0901',
        package: 'Auto Post Packages',
        joinDate: '2023-12-28',
        status: 'Active',
        originalLeadId: null
    },
    {
        id: 'CUST-007',
        name: 'David Kim',
        email: 'david.kim@techsolutions.io',
        phone: '+1 (408) 555-0134',
        package: 'Bot Reply Packages',
        joinDate: '2024-01-08',
        status: 'Trial',
        originalLeadId: null
    },
    {
        id: 'CUST-008',
        name: 'Emily Brown',
        email: 'emily.brown@creativestudio.net',
        phone: '+1 (213) 555-0567',
        package: 'Video Packs',
        joinDate: '2023-12-15',
        status: 'Inactive',
        originalLeadId: null
    },
    {
        id: 'CUST-009',
        name: 'Christopher Taylor',
        email: 'christopher.taylor@enterprise.com',
        phone: '+1 (415) 555-0789',
        package: 'AI Tools & Automation',
        joinDate: '2024-01-10',
        status: 'Active',
        originalLeadId: null
    },
    {
        id: 'CUST-010',
        name: 'Amanda Wilson',
        email: 'amanda.wilson@brandagency.com',
        phone: '+1 (646) 555-0123',
        package: 'Payment Integration',
        joinDate: '2024-01-22',
        status: 'Trial',
        originalLeadId: null
    }
];

// Sample Data (if no leads exist) - A Zone Studio Services
const sampleLeads = [
        {
            id: '1',
        name: 'James Thompson',
        email: 'james.thompson@techcorp.com',
        phone: '+1 (415) 555-0123',
        service: 'Bot Reply Packages',
        date: '2024-01-20',
        status: 'New'
        },
        {
            id: '2',
        name: 'Maria Rodriguez',
        email: 'maria.rodriguez@marketingpro.io',
        phone: '+1 (212) 555-0456',
        service: 'Content Packs',
        date: '2024-01-19',
        status: 'New'
        },
        {
            id: '3',
        name: 'Robert Chen',
        email: 'robert.chen@startupxyz.com',
        phone: '+1 (310) 555-0789',
        service: 'Content Packs',
        date: '2024-01-18',
        status: 'New'
    },
    {
        id: '4',
        name: 'Sarah Williams',
        email: 'sarah.williams@mediagroup.net',
        phone: '+1 (617) 555-0234',
        service: 'Video Packs',
        date: '2024-01-17',
        status: 'New'
    },
    {
        id: '5',
        name: 'Michael Anderson',
        email: 'michael.anderson@innovateai.com',
        phone: '+1 (206) 555-0567',
        service: 'AI Tools & Automation',
        date: '2024-01-16',
        status: 'New'
    }
];

// Sample Project Data (if no projects exist)
const sampleProjects = [
    {
        id: 'PROJ-001',
        name: 'Bot Training for James Thompson',
        customer: 'James Thompson',
        customerId: 'CUST-001',
        service: 'Bot Reply Packages',
        status: 'todo',
        priority: 'High',
        dueDate: '2024-02-05',
        assignedStaff: 'John Smith',
        description: 'Setup and training for AI chatbot system'
    },
    {
        id: 'PROJ-002',
        name: 'Content Creation for Maria Rodriguez',
        customer: 'Maria Rodriguez',
        customerId: 'CUST-002',
        service: 'Content Packs',
        status: 'in-progress',
        priority: 'Medium',
        dueDate: '2024-01-28',
        assignedStaff: 'Sarah Johnson',
        description: 'Create 20 blog posts and social media content'
    },
    {
        id: 'PROJ-003',
        name: 'Short Video Editing for Sarah Williams',
        customer: 'Sarah Williams',
        customerId: 'CUST-004',
        service: 'Video Packs',
        status: 'in-review',
        priority: 'High',
        dueDate: '2024-01-25',
        assignedStaff: 'Mike Chen',
        description: 'Edit 10 promotional video clips'
    },
    {
        id: 'PROJ-004',
        name: 'AI Automation Setup for Michael Anderson',
        customer: 'Michael Anderson',
        customerId: 'CUST-005',
        service: 'AI Tools & Automation',
        status: 'completed',
        priority: 'High',
        dueDate: '2024-01-20',
        assignedStaff: 'Emily Davis',
        description: 'Implement workflow automation system'
    },
    {
        id: 'PROJ-005',
        name: 'Content Strategy for Robert Chen',
        customer: 'Robert Chen',
        customerId: 'CUST-003',
        service: 'Content Packs',
        status: 'todo',
        priority: 'Low',
        dueDate: '2024-02-10',
        assignedStaff: 'Sarah Johnson',
        description: 'Develop content calendar and strategy'
    },
    {
        id: 'PROJ-006',
        name: 'Bot Reply Configuration for David Kim',
        customer: 'David Kim',
        customerId: 'CUST-007',
        service: 'Bot Reply Packages',
        status: 'in-progress',
        priority: 'Medium',
        dueDate: '2024-01-30',
        assignedStaff: 'John Smith',
        description: 'Configure chatbot responses and integrations'
    },
    {
        id: 'PROJ-007',
        name: 'Video Production for Jennifer Martinez',
        customer: 'Jennifer Martinez',
        customerId: 'CUST-006',
        service: 'Video Packs',
        status: 'in-review',
        priority: 'Medium',
        dueDate: '2024-01-27',
        assignedStaff: 'Mike Chen',
        description: 'Produce marketing video series'
    },
    {
        id: 'PROJ-008',
        name: 'Auto Post Setup for Amanda Wilson',
        customer: 'Amanda Wilson',
        customerId: 'CUST-010',
        service: 'Auto Post Packages',
        status: 'todo',
        priority: 'Low',
        dueDate: '2024-02-15',
        assignedStaff: 'David Wilson',
        description: 'Setup automated social media posting'
    }
];

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeLeads();
    initializeCustomers();
    initializeProjects();
    initializeDashboard();
    setupEventListeners();
    renderLeadsTable();
});

function initializeLeads() {
    // Load leads from localStorage or initialize with sample data
    if (leads.length === 0) {
        leads = [...sampleLeads];
        saveLeads();
    }
    filteredLeads = [...leads];
}

function initializeCustomers() {
    // Load customers from localStorage or initialize with sample data
    if (customers.length === 0) {
        customers = [...sampleCustomers];
        saveCustomers();
    }
    filteredCustomers = [...customers];
}

function saveCustomers() {
    localStorage.setItem('aZoneCustomers', JSON.stringify(customers));
}

function initializeProjects() {
    // Load projects from localStorage or initialize with sample data
    if (projects.length === 0) {
        projects = [...sampleProjects];
        saveProjects();
    }
    filteredProjects = [...projects];
}

function saveProjects() {
    localStorage.setItem('aZoneProjects', JSON.stringify(projects));
}

function saveLeads() {
    localStorage.setItem('aZoneLeads', JSON.stringify(leads));
}

function initializeDashboard() {
    // Set default active section to dashboard (overview)
    switchSection('dashboard');
    // Initialize dashboard data
    updateDashboardKPIs();
    renderRecentLeads();
}

function setupEventListeners() {
    // Sidebar Navigation
    const navItems = document.querySelectorAll('.nav-item[data-section]');
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
            const section = item.dataset.section;
        
            // Update active nav item
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        
            // Switch section
            switchSection(section);
        });
    });

    // Notification Button
    const notificationBtn = document.getElementById('notification-btn');
    const notificationDropdown = document.getElementById('notification-dropdown');
    
    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationDropdown.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!notificationBtn.contains(e.target) && !notificationDropdown.contains(e.target)) {
                notificationDropdown.classList.remove('active');
            }
        });
    }

    // Logout Button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to logout?')) {
                console.log('Logout clicked');
            }
        });
    }

    // Leads Search
    const leadSearch = document.getElementById('lead-search');
    if (leadSearch) {
        leadSearch.addEventListener('input', handleSearch);
    }

    // Filter Dropdowns
    const filterService = document.getElementById('filter-service');
    const filterStatus = document.getElementById('filter-status');
    
    if (filterService) {
        filterService.addEventListener('change', handleFilter);
    }
    
    if (filterStatus) {
        filterStatus.addEventListener('change', handleFilter);
    }

    // Clear Filters
    const clearFiltersBtn = document.getElementById('clear-filters-btn');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', clearFilters);
    }

    // Sortable Table Headers
    const sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            handleSort(column);
        });
    });

    // Add Lead Button
    const addLeadBtn = document.getElementById('add-lead-btn');
    if (addLeadBtn) {
        addLeadBtn.addEventListener('click', () => {
            alert('Add Lead functionality will be implemented here');
        });
    }

    // Customer Search
    const customerSearch = document.getElementById('customer-search');
    if (customerSearch) {
        customerSearch.addEventListener('input', handleCustomerSearch);
    }

    // Customer Filter Dropdowns
    const filterCustomerStatus = document.getElementById('filter-customer-status');
    const filterCustomerPackage = document.getElementById('filter-customer-package');
    
    if (filterCustomerStatus) {
        filterCustomerStatus.addEventListener('change', handleCustomerFilter);
    }
    
    if (filterCustomerPackage) {
        filterCustomerPackage.addEventListener('change', handleCustomerFilter);
    }

    // Clear Customer Filters
    const clearCustomerFiltersBtn = document.getElementById('clear-customer-filters-btn');
    if (clearCustomerFiltersBtn) {
        clearCustomerFiltersBtn.addEventListener('click', clearCustomerFilters);
    }

    // Customer Table Sort Headers
    const customerSortHeaders = document.querySelectorAll('#customers-table .sortable');
    customerSortHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            handleCustomerSort(column);
        });
    });

    // Add Customer Button
    const addCustomerBtn = document.getElementById('add-customer-btn');
    if (addCustomerBtn) {
        addCustomerBtn.addEventListener('click', () => {
            alert('Add Customer functionality will be implemented here');
        });
    }

    // Project Search
    const projectSearch = document.getElementById('project-search');
    if (projectSearch) {
        projectSearch.addEventListener('input', handleProjectSearch);
    }

    // Project Filter Dropdowns
    const filterProjectService = document.getElementById('filter-project-service');
    const filterProjectStaff = document.getElementById('filter-project-staff');
    const filterProjectPriority = document.getElementById('filter-project-priority');
    
    if (filterProjectService) {
        filterProjectService.addEventListener('change', handleProjectFilter);
    }
    
    if (filterProjectStaff) {
        filterProjectStaff.addEventListener('change', handleProjectFilter);
    }
    
    if (filterProjectPriority) {
        filterProjectPriority.addEventListener('change', handleProjectFilter);
    }

    // Clear Project Filters
    const clearProjectFiltersBtn = document.getElementById('clear-project-filters-btn');
    if (clearProjectFiltersBtn) {
        clearProjectFiltersBtn.addEventListener('click', clearProjectFilters);
    }

    // Add Project Button
    const addProjectBtn = document.getElementById('add-project-btn');
    if (addProjectBtn) {
        addProjectBtn.addEventListener('click', () => {
            alert('Add Project functionality will be implemented here');
        });
    }
}

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    applyFilters(searchTerm);
}

function handleFilter() {
    applyFilters();
}

function clearFilters() {
    document.getElementById('lead-search').value = '';
    document.getElementById('filter-service').value = '';
    document.getElementById('filter-status').value = '';
    applyFilters();
}

function applyFilters(searchTerm = null) {
    const searchInput = document.getElementById('lead-search');
    const serviceFilter = document.getElementById('filter-service').value;
    const statusFilter = document.getElementById('filter-status').value;
    
    const search = searchTerm !== null ? searchTerm : searchInput.value.toLowerCase().trim();
    
    filteredLeads = leads.filter(lead => {
        // Search filter
        const matchesSearch = !search || 
            lead.name.toLowerCase().includes(search) ||
            lead.email.toLowerCase().includes(search) ||
            lead.phone.toLowerCase().includes(search);
        
        // Service filter
        const matchesService = !serviceFilter || lead.service === serviceFilter;
        
        // Status filter
        const matchesStatus = !statusFilter || lead.status === statusFilter;
        
        return matchesSearch && matchesService && matchesStatus;
    });
    
    // Apply current sort
    if (currentSort.column) {
        sortLeads(currentSort.column, currentSort.direction, false);
    } else {
        renderLeadsTable();
    }
}

function handleSort(column) {
    let direction = 'asc';
    
    // If clicking the same column, toggle direction
    if (currentSort.column === column) {
        direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    }
    
    sortLeads(column, direction, true);
}

function sortLeads(column, direction, updateState = true) {
    if (updateState) {
        currentSort = { column, direction };
    }
    
    filteredLeads.sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];
        
        // Handle date sorting
        if (column === 'date') {
            aVal = new Date(aVal);
            bVal = new Date(bVal);
        } else {
            // String comparison
            aVal = String(aVal).toLowerCase();
            bVal = String(bVal).toLowerCase();
        }
        
        if (aVal < bVal) return direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return direction === 'asc' ? 1 : -1;
        return 0;
    });
    
    updateSortIcons(column, direction);
    renderLeadsTable();
}

function updateSortIcons(column, direction) {
    // Reset all sort icons
    document.querySelectorAll('.sortable').forEach(header => {
        header.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Set active sort icon
    const activeHeader = document.querySelector(`.sortable[data-column="${column}"]`);
    if (activeHeader) {
        activeHeader.classList.add(`sort-${direction}`);
    }
}

function renderLeadsTable() {
    const tbody = document.getElementById('leads-table-body');
    const emptyState = document.getElementById('table-empty');
    
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (filteredLeads.length === 0) {
        tbody.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
        }
        return;
    }
    
    tbody.style.display = '';
    if (emptyState) {
        emptyState.style.display = 'none';
    }
    
    filteredLeads.forEach(lead => {
        const row = createLeadRow(lead);
        tbody.appendChild(row);
    });
    
    // Attach event listeners to action buttons
    attachActionListeners();
}

function createLeadRow(lead) {
    const row = document.createElement('tr');
    row.dataset.id = lead.id;
    
    // Format date
    const formattedDate = formatDate(lead.date);
    
    // Status badge
    const statusBadge = `<span class="status-badge ${lead.status.toLowerCase()}">${lead.status}</span>`;
    
    // Action buttons
    const markContactedDisabled = lead.status === 'Contacted' || lead.status === 'Converted' ? 'disabled' : '';
    const convertDisabled = lead.status === 'Converted' ? 'disabled' : '';
    
    row.innerHTML = `
        <td>${lead.name}</td>
        <td>${lead.email}</td>
        <td>${lead.phone}</td>
        <td>${lead.service}</td>
        <td>${formattedDate}</td>
        <td>${statusBadge}</td>
        <td>
            <div class="action-buttons">
                <button class="btn-action contacted" data-action="contacted" data-id="${lead.id}" ${markContactedDisabled}>
                    <i class="fas fa-phone"></i>
                    Mark as Contacted
                </button>
                <button class="btn-action convert" data-action="convert" data-id="${lead.id}" ${convertDisabled}>
                    <i class="fas fa-check-circle"></i>
                    Convert to Customer
                </button>
            </div>
        </td>
    `;
    
    return row;
}

function attachActionListeners() {
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const action = button.dataset.action;
            const leadId = button.dataset.id;
            
            if (button.disabled) return;
            
            handleLeadAction(leadId, action);
        });
    });
}

function handleLeadAction(leadId, action) {
    const lead = leads.find(l => l.id === leadId);
    if (!lead) return;
    
    if (action === 'contacted') {
        if (confirm(`Mark "${lead.name}" as Contacted?`)) {
            lead.status = 'Contacted';
            saveLeads();
            applyFilters();
            showNotification(`Lead "${lead.name}" marked as Contacted`);
        }
    } else if (action === 'convert') {
        // Step A: Validate lead can be converted
        if (lead.status === 'Converted') {
            alert('This lead has already been converted.');
            return;
        }
        
        if (!lead.name || !lead.email || !lead.service) {
            alert('Cannot convert lead: Missing required information.');
            return;
        }
        
        // Check for duplicate customer email
        const existingCustomer = customers.find(c => c.email.toLowerCase() === lead.email.toLowerCase());
        if (existingCustomer) {
            const proceed = confirm(`A customer with email "${lead.email}" already exists.\n\nDo you want to proceed and create a new project for this lead?`);
            if (!proceed) return;
        }
        
        if (confirm(`Convert "${lead.name}" to Customer and create a new project?`)) {
            // Step A: Update Lead Status
            lead.status = 'Converted';
            if (!lead.convertedDate) {
                lead.convertedDate = new Date().toISOString().split('T')[0];
            }
            saveLeads();
            
            // Step B: Create Customer Record
            const customerId = generateCustomerId();
            const customer = {
                id: customerId,
                name: lead.name,
                email: lead.email,
                phone: lead.phone,
                package: lead.service,  // Interested Service becomes Current Package
                joinDate: new Date().toISOString().split('T')[0],
                status: 'Trial',  // Default status for new customers
                originalLeadId: lead.id  // Reference to original lead
            };
            
            // Only add customer if email doesn't exist
            if (!existingCustomer) {
                customers.push(customer);
                saveCustomers();
            }
            
            // Step C: Create Project Record
            const projectId = generateProjectId();
            const projectName = generateProjectName(lead.service, lead.name);
            const project = {
                id: projectId,
                name: projectName,
                customer: lead.name,
                customerId: existingCustomer ? existingCustomer.id : customerId,
                service: lead.service,
                status: 'todo',  // Default: To Do column
                priority: 'Medium',  // Default priority
                dueDate: calculateDueDate(14),  // Default: 14 days from today
                assignedStaff: 'Unassigned',  // Default staff assignment
                description: generateProjectDescription(lead.service),
                createdDate: new Date().toISOString().split('T')[0],
                originalLeadId: lead.id  // Reference to original lead
            };
            
            projects.push(project);
            saveProjects();
            
            // Update filtered data
            applyFilters();
            if (filteredCustomers.length > 0) {
                applyCustomerFilters();
            }
            if (filteredProjects.length > 0) {
                applyProjectFilters();
            }
            
            // Step D: Display Success Notification
            const customerUsed = existingCustomer ? existingCustomer.name : customer.name;
            showNotification(
                `Lead successfully converted! ` +
                `Customer '${customerUsed}' ${existingCustomer ? 'exists' : 'created'}. ` +
                `Project '${projectName}' added to 'To Do' list.`
            );
            
            // Refresh UI if relevant sections are active
            const activeSection = document.querySelector('.section-content.active')?.id;
            if (activeSection === 'users-section') {
                renderCustomersTable();
            } else if (activeSection === 'projects-section') {
                renderKanbanBoard();
            } else if (activeSection === 'dashboard-section') {
                updateDashboardKPIs();
                renderRecentLeads();
            }
        }
    }
}

// Helper Functions for Lead Conversion

function generateCustomerId() {
    // Generate next customer ID (CUST-001, CUST-002, etc.)
    const maxId = customers.reduce((max, customer) => {
        const num = parseInt(customer.id.replace('CUST-', ''));
        return num > max ? num : max;
    }, 0);
    return `CUST-${String(maxId + 1).padStart(3, '0')}`;
}

function generateProjectId() {
    // Generate next project ID (PROJ-001, PROJ-002, etc.)
    const maxId = projects.reduce((max, project) => {
        const num = parseInt(project.id.replace('PROJ-', ''));
        return num > max ? num : max;
    }, 0);
    return `PROJ-${String(maxId + 1).padStart(3, '0')}`;
}

function generateProjectName(service, customerName) {
    // Generate descriptive project name based on service type
    const namePatterns = {
        'Bot Reply Packages': `Bot Setup for ${customerName}`,
        'Content Packs': `Content Creation for ${customerName}`,
        'Video Packs': `Video Production for ${customerName}`,
        'AI Tools & Automation': `AI Automation Setup for ${customerName}`,
        'Auto Post Packages': `Auto Post Setup for ${customerName}`,
        'Payment Integration': `Payment Integration for ${customerName}`
    };
    
    return namePatterns[service] || `Project Setup for ${customerName}`;
}

function generateProjectDescription(service) {
    // Generate project description based on service type
    const descriptions = {
        'Bot Reply Packages': 'Setup and configure AI chatbot system with training and integration',
        'Content Packs': 'Create high-quality content including blog posts and social media materials',
        'Video Packs': 'Produce and edit professional video content for marketing and promotion',
        'AI Tools & Automation': 'Implement AI-powered automation workflows and tools',
        'Auto Post Packages': 'Configure automated social media posting system',
        'Payment Integration': 'Integrate payment processing system with platform'
    };
    
    return descriptions[service] || 'Project setup and configuration';
}

function calculateDueDate(daysFromNow) {
    // Calculate due date (default 14 days from today)
    const dueDate = new Date();
    dueDate.setDate(dueDate.getDate() + daysFromNow);
    return dueDate.toISOString().split('T')[0];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function showNotification(message) {
    // Simple notification (can be enhanced with toast notifications)
    console.log(message);
    // You can add a toast notification library here if needed
}

function switchSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section-content');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    const activeSection = document.getElementById(`${sectionName}-section`);
    if (activeSection) {
        activeSection.classList.add('active');
    }

    // Update page title and breadcrumb
    updatePageTitle(sectionName);
    updateBreadcrumb(sectionName);
    
    // Re-render content based on section
    if (sectionName === 'leads') {
        renderLeadsTable();
    } else if (sectionName === 'dashboard') {
        updateDashboardKPIs();
        renderRecentLeads();
    } else if (sectionName === 'users') {
        renderCustomersTable();
    } else if (sectionName === 'projects') {
        renderKanbanBoard();
    }
}

function updatePageTitle(sectionName) {
    const titles = {
        leads: 'Leads & Contacts',
        dashboard: 'Dashboard',
        users: 'Users',
        services: 'Services',
        projects: 'Projects',
        payments: 'Payments',
        analytics: 'Analytics',
        settings: 'Settings'
    };

    const pageTitle = document.querySelector('.page-title');
    if (pageTitle) {
        pageTitle.textContent = titles[sectionName] || 'Dashboard';
    }
}

function updateBreadcrumb(sectionName) {
    const breadcrumbs = {
        leads: 'Home / Leads & Contacts',
        dashboard: 'Home / Dashboard',
        users: 'Home / Users',
        services: 'Home / Services',
        projects: 'Home / Projects',
        payments: 'Home / Payments',
        analytics: 'Home / Analytics',
        settings: 'Home / Settings'
    };

    const breadcrumb = document.querySelector('.breadcrumb');
    if (breadcrumb) {
        breadcrumb.textContent = breadcrumbs[sectionName] || 'Home / Dashboard';
    }
}

// Dashboard KPI Functions
function updateDashboardKPIs() {
    // Calculate KPI values from leads data
    const now = new Date();
    const thirtyDaysAgo = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000));
    
    // New Leads (Past 30 Days)
    const newLeads30Days = leads.filter(lead => {
        const leadDate = new Date(lead.date);
        return leadDate >= thirtyDaysAgo;
    }).length;
    
    // Calculate trend (dummy data for now - can be calculated from historical data)
    const newLeadsTrend = 15.5; // Percentage change
    
    // Active Projects (dummy data - can be linked to projects array if exists)
    const activeProjects = 12;
    const activeProjectsTrend = 8.2;
    
    // Total Customers (Converted leads + existing customers)
    const convertedLeads = leads.filter(lead => lead.status === 'Converted').length;
    const totalCustomers = convertedLeads + 45; // Add base customers
    const customersTrend = 12.3;
    
    // Monthly Revenue (dummy data)
    const monthlyRevenue = 32450;
    const revenueGoal = 50000;
    const revenuePercentage = Math.round((monthlyRevenue / revenueGoal) * 100);
    
    // Update KPI Cards
    const kpiNewLeads = document.getElementById('kpi-new-leads');
    const kpiLeadsTrend = document.getElementById('kpi-leads-trend');
    const kpiActiveProjects = document.getElementById('kpi-active-projects');
    const kpiProjectsTrend = document.getElementById('kpi-projects-trend');
    const kpiTotalCustomers = document.getElementById('kpi-total-customers');
    const kpiCustomersTrend = document.getElementById('kpi-customers-trend');
    const kpiMonthlyRevenue = document.getElementById('kpi-monthly-revenue');
    const kpiRevenueTrend = document.getElementById('kpi-revenue-trend');
    
    if (kpiNewLeads) kpiNewLeads.textContent = newLeads30Days;
    if (kpiLeadsTrend) kpiLeadsTrend.textContent = `${newLeadsTrend}%`;
    
    if (kpiActiveProjects) kpiActiveProjects.textContent = activeProjects;
    if (kpiProjectsTrend) kpiProjectsTrend.textContent = `${activeProjectsTrend}%`;
    
    if (kpiTotalCustomers) kpiTotalCustomers.textContent = totalCustomers;
    if (kpiCustomersTrend) kpiCustomersTrend.textContent = `${customersTrend}%`;
    
    if (kpiMonthlyRevenue) kpiMonthlyRevenue.textContent = `$${monthlyRevenue.toLocaleString()}`;
    if (kpiRevenueTrend) kpiRevenueTrend.textContent = `${revenuePercentage}%`;
}

function renderRecentLeads() {
    const tbody = document.getElementById('recent-leads-table-body');
    const emptyState = document.getElementById('recent-leads-empty');
    
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    // Get last 5 leads sorted by date (most recent first)
    const recentLeads = [...leads]
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 5);
    
    if (recentLeads.length === 0) {
        tbody.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
        }
        return;
    }
    
    tbody.style.display = '';
    if (emptyState) {
        emptyState.style.display = 'none';
    }
    
    recentLeads.forEach(lead => {
        const row = createRecentLeadRow(lead);
        tbody.appendChild(row);
    });
}

function createRecentLeadRow(lead) {
    const row = document.createElement('tr');
    row.dataset.id = lead.id;
    
    // Status badge
    const statusBadge = `<span class="status-badge ${lead.status.toLowerCase()}">${lead.status}</span>`;
    
    row.innerHTML = `
        <td>${lead.name}</td>
        <td>${lead.service}</td>
        <td>${statusBadge}</td>
    `;
    
    return row;
}

// View All Leads Link
const viewAllLeadsLink = document.getElementById('view-all-leads');
if (viewAllLeadsLink) {
    viewAllLeadsLink.addEventListener('click', (e) => {
        e.preventDefault();
        // Switch to leads section
        const leadsNavItem = document.querySelector('.nav-item[data-section="leads"]');
        if (leadsNavItem) {
            leadsNavItem.click();
        }
    });
}

// Chart Period Select
const chartPeriodSelect = document.querySelector('.chart-period-select');
if (chartPeriodSelect) {
    chartPeriodSelect.addEventListener('change', (e) => {
        // Handle chart period change
        console.log('Chart period changed to:', e.target.value);
        // This can be used to update chart data when chart library is integrated
    });
}

// Customer Management Functions
function handleCustomerSearch(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    applyCustomerFilters(searchTerm);
}

function handleCustomerFilter() {
    applyCustomerFilters();
}

function clearCustomerFilters() {
    document.getElementById('customer-search').value = '';
    document.getElementById('filter-customer-status').value = '';
    document.getElementById('filter-customer-package').value = '';
    applyCustomerFilters();
}

function applyCustomerFilters(searchTerm = null) {
    const searchInput = document.getElementById('customer-search');
    const statusFilter = document.getElementById('filter-customer-status')?.value || '';
    const packageFilter = document.getElementById('filter-customer-package')?.value || '';
    
    const search = searchTerm !== null ? searchTerm : searchInput.value.toLowerCase().trim();
    
    filteredCustomers = customers.filter(customer => {
        // Search filter
        const matchesSearch = !search || 
            customer.id.toLowerCase().includes(search) ||
            customer.name.toLowerCase().includes(search) ||
            customer.email.toLowerCase().includes(search) ||
            customer.phone.toLowerCase().includes(search);
        
        // Status filter
        const matchesStatus = !statusFilter || customer.status === statusFilter;
        
        // Package filter
        const matchesPackage = !packageFilter || customer.package === packageFilter;
        
        return matchesSearch && matchesStatus && matchesPackage;
    });
    
    // Apply current sort
    if (customerSort.column) {
        sortCustomers(customerSort.column, customerSort.direction, false);
    } else {
        renderCustomersTable();
    }
}

function handleCustomerSort(column) {
    let direction = 'asc';
    
    // If clicking the same column, toggle direction
    if (customerSort.column === column) {
        direction = customerSort.direction === 'asc' ? 'desc' : 'asc';
    }
    
    sortCustomers(column, direction, true);
}

function sortCustomers(column, direction, updateState = true) {
    if (updateState) {
        customerSort = { column, direction };
    }
    
    filteredCustomers.sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];
        
        // Handle date sorting
        if (column === 'joinDate') {
            aVal = new Date(aVal);
            bVal = new Date(bVal);
        } else {
            // String comparison
            aVal = String(aVal).toLowerCase();
            bVal = String(bVal).toLowerCase();
        }
        
        if (aVal < bVal) return direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return direction === 'asc' ? 1 : -1;
        return 0;
    });
    
    updateCustomerSortIcons(column, direction);
    renderCustomersTable();
}

function updateCustomerSortIcons(column, direction) {
    // Reset all sort icons in customers table
    document.querySelectorAll('#customers-table .sortable').forEach(header => {
        header.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Set active sort icon
    const activeHeader = document.querySelector(`#customers-table .sortable[data-column="${column}"]`);
    if (activeHeader) {
        activeHeader.classList.add(`sort-${direction}`);
    }
}

function renderCustomersTable() {
    const tbody = document.getElementById('customers-table-body');
    const emptyState = document.getElementById('customers-empty');
    
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (filteredCustomers.length === 0) {
        tbody.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
        }
        return;
    }
    
    tbody.style.display = '';
    if (emptyState) {
        emptyState.style.display = 'none';
    }
    
    filteredCustomers.forEach(customer => {
        const row = createCustomerRow(customer);
        tbody.appendChild(row);
    });
    
    // Attach event listeners to action buttons
    attachCustomerActionListeners();
}

function createCustomerRow(customer) {
    const row = document.createElement('tr');
    row.dataset.id = customer.id;
    
    // Format date
    const formattedDate = formatDate(customer.joinDate);
    
    // Status badge
    const statusBadge = `<span class="status-badge ${customer.status.toLowerCase()}">${customer.status}</span>`;
    
    // Action buttons
    const suspendDisabled = customer.status === 'Suspended' ? 'disabled' : '';
    const suspendText = customer.status === 'Suspended' ? 'Unsuspend' : 'Suspend Account';
    
    row.innerHTML = `
        <td>${customer.id}</td>
        <td>${customer.name}</td>
        <td>${customer.email}</td>
        <td>${customer.phone}</td>
        <td>${customer.package}</td>
        <td>${formattedDate}</td>
        <td>${statusBadge}</td>
        <td>
            <div class="action-buttons">
                <button class="btn-action view-profile" data-action="view-profile" data-id="${customer.id}">
                    <i class="fas fa-user-circle"></i>
                    View Profile
                </button>
                <button class="btn-action suspend" data-action="suspend" data-id="${customer.id}" ${suspendDisabled}>
                    <i class="fas fa-ban"></i>
                    ${suspendText}
                </button>
                <button class="btn-action upgrade" data-action="upgrade" data-id="${customer.id}">
                    <i class="fas fa-arrow-up"></i>
                    Upgrade/Downgrade
                </button>
            </div>
        </td>
    `;
    
    return row;
}

function attachCustomerActionListeners() {
    const actionButtons = document.querySelectorAll('#customers-table .btn-action');
    actionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const action = button.dataset.action;
            const customerId = button.dataset.id;
            
            if (button.disabled) return;
            
            handleCustomerAction(customerId, action);
        });
    });
}

function handleCustomerAction(customerId, action) {
    const customer = customers.find(c => c.id === customerId);
    if (!customer) return;
    
    if (action === 'view-profile') {
        // View customer profile (can open modal or navigate to detail page)
        alert(`View Profile for ${customer.name}\n\nCustomer ID: ${customer.id}\nEmail: ${customer.email}\nPhone: ${customer.phone}\nPackage: ${customer.package}\nStatus: ${customer.status}\nJoin Date: ${formatDate(customer.joinDate)}`);
    } else if (action === 'suspend') {
        if (customer.status === 'Suspended') {
            if (confirm(`Unsuspend account for "${customer.name}"?`)) {
                customer.status = 'Active';
                saveCustomers();
                applyCustomerFilters();
                showNotification(`Account for "${customer.name}" has been unsuspended`);
            }
        } else {
            if (confirm(`Suspend account for "${customer.name}"?`)) {
                customer.status = 'Suspended';
                saveCustomers();
                applyCustomerFilters();
                showNotification(`Account for "${customer.name}" has been suspended`);
            }
        }
    } else if (action === 'upgrade') {
        // Upgrade/Downgrade package modal (simplified for now)
        const packages = [
            'Bot Reply Packages',
            'Auto Post Packages',
            'Content Packs',
            'Video Packs',
            'AI Tools & Automation',
            'Payment Integration'
        ];
        const currentPackageIndex = packages.indexOf(customer.package);
        const nextPackage = packages[(currentPackageIndex + 1) % packages.length];
        
        if (confirm(`Change package for "${customer.name}" from "${customer.package}" to "${nextPackage}"?`)) {
            customer.package = nextPackage;
            saveCustomers();
            applyCustomerFilters();
            showNotification(`Package for "${customer.name}" has been changed to "${nextPackage}"`);
        }
    }
}

// Project Management Functions
function handleProjectSearch(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    applyProjectFilters(searchTerm);
}

function handleProjectFilter() {
    applyProjectFilters();
}

function clearProjectFilters() {
    document.getElementById('project-search').value = '';
    document.getElementById('filter-project-service').value = '';
    document.getElementById('filter-project-staff').value = '';
    document.getElementById('filter-project-priority').value = '';
    applyProjectFilters();
}

function applyProjectFilters(searchTerm = null) {
    const searchInput = document.getElementById('project-search');
    const serviceFilter = document.getElementById('filter-project-service')?.value || '';
    const staffFilter = document.getElementById('filter-project-staff')?.value || '';
    const priorityFilter = document.getElementById('filter-project-priority')?.value || '';
    
    const search = searchTerm !== null ? searchTerm : searchInput.value.toLowerCase().trim();
    
    filteredProjects = projects.filter(project => {
        // Search filter
        const matchesSearch = !search || 
            project.name.toLowerCase().includes(search) ||
            project.customer.toLowerCase().includes(search) ||
            project.id.toLowerCase().includes(search);
        
        // Service filter
        const matchesService = !serviceFilter || project.service === serviceFilter;
        
        // Staff filter
        const matchesStaff = !staffFilter || project.assignedStaff === staffFilter;
        
        // Priority filter
        const matchesPriority = !priorityFilter || project.priority === priorityFilter;
        
        return matchesSearch && matchesService && matchesStaff && matchesPriority;
    });
    
    renderKanbanBoard();
}

function renderKanbanBoard() {
    // Clear all columns
    const columns = {
        todo: document.getElementById('todo-column'),
        'in-progress': document.getElementById('in-progress-column'),
        'in-review': document.getElementById('in-review-column'),
        completed: document.getElementById('completed-column')
    };
    
    // Clear column bodies
    Object.values(columns).forEach(column => {
        if (column) column.innerHTML = '';
    });
    
    // Group projects by status
    const projectsByStatus = {
        todo: [],
        'in-progress': [],
        'in-review': [],
        completed: []
    };
    
    filteredProjects.forEach(project => {
        if (projectsByStatus[project.status]) {
            projectsByStatus[project.status].push(project);
        }
    });
    
    // Render projects in each column
    Object.keys(projectsByStatus).forEach(status => {
        const column = columns[status];
        if (column) {
            projectsByStatus[status].forEach(project => {
                const card = createProjectCard(project);
                column.appendChild(card);
            });
        }
    });
    
    // Update column counts
    updateColumnCounts();
}

function updateColumnCounts() {
    const counts = {
        todo: 0,
        'in-progress': 0,
        'in-review': 0,
        completed: 0
    };
    
    filteredProjects.forEach(project => {
        if (counts[project.status] !== undefined) {
            counts[project.status]++;
        }
    });
    
    document.getElementById('todo-count').textContent = counts.todo;
    document.getElementById('in-progress-count').textContent = counts['in-progress'];
    document.getElementById('in-review-count').textContent = counts['in-review'];
    document.getElementById('completed-count').textContent = counts.completed;
}

function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    card.dataset.id = project.id;
    
    // Format due date
    const dueDate = new Date(project.dueDate);
    const now = new Date();
    const daysUntilDue = Math.ceil((dueDate - now) / (1000 * 60 * 60 * 24));
    
    let dueDateClass = '';
    if (daysUntilDue < 0) {
        dueDateClass = 'overdue';
    } else if (daysUntilDue <= 3) {
        dueDateClass = 'due-soon';
    }
    
    const formattedDate = formatDate(project.dueDate);
    
    // Priority badge
    const priorityBadge = `<span class="priority-badge ${project.priority.toLowerCase()}">${project.priority}</span>`;
    
    // Service badge
    const serviceBadge = `<span class="service-badge">${project.service}</span>`;
    
    card.innerHTML = `
        <div class="project-card-header">
            <h4 class="project-name">${project.name}</h4>
            ${priorityBadge}
        </div>
        <div class="project-card-body">
            <div class="project-info-item">
                <i class="fas fa-user"></i>
                <span class="customer-name">${project.customer}</span>
            </div>
            ${serviceBadge}
            <div class="project-info-item">
                <i class="fas fa-calendar"></i>
                <span class="due-date ${dueDateClass}">Due: ${formattedDate}</span>
            </div>
        </div>
        <div class="project-card-footer">
            <div class="assigned-staff">
                <i class="fas fa-user-circle"></i>
                <span>${project.assignedStaff}</span>
            </div>
            <div class="project-actions">
                <button class="project-action-btn" data-action="view" data-id="${project.id}" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="project-action-btn" data-action="edit" data-id="${project.id}" title="Edit Project">
                    <i class="fas fa-edit"></i>
                </button>
            </div>
        </div>
    `;
    
    // Add click handlers
    const actionButtons = card.querySelectorAll('.project-action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const action = button.dataset.action;
            const projectId = button.dataset.id;
            handleProjectAction(projectId, action);
        });
    });
    
    // Card click handler (can be used for status change simulation)
    card.addEventListener('click', (e) => {
        if (!e.target.closest('.project-action-btn')) {
            // Show project details
            handleProjectAction(project.id, 'view');
        }
    });
    
    return card;
}

function handleProjectAction(projectId, action) {
    const project = projects.find(p => p.id === projectId);
    if (!project) return;
    
    if (action === 'view') {
        alert(`Project: ${project.name}\n\nCustomer: ${project.customer}\nService: ${project.service}\nStatus: ${project.status}\nPriority: ${project.priority}\nDue Date: ${formatDate(project.dueDate)}\nAssigned To: ${project.assignedStaff}\n\nDescription: ${project.description || 'No description'}`);
    } else if (action === 'edit') {
        // Simulate status change (move to next column)
        const statuses = ['todo', 'in-progress', 'in-review', 'completed'];
        const currentIndex = statuses.indexOf(project.status);
        if (currentIndex < statuses.length - 1) {
            const nextStatus = statuses[currentIndex + 1];
            if (confirm(`Move "${project.name}" from ${project.status} to ${nextStatus}?`)) {
                project.status = nextStatus;
                saveProjects();
                applyProjectFilters();
                showNotification(`Project "${project.name}" moved to ${nextStatus}`);
            }
        } else {
            alert(`Project "${project.name}" is already completed and cannot be moved.`);
        }
    }
}

// Export functions for external use if needed
window.switchSection = switchSection;
window.updateDashboardKPIs = updateDashboardKPIs;
window.renderRecentLeads = renderRecentLeads;
window.renderCustomersTable = renderCustomersTable;
window.renderKanbanBoard = renderKanbanBoard;
window.addLead = function(leadData) {
    const newLead = {
        id: Date.now().toString(),
        ...leadData,
        status: 'New',
        date: new Date().toISOString().split('T')[0]
    };
    leads.push(newLead);
    saveLeads();
    applyFilters();
    // Update dashboard if on dashboard section
    if (document.getElementById('dashboard-section')?.classList.contains('active')) {
        updateDashboardKPIs();
        renderRecentLeads();
    }
};
