import React, { useState } from "react";

import SettingsIcon from "../Settings/SettingsIcon";
//import CartContext from "../../store/cart-context";
import classes from "./HeaderSettingsButton.module.css";

const HeaderSettingsButton = (props) => {
  const [btnIsHighlighted] = useState(false);

  const btnClasses = `${classes.button} ${
    btnIsHighlighted ? classes.bump : ""
  }`;

  return (
    <button className={btnClasses} onClick={props.onClick}>
      <span className={classes.icon}>
        <SettingsIcon />
      </span>
      <span>Settings</span>
    </button>
  );
};

export default HeaderSettingsButton;
