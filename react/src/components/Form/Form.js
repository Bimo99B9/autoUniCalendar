import useInput from "../../hooks/use-input";
import HeaderSettingsButton from "./HeaderSettingsButton";
import React from 'react';

import classes from "./Form.module.css";

const Form = (props) => {
  const {
    value: enteredCode,
    isValid: codeIsValid,
    hasError: codeHasError,
    valueChangeHandler: codeChangeHandler,
    inputBlurHandler: codeBlurHandler,
    reset: codeReset,
  } = useInput((value) => value.length === 37 && value.charAt(0) === '0' && value.charAt(1) === '0' && value.charAt(2) === '0' && value.charAt(3) === '0' && value.charAt(27) === ':' && value.charAt(28) === '1' && value.charAt(29) === 'd');

  const {
    value: enteredName,
    isValid: nameIsValid,
    hasError: nameHasError,
    valueChangeHandler: nameChangeHandler,
    inputBlurHandler: nameBlurHandler,
    reset: nameReset,
  } = useInput((value) => value.length > 0);

  console.log(enteredCode.length);

  let formIsValid = false;

  if (codeIsValid && nameIsValid) {
    formIsValid = true;
  }

  const formSubmissionHandler = (event) => {
    event.preventDefault();
    if (!codeIsValid) {
      console.log("Code is not valid");
      return;
    }
    if (!nameIsValid) {
      console.log("Name is not valid (cannot be empty)");
      return;
    }

    fetch('http://127.0.0.1:5000', {
      method: 'POST',
      body: JSON.stringify({
        jsessionid: enteredCode,
        filename: enteredName
      })
    });
  }

  const codeInputClasses = `${classes.form} ${
    codeHasError ? classes.invalid : ""
  }`;

  const nameInputClasses = `${classes.form} ${
    codeHasError ? classes.invalid : ""
  }`;

  // const codeInputClasses = codeHasError
  //   ? {"form-control invalid"}
  //   : "form-control";

  // const nameInputClasses = nameHasError
  //   ? "form-control invalid"
  //   : "form-control";

  return (
    <form onSubmit={formSubmissionHandler}>
      <div className={classes.control}>
        <div className={codeInputClasses}>
          <label htmlFor="codigo">Código</label>
          <input
            type="text"
            id="codigo"
            onChange={codeChangeHandler}
            onBlur={codeBlurHandler}
            value={enteredCode}
          />
          {codeHasError && (
            <p className={classes.error}>El código no es válido.</p>
          )}
        </div>
        <div className={nameInputClasses}>
          <label htmlFor="saveAs">Guardar Como</label>
          <input
            type="text"
            id="saveAs"
            onChange={nameChangeHandler}
            onBlur={nameBlurHandler}
            value={enteredName}
          />
          {nameHasError && (
            <p className={classes.error}>El nombre del fichero no es válido.</p>
          )}
        </div>
        <div className={classes.actions}>
          <HeaderSettingsButton onClick={props.onShowSettings} />
          <button className="button" disabled={!formIsValid}>
            Generar
          </button>
        </div>
      </div>
    </form>
  );
};

export default Form;
