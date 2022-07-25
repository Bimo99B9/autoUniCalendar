import React, { useState } from "react";

import SettingsIcon from "../Settings/SettingsIcon";
//import CartContext from "../../store/cart-context";
import classes from "./HeaderSettingsButton.module.css";

const HeaderSettingsButton = (props) => {
  const [btnIsHighlighted] = useState(false);
  // const cartCtx = useContext(CartContext);

  // const { items } = cartCtx;

  // const numberOfCartItems = items.reduce((curNumber, item) => {
  //   return curNumber + item.amount;
  // }, 0);

  const btnClasses = `${classes.button} ${
    btnIsHighlighted ? classes.bump : ""
  }`;

  // useEffect(() => {
  //   if (items.length === 0) {
  //     return;
  //   }
  //   setBtnIsHighlighted(true);

  //   const timer = setTimeout(() => {
  //     setBtnIsHighlighted(false);
  //   }, 300);

  //   return () => {
  //     clearTimeout(timer);
  //   };
  // }, [items]);

  /* <button className={btnClasses} onClick={props.onClick}> */

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
