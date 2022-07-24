import React from "react";
import Modal from "../../UI/Modal";
import Options from "./Options";
import classes from "./Settings.module.css";

const Settings = (props) => {
  // Function for updating script settings
  const settingsHandler = () => {
    console.log("CONFIRMACION");
  };

  // Buttons for the modal
  const modalActions = (
    <div className={classes.overall}>
      <Options />
      <div className={classes.buttons}>
        <button className={classes["button--alt"]} onClick={props.onClose}>
          Close
        </button>
        <button className={classes.button} onClick={settingsHandler}>
          Update
        </button>
      </div>
    </div>
  );

  /* 
  
    */

  // Should be the content of the modal like the checkboxs and radio buttons
  const settingsModalContent = <React.Fragment>{modalActions}</React.Fragment>;

  return <Modal onClose={props.onClose}>{settingsModalContent}</Modal>;
};

export default Settings;
