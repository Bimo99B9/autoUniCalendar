import useInput from "../../hooks/use-input";
import HeaderSettingsButton from "./HeaderSettingsButton";
import React from "react";

import SettingsContext from "../../store/settings-context";
import classes from "./Form.module.css";

const Form = (props) => {
  const ctx = React.useContext(SettingsContext);

  const {
    value: enteredCode,
    isValid: codeIsValid,
    hasError: codeHasError,
    valueChangeHandler: codeChangeHandler,
    inputBlurHandler: codeBlurHandler,
    reset: codeReset,
  } = useInput(
    (value) =>
      value.length === 37 &&
      value.charAt(0) === "0" &&
      value.charAt(1) === "0" &&
      value.charAt(2) === "0" &&
      value.charAt(3) === "0" &&
      value.charAt(27) === ":" &&
      value.charAt(28) === "1" &&
      value.charAt(29) === "d"
  );

  let formIsValid = false;

  if (codeIsValid) {
    formIsValid = true;
  }

  const formSubmissionHandler = (event) => {
    event.preventDefault();
    if (!codeIsValid) {
      console.log("Code is not valid");
      return;
    }

    console.log("all good");

    document.getElementById("form").submit();
    codeReset();
  };

  const codeInputClasses = `${classes.form} ${
    codeHasError ? classes.invalid : ""
  }`;

  return (
    <React.Fragment>
      <form method="post" onSubmit={formSubmissionHandler} id="form">
        <div className={classes.control}>
          <div className={codeInputClasses}>
            <label htmlFor="codigo">Código</label>
            <input
              type="text"
              id="codigo"
              name="jsessionid"
              onChange={codeChangeHandler}
              onBlur={codeBlurHandler}
              value={enteredCode}
            />
            {codeHasError && (
              <p className={classes.error}>El código no es válido.</p>
            )}
          </div>
          <div>
            <input type="hidden" name="filename" value={ctx.saveas} />
          </div>
        </div>
      </form>

      <div className={classes.actions}>
        <HeaderSettingsButton onClick={props.onShowSettings} />
        <button className="button" disabled={!formIsValid} onClick={formSubmissionHandler}>
          Generar
        </button>
      </div>
    </React.Fragment>
  );
};

export default Form;
