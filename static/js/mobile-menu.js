/**
 * Mobile Menu Handler
 * Hamburger menu toggle and touch-friendly navigation
 */

class MobileMenu {
    constructor() {
        this.sidebar = document.querySelector('.sidebar');
        this.toggleButton = null;
        this.overlay = null;
        this.isOpen = false;
        this.init();
    }
    
    init() {
        // Create hamburger menu button
        this.createToggleButton();
        
        // Create overlay
        this.createOverlay();
        
        // Bind events
        this.bindEvents();
        
        // Handle window resize
        this.handleResize();
        
        // Close menu on route change (if using SPA)
        this.handleRouteChange();
    }
    
    createToggleButton() {
        // Check if button already exists
        if (document.getElementById('mobile-menu-toggle')) {
            this.toggleButton = document.getElementById('mobile-menu-toggle');
            return;
        }
        
        // Create hamburger button
        this.toggleButton = document.createElement('button');
        this.toggleButton.id = 'mobile-menu-toggle';
        this.toggleButton.className = 'mobile-menu-toggle';
        this.toggleButton.setAttribute('aria-label', 'Menu');
        this.toggleButton.setAttribute('aria-expanded', 'false');
        this.toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
        
        // Insert before sidebar or at top of body
        if (this.sidebar) {
            document.body.insertBefore(this.toggleButton, document.body.firstChild);
        } else {
            document.body.appendChild(this.toggleButton);
        }
    }
    
    createOverlay() {
        // Check if overlay already exists
        if (document.getElementById('sidebar-overlay')) {
            this.overlay = document.getElementById('sidebar-overlay');
            return;
        }
        
        // Create overlay
        this.overlay = document.createElement('div');
        this.overlay.id = 'sidebar-overlay';
        this.overlay.className = 'sidebar-overlay';
        
        // Insert after toggle button
        if (this.toggleButton && this.toggleButton.nextSibling) {
            this.toggleButton.parentNode.insertBefore(this.overlay, this.toggleButton.nextSibling);
        } else {
            document.body.appendChild(this.overlay);
        }
    }
    
    bindEvents() {
        // Toggle button click
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggle();
            });
        }
        
        // Overlay click to close
        if (this.overlay) {
            this.overlay.addEventListener('click', () => {
                this.close();
            });
        }
        
        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
        
        // Close on window resize (if going to desktop)
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Close when clicking outside (on mobile)
        document.addEventListener('click', (e) => {
            if (this.isOpen && window.innerWidth <= 1024) {
                if (!this.sidebar.contains(e.target) && 
                    !this.toggleButton.contains(e.target) &&
                    e.target !== this.overlay) {
                    this.close();
                }
            }
        });
        
        // Prevent body scroll when menu is open
        this.preventBodyScroll();
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        if (!this.sidebar) return;
        
        this.isOpen = true;
        this.sidebar.classList.add('mobile-open');
        
        if (this.toggleButton) {
            this.toggleButton.classList.add('active');
            this.toggleButton.setAttribute('aria-expanded', 'true');
            // Change icon to X
            const icon = this.toggleButton.querySelector('i');
            if (icon) {
                icon.className = 'fas fa-times';
            }
        }
        
        if (this.overlay) {
            this.overlay.classList.add('show');
        }
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        const firstLink = this.sidebar.querySelector('a');
        if (firstLink) {
            setTimeout(() => firstLink.focus(), 100);
        }
    }
    
    close() {
        if (!this.sidebar) return;
        
        this.isOpen = false;
        this.sidebar.classList.remove('mobile-open');
        
        if (this.toggleButton) {
            this.toggleButton.classList.remove('active');
            this.toggleButton.setAttribute('aria-expanded', 'false');
            // Change icon back to hamburger
            const icon = this.toggleButton.querySelector('i');
            if (icon) {
                icon.className = 'fas fa-bars';
            }
        }
        
        if (this.overlay) {
            this.overlay.classList.remove('show');
        }
        
        // Restore body scroll
        document.body.style.overflow = '';
    }
    
    handleResize() {
        // Close menu if window is resized to desktop size
        if (window.innerWidth > 1024 && this.isOpen) {
            this.close();
        }
        
        // Show/hide toggle button based on screen size
        if (this.toggleButton) {
            if (window.innerWidth <= 1024) {
                this.toggleButton.style.display = 'flex';
            } else {
                this.toggleButton.style.display = 'none';
                this.close();
            }
        }
    }
    
    handleRouteChange() {
        // Close menu when navigation link is clicked (for SPA)
        if (this.sidebar) {
            const links = this.sidebar.querySelectorAll('a[href]');
            links.forEach(link => {
                link.addEventListener('click', () => {
                    // Small delay to allow navigation
                    setTimeout(() => {
                        if (window.innerWidth <= 1024) {
                            this.close();
                        }
                    }, 100);
                });
            });
        }
    }
    
    preventBodyScroll() {
        // Prevent body scroll when menu is open on mobile
        const observer = new MutationObserver(() => {
            if (this.isOpen && window.innerWidth <= 1024) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
        
        if (this.sidebar) {
            observer.observe(this.sidebar, {
                attributes: true,
                attributeFilter: ['class']
            });
        }
    }
}

// ============================================
// Touch Event Improvements
// ============================================

class TouchHandler {
    constructor() {
        this.init();
    }
    
    init() {
        // Improve touch response for buttons
        this.improveButtonTouch();
        
        // Add swipe gestures for sidebar
        this.addSwipeGestures();
        
        // Prevent double-tap zoom on buttons
        this.preventDoubleTapZoom();
    }
    
    improveButtonTouch() {
        // Add touch feedback to all buttons
        const buttons = document.querySelectorAll('button, .btn, a.btn, .sidebar-nav a');
        
        buttons.forEach(button => {
            // Touch start
            button.addEventListener('touchstart', function(e) {
                this.style.transform = 'scale(0.98)';
                this.style.opacity = '0.9';
            }, { passive: true });
            
            // Touch end
            button.addEventListener('touchend', function(e) {
                setTimeout(() => {
                    this.style.transform = '';
                    this.style.opacity = '';
                }, 150);
            }, { passive: true });
            
            // Touch cancel
            button.addEventListener('touchcancel', function(e) {
                this.style.transform = '';
                this.style.opacity = '';
            }, { passive: true });
        });
    }
    
    addSwipeGestures() {
        const sidebar = document.querySelector('.sidebar');
        if (!sidebar) return;
        
        let touchStartX = 0;
        let touchStartY = 0;
        let touchEndX = 0;
        let touchEndY = 0;
        
        sidebar.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });
        
        sidebar.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            handleSwipe();
        }, { passive: true });
        
        const handleSwipe = () => {
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            
            // Swipe right to open (from left edge)
            if (touchStartX < 20 && deltaX > 50 && Math.abs(deltaY) < 50) {
                if (window.innerWidth <= 1024 && !window.mobileMenu.isOpen) {
                    window.mobileMenu.open();
                }
            }
            
            // Swipe left to close
            if (deltaX < -50 && Math.abs(deltaY) < 50) {
                if (window.innerWidth <= 1024 && window.mobileMenu.isOpen) {
                    window.mobileMenu.close();
                }
            }
        };
    }
    
    preventDoubleTapZoom() {
        let lastTouchEnd = 0;
        
        document.addEventListener('touchend', (e) => {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, { passive: false });
    }
}

