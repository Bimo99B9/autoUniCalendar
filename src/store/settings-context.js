import React, { createContext, useState } from "react";

const SettingsContext = createContext({
  check: (name) => {},
  university: "",
});

export const SettingsProvider = (props) => {
  const [university, setUniversity] = useState("epi");

  const checkHandler = (name) => {
    setUniversity(name);
    console.log(name);
  };

  return (
    <SettingsContext.Provider
      value={{
        check: checkHandler,
        university: university,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
