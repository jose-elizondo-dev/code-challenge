export default function CreateView({ form, onChange, onSubmit, loading }) {
    return (
        <form onSubmit={onSubmit}>
            <h2>Create Item</h2>

            <input name="name" placeholder="Name" value={form.name} onChange={onChange} disabled={loading} required />
            <input name="price" type="number" step="0.01" min="0" placeholder="Price" value={form.price} onChange={onChange} disabled={loading} required />

            <select name="category" value={form.category} onChange={onChange} disabled={loading}>
                <option value="main">Main</option>
                <option value="side">Side</option>
                <option value="drink">Drink</option>
                <option value="dessert">Dessert</option>
            </select>

            <label>
                <input type="checkbox" name="isAvailable" checked={form.isAvailable} onChange={onChange} disabled={loading} />
                Available
            </label>

            <button type="submit" disabled={loading}> {loading ? "Creating..." : "Create"}</button>
        </form>
    );
}
