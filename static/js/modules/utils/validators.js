/**
 * Validators Module
 * @module utils/validators
 * @description Input validation utilities
 */

/**
 * Validation result object
 * @typedef {Object} ValidationResult
 * @property {boolean} valid - Whether validation passed
 * @property {string} [message] - Error message if invalid
 */

/**
 * Validate a required field
 * @param {string} value - Value to validate
 * @param {string} fieldName - Field name for error message
 * @returns {ValidationResult} - Validation result
 */
export function validateRequired(value, fieldName = 'Este campo') {
    const trimmed = String(value || '').trim();
    if (!trimmed) {
        return { valid: false, message: `${fieldName} es requerido` };
    }
    return { valid: true };
}

/**
 * Validate a name field
 * @param {string} name - Name to validate
 * @returns {ValidationResult} - Validation result
 */
export function validateName(name) {
    const required = validateRequired(name, 'El nombre');
    if (!required.valid) return required;
    
    const trimmed = name.trim();
    if (trimmed.length < 2) {
        return { valid: false, message: 'El nombre debe tener al menos 2 caracteres' };
    }
    if (trimmed.length > 100) {
        return { valid: false, message: 'El nombre no puede exceder 100 caracteres' };
    }
    
    return { valid: true };
}

/**
 * Validate a price field
 * @param {string|number} price - Price to validate
 * @returns {ValidationResult} - Validation result
 */
export function validatePrice(price) {
    const required = validateRequired(price, 'El precio');
    if (!required.valid) return required;
    
    const numPrice = parseFloat(price);
    if (isNaN(numPrice)) {
        return { valid: false, message: 'El precio debe ser un número válido' };
    }
    if (numPrice < 0) {
        return { valid: false, message: 'El precio no puede ser negativo' };
    }
    if (numPrice > 999999.99) {
        return { valid: false, message: 'El precio excede el máximo permitido' };
    }
    
    return { valid: true };
}

/**
 * Validate a date field
 * @param {string} dateStr - Date string in YYYY-MM-DD format
 * @returns {ValidationResult} - Validation result
 */
export function validateDate(dateStr) {
    const required = validateRequired(dateStr, 'La fecha');
    if (!required.valid) return required;
    
    // Check format YYYY-MM-DD
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateStr)) {
        return { valid: false, message: 'La fecha debe estar en formato YYYY-MM-DD' };
    }
    
    // Check valid date
    const date = new Date(dateStr + 'T00:00:00');
    if (isNaN(date.getTime())) {
        return { valid: false, message: 'La fecha no es válida' };
    }
    
    return { valid: true };
}

/**
 * Validate notes field (optional, max length)
 * @param {string} notes - Notes to validate
 * @param {number} maxLength - Maximum length
 * @returns {ValidationResult} - Validation result
 */
export function validateNotes(notes, maxLength = 500) {
    if (!notes) return { valid: true };
    
    if (notes.length > maxLength) {
        return { valid: false, message: `Las notas no pueden exceder ${maxLength} caracteres` };
    }
    
    return { valid: true };
}

/**
 * Validate session form data
 * @param {Object} data - Session form data
 * @param {string} data.session_date - Session date
 * @param {string|number} data.session_price - Session price
 * @param {string} [data.notes] - Optional notes
 * @returns {ValidationResult} - Validation result
 */
export function validateSessionForm(data) {
    const dateResult = validateDate(data.session_date);
    if (!dateResult.valid) return dateResult;
    
    const priceResult = validatePrice(data.session_price);
    if (!priceResult.valid) return priceResult;
    
    if (data.notes) {
        const notesResult = validateNotes(data.notes);
        if (!notesResult.valid) return notesResult;
    }
    
    return { valid: true };
}

/**
 * Validate patient form data
 * @param {Object} data - Patient form data
 * @param {string} data.name - Patient name
 * @param {string} [data.notes] - Optional notes
 * @returns {ValidationResult} - Validation result
 */
export function validatePatientForm(data) {
    const nameResult = validateName(data.name);
    if (!nameResult.valid) return nameResult;
    
    if (data.notes) {
        const notesResult = validateNotes(data.notes);
        if (!notesResult.valid) return notesResult;
    }
    
    return { valid: true };
}
