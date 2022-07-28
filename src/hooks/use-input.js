import { useState } from "react";

// Custom hook to use the input
const useInput = (validateValue) => {
  const [enteredValue, setEnteredValue] = useState(""); // State for the entered input value
  const [isTouched, setIsTouched] = useState(false); // State to check if the input has been touched

  const valueIsValid = validateValue(enteredValue); // Check if the input value is valid through the validateValue function
  const hasError = !valueIsValid && isTouched; // Check if the input has an error (if it is not valid and it has been touched)

  // Function to update the enteredValue of the input
  const valueChangeHandler = (event) => {
    setEnteredValue(event.target.value);
  };

  // Function to update the isTouched state of the input
  const inputBlurHandler = () => {
    if (enteredValue.trim().length === 0) {
      setIsTouched(false);
    } else {
      setIsTouched(true);
    }
  };

  // Reset for the enteredValue and isTouched state
  const reset = () => {
    setEnteredValue("");
    setIsTouched(false);
  };

  return {
    value: enteredValue,
    isValid: valueIsValid,
    hasError,
    valueChangeHandler,
    inputBlurHandler,
    reset,
  };
};

export default useInput;
