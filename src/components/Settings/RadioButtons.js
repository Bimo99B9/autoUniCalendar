import React, { useContext, useState } from "react";
import classes from "./RadioButtons.module.css";
import SettingsContext from "../../store/settings-context";

const universityList = [
  { value: "uo", label: "University of Oviedo" },
  { value: "epi", label: "EPI Gijón" },
];

const RadioButtons = (props) => {
  // const settingsContext = useContext(SettingsContext);

  // const onClickHandler = (event) => {
  //   if (event.target.name === "epi") {
  //     settingsContext.check("epi");
  //     console.log("1");
  //   } else if (event.target.name === "uo") {
  //     settingsContext.check("uo");
  //     console.log("2");
  //   }
  // };

  const handleChange = (e) => {
    props.onClick(e.target.value);
  };

  return (
    <div>
      {universityList.map((x, i) => (
        <div className={classes.form}>
          <label key={i}>
            <input
              type="radio"
              name="university"
              value={x.value}
              onChange={handleChange}
              defaultChecked={x.value === "epi"}
            />{" "}
            {x.label}
          </label>
        </div>
      ))}
    </div>
  );
};

/*
<form>
      <div>
        <input
          type="radio"
          value="uo"
          checked={settingsContext.university === "uo"}
          onChange={onClickHandler}
          name="uo"
        />{" "}
        University of Oviedo
        <input
          type="radio"
          value="epi"
          checked={settingsContext.university === "epi"}
          onChange={settingsContext.check("epi")}
          name="epi"
        />{" "}
        EPI Gijón
      </div>
    </form>


*/

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
