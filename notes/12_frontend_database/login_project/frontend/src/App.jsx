import { Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ClockIn from "./pages/ClockIn";
import Success from "./pages/Success";
import Failed from "./pages/Failed";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/clockin" element={<ClockIn />} />
      <Route path="/success" element={<Success />} />
      <Route path="/failed" element={<Failed />} />
    </Routes>
  );
}

export default App;