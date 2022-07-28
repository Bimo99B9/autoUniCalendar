import React, { useState, useEffect, useContext } from "react";

import classes from "./Checkboxes.module.css";
import SettingsContext from "../../store/settings-context";

// Component that represents the 3 checkboxes
const Checkboxes = () => {
  // Access the settings context
  const ctx = useContext(SettingsContext);

  // State for the checkboxes
  const [parse, setParse] = useState({ parse: true, parseDisabled: false });
  const [experimental, setExperimental] = useState({
    experimental: true,
    experimentalDisabled: false,
  });
  const [classParse, setClassParse] = useState({
    classParsing: true,
    classParsingDisabled: false,
  });

  // No dependecies as we want the checkboxes to be updated only on first render
  useEffect(() => {
    if (ctx.university === "uo") {
      console.log("entra uo");
      setParse({
        parse: ctx.oviedoCheck.parse,
        parseDisabled: ctx.oviedoCheck.parseDisabled,
      });
      setExperimental({
        experimental: ctx.oviedoCheck.experimental,
        experimentalDisabled: ctx.oviedoCheck.experimentalDisabled,
      });
      setClassParse({
        classParsing: ctx.oviedoCheck.classParsing,
        classParsingDisabled: ctx.oviedoCheck.classParsingDisabled,
      });
    } else if (ctx.university === "epi") {
      console.log("entra epi");
      setParse({
        parse: ctx.epiCheck.parse,
        parseDisabled: ctx.epiCheck.parseDisabled,
      });
      setExperimental({
        experimental: ctx.epiCheck.experimental,
        experimentalDisabled: ctx.epiCheck.experimentalDisabled,
      });
      setClassParse({
        classParsing: ctx.epiCheck.classParsing,
        classParsingDisabled: ctx.epiCheck.classParsingDisabled,
      });
    }
  }, [ctx.university, ctx.update]);

  // Effect for updating the checkboxes
  useEffect(() => {
    ctx.parseHandler(parse.parse);
    ctx.experimentalHandler(experimental.experimental);
    ctx.classParsingHandler(classParse.classParsing);
  }, [parse.parse, experimental.experimental, classParse.classParsing]);

  // Function that handles the checkbox change (parse or location)
  const parseHandler = () => {
    setParse((previousState) => ({
      ...previousState,
      parse: !previousState.parse,
    }));
    ctx.updateHandler(true);
  };

  // Function that handles the checkbox change (experimental or experimental-location)
  const experimentalHandler = () => {
    setExperimental((previousState) => ({
      ...previousState,
      experimental: !previousState.experimental,
    }));
    ctx.updateHandler(true);
  };

  // Function that handles the checkbox change (class-type or class-type)
  const classParsingHandler = () => {
    setClassParse((previousState) => ({
      ...previousState,
      classParsing: !previousState.classParsing,
    }));
    ctx.updateHandler(true);
  };

  return (
    <div className={classes.overall}>
      <div>
        <input
          type="checkbox"
          id="location-parsing"
          checked={parse.parse}
          onChange={parseHandler}
          disabled={parse.parseDisabled}
        />
        <label htmlFor="location-parsing">
          Enable location parsing (EPI Gijón)
        </label>
      </div>
      <div>
        <input
          type="checkbox"
          id="experimental-parsing"
          checked={experimental.experimental}
          onChange={experimentalHandler}
          disabled={experimental.experimentalDisabled}
        />
        <label htmlFor="experimental-parsing">
          Enable experimental location parsing (EPI Gijón)
        </label>
      </div>
      <div>
        <input
          type="checkbox"
          id="class-parsing"
          checked={classParse.classParsing}
          onChange={classParsingHandler}
        />
        <label htmlFor="class-parsing">Enable class type parsing</label>
      </div>
    </div>
  );
};

export default Checkboxes;
