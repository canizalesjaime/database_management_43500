import { useNavigate } from "react-router-dom";

function Failed() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1 className="failed">
        Failed
      </h1>

      <button onClick={() => navigate("/")}>
        Return Home
      </button>
    </div>
  );
}

export default Failed;