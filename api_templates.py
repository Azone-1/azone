# API Route Templates for AZone Project
# ဒီ file ကို web_app.py ထဲမှာ import လုပ်ပြီး သုံးနိုင်တယ်

from flask import request, jsonify
from functools import wraps
from flask_login import login_required, current_user
import logging
import db_manager

logger = logging.getLogger(__name__)

# App instance will be set from web_app.py
app = None

def init_api_templates(flask_app):
    """Initialize API templates with Flask app instance"""
    global app
    app = flask_app

# ============================================
# Helper Decorators
# ============================================

def role_required(*roles):
    """Check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            if current_user.role not in roles:
                return jsonify({'success': False, 'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================
# Leads API Templates
# ============================================

def get_leads_template():
    """
    Template for GET /api/leads
    TODO: Connect to database and fetch leads
    """
    @app.route('/api/leads', methods=['GET'])
    @login_required
    def get_leads():
        """Get all leads with optional filtering"""
        try:
            # Get query parameters
            search = request.args.get('search', '').strip()
            service_filter = request.args.get('service', '').strip()
            status_filter = request.args.get('status', '').strip()
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 50))
            
            # Connect to database and query leads
            leads, total = db_manager.get_leads(
                search=search,
                service=service_filter,
                status=status_filter,
                page=page,
                per_page=per_page
            )
            
            return jsonify({
                'success': True,
                'data': leads,
                'total': total,
                'page': page,
                'per_page': per_page
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching leads: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch leads',
                'message': str(e)
            }), 500

def create_lead_template():
    """
    Template for POST /api/leads
    TODO: Connect to database and save lead
    """
    @app.route('/api/leads', methods=['POST'])
    @login_required
    def create_lead():
        """Create a new lead"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['name', 'email', 'phone', 'service']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'error': f'{field} is required'
                    }), 400
            
            # Connect to database and save lead
            lead_id = db_manager.create_lead(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                service=data['service'],
                status=data.get('status', 'New'),
                created_by=current_user.id if current_user.is_authenticated else None
            )
            
            return jsonify({
                'success': True,
                'message': 'Lead created successfully',
                'data': {
                    'id': lead_id,
                    'name': data['name'],
                    'email': data['email']
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating lead: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to create lead',
                'message': str(e)
            }), 500

def update_lead_template():
    """
    Template for PUT /api/leads/<lead_id>
    TODO: Connect to database and update lead
    """
    @app.route('/api/leads/<int:lead_id>', methods=['PUT'])
    @login_required
    def update_lead(lead_id):
        """Update an existing lead"""
        try:
            data = request.get_json()
            
            # Connect to database and update lead
            success = db_manager.update_lead(lead_id, **data)
            
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Lead not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Lead updated successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error updating lead: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to update lead',
                'message': str(e)
            }), 500

def delete_lead_template():
    """
    Template for DELETE /api/leads/<lead_id>
    TODO: Connect to database and delete lead
    """
    @app.route('/api/leads/<int:lead_id>', methods=['DELETE'])
    @login_required
    @role_required('owner', 'editor')
    def delete_lead(lead_id):
        """Delete a lead"""
        try:
            # Connect to database and delete lead
            success = db_manager.delete_lead(lead_id)
            
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Lead not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Lead deleted successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error deleting lead: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to delete lead',
                'message': str(e)
            }), 500

# ============================================
# Customers API Templates
# ============================================

def get_customers_template():
    """
    Template for GET /api/customers
    TODO: Connect to database and fetch customers
    """
    @app.route('/api/customers', methods=['GET'])
    @login_required
    def get_customers():
        """Get all customers with optional filtering"""
        try:
            search = request.args.get('search', '').strip()
            status_filter = request.args.get('status', '').strip()
            package_filter = request.args.get('package', '').strip()
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 50))
            
            # Connect to database and query customers
            customers, total = db_manager.get_customers(
                search=search,
                status=status_filter,
                package=package_filter,
                page=page,
                per_page=per_page
            )
            
            return jsonify({
                'success': True,
                'data': customers,
                'total': total,
                'page': page,
                'per_page': per_page
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching customers: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch customers',
                'message': str(e)
            }), 500

