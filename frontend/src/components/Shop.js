import React, { useState } from "react";
import { authenticateUser, initiatePayment } from "../api/piAPI";

const Shop = () => {
  const [user, setUser] = useState(null);

  const handleSignIn = async () => {
    const authenticatedUser = await authenticateUser();
    if (authenticatedUser) setUser(authenticatedUser);
  };

  const handlePurchase = async () => {
    await initiatePayment(10, "Purchase Sword", { itemId: "sword123" });
  };

  return (
    <div>
      <button onClick={handleSignIn}>Sign In with Pi</button>
      {user && <button onClick={handlePurchase}>Purchase Sword for 10 Pi</button>}
    </div>
  );
};

export default Shop;
