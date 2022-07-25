import React from "react";
import Checkboxes from "./Checkboxes";

import classes from "./Options.module.css";
import RadioButtons from "./RadioButtons";

const Options = (props) => {
  return (
    <React.Fragment>
      <div className={classes.options}>
        <h2>Settings</h2>
      </div>
      <RadioButtons onClick={props.onCheck} university={props.university} />
      <Checkboxes university={props.university} />
    </React.Fragment>
  );
};

export default Options;
