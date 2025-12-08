"""
Optimization Script
Minifies CSS/JS, optimizes images, and prepares production build
"""

import os
import re
import shutil
from pathlib import Path

def minify_css(content):
    """Minify CSS by removing comments and whitespace"""
    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)
    # Remove whitespace around specific characters
    content = re.sub(r'\s*([{}:;,])\s*', r'\1', content)
    # Remove trailing semicolons before closing braces
    content = re.sub(r';}', '}', content)
    # Remove leading/trailing whitespace
    content = content.strip()
    return content

def minify_js(content):
    """Basic JavaScript minification"""
    # Remove single-line comments (but not URLs)
    content = re.sub(r'//(?!https?://)[^\n]*', '', content)
    # Remove multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove extra whitespace (but preserve newlines in strings)
    lines = content.split('\n')
    minified = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('//'):
            minified.append(stripped)
    return ' '.join(minified)

def optimize_static_files():
    """Optimize static files for production"""
    static_dir = Path('static')
    
    # Create optimized directory
    optimized_dir = static_dir / 'optimized'
    optimized_dir.mkdir(exist_ok=True)
    
    # Minify CSS files
    css_dir = static_dir / 'css'
    if css_dir.exists():
        css_optimized = optimized_dir / 'css'
        css_optimized.mkdir(exist_ok=True)
        
        for css_file in css_dir.glob('*.css'):
            print(f"Minifying {css_file.name}...")
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            minified = minify_css(content)
            
            output_file = css_optimized / css_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(minified)
            print(f"  Saved to {output_file}")
    
    # Minify JS files
    js_dir = static_dir / 'js'
    if js_dir.exists():
        js_optimized = optimized_dir / 'js'
        js_optimized.mkdir(exist_ok=True)
        
        for js_file in js_dir.glob('*.js'):
            print(f"Minifying {js_file.name}...")
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            minified = minify_js(content)
            
            output_file = js_optimized / js_file.name
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(minified)
            print(f"  Saved to {output_file}")
    
    print("\n✅ Optimization complete!")
    print(f"Optimized files saved to: {optimized_dir}")

def create_production_config():
    """Create production configuration file"""
    config = """# Production Configuration
DEBUG = False
SECRET_KEY = 'CHANGE-THIS-IN-PRODUCTION'

# Database
DATABASE_URL = 'sqlite:///bots.db'

# Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Performance
SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
"""
    
    with open('config_production.py', 'w') as f:
        f.write(config)
    
    print("✅ Production config created: config_production.py")

if __name__ == '__main__':
    print("🚀 Starting optimization...\n")
    optimize_static_files()
    create_production_config()
    print("\n✨ All done!")

