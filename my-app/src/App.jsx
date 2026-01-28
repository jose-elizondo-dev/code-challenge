import CreateContainer from "./Containers/CreateContainer";
import ListContainer from "./Containers/ListContainer";
import UpdateContainer from "./Containers/UpdateContainer";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import "./App.css";

const App = () => {

  return (
    <>
      <BrowserRouter>
        <nav style={{ display: "flex", gap: 12, padding: 12 }}>
          <Link to="/items">List</Link>
          <Link to="/create">Create</Link>
        </nav>

        <Routes>
          <Route path="/" element={<ListContainer />} />
          <Route path="/items" element={<ListContainer />} />
          <Route path="/create" element={<CreateContainer />} />
          <Route path="/update/:id" element={<UpdateContainer />} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </>
  );

}

export default App;
