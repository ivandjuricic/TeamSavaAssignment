import React, { useState } from "react";
import { passwordResetRequest } from "./client";
import { navigate } from "@reach/router";

function PasswordReset(props) {
  const { resetToken } = props;
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        passwordResetRequest(resetToken, password1, password2)
          .then(function (response) {
            if (response.status !== 204) {
              return Promise.reject("Bad request");
            }
            return response;
          })
          .then(function (data) {
            navigate("/login");
          });
      }}
    >
      <h3>Setup a new password</h3>
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password1}
        onChange={(event) => setPassword1(event.target.value)}
      />
      <input
        type="password"
        name="password2"
        placeholder="Retype password"
        value={password2}
        onChange={(event) => setPassword2(event.target.value)}
      />
      <input type="submit" value="Submit" />
    </form>
  );
}

export default PasswordReset;
