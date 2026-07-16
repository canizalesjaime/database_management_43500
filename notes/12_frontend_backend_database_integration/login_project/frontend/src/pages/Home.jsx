import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1>Employee Time Clock</h1>

      <button onClick={() => navigate("/login")}>
        Login
      </button>

      <button
        className="secondaryButton"
        onClick={() => navigate("/register")}
      >
        Register
      </button>
    </div>
  );
}

export default Home;