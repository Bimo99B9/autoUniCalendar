import React, { useState } from "react";

const Checkboxes = (props) => {
  const [isChecked, setIsChecked] = useState(false);

  const checkHandler = () => {
    setIsChecked(!isChecked);
  };

  return (
    <div>
      <input
        type="checkbox"
        id="checkbox"
        checked={isChecked}
        onChange={checkHandler}
      />
      <label htmlFor="checkbox">Enable location parsing (EPI Gijón) </label>
    </div>
  );
};

export default Checkboxes;
