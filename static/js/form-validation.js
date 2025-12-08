/**
 * Comprehensive Form Validation Library
 * Myanmar (Burmese) Language Support
 * Real-time validation with visual feedback
 */

// ============================================
// Myanmar Error Messages
// ============================================
const ValidationMessages = {
    // Required fields
    required: (fieldName) => `${fieldName} ထည့်သွင်းရန် လိုအပ်ပါသည်`,
    
    // Email validation
    emailInvalid: 'မှန်ကန်သော အီးမေးလ် လိပ်စာ ထည့်သွင်းပါ',
    emailRequired: 'အီးမေးလ် ထည့်သွင်းရန် လိုအပ်ပါသည်',
    
    // URL validation
    urlInvalid: 'မှန်ကန်သော URL ထည့်သွင်းပါ (http:// or https://)',
    urlRequired: 'URL ထည့်သွင်းရန် လိုအပ်ပါသည်',
    
    // Phone validation
    phoneInvalid: 'မှန်ကန်သော ဖုန်းနံပါတ် ထည့်သွင်းပါ',
    phoneRequired: 'ဖုန်းနံပါတ် ထည့်သွင်းရန် လိုအပ်ပါသည်',
    
    // Number validation
    numberInvalid: 'မှန်ကန်သော ဂဏန်း ထည့်သွင်းပါ',
    numberMin: (min) => `အနည်းဆုံး ${min} ဖြစ်ရမည်`,
    numberMax: (max) => `အများဆုံး ${max} ဖြစ်ရမည်`,
    numberRange: (min, max) => `${min} နှင့် ${max} အကြား ဖြစ်ရမည်`,
    
    // Text length
    textMin: (min) => `အနည်းဆုံး ${min} လုံး ရှိရမည်`,
    textMax: (max) => `အများဆုံး ${max} လုံး ဖြစ်ရမည်`,
    textLength: (min, max) => `${min} နှင့် ${max} အကြား ဖြစ်ရမည်`,
    
    // JSON validation
    jsonInvalid: 'မှန်ကန်သော JSON format ဖြစ်ရမည်',
    jsonRequired: 'JSON data ထည့်သွင်းရန် လိုအပ်ပါသည်',
    
    // File validation
    fileTypeInvalid: (allowedTypes) => `ခွင့်ပြုထားသော file types: ${allowedTypes.join(', ')}`,
    fileSizeMax: (maxSize) => `File size သည် ${maxSize} ထက် မကြီးရပါ`,
    fileRequired: 'File ရွေးချယ်ရန် လိုအပ်ပါသည်',
    
    // Pattern validation
    patternInvalid: 'ပုံစံမှန်ကန်မှု မရှိပါ',
    
    // General
    validationError: 'အချက်အလက်များ စစ်ဆေးရာတွင် အမှားအယွင်း ဖြစ်ပွားပါသည်',
    formInvalid: 'ကျေးဇူးပြု၍ အမှားများကို ပြင်ဆင်ပါ'
};

// ============================================
// Validation Rules
// ============================================
const ValidationRules = {
    // Email regex
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    
    // URL regex
    url: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/,
    
    // Phone regex (supports Myanmar and international)
    phone: /^[\+]?[0-9\s\-\(\)]{8,20}$/,
    
    // JSON pattern
    jsonPattern: /^[\s\S]*\{[\s\S]*\}[\s\S]*$|^[\s\S]*\[[\s\S]*\][\s\S]*$/,
    
    // Bot name pattern (alphanumeric, Myanmar characters, spaces, hyphens, underscores)
    // Myanmar Unicode range: U+1000 to U+109F (Myanmar script)
    // Also includes extended Myanmar: U+AA60 to U+AA7F
    botName: /^[\u1000-\u109F\uAA60-\uAA7Fa-zA-Z0-9\s\-_]{2,50}$/,
    
    // Variable name pattern (for bot variables)
    variableName: /^[a-zA-Z_][a-zA-Z0-9_]*$/
};

