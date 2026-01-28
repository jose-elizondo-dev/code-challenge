export default function CreateView({ form, onChange, onSubmit }) {
    return (
        <form onSubmit={onSubmit}>
            <h2>Create Item</h2>

            <input name="name" placeholder="Name" value={form.name} onChange={onChange} />
            <input name="price" type="number" placeholder="Price" value={form.price} onChange={onChange} />

            <select name="category" value={form.category} onChange={onChange}>
                <option value="main">Main</option>
                <option value="side">Side</option>
                <option value="drink">Drink</option>
                <option value="dessert">Dessert</option>
            </select>

            <label>
                <input type="checkbox" name="isAvailable" checked={form.isAvailable} onChange={onChange} />
                Available
            </label>

            <button>Create</button>
        </form>
    );
}
