import React from "react";
import Checkboxes from "./Checkboxes";

import classes from "./Options.module.css";
import RadioButtons from "./RadioButtons";
// import SettingsContext from "../../store/settings-context";

const Options = (props) => {
  // const ctx = React.useContext(SettingsContext);

  return (
    <React.Fragment>
      <div className={classes.options}>
        <h2>Settings</h2>
      </div>
      <RadioButtons onClick={props.onCheck} />
      <Checkboxes />
    </React.Fragment>
  );
};

export default Options;
