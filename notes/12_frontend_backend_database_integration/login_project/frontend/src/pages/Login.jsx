import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await api.post("/login", {
        email,
        password,
      });

      if (response.data.success) {
        navigate("/clockin", {
          state: {
            email: email,
          },
        });
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
      <h2>Login</h2>

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

      <button onClick={handleLogin}>
        Login
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

export default Login;