import { useHistory } from "react-router-dom";
import classes from "./NotValidCookie.module.css";

const NotValidCookie = () => {
  const history = useHistory();

  // If the backend can call the error page as a redirect, this will redirect to the error page (not reload neither state loss)
  const returnButtonHandler = () => {
    history.push("/");
  };

  return (
    <div class={classes.body} id={classes.notfound}>
      <div class={classes.notfound}>
        <div class={classes.notfound404}>
          <h1>
            4<span>0</span>4
          </h1>
        </div>
        <h2>The cookie session expired (try getting a new one).</h2>
        <div className={classes.button}>
          <button onClick={returnButtonHandler}>Volver</button>
        </div>
      </div>
    </div>
  );
};

export default NotValidCookie;
