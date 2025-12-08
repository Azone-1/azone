/**
 * Loading States & User Feedback System
 * Myanmar Language Support
 * Non-blocking UI with toast notifications
 */

// ============================================
// Myanmar Feedback Messages
// ============================================
const FeedbackMessages = {
    // Loading messages
    loading: {
        saving: 'သိမ်းဆည်းနေသည်...',
        loading: 'ကျေးဇူးပြု၍ စောင့်ပါ...',
        processing: 'လုပ်ဆောင်နေသည်...',
        fetching: 'ဒေတာ ယူနေသည်...',
        uploading: 'ပေးပို့နေသည်...',
        downloading: 'ဒေါင်းလုဒ်လုပ်နေသည်...',
        deleting: 'ဖျက်နေသည်...',
        exporting: 'ထုတ်ယူနေသည်...',
        importing: 'တင်သွင်းနေသည်...',
        validating: 'စစ်ဆေးနေသည်...',
        connecting: 'ချိတ်ဆက်နေသည်...'
    },
    
    // Success messages
    success: {
        saved: 'သိမ်းဆည်းပြီးပါပြီ',
        updated: 'ပြင်ဆင်ပြီးပါပြီ',
        deleted: 'ဖျက်ပြီးပါပြီ',
        exported: 'ထုတ်ယူပြီးပါပြီ',
        imported: 'တင်သွင်းပြီးပါပြီ',
        published: 'ထုတ်ဝေပြီးပါပြီ',
        connected: 'ချိတ်ဆက်ပြီးပါပြီ',
        sent: 'ပေးပို့ပြီးပါပြီ',
        uploaded: 'တင်သွင်းပြီးပါပြီ'
    },
    
    // Error messages
    error: {
        saveFailed: 'သိမ်းဆည်းရာတွင် အမှားအယွင်း ဖြစ်ပွားပါသည်',
        loadFailed: 'ဒေတာ ယူရာတွင် အမှားအယွင်း ဖြစ်ပွားပါသည်',
        deleteFailed: 'ဖျက်ရာတွင် အမှားအယွင်း ဖြစ်ပွားပါသည်',
        networkError: 'ကွန်ရက်ချိတ်ဆက်မှု အမှားအယွင်း',
        serverError: 'ဆာဗာ အမှားအယွင်း',
        timeout: 'အချိန်ကုန်သွားပါသည်',
        unauthorized: 'ခွင့်ပြုချက် မရှိပါ',
        notFound: 'ဒေတာ မတွေ့ရှိပါ',
        validationError: 'အချက်အလက်များ မမှန်ကန်ပါ'
    },
    
    // Info messages
    info: {
        noData: 'ဒေတာ မရှိပါ',
        noResults: 'ရလဒ်များ မတွေ့ရှိပါ',
        changesSaved: 'ပြောင်းလဲမှုများ သိမ်းဆည်းပြီးပါပြီ',
        autoSaved: 'အလိုအလျောက် သိမ်းဆည်းပြီးပါပြီ'
    }
};

// ============================================
// Toast Notification System
// ============================================
class ToastManager {
    constructor() {
        this.container = this.createContainer();
        this.toasts = new Map();
        this.maxToasts = 5;
    }
    
    createContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }
    
    show(message, type = 'info', options = {}) {
        const {
            title = '',
            duration = type === 'success' ? 3000 : 5000,
            persistent = false,
            action = null
        } = options;
        
        // Remove oldest toast if at max
        if (this.toasts.size >= this.maxToasts) {
            const firstToast = Array.from(this.toasts.values())[0];
            this.remove(firstToast.id);
        }
        
        const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const toast = this.createToast(toastId, message, type, title, action);
        
        this.container.appendChild(toast);
        this.toasts.set(toastId, toast);
        
        // Show toast
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        // Auto-dismiss
        if (!persistent && duration > 0) {
            const progressBar = toast.querySelector('.toast-progress');
            if (progressBar) {
                progressBar.style.transition = `width ${duration}ms linear`;
                progressBar.style.width = '0%';
            }
            
            setTimeout(() => {
                this.remove(toastId);
            }, duration);
        }
        
        return toastId;
    }
    
    createToast(id, message, type, title, action) {
        const toast = document.createElement('div');
        toast.id = id;
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        
        toast.innerHTML = `
            <i class="fas ${icons[type]} toast-icon"></i>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="window.toastManager.remove('${id}')">
                <i class="fas fa-times"></i>
            </button>
            <div class="toast-progress" style="width: 100%;"></div>
        `;
        
        return toast;
    }
    
    remove(toastId) {
        const toast = this.toasts.get(toastId);
        if (!toast) return;
        
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            this.toasts.delete(toastId);
        }, 300);
    }
    
    success(message, options = {}) {
        return this.show(message, 'success', options);
    }
    
    error(message, options = {}) {
        return this.show(message, 'error', options);
    }
    
    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }
    
    info(message, options = {}) {
        return this.show(message, 'info', options);
    }
    
    clear() {
        this.toasts.forEach((toast, id) => {
            this.remove(id);
        });
    }
}

