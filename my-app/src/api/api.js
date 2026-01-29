// Load environment variables from Vite
const BASE_URL = import.meta.env.VITE_API_BASE_URL;  // Backend URL
const API_TOKEN = import.meta.env.VITE_API_TOKEN;    // Authentication token

/**
 * Generate authentication headers for protected endpoints
 * @returns {Object} Headers object with Authorization and Content-Type
 */
function authHeaders() {
    return {
        Authorization: `Bearer ${API_TOKEN}`,  // Bearer token authentication
        "Content-Type": "application/json",    // JSON content type
    };
}

/**
 * Fetch menu items with filtering, sorting, and pagination
 * @param {Object} params - Query parameters for filtering
 * @returns {Promise} Promise resolving to menu data
 */

export async function fetchMenu(params) {
    // Filter out undefined or empty parameters to keep URL clean
    const filteredParams = {};
    for (const key in params) {
        if (params[key] !== undefined && params[key] !== "") {
            filteredParams[key] = params[key];
        }
    }

    // Build query string from filtered parameters
    const query = new URLSearchParams(filteredParams).toString();

    // Make GET request to menu endpoint
    const res = await fetch(`${BASE_URL}/api/menu?${query}`);

    // Throw error if response is not OK (4xx or 5xx)
    if (!res.ok) throw new Error("Failed to fetch menu");

    // Parse and return JSON response
    return res.json();
}

/**
 * Fetch a single menu item by ID
 * @param {string} id - Item ID to fetch
 * @returns {Promise} Promise resolving to item data
 */
export async function fetchItem(id) {
    const res = await fetch(`${BASE_URL}/api/menu/${id}`);
    if (!res.ok) throw new Error("Failed to fetch item");
    return res.json();
}

/**
 * Create a new menu item (protected)
 * @param {Object} data - Item data to create
 * @returns {Promise} Promise resolving to created item
 * @throws {Object} Error object with status and message
 */
export async function createItem(data) {
    const res = await fetch(`${BASE_URL}/api/menu`, {
        method: "POST",
        headers: authHeaders(),            // Include authentication
        body: JSON.stringify(data),        // Stringify request body
    });

    if (!res.ok) {
        let errorBody = {};
        try {
            // Try to parse error response body
            errorBody = await res.json();
        } catch {
            // If response is not JSON, use empty object
        }

        // Throw structured error with status code and message
        throw {
            status: res.status,
            message: errorBody.detail || "Unknown error",
        };
    }

    return res.json();
}

/**
 * Update an existing menu item (protected)
 * @param {string} id - Item ID to update
 * @param {Object} data - Partial item data to update
 * @returns {Promise} Promise resolving to updated item
 */
export async function updateItem(id, data) {
    const res = await fetch(`${BASE_URL}/api/menu/${id}`, {
        method: "PATCH",                    // PATCH for partial updates
        headers: authHeaders(),
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Update failed");
    return res.json();
}

/**
 * Soft delete a menu item (protected)
 * @param {string} id - Item ID to delete
 * @returns {Promise} Promise resolving to deleted item
 */
export async function deleteItem(id) {
    const res = await fetch(`${BASE_URL}/api/menu/${id}`, {
        method: "DELETE",
        headers: authHeaders(),
    });
    if (!res.ok) throw new Error("Delete failed");
    return res.json();
}