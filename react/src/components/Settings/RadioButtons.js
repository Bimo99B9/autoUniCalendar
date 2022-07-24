import React from 'react';
import classes from "./RadioButtons.module.css";

const RadioButtons = () => {
  return (
    <form>
      <div className={classes.form}>
        <input type="radio" name="option1" id="option1" value="option1" />
        <label for="option1">Option1</label>
      </div>
      <div className={classes.form}>
        <input type="radio" name="option2" id="option2" value="option2" />
        <label for="option2">Option2</label>
      </div>
    </form>
  );
};

/*
<form className={classes.form}>
      <div className="radio">
        <label>
          <input type="radio" value="option1" checked={true} />
          Option 1
        </label>
      </div>
      <div className="radio">
        <label>
          <input type="radio" value="option2" />
          Option 2
        </label>
      </div>
    </form>
*/

export default RadioButtons;
