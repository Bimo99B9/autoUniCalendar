import React from "react";
import Checkboxes from "./Checkboxes";

import classes from "./Options.module.css";

// General component for the radio buttons and checkboxes
const Options = (props) => {
  return (
    <React.Fragment>
      <div className={classes.options}>
        <h3>Settings</h3>
      </div>
      <div className={classes.cajitas}>
        <Checkboxes university={props.university}/>
      </div>
    </React.Fragment>
  );
};

export default Options;
