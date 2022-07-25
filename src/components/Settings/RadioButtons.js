import React from "react";
import classes from "./RadioButtons.module.css";

// Hard-coded list of universities
const universityList = [
  { value: "uo", label: "University of Oviedo", id: "uo" },
  { value: "epi", label: "EPI Gijón", id: "epi" },
];

const RadioButtons = (props) => {
  // Function that updates the university setting state
  const handleChange = (e) => {
    props.onClick(e.target.value);
  };

  // Key should be in the outer component to have access to the whole block
  return (
    <div>
      {universityList.map((x, i) => (
        <div className={classes.form} key={x.id}>
          <label>
            <input
              type="radio"
              name="university"
              value={x.value}
              onChange={handleChange}
              defaultChecked={x.value === props.university}
            />{" "}
            {x.label}
          </label>
        </div>
      ))}
    </div>
  );
};

export default RadioButtons;
