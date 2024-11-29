import React, { useState, useEffect } from "react";
import { getInventory, upgradeItem } from "../api/inventoryAPI";

const InventoryUpgrades = () => {
  const [items, setItems] = useState([]);
  const [currency, setCurrency] = useState(0);

  useEffect(() => {
    const fetchInventory = async () => {
      const data = await getInventory();
      setItems(data.items);
      setCurrency(data.currency);
    };
    fetchInventory();
  }, []);

  const handleUpgradeItem = async (itemId) => {
    const result = await upgradeItem(itemId);
    if (result.error) {
      alert(result.error);
    } else {
      setItems(result.items);
      setCurrency(result.currency);
    }
  };

  return (
    <div className="container">
      <h2>Upgrade Your Items</h2>
      <p>Currency: {currency}</p>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <h3>{item.name}</h3>
            <p>Level: {item.upgrade_level}</p>
            <p>Rarity: {item.rarity}</p>
            <button onClick={() => handleUpgradeItem(item.id)}>Upgrade (Cost: {item.upgrade_level * 10})</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default InventoryUpgrades;