// ============================================
// Form Mobile Optimizations
// ============================================

class MobileFormOptimizer {
    constructor() {
        this.init();
    }
    
    init() {
        // Optimize form inputs for mobile
        this.optimizeInputs();
        
        // Add input mode attributes
        this.addInputModes();
        
        // Handle form submission on mobile
        this.optimizeFormSubmission();
    }
    
    optimizeInputs() {
        // Add proper input types for mobile keyboards
        const emailInputs = document.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.setAttribute('autocapitalize', 'none');
            input.setAttribute('autocorrect', 'off');
        });
        
        const telInputs = document.querySelectorAll('input[type="tel"]');
        telInputs.forEach(input => {
            input.setAttribute('inputmode', 'tel');
        });
        
        const numberInputs = document.querySelectorAll('input[type="number"]');
        numberInputs.forEach(input => {
            input.setAttribute('inputmode', 'numeric');
        });
    }
    
    addInputModes() {
        // Add inputmode for better mobile keyboards
        const urlInputs = document.querySelectorAll('input[type="url"], input[name*="url"], input[id*="url"]');
        urlInputs.forEach(input => {
            input.setAttribute('inputmode', 'url');
        });
        
        const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
        searchInputs.forEach(input => {
            input.setAttribute('inputmode', 'search');
        });
    }
    
    optimizeFormSubmission() {
        // Prevent form submission on enter key (mobile keyboards)
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                // Ensure form is properly validated before submission
                const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
                if (submitButton && submitButton.disabled) {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }
}

// ============================================
// Initialize on DOM Ready
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize mobile menu
    window.mobileMenu = new MobileMenu();
    
    // Initialize touch handler
    window.touchHandler = new TouchHandler();
    
    // Initialize form optimizer
    window.mobileFormOptimizer = new MobileFormOptimizer();
    
    // Handle orientation change
    window.addEventListener('orientationchange', () => {
        setTimeout(() => {
            if (window.mobileMenu) {
                window.mobileMenu.handleResize();
            }
        }, 100);
    });
});

// Export for use in other scripts
window.MobileMenu = MobileMenu;
window.TouchHandler = TouchHandler;
window.MobileFormOptimizer = MobileFormOptimizer;

