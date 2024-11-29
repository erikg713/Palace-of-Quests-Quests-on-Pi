import React, { useState } from "react";
import { authenticateUser } from "../api/piAPI";

const Shop = () => {
  const [user, setUser] = useState(null);

  const handleSignIn = async () => {
    const authenticatedUser = await authenticateUser();
    if (authenticatedUser) setUser(authenticatedUser);
  };

  return (
    <div>
      <button onClick={handleSignIn}>Sign In with Pi</button>
    </div>
  );
};

export default Shop;
