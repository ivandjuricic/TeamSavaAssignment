import React, { useContext } from "react";
import ProfileContext from "./profileContext";
import { useState } from "react";
import { navigate } from "@reach/router";

export default function Header() {
  const { name, updateContextValues } = useContext(ProfileContext);
  const [showMenu, setShowMenu] = useState(false);
  return (
    <header>
      <div>
        <img
          src="https://team-sava.com/wp-content/uploads/2019/07/cropped-favicon512-180x180.png"
          alt="logo"
          height="50px"
        />
        <h3>Team Sava Home Assignment</h3>
      </div>
      {name && (
        <div
          onClick={() => setShowMenu(!showMenu)}
          style={{
            position: "absolute",
            right: "20px",
            display: "flex",
            alignItems: "center",
          }}
        >
          <small style={{ marginRight: "10px" }}>{name}</small>
          <img
            src="http://1.bp.blogspot.com/_7wsQzULWIwo/SxL-DRXzmWI/AAAAAAAACY0/d1g3ymxGLEQ/s400/avatar.gif"
            alt="profile"
            height="50"
            width="50"
          />
        </div>
      )}
      {showMenu && (
        <div
          style={{
            position: "absolute",
            right: "10px",
            top: "125px",
            height: "50px",
            width: "120px",
            backgroundColor: "#d6dde1",
          }}
        >
          <button
            style={{
              width: "100%",
              height: "30px",
              backgroundColor: "#d6dde1",
              border: "none",
            }}
            onClick={() => {
              setShowMenu(false);
              localStorage.removeItem("access");
              localStorage.removeItem("refresh");
              updateContextValues({ name: "" });
              navigate("/login");
            }}
          >
            Logout
          </button>
        </div>
      )}
    </header>
  );
}