// ============================================
// Form Validator Class
// ============================================
class FormValidator {
    constructor(formId, options = {}) {
        this.form = document.getElementById(formId);
        if (!this.form) {
            console.error(`Form with ID "${formId}" not found`);
            return;
        }
        
        this.options = {
            realTime: options.realTime !== false, // Default: true
            showIcons: options.showIcons !== false, // Default: true
            validateOnBlur: options.validateOnBlur !== false, // Default: true
            ...options
        };
        
        this.fields = new Map();
        this.init();
    }
    
    init() {
        // Find all fields with validation attributes
        const fields = this.form.querySelectorAll('[data-validate], [required], input, textarea, select');
        
        fields.forEach(field => {
            if (field.type === 'submit' || field.type === 'button') return;
            
            const fieldConfig = this.parseFieldConfig(field);
            if (fieldConfig) {
                this.fields.set(field.name || field.id, fieldConfig);
                this.setupFieldValidation(field, fieldConfig);
            }
        });
        
        // Form submit validation
        this.form.addEventListener('submit', (e) => {
            if (!this.validateForm()) {
                e.preventDefault();
                e.stopPropagation();
                this.showFormError();
            }
        });
    }
    
    parseFieldConfig(field) {
        const config = {
            field: field,
            rules: [],
            label: this.getFieldLabel(field),
            required: field.hasAttribute('required') || field.dataset.required === 'true',
            realTime: field.dataset.realTime !== 'false'
        };
        
        // Parse validation rules from data attributes
        if (field.dataset.validate) {
            const rules = field.dataset.validate.split('|');
            rules.forEach(rule => {
                const [ruleName, ...params] = rule.split(':');
                config.rules.push({ name: ruleName, params: params });
            });
        }
        
        // Auto-detect validation type from input type
        if (field.type === 'email') {
            config.rules.push({ name: 'email' });
        } else if (field.type === 'url' || field.name?.toLowerCase().includes('url')) {
            config.rules.push({ name: 'url' });
        } else if (field.type === 'tel' || field.name?.toLowerCase().includes('phone')) {
            config.rules.push({ name: 'phone' });
        } else if (field.type === 'number') {
            config.rules.push({ name: 'number' });
        }
        
        // Min/Max length from attributes
        if (field.minLength && field.minLength > 0) {
            config.rules.push({ name: 'minLength', params: [field.minLength] });
        }
        if (field.maxLength && field.maxLength > 0) {
            config.rules.push({ name: 'maxLength', params: [field.maxLength] });
        }
        
        // Min/Max value for numbers
        if (field.min !== undefined && field.min !== '') {
            config.rules.push({ name: 'min', params: [field.min] });
        }
        if (field.max !== undefined && field.max !== '') {
            config.rules.push({ name: 'max', params: [field.max] });
        }
        
        // JSON validation for textareas with json class or data-json attribute
        if (field.dataset.json === 'true' || field.classList.contains('json-input')) {
            config.rules.push({ name: 'json' });
        }
        
        return config.rules.length > 0 || config.required ? config : null;
    }
    
    getFieldLabel(field) {
        const label = this.form.querySelector(`label[for="${field.id}"]`);
        if (label) {
            return label.textContent.replace(/\s*\*?\s*$/, '').trim();
        }
        return field.placeholder || field.name || 'Field';
    }
    
    setupFieldValidation(field, config) {
        // Real-time validation
        if (this.options.realTime && config.realTime) {
            field.addEventListener('input', () => {
                this.validateField(field.name || field.id);
            });
        }
        
        // Blur validation
        if (this.options.validateOnBlur) {
            field.addEventListener('blur', () => {
                this.validateField(field.name || field.id);
            });
        }
        
        // Add required indicator
        if (config.required) {
            this.addRequiredIndicator(field);
        }
        
        // Add character counter if maxLength exists and is valid (> 0)
        if (field.maxLength && field.maxLength > 0) {
            this.addCharacterCounter(field);
        }
    }
    
