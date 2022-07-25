import React from "react";
import Modal from "../UI/Modal";
import Options from "./Options";
import Saver from "./Saver";
import classes from "./Settings.module.css";
import SettingsContext from "../../store/settings-context";

const Settings = (props) => {
  const ctx = React.useContext(SettingsContext);
  // Function for updating script settings
  const settingsHandler = () => {
    console.log(ctx.university);
    console.log(ctx.saveas);
    console.log("CONFIRMACION");
  };

  return (
    <Modal onClose={props.onClose}>
      <div className={classes.overall}>
        <Saver onSave={ctx.saveNameHandler} />
        <Options onCheck={ctx.check} />
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
