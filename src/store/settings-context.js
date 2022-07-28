import React, { createContext, useEffect, useState } from "react";

// Default values for the context
export const DEFAULT_FILENAME = "Calendario";
export const DEFAULT_UNIVERSITY = "epi";

// Context for the settings of the app (better autocomplete)
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
});

export const SettingsProvider = (props) => {
  const [university, setUniversity] = useState("epi"); // State for the university
  const [saveas, setSaveas] = useState("Calendario"); // State for the filename

  // States for checkboxes
  const [update, setUpdate] = useState(false);
  const [isCheckedParsing, setIsCheckedParsing] = useState(true);
  const [isCheckedExperimental, setIsCheckedExperimental] = useState(true);
  const [isClassParsing, setIsClassParsing] = useState(true);

  // More general states which are used in the form to save the settings
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

  // useEffect hooks to update the states of the checkboxes
  useEffect(() => {
    if (university === "epi") {
      setEpiCheck((existingValues) => ({
        ...existingValues,
        parse: isCheckedParsing,
        parseDisabled: false,
        experimental: isCheckedParsing === true ? true : false,
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

  // Function to set the university state
  const checkHandler = (name) => {
    setUniversity(name);
  };

  // Function to set the filename state
  const saveNameHandler = (name) => {
    setSaveas(name);
  };

  // Functions to set the checkboxes state
  const parseHandler = (state) => {
    setIsCheckedParsing(state);
  };
  const experimentalHandler = (state) => {
    setIsCheckedExperimental(state);
  };
  const classParsingHandler = (state) => {
    setIsClassParsing(state);
  };

  // Function to set the update state
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
        parseHandler: parseHandler,
        experimentalHandler: experimentalHandler,
        classParsingHandler: classParsingHandler,
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
