import jwt from "jwt-decode";

export function signUpRequest(email, password, password2, firstName, lastName) {
  const host = process.env.REACT_APP_BACKEND_HOST;
  const endpoint = host + "/api/v1/auth-user/";
  return fetch(endpoint, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
      password2,
      first_name: firstName,
      last_name: lastName,
    }),
  });
}

export function emailPasswordResetRequest(email) {
  const host = process.env.REACT_APP_BACKEND_HOST;
  const endpoint = host + "/api/v1/reset-token/";
  return fetch(endpoint, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
    }),
  });
}

export function passwordResetRequest(token, password1, password2) {
  const host = process.env.REACT_APP_BACKEND_HOST;
  const endpoint = host + "/api/v1/reset-password/";
  return fetch(endpoint, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token,
      password1,
      password2,
    }),
  });
}

export function getResetToken(token) {
  const host = process.env.REACT_APP_BACKEND_HOST;
  const endpoint = host + "/api/v1/reset-token/" + token;
  return fetch(endpoint, {
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export function loginRequest(email, password) {
  const host = process.env.REACT_APP_BACKEND_HOST;
  const endpoint = host + "/api/v1/auth-token/";
  return fetch(endpoint, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });
}

export function profileRequest() {
  const host = process.env.REACT_APP_BACKEND_HOST;
  const accessToken = localStorage.getItem("access");
  const userData = jwt(accessToken);
  const userId = userData.user_id;
  const endpoint = host + "/api/v1/auth-user/" + userId + "/";
  return fetch(endpoint, {
    headers: {
      Authorization: "Bearer " + accessToken,
    },
  });
}
