import CreateContainer from "./Containers/CreateContainer";
import ListContainer from "./Containers/ListContainer";
import UpdateContainer from "./Containers/UpdateContainer";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import "./App.css";

const App = () => {

  return (
    <>
      {/* BrowserRouter enables client-side routing */}
      <BrowserRouter>
        {/* Navigation bar with links to main sections */}
        <nav style={{ display: "flex", gap: 12, padding: 12 }}>
          <Link to="/menu">List</Link>
          <Link to="/create">Create</Link>
        </nav>

        <Routes>
          {/* Root path redirects to menu listing */}
          <Route path="/" element={<ListContainer />} />

          {/* Menu listing page */}
          <Route path="/menu" element={<ListContainer />} />

          {/* Create new item page */}
          <Route path="/create" element={<CreateContainer />} />

          {/* Update existing item page (dynamic route with ID parameter) */}
          <Route path="/update/:id" element={<UpdateContainer />} />

          {/* Catch-all route: redirect unknown paths to root */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </>
  );

}

export default App;
