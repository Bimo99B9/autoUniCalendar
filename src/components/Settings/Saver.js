import React from "react";

import useInput from "../../hooks/use-input";
import classes from "./Saver.module.css";

const Saver = (props) => {
  const {
    value: enteredName,
    valueChangeHandler: nameChangeHandler,
    inputBlurHandler: nameBlurHandler,
  } = useInput((value) => value.length > 0);

  const nameHandlerValue = (name) => {
    if (name.target.value.trim().length > 0) {
      nameChangeHandler(name);
      props.onSave(name.target.value);
    } else if (name.target.value === "") {
      console.log("Name is empty");
      nameChangeHandler(name);
      props.onSave("Calendario");
    }
  };

  return (
    <React.Fragment>
      <div className={classes.saveas}>
        <h2>Guardar como</h2>
      </div>
      <div className={classes.form}>
        <input
          type="text"
          id="saveAs"
          name="filename"
          onChange={nameHandlerValue}
          onBlur={nameBlurHandler}
          value={enteredName}
        />
      </div>
    </React.Fragment>
  );
};

export default Saver;