// ============================================
// Loading Overlay Manager
// ============================================
class LoadingOverlay {
    constructor() {
        this.overlay = null;
        this.activeCount = 0;
    }
    
    show(message = 'ကျေးဇူးပြု၍ စောင့်ပါ...') {
        if (!this.overlay) {
            this.overlay = this.createOverlay();
            document.body.appendChild(this.overlay);
        }
        
        const messageEl = this.overlay.querySelector('.loading-overlay-message');
        if (messageEl) {
            messageEl.textContent = message;
        }
        
        this.activeCount++;
        this.overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    
    hide() {
        if (this.activeCount > 0) {
            this.activeCount--;
        }
        
        if (this.activeCount === 0 && this.overlay) {
            this.overlay.classList.remove('show');
            document.body.style.overflow = '';
        }
    }
    
    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-overlay-content">
                <div class="loading-overlay-spinner"></div>
                <div class="loading-overlay-message">ကျေးဇူးပြု၍ စောင့်ပါ...</div>
            </div>
        `;
        return overlay;
    }
}

// ============================================
// Button Loading State Manager
// ============================================
class ButtonLoader {
    static setLoading(button, loading = true, text = null) {
        if (!button) return;
        
        if (loading) {
            const originalText = button.innerHTML;
            button.dataset.originalText = originalText;
            button.classList.add('btn-loading');
            button.disabled = true;
            
            if (text) {
                button.innerHTML = `<span class="btn-text">${text}</span>`;
            } else {
                const textContent = button.textContent.trim();
                button.innerHTML = `<span class="btn-text">${textContent}</span>`;
            }
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
            
            if (button.dataset.originalText) {
                button.innerHTML = button.dataset.originalText;
                delete button.dataset.originalText;
            }
        }
    }
    
    static setText(button, text) {
        if (!button) return;
        const btnText = button.querySelector('.btn-text');
        if (btnText) {
            btnText.textContent = text;
        } else {
            button.innerHTML = `<span class="btn-text">${text}</span>`;
        }
    }
}

// ============================================
// Progress Bar Manager
// ============================================
class ProgressBar {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = containerId;
            this.container.className = 'progress-container';
        }
        
        this.options = {
            showLabel: options.showLabel !== false,
            showPercentage: options.showPercentage !== false,
            ...options
        };
        
        this.progressBar = null;
        this.label = null;
        this.init();
    }
    
    init() {
        this.container.innerHTML = `
            <div class="progress-bar" style="width: 0%;"></div>
            ${this.options.showLabel ? '<div class="progress-label"><span class="progress-percentage">0%</span></div>' : ''}
        `;
        
        this.progressBar = this.container.querySelector('.progress-bar');
        if (this.options.showLabel) {
            this.label = this.container.querySelector('.progress-label');
        }
    }
    
    setProgress(percentage, message = null) {
        const percent = Math.max(0, Math.min(100, percentage));
        this.progressBar.style.width = `${percent}%`;
        
        if (this.label) {
            const percentageEl = this.label.querySelector('.progress-percentage');
            if (percentageEl) {
                percentageEl.textContent = `${Math.round(percent)}%`;
            }
            
            if (message) {
                const textNode = this.label.childNodes[this.label.childNodes.length - 1];
                if (textNode && textNode.nodeType === 3) {
                    textNode.textContent = ` - ${message}`;
                } else {
                    this.label.appendChild(document.createTextNode(` - ${message}`));
                }
            }
        }
    }
    
    show() {
        this.container.style.display = 'block';
    }
    
    hide() {
        this.container.style.display = 'none';
    }
    
    reset() {
        this.setProgress(0);
    }
}

// ============================================
// Tooltip Manager
// ============================================
class TooltipManager {
    constructor() {
        this.tooltips = new Map();
        this.init();
    }
    
    init() {
        // Auto-initialize tooltips with data-tooltip attribute
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('[data-tooltip]').forEach(element => {
                this.attach(element);
            });
        });
    }
    
    attach(element, message = null, position = 'top') {
        const tooltipMessage = message || element.dataset.tooltip;
        const tooltipPosition = element.dataset.tooltipPosition || position;
        
        if (!tooltipMessage) return;
        
        const tooltip = this.createTooltip(tooltipMessage, tooltipPosition);
        element.classList.add('tooltip-wrapper');
        element.appendChild(tooltip);
        
        const showTooltip = () => {
            tooltip.classList.add('show');
        };
        
        const hideTooltip = () => {
            tooltip.classList.remove('show');
        };
        
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
        element.addEventListener('focus', showTooltip);
        element.addEventListener('blur', hideTooltip);
        
        this.tooltips.set(element, tooltip);
    }
    
    createTooltip(message, position) {
        const tooltip = document.createElement('div');
        tooltip.className = `tooltip tooltip-${position}`;
        tooltip.textContent = message;
        return tooltip;
    }
    
    show(element, message, position = 'top', duration = 0) {
        if (this.tooltips.has(element)) {
            this.tooltips.get(element).classList.add('show');
        } else {
            this.attach(element, message, position);
            const tooltip = this.tooltips.get(element);
            if (tooltip) {
                tooltip.classList.add('show');
            }
        }
        
        if (duration > 0) {
            setTimeout(() => {
                this.hide(element);
            }, duration);
        }
    }
    
    hide(element) {
        const tooltip = this.tooltips.get(element);
        if (tooltip) {
            tooltip.classList.remove('show');
        }
    }
}

// ============================================
// Loading State Manager (Main API)
// ============================================
class LoadingManager {
    constructor() {
        this.overlay = new LoadingOverlay();
        this.activeLoadings = new Map();
    }
    
    // Show loading overlay
    showOverlay(message = null) {
        this.overlay.show(message || FeedbackMessages.loading.loading);
    }
    
    // Hide loading overlay
    hideOverlay() {
        this.overlay.hide();
    }
    
    // Set button loading state
    setButtonLoading(button, loading = true, text = null) {
        ButtonLoader.setLoading(button, loading, text);
    }
    
    // Set element loading state
    setElementLoading(element, loading = true) {
        if (!element) return;
        
        if (loading) {
            element.classList.add('loading-inline');
            if (!element.querySelector('.loading-spinner')) {
                const spinner = document.createElement('span');
                spinner.className = 'loading-spinner';
                element.insertBefore(spinner, element.firstChild);
            }
        } else {
            element.classList.remove('loading-inline');
            const spinner = element.querySelector('.loading-spinner');
            if (spinner) {
                spinner.remove();
            }
        }
    }
    
    // Set card loading state
    setCardLoading(card, loading = true) {
        if (!card) return;
        
        if (loading) {
            card.classList.add('card-loading');
        } else {
            card.classList.remove('card-loading');
        }
    }
    
    // Set form disabled state
    setFormDisabled(form, disabled = true) {
        if (!form) return;
        
        if (disabled) {
            form.classList.add('form-disabled');
            const inputs = form.querySelectorAll('input, textarea, select, button');
            inputs.forEach(input => {
                input.disabled = true;
            });
        } else {
            form.classList.remove('form-disabled');
            const inputs = form.querySelectorAll('input, textarea, select, button');
            inputs.forEach(input => {
                input.disabled = false;
            });
        }
    }
    
    // Async operation wrapper
    async execute(operation, options = {}) {
        const {
            loadingMessage = null,
            successMessage = null,
            errorMessage = null,
            showOverlay = false,
            button = null,
            buttonText = null
        } = options;
        
        let loadingId = null;
        
        try {
            // Show loading
            if (showOverlay) {
                this.showOverlay(loadingMessage);
            }
            
            if (button) {
                this.setButtonLoading(button, true, buttonText);
            }
            
            // Execute operation
            const result = await operation();
            
            // Show success
            if (successMessage) {
                window.toastManager.success(successMessage);
            }
            
            return result;
            
        } catch (error) {
            // Show error
            const errorMsg = errorMessage || error.message || FeedbackMessages.error.networkError;
            window.toastManager.error(errorMsg);
            throw error;
            
        } finally {
            // Hide loading
            if (showOverlay) {
                this.hideOverlay();
            }
            
            if (button) {
                this.setButtonLoading(button, false);
            }
        }
    }
}

// ============================================
// Fetch Wrapper with Loading States
// ============================================
async function fetchWithLoading(url, options = {}, loadingOptions = {}) {
    const {
        showOverlay = false,
        loadingMessage = FeedbackMessages.loading.fetching,
        successMessage = null,
        errorMessage = null,
        button = null
    } = loadingOptions;
    
    return window.loadingManager.execute(async () => {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || errorData.error || `HTTP ${response.status}`);
        }
        
        return await response.json();
    }, {
        showOverlay,
        loadingMessage,
        successMessage,
        errorMessage,
        button
    });
}

// ============================================
// Initialize Global Managers
// ============================================
window.toastManager = new ToastManager();
window.loadingManager = new LoadingManager();
window.tooltipManager = new TooltipManager();
window.fetchWithLoading = fetchWithLoading;

// ============================================
// Convenience Functions
// ============================================

// Show toast
window.showToast = function(message, type = 'info', options = {}) {
    return window.toastManager.show(message, type, options);
};

// Show success toast
window.showSuccess = function(message, options = {}) {
    return window.toastManager.success(message, options);
};

// Show error toast
window.showError = function(message, options = {}) {
    return window.toastManager.error(message, options);
};

// Show loading overlay
window.showLoading = function(message = null) {
    window.loadingManager.showOverlay(message);
};

// Hide loading overlay
window.hideLoading = function() {
    window.loadingManager.hideOverlay();
};

// Set button loading
window.setButtonLoading = function(button, loading = true, text = null) {
    ButtonLoader.setLoading(button, loading, text);
};

// Export for use in other scripts
window.ButtonLoader = ButtonLoader;
window.ProgressBar = ProgressBar;
window.LoadingManager = LoadingManager;
window.FeedbackMessages = FeedbackMessages;