    addRequiredIndicator(field) {
        const label = this.form.querySelector(`label[for="${field.id}"]`);
        if (label && !label.querySelector('.required-indicator')) {
            const indicator = document.createElement('span');
            indicator.className = 'required-indicator';
            indicator.textContent = ' *';
            indicator.style.color = '#EF4444';
            label.appendChild(indicator);
        }
    }
    
    addCharacterCounter(field) {
        const wrapper = field.closest('.form-group') || field.parentElement;
        const counter = document.createElement('div');
        counter.className = 'character-counter';
        counter.style.fontSize = '0.75rem';
        counter.style.color = '#94a3b8';
        counter.style.marginTop = '0.25rem';
        wrapper.appendChild(counter);
        
        const updateCounter = () => {
            const current = field.value.length;
            const max = field.maxLength;
            if (max && max > 0) {
                counter.textContent = `${current} / ${max} လုံး`;
                if (current > max * 0.9) {
                    counter.style.color = '#F59E0B';
                } else {
                    counter.style.color = '#94a3b8';
                }
            } else {
                counter.textContent = `${current} လုံး`;
                counter.style.color = '#94a3b8';
            }
        };
        
        field.addEventListener('input', updateCounter);
        updateCounter();
    }
    
    validateField(fieldName) {
        const config = this.fields.get(fieldName);
        if (!config) return true;
        
        const field = config.field;
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        // Required validation
        if (config.required && !value) {
            isValid = false;
            errorMessage = ValidationMessages.required(config.label);
        }
        
        // Rule validations
        if (isValid && value) {
            for (const rule of config.rules) {
                const result = this.validateRule(value, rule, config);
                if (!result.valid) {
                    isValid = false;
                    errorMessage = result.message;
                    break;
                }
            }
        }
        
        // Update UI
        this.updateFieldUI(field, isValid, errorMessage);
        
        return isValid;
    }
    
    validateRule(value, rule, config) {
        switch (rule.name) {
            case 'email':
                if (!ValidationRules.email.test(value)) {
                    return { valid: false, message: ValidationMessages.emailInvalid };
                }
                break;
                
            case 'url':
                if (!ValidationRules.url.test(value)) {
                    return { valid: false, message: ValidationMessages.urlInvalid };
                }
                break;
                
            case 'phone':
                if (!ValidationRules.phone.test(value)) {
                    return { valid: false, message: ValidationMessages.phoneInvalid };
                }
                break;
                
            case 'number':
                const num = parseFloat(value);
                if (isNaN(num)) {
                    return { valid: false, message: ValidationMessages.numberInvalid };
                }
                if (rule.params[0] && num < parseFloat(rule.params[0])) {
                    return { valid: false, message: ValidationMessages.numberMin(rule.params[0]) };
                }
                if (rule.params[1] && num > parseFloat(rule.params[1])) {
                    return { valid: false, message: ValidationMessages.numberMax(rule.params[1]) };
                }
                break;
                
            case 'minLength':
                if (value.length < parseInt(rule.params[0])) {
                    return { valid: false, message: ValidationMessages.textMin(rule.params[0]) };
                }
                break;
                
            case 'maxLength':
                if (value.length > parseInt(rule.params[0])) {
                    return { valid: false, message: ValidationMessages.textMax(rule.params[0]) };
                }
                break;
                
            case 'json':
                try {
                    JSON.parse(value);
                } catch (e) {
                    return { valid: false, message: ValidationMessages.jsonInvalid };
                }
                break;
                
            case 'botName':
                if (!ValidationRules.botName.test(value)) {
                    return { valid: false, message: 'Bot အမည်သည် မြန်မာစာ၊ အင်္ဂလိပ်စာလုံး၊ ဂဏန်း၊ space, hyphen, underscore သာ ပါဝင်နိုင်ပါသည် (2-50 လုံး)' };
                }
                break;
                
            case 'pattern':
                if (rule.params[0]) {
                    const pattern = new RegExp(rule.params[0]);
                    if (!pattern.test(value)) {
                        return { valid: false, message: ValidationMessages.patternInvalid };
                    }
                }
                break;
        }
        
        return { valid: true };
    }
    
