import React, { useState, useEffect, useContext } from "react";

import classes from "./Checkboxes.module.css";
import SettingsContext from "../../store/settings-context";

const Checkboxes = () => {
  const ctx = useContext(SettingsContext);
  // const [isCheckedParsing, setIsCheckedParsing] = useState(true);
  // const [isCheckedExperimental, setIsCheckedExperimental] = useState(true);
  // const [isClassParsing, setIsClassParsing] = useState(true);

  useEffect(() => {
    if (ctx.university === "uo") {
      ctx.parseHandler(false);
      ctx.experimentalHandler(false);
      ctx.classParsingHandler(true);
    } else if (ctx.university === "epi") {
      ctx.parseHandler(true);
      ctx.experimentalHandler(true);
      ctx.classParsingHandler(true);
    }
  }, [ctx.university]);

  const checkParsingHandler = () => {
    ctx.parseHandler(!ctx.parse);
  };

  const checkExperimentalHandler = () => {
    ctx.experimentalHandler(!ctx.experimental);
  };

  const checkClassParsingHandler = () => {
    ctx.classParsingHandler(!ctx.classParsing);
  };

  return (
    <div className={classes.overall}>
      <div>
        <input
          type="checkbox"
          id="location-parsing"
          checked={ctx.parse}
          onChange={checkParsingHandler}
          disabled={ctx.university === "uo"}
        />
        <label htmlFor="location-parsing">
          Enable location parsing (EPI Gijón)
        </label>
      </div>
      <div>
        <input
          type="checkbox"
          id="experimental-parsing"
          checked={ctx.experimental}
          onChange={checkExperimentalHandler}
          disabled={ctx.university === "uo"}
        />
        <label htmlFor="experimental-parsing">
          Enable experimental location parsing (EPI Gijón)
        </label>
      </div>
      <div>
        <input
          type="checkbox"
          id="class-parsing"
          checked={ctx.classParsing}
          onChange={checkClassParsingHandler}
        />
        <label htmlFor="class-parsing">Enable class type parsing</label>
      </div>
    </div>
  );
};

export default Checkboxes;
