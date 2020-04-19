import React, { useState } from "react";
import { Link, navigate } from "@reach/router";
import { loginRequest } from "./client";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div>
      <h1>Welcome to Ivans Home Assignment</h1>
      <div style={{ marginBottom: "20px" }}>
        <p>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          const request = loginRequest(email, password);
          request
            .then(function (response) {
              if (response.status !== 200) {
                return Promise.reject("Fail login");
              }
              return response.json();
            })
            .then(function (data) {
              localStorage.setItem("access", data.access);
              localStorage.setItem("refresh", data.refresh);
              navigate("/");
            });
        }}
      >
        <h3>Log in</h3>
        <input
          type="text"
          name="email"
          placeholder="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
        <input
          type="password"
          name="password"
          placeholder="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <input type="submit" value="Submit" />
      </form>
      <p>Forgot password?</p>
      <p>
        Use <Link to="/reset-password">this</Link> form to ask for a new one
      </p>
    </div>
  );
}

export default Login;
