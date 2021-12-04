import "./App.css";

import React, { useState } from "react";
import { onMessageListener } from "./firebaseInit";
import Notifications from "./components/Notifications/Notifications";
import ReactNotificationComponent from "./components/Notifications/ReactNotification";

// https://i.ibb.co/Q82zxFt/Screen-Shot-2021-12-04-at-12-59-17-AM.png

function App() {
  const [show, setShow] = useState(false);
  const [notification, setNotification] = useState({ title: "", body: "" });

  console.log(show, notification);

  onMessageListener()
    .then((payload) => {
      setShow(true);
      setNotification({
        title: payload.notification.title,
        body: payload.notification.body,
        image: payload.notification.image
      });
      console.log(payload);
    })
    .catch((err) => console.log("failed: ", err));

  return (
    <div className="App">
      {show ? (
        <ReactNotificationComponent
          title={notification.title}
          body={notification.body}
          image={notification.image}
        />
      ) : (
        <></>
      )}
      <Notifications />
      <h1>SW-Adblock</h1>
    </div>
  );
}

export default App;
