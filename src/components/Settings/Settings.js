import React from "react";
import Modal from "../UI/Modal";
import Options from "./Options";
import classes from "./Settings.module.css";

const Settings = (props) => {
  // Function for updating script settings
  const settingsHandler = () => {
    console.log("CONFIRMACION");
  };

  return (
    <Modal onClose={props.onClose}>
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
    </Modal>
  );
};

export default Settings;
