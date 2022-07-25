import React from "react";

import useInput from "../../hooks/use-input";
import classes from "./Saver.module.css";

const Saver = (props) => {
  const {
    value: enteredName,
    valueChangeHandler: nameChangeHandler,
    inputBlurHandler: nameBlurHandler,
  } = useInput((value) => value.length > 0);

  // Not needed anymore
  //   let formIsValid = false;

  //   if (nameIsValid) {
  //     formIsValid = true;
  //   }

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

  // const nameInputClasses = `${classes.form} ${
  //   nameHasError ? classes.invalid : ""
  // }`;

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

/* 
{nameHasError && (
          <p className={classes.error}>El nombre del fichero no es válido.</p>
        )}
*/

export default Saver;
