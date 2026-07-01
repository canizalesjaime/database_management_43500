import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../services/api";

function ClockIn() {
  const navigate = useNavigate();
  const location = useLocation();

  // Email passed from Login.jsx
  const email = location.state?.email || "";

  // Save the clock-in time when the page first loads
  const [clockInTime] = useState(new Date());

  // If someone navigates here manually, return home
  if (email === "") {
    navigate("/");
    return null;
  }

  const handleClockOut = async () => {
    try {
      const clockOutTime = new Date();

      const response = await api.post("/clockout", {
        email: email,
        clock_in: clockInTime.toISOString(),
        clock_out: clockOutTime.toISOString(),
      });

      if (response.data.success) {
        navigate("/");
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
      <h2>Welcome</h2>

      <p>
        <strong>Email</strong>
      </p>

      <p>{email}</p>

      <br />

      <p>
        <strong>Clock In Time</strong>
      </p>

      <div className="clockTime">
        {clockInTime.toLocaleString()}
      </div>

      <button onClick={handleClockOut}>
        Clock Out
      </button>
    </div>
  );
}

export default ClockIn;