import { useState } from "react";

import Form from "./components/Form/Form";
import Settings from "./components/Settings/Settings";
import classes from "./App.module.css";

function App() {
  const [showSettings, setShowSettings] = useState(false);

  const showSettingsHandler = () => {
    setShowSettings(true);
  };

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
