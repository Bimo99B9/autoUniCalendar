import React from "react";

import useInput from "../../hooks/use-input";
import classes from "./Saver.module.css";

// Component to set the name of the filename
const Saver = (props) => {
  // useInput hook to get the name of filename
  const {
    value: enteredName,
    valueChangeHandler: nameChangeHandler,
    inputBlurHandler: nameBlurHandler,
  } = useInput((value) => value.length > 0);

  // Function to set the name of the file
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
          placeholder="Calendario"
        />
        <input
          className={classes.extension}
          type="text"
          value=".csv"
          name="extension"
          id="extension"
          disabled={true}
        />
      </div>
    </React.Fragment>
  );
};

export default Saver;
