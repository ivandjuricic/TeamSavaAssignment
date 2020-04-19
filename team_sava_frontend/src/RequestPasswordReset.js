import React, { useState } from "react";
import { emailPasswordResetRequest } from "./client";
import { navigate } from "@reach/router";

function RequestPasswordReset() {
  const [email, setEmail] = useState("");
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        emailPasswordResetRequest(email).then(() => {
          navigate("/login");
        });
      }}
    >
      <h3>ASK FOR PASSWORD RESET LINK</h3>
      <small>We will send you an email with pasword reset information</small>
      <br />
      <input
        type="text"
        name="email"
        placeholder="Email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <input type="submit" value="Submit" />
    </form>
  );
}

export default RequestPasswordReset;
