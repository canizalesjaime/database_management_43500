import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      const response = await api.post("/register", {
        email,
        password,
      });

      if (response.data.success) {
        navigate("/success");
      } else {
        navigate("/failed");
      }
    } catch (error) {
      console.error(error);
      navigate("/failed");
    }
  };

  return (
    <div className="container">
      <h2>Register</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleRegister}>
        Register
      </button>

      <button
        className="secondaryButton"
        onClick={() => navigate("/")}
      >
        Home
      </button>
    </div>
  );
}

export default Register;