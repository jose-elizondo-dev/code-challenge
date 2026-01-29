import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchItem, updateItem } from "../api/api";
import UpdateView from "../Views/UpdateView";

export default function UpdateContainer() {
    const { id } = useParams();
    const [item, setItem] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    /**
     * Effect hook to load item data when component mounts or ID changes
     */
    useEffect(() => {
        async function loadItem() {
            try {
                setLoading(true);
                setError(null);
                const itemData = await fetchItem(id);
                setItem(itemData);
            } catch (err) {
                console.error(err);
                setError(err.message);
                setItem(undefined);
            } finally {
                setLoading(false);
            }
        }
        loadItem();
    }, [id]);


    if (loading) return <div className="loading">Loading item...</div>;
    if (error) return <div className="error">Error: {error}</div>;
    if (item === undefined) return <div className="not-found">Item not found</div>;


    /**
    * Handle saving updated item
    * @param {Object} data - Updated item data
    */
    const handleSave = async (data) => {
        try {
            await updateItem(id, data);
            alert("Item updated successfully");
            const updatedItem = await fetchItem(id);
            setItem(updatedItem);
        } catch (err) {
            alert(`Update failed: ${err.message}`);
        }
    };

    // Render UpdateView with item data and save handler
    return <UpdateView item={item} onSave={handleSave} />;



}
