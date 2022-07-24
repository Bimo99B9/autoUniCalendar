import React, { useEffect, useState } from "react";

const SettingsContext = React.createContext({
  isEPI: true,
  isUO: false,
  check: (name) => {},
});

export const SettingsProvider = (props) => {
  const [isEPI, setIsEPI] = useState(true);
  const [isUO, setIsUO] = useState(false);

  const checkHandler = (name) => {
    console.log(name);
    if (name.trim() === "uo") {
      if (isUO === false && isEPI === true) {
        setIsEPI(false);
        setIsUO(true);
      } else if (isUO === true && isEPI === false) {
        setIsEPI(false);
        setIsUO(false);
      } else if (isUO === false && isEPI === false) {
        setIsEPI(true);
        setIsUO(false);
      }
    } else if (name.trim() === "epi") {
      if (isEPI === false && isUO === true) {
        setIsEPI(true);
        setIsUO(false);
      } else if (isEPI === true && isUO === false) {
        setIsEPI(false);
        setIsUO(false);
      } else if (isEPI === false && isUO === false) {
        setIsEPI(true);
        setIsUO(false);
      }
    }
  };

  return (
    <SettingsContext.Provider
      value={{
        isEpi: isEPI,
        isUO: isUO,
        check: checkHandler,
      }}
    >
      {props.children}
    </SettingsContext.Provider>
  );
};

export default SettingsContext;
