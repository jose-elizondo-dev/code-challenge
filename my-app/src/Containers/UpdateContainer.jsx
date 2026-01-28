import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchMenu, updateItem } from "../api/api";
import UpdateView from "../Views/UpdateView";

export default function UpdateContainer() {
    const { id } = useParams();
    const [item, setItem] = useState(null);

    useEffect(() => {
        async function loadItem() {
            try {
                const res = await fetchMenu({});
                const found = res.items.find((i) => i.id === id); // alphanumeric id
                setItem(found);
            } catch (err) {
                console.error(err);
                setItem(undefined); // to show error if it does not load
            }
        }
        loadItem();
    }, [id]);

    if (item === null) return <p>Loading...</p>;
    if (item === undefined) return <p>Item not found</p>;

    return (
        <UpdateView
            item={item}
            onSave={async (data) => {
                await updateItem(id, data);
                alert("Updated");
            }}
        />
    );



}
