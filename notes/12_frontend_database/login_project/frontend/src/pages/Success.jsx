import { useNavigate } from "react-router-dom";

function Success() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1 className="success">
        Success!
      </h1>

      <button onClick={() => navigate("/")}>
        Return Home
      </button>
    </div>
  );
}

export default Success;