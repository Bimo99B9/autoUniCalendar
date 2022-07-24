import React, { useContext } from "react";
import classes from "./RadioButtons.module.css";
import SettingsContext from "../../store/settings-context";

const RadioButtons = () => {
  const settingsContext = useContext(SettingsContext);

  const onClickHandler = (event) => {
    if (event.target.name === "epi") {
      settingsContext.check("epi");
      console.log("1");
    } else if (event.target.name === "uo") {
      settingsContext.check("uo");
      console.log("2");
    }
  };

  return (
    <form>
      <div>
        <input type="radio" value="MALE" defaultChecked name="gender" /> Male
        <input type="radio" value="FEMALE" name="gender" /> Female
      </div>
    </form>
  );
};

/*

<div className={classes.form}>
        <input
          type="radio"
          name="uo"
          id="uo"
          value="uo"
          onClick={settingsContext.check("epi")}
          checked={settingsContext.isUO}
        />
        <label htmlFor="uo">University of Oviedo</label>
      </div>
      <div className={classes.form}>
        <input
          type="radio"
          name="epi"
          id="epi"
          value="epi"
          onClick={settingsContext.check("uo")}
          checked={settingsContext.isEPI}
        />
        <label htmlFor="epi">EPI Gijón</label>
      </div>


*/

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
