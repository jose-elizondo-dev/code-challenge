const BASE_URL = import.meta.env.VITE_API_BASE_URL;
const API_TOKEN = import.meta.env.VITE_API_TOKEN;

function authHeaders() {
    return {
        Authorization: `Bearer ${API_TOKEN}`,
        "Content-Type": "application/json",
    };
}

export async function fetchMenu(params) {
    // Filter out parameters that are undefined or empty
    const filteredParams = {};
    for (const key in params) {
        if (params[key] !== undefined && params[key] !== "") {
            filteredParams[key] = params[key];
        }
    }

    const query = new URLSearchParams(filteredParams).toString();
    const res = await fetch(`${BASE_URL}/api/menu?${query}`);
    if (!res.ok) throw new Error("Failed to fetch menu");
    return res.json();
}

export async function fetchItem(id) {
    const res = await fetch(`${BASE_URL}/api/menu/${id}`);
    if (!res.ok) throw new Error("Failed to fetch item");
    return res.json();
}

export async function createItem(data) {
    const res = await fetch(`${BASE_URL}/api/menu`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify(data),
    });

    if (!res.ok) {
        let errorBody = {};
        try {
            errorBody = await res.json();
        } catch { }

        throw {
            status: res.status,
            message: errorBody.detail || "Unknown error",
        };
    }

    return res.json();
}




export async function updateItem(id, data) {
    const res = await fetch(`${BASE_URL}/api/menu/${id}`, {
        method: "PATCH",
        headers: authHeaders(),
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Update failed");
    return res.json();
}



export async function deleteItem(id) {
    const res = await fetch(`${BASE_URL}/api/menu/${id}`, {
        method: "DELETE",
        headers: authHeaders(),
    });
    if (!res.ok) throw new Error("Delete failed");
    return res.json();
}
