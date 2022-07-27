import React, { createContext, useEffect, useState } from "react";

export const DEFAULT_FILENAME = "Calendario";
export const DEFAULT_UNIVERSITY = "epi";

const SettingsContext = createContext({
  check: (name) => {},
  university: "",
  saveNameHandler: (name) => {},
  saveas: "",
  parse: true,
  experimental: true,
  classParsing: true,
  parseHandler: (state) => {},
  experimentalHandler: (state) => {},
  classParsingHandler: (state) => {},
  update: false,
  updateHandler: (state) => {},
  // isTouched: false,
  // isTouchHandler: (state) => {},
});

export const SettingsProvider = (props) => {
  const [university, setUniversity] = useState("epi");
  const [saveas, setSaveas] = useState("Calendario");
  // States for checkboxes
  // const [isTouched, setIsTouched] = useState(false);
  const [update, setUpdate] = useState(false);
  const [isCheckedParsing, setIsCheckedParsing] = useState(true);
  const [isCheckedExperimental, setIsCheckedExperimental] = useState(true);
  const [isClassParsing, setIsClassParsing] = useState(true);

  // Cambio en estado de checkboxes para intentar hacer un estado por universidad
  const [oviedoCheck, setOviedoCheck] = useState({
    parse: false,
    experimental: false,
    classParsing: true,
    parseDisabled: true,
    experimentalDisabled: true,
    classParsingDisabled: false,
  });

  const [epiCheck, setEpiCheck] = useState({
    parse: true,
    experimental: true,
    classParsing: true,
    parseDisabled: false,
    experimentalDisabled: false,
    classParsingDisabled: false,
  });

  useEffect(() => {
    if (university === "epi") {
      setEpiCheck((existingValues) => ({
        ...existingValues,
        parse: isCheckedParsing,
        parseDisabled: false,
        experimental: isCheckedParsing === true ? isCheckedExperimental : false,
        experimentalDisabled: isCheckedParsing === true ? false : true,
        classParsingDisabled: false,
      }));
    }
    setUpdate(false);
  }, [isCheckedParsing]);

  useEffect(() => {
    console.log("entra");
    if (university === "epi") {
      setEpiCheck((previousState) => ({
        ...previousState,
        experimental: isCheckedParsing === true ? isCheckedExperimental : false,
      }));
    }
    setUpdate(false);
  }, [isCheckedExperimental]);

  useEffect(() => {
    console.log("entra en classParsing");
    if (university === "uo") {
      setOviedoCheck((previousState) => ({
        ...previousState,
        classParsing: isClassParsing,
      }));
    } else {
      setEpiCheck((previousState) => ({
        ...previousState,
        classParsing: isClassParsing,
      }));
    }
    setUpdate(false);
  }, [isClassParsing]);

  const checkHandler = (name) => {
    setUniversity(name);
  };

  const saveNameHandler = (name) => {
    setSaveas(name);
  };

  const parseHandler = (state) => {
    setIsCheckedParsing(state);
  };

  const experimentalHandler = (state) => {
    setIsCheckedExperimental(state);
  };

  const classParsingHandler = (state) => {
    // console.log(state);
    // if (university === "uo") {
    //   setOviedoCheck({
    //     parse: false,
    //     experimental: false,
    //     classParsing: state,
    //     parseDisabled: true,
    //     experimentalDisabled: true,
    //     classParsingDisabled: false,
    //   });
    // } else {
    //   setEpiCheck({
    //     parse: epiCheck.parse,
    //     experimental: epiCheck.experimental,
    //     classParsing: state,
    //     parseDisabled: false,
    //     experimentalDisabled: false,
    //     classParsingDisabled: false,
    //   });
    // }
    setIsClassParsing(state);
  };

  // const isTouchedHandler = (state) => {
  //   setIsTouched(state);
  // };

  const updateHandler = (state) => {
    setUpdate(state);
  };

  return (
    <SettingsContext.Provider
      value={{
        check: checkHandler,
        university: university,
        saveNameHandler: saveNameHandler,
        saveas: saveas,
        // parse: isCheckedParsing,
        // experimental: isCheckedExperimental,
        // classParsing: isClassParsing,
        parseHandler: parseHandler,
        experimentalHandler: experimentalHandler,
        classParsingHandler: classParsingHandler,
        // isTouched: isTouched,
        // isTouchHandler: isTouchedHandler,
        oviedoCheck: oviedoCheck,
        epiCheck: epiCheck,
        update: update,
        updateHandler: updateHandler,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
