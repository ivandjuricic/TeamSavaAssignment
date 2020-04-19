import React, { useState } from "react";
import { signUpRequest } from "./client";
import { navigate } from "@reach/router";

function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        signUpRequest(email, password, password2, firstName, lastName)
          .then(function (response) {
            if (response.status !== 201) {
              return Promise.reject("Bad request");
            }
            return response.json();
          })
          .then(function (data) {
            navigate("/login  ");
          });
      }}
    >
      <h3>Sign up</h3>
      <input
        type="text"
        name="email"
        placeholder="Email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />
      <input
        type="password"
        name="password2"
        placeholder="Retype password"
        value={password2}
        onChange={(event) => setPassword2(event.target.value)}
      />
      <input
        type="text"
        name="firstName"
        placeholder="First name"
        value={firstName}
        onChange={(event) => setFirstName(event.target.value)}
      />
      <input
        type="text"
        name="lastName"
        placeholder="Last name"
        value={lastName}
        onChange={(event) => setLastName(event.target.value)}
      />
      <input type="submit" value="Submit" />
    </form>
  );
}

export default SignUp;
