import React, { useState, useEffect, useContext } from "react";

import classes from "./Checkboxes.module.css";
import SettingsContext from "../../store/settings-context";

const Checkboxes = () => {
  const ctx = useContext(SettingsContext);

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
  }, [ctx.university]);

  // useEffect(() => {
  //   setParse({
  //     parse: ctx.epiCheck.parse,
  //     parseDisabled: ctx.epiCheck.parseDisabled,
  //   });
  //   setExperimental({
  //     experimental: ctx.epiCheck.experimental,
  //     experimentalDisabled: ctx.epiCheck.experimentalDisabled,
  //   });
  //   setClassParse({
  //     classParsing: ctx.epiCheck.classParsing,
  //     classParsingDisabled: ctx.epiCheck.classParsingDisabled,
  //   });
  // }, [ctx.epiCheck]);

  // Effect for updating the checkboxes
  useEffect(() => {
    ctx.parseHandler(parse.parse);
    ctx.experimentalHandler(experimental.experimental);
    ctx.classParsingHandler(classParse.classParsing);
  }, [parse.parse, experimental.experimental, classParse.classParsing]);

  const parseHandler = () => {
    setParse((previousState) => ({
      ...previousState,
      parse: !previousState.parse,
    }));
  };

  const experimentalHandler = () => {
    setExperimental((previousState) => ({
      ...previousState,
      experimental: !previousState.experimental,
    }));
  };

  const classParsingHandler = () => {
    setClassParse((previousState) => ({
      ...previousState,
      classParsing: !previousState.classParsing,
    }));
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
