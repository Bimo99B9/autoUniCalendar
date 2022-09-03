import { parse } from "nth-check";
import React, { createContext, useEffect, useState } from "react";

// Default values for the context
export const DEFAULT_FILENAME = "Calendario";
export const DEFAULT_UNIVERSITY = "epi";

// Context for the settings of the app (better autocomplete)
const SettingsContext = createContext({
  
  saveNameHandler: (name) => {},
  saveas: "",
  parse: true,
  parseHandler: (state) => {},
  classParsing: true,
  classParsingHandler: (state) => {},
  update: false,
  updateHandler: (state) => {},
  extension: ".ics",
  extensionHandler: (extension) => {},
});

export const SettingsProvider = (props) => {
  const [saveas, setSaveas] = useState("Calendario"); // State for the filename

  // States for checkboxes
  const [update, setUpdate] = useState(false);
  const [isCheckedParsing, setIsCheckedParsing] = useState(true);
  const [isClassParsing, setIsClassParsing] = useState(true);

  // State for the extension of the file
  const [extension, setExtension] = useState(".ics");

  // More general states which are used in the form to save the settings
  // const [oviedoCheck, setOviedoCheck] = useState({
  //   parse: false,
  //   classParsing: true,
  //   parseDisabled: true,
  //   classParsingDisabled: false,
  // });
  // const [epiCheck, setEpiCheck] = useState({
  //   parse: true,
  //   classParsing: true,
  //   parseDisabled: false,
  //   classParsingDisabled: false,
  // });

  // useEffect hooks to update the states of the checkboxes
  // useEffect(() => {
  //   if (university === "epi") {
  //     setEpiCheck((existingValues) => ({
  //       ...existingValues,
  //       parse: isCheckedParsing,
  //       parseDisabled: false,
  //       classParsingDisabled: false,
  //     }));
  //   }
  //   setUpdate(false);
  // }, [isCheckedParsing]);
  // useEffect(() => {
  //   if (university === "uo") {
  //     setOviedoCheck((previousState) => ({
  //       ...previousState,
  //       classParsing: isClassParsing,
  //     }));
  //   } else {
  //     setEpiCheck((previousState) => ({
  //       ...previousState,
  //       classParsing: isClassParsing,
  //     }));
  //   }
  //   setUpdate(false);
  // }, [isClassParsing]);

  // Function to set the filename state
  const saveNameHandler = (name) => {
    setSaveas(name);
  };

  // Functions to set the checkboxes state
  const parseHandler = (state) => {
    setIsCheckedParsing(state);
  };
  const classParsingHandler = (state) => {
    setIsClassParsing(state);
  };

  // Function to set the update state
  const updateHandler = (state) => {
    setUpdate(state);
  };

  // Function to set the extension state
  const extensionHandler = (extension) => {
    setExtension(extension);
  };

  return (
    <SettingsContext.Provider
      value={{
        // check: checkHandler,
        saveNameHandler: saveNameHandler,
        saveas: saveas,
        parseHandler: parseHandler,
        parse: isCheckedParsing,
        classParsing: isClassParsing,
        classParsingHandler: classParsingHandler,
        update: update,
        updateHandler: updateHandler,
        extension: extension,
        extensionHandler: extensionHandler,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
