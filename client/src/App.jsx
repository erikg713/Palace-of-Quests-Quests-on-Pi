// frontend/src/App.js
import React, { useState } from "react";
import { PiSDK } from "@pi-network/pi-sdk";  // Install Pi SDK

const App = () => {
  const [userData, setUserData] = useState(null);
  
  const authenticatePiUser = async () => {
    try {
      const authData = await PiSDK.auth({ permissions: ["payments", "username"] });
      setUserData(authData);
    } catch (error) {
      console.error("Pi Authentication Error:", error);
    }
  };

  return (
    <div>
      <h1>WELCOME TO PALACE OF QUESTS!!!!</h1>
      {userData ? (
        <div>
          <h2>Welcome, {userData.username}!</h2>
          <p>Pi Address: {userData.wallet_address}</p>
        </div>
      ) : (
        <button onClick={authenticatePiUser}>Login with Pi Network</button>
      )}
    </div>
  );
};

export default App;
