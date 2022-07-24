import React from "react";
import Checkboxes from "./Checkboxes";

import classes from "./Options.module.css";
import RadioButtons from "./RadioButtons";

const Options = () => {
  return (
    <React.Fragment>
      <div className={classes.options}>
        <h2>Settings</h2>
      </div>
      <RadioButtons />
      <Checkboxes />
    </React.Fragment>
  );
};

export default Options;
