import React from "react";
import "./App.css";
import { Router } from "@reach/router";
import SignUp from "./SignUp";
import LogIn from "./LogIn";
import RequestPasswordReset from "./RequestPasswordReset";
import PasswordReset from "./PasswordReset";
import Dash from "./Dash";
import Header from "./Header";
import { ProfileProvider } from "./profileContext";

function App() {
  return (
    <div className="App">
      <ProfileProvider>
        <Header />
        <main>
          <Router>
            <Dash path="/" />
            <SignUp path="/signup" />
            <RequestPasswordReset path="/reset-password" />
            <PasswordReset path="/reset-password/:resetToken" />
            <LogIn path="/login" />
          </Router>
        </main>
        <footer>
          <p>footer</p>
        </footer>
      </ProfileProvider>
    </div>
  );
}

export default App;
