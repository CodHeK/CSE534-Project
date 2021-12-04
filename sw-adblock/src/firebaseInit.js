import firebase from "firebase/app";
import "firebase/messaging";

const firebaseConfig = {
  apiKey: "AIzaSyAjOJcUwx91cV7GwQGr3C22TPfKVW6Oo_8",
  authDomain: "sw-adblock.firebaseapp.com",
  projectId: "sw-adblock",
  storageBucket: "sw-adblock.appspot.com",
  messagingSenderId: "514398755626",
  appId: "1:514398755626:web:bab8eecd2618ef85f09c53"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

const { REACT_APP_VAPID_KEY } = process.env;
const publicKey = REACT_APP_VAPID_KEY;

export const getToken = async (setTokenFound) => {
  let currentToken = "";

  try {
    currentToken = await messaging.getToken({ vapidKey: publicKey });
    if (currentToken) {
      setTokenFound(true);
    } else {
      setTokenFound(false);
    }
  } catch (error) {
    console.log("An error occurred while retrieving token. ", error);
  }

  return currentToken;
};

export const onMessageListener = () =>
  new Promise((resolve) => {
    messaging.onMessage((payload) => {
      resolve(payload);
    });
  });
