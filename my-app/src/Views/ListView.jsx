import { Link } from "react-router-dom";
import "./ListView.css";

export default function ListView({ data, params, setParams, onDelete }) {
    return (
        <>
            <h2>Menu</h2>

            <input placeholder="Search" onChange={(e) => setParams({ ...params, search: e.target.value })} />

            <select onChange={(e) => setParams({ ...params, category: e.target.value })}>
                <option value="">All</option>
                <option value="main">Main</option>
                <option value="side">Side</option>
                <option value="drink">Drink</option>
                <option value="dessert">Dessert</option>
            </select>

            <select onChange={(e) => setParams({ ...params, available: e.target.value === "" ? "" : e.target.value === "true" })}>
                <option value="">All</option>
                <option value="true">Available</option>
                <option value="false">Unavailable</option>
            </select>

            <select onChange={(e) => setParams({ ...params, sort: e.target.value })}>
                <option value="name">Name</option>
                <option value="price">Price</option>
            </select>

            <select onChange={(e) => setParams({ ...params, order: e.target.value })}>
                <option value="asc">ASC</option>
                <option value="desc">DESC</option>
            </select>

            <ul>
                {data.items.map((i) => (
                    <li key={i.id}>
                        {i.name} - ${i.price} ({i.category})
                        <Link to={`/update/${i.id}`}>Edit</Link>
                        <button onClick={() => onDelete(i.id)}>Delete</button>
                    </li>
                ))}
            </ul>

            <button disabled={params.page === 1} onClick={() => setParams({ ...params, page: params.page - 1 })}>
                Prev
            </button>
            <button onClick={() => setParams({ ...params, page: params.page + 1 })}>
                Next
            </button>
        </>
    );
}