def create_customer_template():
    """
    Template for POST /api/customers
    TODO: Connect to database and save customer
    """
    @app.route('/api/customers', methods=['POST'])
    @login_required
    def create_customer():
        """Create a new customer"""
        try:
            data = request.get_json()
            
            required_fields = ['name', 'email', 'phone']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'error': f'{field} is required'
                    }), 400
            
            # Connect to database and save customer
            customer_id = db_manager.create_customer(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                package=data.get('package', ''),
                status=data.get('status', 'Active')
            )
            
            return jsonify({
                'success': True,
                'message': 'Customer created successfully',
                'data': {
                    'id': customer_id,
                    'name': data['name'],
                    'email': data['email']
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to create customer',
                'message': str(e)
            }), 500

# ============================================
# Projects API Templates
# ============================================

def get_projects_template():
    """
    Template for GET /api/projects
    TODO: Connect to database and fetch projects
    """
    @app.route('/api/projects', methods=['GET'])
    @login_required
    def get_projects():
        """Get all projects with optional filtering"""
        try:
            search = request.args.get('search', '').strip()
            status_filter = request.args.get('status', '').strip()
            service_filter = request.args.get('service', '').strip()
            
            # Connect to database and query projects
            projects = db_manager.get_projects(
                search=search,
                status=status_filter,
                service=service_filter
            )
            
            return jsonify({
                'success': True,
                'data': projects
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch projects',
                'message': str(e)
            }), 500

def create_project_template():
    """
    Template for POST /api/projects
    TODO: Connect to database and save project
    """
    @app.route('/api/projects', methods=['POST'])
    @login_required
    def create_project():
        """Create a new project"""
        try:
            data = request.get_json()
            
            required_fields = ['name', 'customer_id', 'service']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'error': f'{field} is required'
                    }), 400
            
            # Connect to database and save project
            project_id = db_manager.create_project(
                name=data['name'],
                customer_id=data['customer_id'],
                service=data['service'],
                status=data.get('status', 'todo'),
                priority=data.get('priority', 'Medium')
            )
            
            return jsonify({
                'success': True,
                'message': 'Project created successfully',
                'data': {
                    'id': project_id,
                    'name': data['name']
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to create project',
                'message': str(e)
            }), 500

def update_project_status_template():
    """
    Template for PUT /api/projects/<project_id>/status
    TODO: Connect to database and update project status
    """
    @app.route('/api/projects/<int:project_id>/status', methods=['PUT'])
    @login_required
    def update_project_status(project_id):
        """Update project status"""
        try:
            data = request.get_json()
            new_status = data.get('status')
            
            if not new_status:
                return jsonify({
                    'success': False,
                    'error': 'status is required'
                }), 400
            
            # Connect to database and update project status
            success = db_manager.update_project_status(project_id, new_status)
            
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Project not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Project status updated successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error updating project status: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to update project status',
                'message': str(e)
            }), 500

# ============================================
# Dashboard API Templates
# ============================================

def get_dashboard_stats_template():
    """
    Template for GET /api/dashboard/stats
    TODO: Connect to database and calculate stats
    """
    @app.route('/api/dashboard/stats', methods=['GET'])
    @login_required
    def get_dashboard_stats():
        """Get dashboard statistics"""
        try:
            # Connect to database and get dashboard stats
            stats = db_manager.get_dashboard_stats()
            
            return jsonify({
                'success': True,
                'data': stats
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching dashboard stats: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch dashboard stats',
                'message': str(e)
            }), 500

def get_dashboard_chart_data_template():
    """
    Template for GET /api/dashboard/chart
    TODO: Connect to database and get chart data
    """
    @app.route('/api/dashboard/chart', methods=['GET'])
    @login_required
    def get_dashboard_chart_data():
        """Get chart data for dashboard"""
        try:
            period = request.args.get('period', '30days')
            
            # Connect to database and get chart data
            chart_data = db_manager.get_chart_data(period=period)
            
            return jsonify({
                'success': True,
                'data': chart_data
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching chart data: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch chart data',
                'message': str(e)
            }), 500

# ============================================
# Usage Instructions
# ============================================

"""
ဒီ templates တွေကို သုံးပုံ:

1. web_app.py ထဲမှာ import လုပ်ပါ:
   from api_templates import *

2. app instance ကို pass လုပ်ပါ (သို့မဟုတ် global app သုံးပါ)

3. Routes တွေကို register လုပ်ပါ:
   get_leads_template()
   create_lead_template()
   # etc...

4. TODO comments တွေကို fill in လုပ်ပါ:
   - Database connection
   - Actual queries
   - Business logic

5. Test လုပ်ပါ!
"""
