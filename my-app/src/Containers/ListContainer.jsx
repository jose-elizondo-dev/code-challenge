import { useEffect, useState } from "react";
import { fetchMenu, deleteItem } from "../api/api";
import ListView from "../Views/ListView";

export default function ListContainer() {
    const [data, setData] = useState({ items: [], total: 0 });
    const [params, setParams] = useState({
        page: 1,
        pageSize: 5,
        search: "",
        category: undefined,
        available: undefined,
        sort: "name",
        order: "asc",
    });

    /**
     * Effect hook to fetch data when parameters change
     * Runs whenever params object changes
     */
    useEffect(() => {
        fetchMenu(params).then(setData);
    }, [params]);



    /**
     * Render ListView component with props
     * - data: Current menu data
     * - params: Current filter parameters
     * - setParams: Function to update parameters
     * - onDelete: Function to handle item deletion
     */

    return (
        <ListView
            data={data}
            params={params}
            setParams={setParams}
            onDelete={async (id) => {
                await deleteItem(id);
                fetchMenu(params).then(setData);
            }}
        />
    );
}
