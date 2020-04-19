import React, { Component } from "react";
import PropTypes from "prop-types";

const defaultState = {
  name: "",
  id: "8",
};

const ProfileContext = React.createContext({
  ...defaultState,
  updateContextValues: (valueObject) => {
    this.setState({ ...valueObject });
  },
});

class ProfileProvider extends Component {
  constructor() {
    super();

    this.state = {
      ...defaultState,
    };
  }

  updateContextValues = (valueObject) => {
    this.setState({ ...valueObject });
  };

  render() {
    const { children } = this.props;
    return (
      <ProfileContext.Provider
        value={{ ...this.state, updateContextValues: this.updateContextValues }}
      >
        {children}
      </ProfileContext.Provider>
    );
  }
}

ProfileProvider.propTypes = {
  name: PropTypes.string,
  id: PropTypes.string,
};

export { ProfileProvider };
export default ProfileContext;
