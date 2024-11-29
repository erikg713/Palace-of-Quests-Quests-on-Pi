import React, { useState, useEffect } from "react";
import { getInventory, equipItem } from "../api/inventoryAPI";

const Inventory = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchInventory = async () => {
      const data = await getInventory();
      setItems(data);
    };
    fetchInventory();
  }, []);

  const handleEquipItem = async (itemId) => {
    const updatedItems = await equipItem(itemId);
    setItems(updatedItems);
  };

  return (
    <div>
      <h2>Inventory</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <h3>{item.name}</h3>
            <p>{item.description}</p>
            {item.equipped ? (
              <p>Equipped</p>
            ) : (
              <button onClick={() => handleEquipItem(item.id)}>Equip</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Inventory;

import React, { useState, useEffect } from "react";
import { getInventory, equipItem, sellItem } from "../api/inventoryAPI";

const Inventory = () => {
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

  const handleEquipItem = async (itemId) => {
    const updatedItems = await equipItem(itemId);
    setItems(updatedItems);
  };

  const handleSellItem = async (itemId) => {
    const result = await sellItem(itemId);
    setItems(result.items);
    setCurrency(result.currency);
  };

  return (
    <div className="container">
      <h2>Your Inventory</h2>
      <p>Currency: {currency}</p>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <h3>{item.name}</h3>
            <p>{item.description}</p>
            {item.equipped ? (
              <p>Equipped</p>
            ) : (
              <>
                <button onClick={() => handleEquipItem(item.id)}>Equip</button>
                <button onClick={() => handleSellItem(item.id)}>Sell</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Inventory;
