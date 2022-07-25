import React, { createContext, useState } from "react";

const SettingsContext = createContext({
  check: (name) => {},
  university: "",
  saveNameHandler: (name) => {},
  saveas: "",
});

export const SettingsProvider = (props) => {
  const [university, setUniversity] = useState("epi");
  const [saveas, setSaveas] = useState("Calendario");

  const checkHandler = (name) => {
    setUniversity(name);
    console.log(name);
  };

  const saveNameHandler = (name) => {
    setSaveas(name);
    console.log(name);
  };

  return (
    <SettingsContext.Provider
      value={{
        check: checkHandler,
        university: university,
        saveNameHandler: saveNameHandler,
        saveas: saveas,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
