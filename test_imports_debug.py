#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug import issues"""
import sys
import os
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))

errors = []

print("Testing imports...")
print("=" * 60)

# Test standard library imports
try:
    import json
    import uuid
    import os
    import threading
    import logging
    from datetime import datetime
    from functools import wraps
    from urllib.parse import unquote_plus
    print("✓ Standard library imports OK")
except Exception as e:
    errors.append(f"Standard library: {e}")
    print(f"✗ Standard library: {e}")

# Test Flask
try:
    from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, abort, Response
    from werkzeug.security import generate_password_hash, check_password_hash
    from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
    print("✓ Flask imports OK")
except Exception as e:
    errors.append(f"Flask: {e}")
    print(f"✗ Flask: {e}")
    traceback.print_exc()

# Test local modules
local_modules = ['db_manager', 'bot_db_manager', 'bot_logic_engine', 'bot_templates', 
                 'gemini_service', 'auth_manager', 'config']

for module in local_modules:
    try:
        __import__(module)
        print(f"✓ {module} OK")
    except Exception as e:
        errors.append(f"{module}: {e}")
        print(f"✗ {module}: {e}")
        traceback.print_exc()

# Test optional modules
try:
    from auth_routes import auth_bp
    print("✓ auth_routes OK")
except Exception as e:
    errors.append(f"auth_routes: {e}")
    print(f"✗ auth_routes: {e}")

try:
    from session_middleware import check_session_timeout, cleanup_expired_sessions_periodically
    print("✓ session_middleware OK")
except Exception as e:
    errors.append(f"session_middleware: {e}")
    print(f"✗ session_middleware: {e}")

print("=" * 60)
if errors:
    print(f"\n✗ Found {len(errors)} import errors:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("\n✓ All imports successful!")
    print("\nTrying to import web_app...")
    try:
        import web_app
        print("✓ web_app imported successfully!")
        print(f"✓ Flask app created: {web_app.app}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error importing web_app: {e}")
        traceback.print_exc()
        sys.exit(1)
