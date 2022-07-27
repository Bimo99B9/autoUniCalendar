import React, { useState } from "react";

//import CartContext from "../../store/cart-context";
import classes from "./HeaderSettingsButton.module.css";

const HeaderSettingsButton = (props) => {
  const [btnIsHighlighted] = useState(false);

  const btnClasses = `${classes.button} ${
    btnIsHighlighted ? classes.bump : ""
  }`;

  return (
    <button className={btnClasses} onClick={props.onClick}>
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      ⚙
    </button>
  );
};

export default HeaderSettingsButton;
