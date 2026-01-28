import { useState } from "react";

export default function UpdateView({ item, onSave }) {
    const [price, setPrice] = useState(item.price);
    const [isAvailable, setIsAvailable] = useState(item.isAvailable);
    const [category, setCategory] = useState(item.category);
    const [name, setName] = useState(item.name);

    return (
        <>
            <h2>Update {item.name}</h2>

            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />

            <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />

            <select value={category} onChange={(e) => setCategory(e.target.value)}>
                <option value="main">Main</option>
                <option value="side">Side</option>
                <option value="drink">Drink</option>
                <option value="dessert">Dessert</option>
            </select>

            <label> <input type="checkbox" checked={isAvailable} onChange={(e) => setIsAvailable(e.target.checked)} /> Available </label>

            <button onClick={() => {
                if (!name.trim()) { alert("Name cannot be empty"); return; }
                if (!price || Number(price) <= 0) { alert("Price must be greater than 0"); return; }
                onSave({ name, category, price: Number(price), isAvailable })
            }}> Save </button>
        </>
    );
}
