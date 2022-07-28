import React, { useState } from "react";

import Form from "./components/Form/Form";
import Settings from "./components/Settings/Settings";
import classes from "./App.module.css";

function App() {
  // State for the modal window to be open or closed
  const [showSettings, setShowSettings] = useState(false);

  // Function to toggle (show) the modal window
  const showSettingsHandler = () => {
    setShowSettings(true);
  };

  // Function to toggle (hide) the modal window
  const hideSettingsHandler = () => {
    setShowSettings(false);
  };

  return (
    <div className={classes.app}>
      {showSettings && <Settings onClose={hideSettingsHandler} />}
      <main>
        <Form onShowSettings={showSettingsHandler} />
      </main>
    </div>
  );
}

export default App;
