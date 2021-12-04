import React from "react";
import PropTypes from "prop-types";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import './ReactNotification.css'

// LIMITED OFFER: $200 BONUS

// Sign up now and get a $200 bonus on your first deposit.

// https://i.ibb.co/Q82zxFt/Screen-Shot-2021-12-04-at-12-59-17-AM.png

const ReactNotificationComponent = ({ title, body, image }) => {
  let hideNotif = title === "";

  const Display = () => {
    return (
      <div className="notif-body">
        <div className="img-container">
          <img src={`${image}`} width="90" height="90" />
        </div>
        <div className="text-container">
           <h4>{title}</h4>
            <p>{body}</p>
        </div>
  
      </div>
    )
  }

  if (!hideNotif) {
    toast(<Display />);
  }

  return (
    <ToastContainer
      autoClose={30000}
      hideProgressBar
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss={false}
      draggable
      pauseOnHover={false}
    />
  );
};

ReactNotificationComponent.defaultProps = {
  title: "This is title",
  body: "Some body",
};

ReactNotificationComponent.propTypes = {
  title: PropTypes.string,
  body: PropTypes.string,
};

export default ReactNotificationComponent;
