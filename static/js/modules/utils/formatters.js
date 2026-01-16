/**
 * Formatters Module
 * @module utils/formatters
 * @description Date and price formatting utilities for Spanish locale
 */

/**
 * Spanish day names (Sunday = index 0)
 * @type {string[]}
 */
const SPANISH_DAYS = [
    'Domingo', 'Lunes', 'Martes', 'Miércoles',
    'Jueves', 'Viernes', 'Sábado'
];

/**
 * Spanish month names
 * @type {string[]}
 */
const SPANISH_MONTHS = [
    'Enero', 'Febrero', 'Marzo', 'Abril',
    'Mayo', 'Junio', 'Julio', 'Agosto',
    'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

/**
 * Format a date string for display in Spanish
 * @param {string} dateStr - Date in YYYY-MM-DD format
 * @returns {string} - Formatted date string (e.g., "Lunes 15/01/2024")
 * @example
 * formatDisplayDate('2024-01-15'); // "Lunes 15/01/2024"
 */
export function formatDisplayDate(dateStr) {
    if (!dateStr) return '';
    
    // Parse date ensuring no timezone issues
    const date = new Date(dateStr + 'T00:00:00');
    
    const dayName = SPANISH_DAYS[date.getDay()];
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${dayName} ${day}/${month}/${year}`;
}

/**
 * Format a date with month name in Spanish
 * @param {string} dateStr - Date in YYYY-MM-DD format
 * @returns {string} - Formatted date (e.g., "15 de Enero, 2024")
 */
export function formatDisplayDateLong(dateStr) {
    if (!dateStr) return '';
    
    const date = new Date(dateStr + 'T00:00:00');
    
    const day = date.getDate();
    const month = SPANISH_MONTHS[date.getMonth()];
    const year = date.getFullYear();
    
    return `${day} de ${month}, ${year}`;
}

/**
 * Format a price for display (matching backend format)
 * @param {number|string} price - Price value
 * @returns {string} - Formatted price string (e.g., "$1,234.56")
 * @example
 * formatPrice(1234.56); // "$1,234.56"
 */
export function formatPrice(price) {
    const numPrice = parseFloat(price);
    if (isNaN(numPrice)) return '$0.00';
    
    return '$' + numPrice.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Parse a formatted price string back to a number
 * @param {string} priceStr - Formatted price string (e.g., "$1,234.56")
 * @returns {number} - Numeric price value
 */
export function parsePrice(priceStr) {
    if (!priceStr) return 0;
    const cleaned = String(priceStr).replace(/[$,]/g, '');
    const parsed = parseFloat(cleaned);
    return isNaN(parsed) ? 0 : parsed;
}

/**
 * Format a date for input fields (YYYY-MM-DD)
 * @param {Date} date - Date object
 * @returns {string} - Formatted date for input
 */
export function formatDateForInput(date) {
    if (!(date instanceof Date) || isNaN(date)) return '';
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}
