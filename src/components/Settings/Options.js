import React from "react";
import Checkboxes from "./Checkboxes";

import classes from "./Options.module.css";
import RadioButtons from "./RadioButtons";

// General component for the radio buttons and checkboxes
const Options = (props) => {
  return (
    <React.Fragment>
      <div className={classes.options}>
        <h3>Settings</h3>
      </div>
      <div className={classes.separation}>
        <fieldset id="radiobuttons">
        <RadioButtons onClick={props.onCheck} university={props.university} />
        </fieldset>
        <Checkboxes university={props.university} />
      </div>
    </React.Fragment>
  );
};

/*
<hr
  style={{
    color: "grey",
    backgroundColor: "grey",
    borderColor: "grey",
    height: 115,
    fontWeight: "bold",
    width: 5,
    marginTop: "0px",
    marginLeft: "auto",
    marginRight: "auto",
    borderRadius: 14,
  }}
/>
*/

export default Options;
