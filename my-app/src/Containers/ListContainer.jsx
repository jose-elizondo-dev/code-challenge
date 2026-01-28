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


    useEffect(() => {
        fetchMenu(params).then(setData);
    }, [params]);


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