    updateFieldUI(field, isValid, errorMessage) {
        const wrapper = field.closest('.form-group') || field.parentElement;
        
        // Remove existing validation UI
        const existingError = wrapper.querySelector('.field-error');
        const existingIcon = wrapper.querySelector('.validation-icon');
        
        if (existingError) existingError.remove();
        if (existingIcon) existingIcon.remove();
        
        // Update field classes
        field.classList.remove('is-valid', 'is-invalid');
        
        if (field.value.trim()) {
            if (isValid) {
                field.classList.add('is-valid');
                if (this.options.showIcons) {
                    this.addValidationIcon(field, 'valid');
                }
            } else {
                field.classList.add('is-invalid');
                if (this.options.showIcons) {
                    this.addValidationIcon(field, 'invalid');
                }
                this.showFieldError(wrapper, errorMessage);
            }
        }
    }
    
    addValidationIcon(field, state) {
        const wrapper = field.closest('.form-group') || field.parentElement;
        const icon = document.createElement('i');
        icon.className = `validation-icon fas ${state === 'valid' ? 'fa-check-circle' : 'fa-exclamation-circle'}`;
        icon.style.position = 'absolute';
        icon.style.right = '12px';
        icon.style.top = '50%';
        icon.style.transform = 'translateY(-50%)';
        icon.style.color = state === 'valid' ? '#10B981' : '#EF4444';
        icon.style.fontSize = '1rem';
        icon.style.pointerEvents = 'none';
        
        if (field.style.position !== 'relative') {
            wrapper.style.position = 'relative';
        }
        wrapper.appendChild(icon);
    }
    
    showFieldError(wrapper, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.style.color = '#EF4444';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '0.5rem';
        errorDiv.style.display = 'flex';
        errorDiv.style.alignItems = 'center';
        errorDiv.style.gap = '0.5rem';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> <span>${message}</span>`;
        wrapper.appendChild(errorDiv);
    }
    
    validateForm() {
        let isValid = true;
        
        this.fields.forEach((config, fieldName) => {
            if (!this.validateField(fieldName)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    showFormError() {
        const firstInvalid = this.form.querySelector('.is-invalid');
        if (firstInvalid) {
            firstInvalid.focus();
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        
        // Show toast notification
        this.showToast(ValidationMessages.formInvalid, 'error');
    }
    
    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `validation-toast validation-toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Hide toast after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
    
    // Public method to manually validate a field
    validate(fieldName) {
        return this.validateField(fieldName);
    }
    
    // Public method to reset validation state
    reset() {
        this.fields.forEach((config, fieldName) => {
            const field = config.field;
            field.classList.remove('is-valid', 'is-invalid');
            const wrapper = field.closest('.form-group') || field.parentElement;
            const error = wrapper.querySelector('.field-error');
            const icon = wrapper.querySelector('.validation-icon');
            if (error) error.remove();
            if (icon) icon.remove();
        });
    }
}

// ============================================
// Auto-initialize validators for common forms
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Contact form
    if (document.getElementById('lead-submission-form')) {
        window.contactFormValidator = new FormValidator('lead-submission-form', {
            realTime: true,
            showIcons: true
        });
    }
    
    // Bot builder form
    if (document.getElementById('botBuilderForm')) {
        window.botFormValidator = new FormValidator('botBuilderForm', {
            realTime: true,
            showIcons: true
        });
    }
    
    // User settings form (if exists)
    if (document.getElementById('userSettingsForm')) {
        window.userSettingsValidator = new FormValidator('userSettingsForm', {
            realTime: true,
            showIcons: true
        });
    }
});

// Export for use in other scripts
window.FormValidator = FormValidator;
window.ValidationMessages = ValidationMessages;
window.ValidationRules = ValidationRules;

