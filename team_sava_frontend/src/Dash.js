import React, { useContext } from "react";
import { Redirect, navigate } from "@reach/router";
import { profileRequest } from "./client";
import ProfileContext from "./profileContext";

export default function Dash() {
  const { name, updateContextValues } = useContext(ProfileContext);
  var shouldRedirect = false;
  if (localStorage.getItem("access")) {
    const data = profileRequest();
    data
      .then((resp) => {
        if (resp.status !== 200) {
          navigate("/login");
        }
        return resp.json();
      })
      .then((data) => {
        if (name !== data.first_name) {
          updateContextValues({ name: data.first_name });
        }
      })
      .catch(() => navigate("/login"));
  } else {
    shouldRedirect = true;
  }
  if (shouldRedirect) {
    return <Redirect to={"/login"} noThrow />;
  }
  return (
    <>
      <h1>LOGGED IN</h1>
      <iframe
        title="rickroll"
        width="560"
        height="315"
        src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
        frameBorder="0"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
    </>
  );
}
