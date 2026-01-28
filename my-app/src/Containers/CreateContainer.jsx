import { useState } from "react";
import { createItem } from "../api/api";
import CreateView from "../Views/CreateView";

export default function CreateContainer() {
    const [form, setForm] = useState({
        name: "",
        category: "main",
        price: "",
        isAvailable: true,
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setForm({ ...form, [name]: type === "checkbox" ? checked : value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!form.name.trim()) {
            alert("Name cannot be empty");
            return;
        }

        if (!form.price || Number(form.price) <= 0) {
            alert("Price must be greater than 0");
            return;
        }

        try {
            await createItem({ ...form, price: Number(form.price) });
            alert("Item created");
            setForm({ name: "", category: "main", price: "", isAvailable: true });

        } catch (err) {
            if (err.status === 401 || err.status === 403) {
                alert("You are not authorized to create items");

            } else if (err.status === 409) {
                alert("An item with this name already exists");

            } else {
                alert("Unexpected error creating item");
                console.error(err);
            }
        }
    };

    return <CreateView form={form} onChange={handleChange} onSubmit={handleSubmit} />;
}
