import React, { createContext, useState } from "react";

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
});

export const SettingsProvider = (props) => {
  const [university, setUniversity] = useState("epi");
  const [saveas, setSaveas] = useState("Calendario");
  // States for checkboxes
  const [isCheckedParsing, setIsCheckedParsing] = useState(true);
  const [isCheckedExperimental, setIsCheckedExperimental] = useState(true);
  const [isClassParsing, setIsClassParsing] = useState(true);

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
    setIsClassParsing(state);
  };

  return (
    <SettingsContext.Provider
      value={{
        check: checkHandler,
        university: university,
        saveNameHandler: saveNameHandler,
        saveas: saveas,
        parse: isCheckedParsing,
        experimental: isCheckedExperimental,
        classParsing: isClassParsing,
        parseHandler: parseHandler,
        experimentalHandler: experimentalHandler,
        classParsingHandler: classParsingHandler,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
