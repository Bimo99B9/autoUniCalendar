import React, { Fragment } from "react";
import ReactDOM from "react-dom";

import classes from "./Modal.module.css";

// Modal backdrop
const Backdrop = (props) => {
  return <div className={classes.backdrop} onClick={props.onClose} />;
};

// Modal overlay which contains the modal
const ModalOverlay = (props) => {
  return (
    <div className={classes.modal}>
      <div className={classes.content}>{props.children}</div>
    </div>
  );
};

// Get the overlays element from the public/index.html file
const portalElement = document.getElementById("overlays");

// Modal component which contains the backdrop and the modal overlay
const Modal = (props) => {
  return (
    <Fragment>
      {ReactDOM.createPortal(
        <Backdrop onClose={props.onClose} />,
        portalElement
      )}
      {ReactDOM.createPortal(
        <ModalOverlay>{props.children}</ModalOverlay>,
        portalElement
      )}
    </Fragment>
  );
};

export default Modal;
