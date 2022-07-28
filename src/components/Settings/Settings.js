import React from "react";
import Modal from "../UI/Modal";
import Options from "./Options";
import Saver from "./Saver";
import classes from "./Settings.module.css";
import SettingsContext from "../../store/settings-context";

// Settings component which contains the modal and the options
const Settings = (props) => {
  // Context to access the settings state
  const ctx = React.useContext(SettingsContext);

  return (
    <Modal onClose={props.onClose}>
      <div className={classes.overall}>
        <Saver onSave={ctx.saveNameHandler} />
        <Options onCheck={ctx.check} university={ctx.university} />
        <div className={classes.buttons}>
          <button className={classes["button--alt"]} onClick={props.onClose}>
            Close
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default Settings;
