import React from "react";

import classes from "./Options.module.css";
import RadioButtons from "./RadioButtons";

const Options = () => {
  return (
    <React.Fragment>
      <div className={classes.options}>
        <h2>Settings</h2>
      </div>

      <RadioButtons />
    </React.Fragment>
  );
};

export default Options;
