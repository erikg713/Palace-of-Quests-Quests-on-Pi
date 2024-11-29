// components/Game/Shop.js
import React from 'react';

const Shop = () => {
  return (
    <div>
      <h2>Shop</h2>
      <ul>
        <li>
          <span>Upgrade 1</span> - 10 Pi
          <button>Buy</button>
        </li>
        <li>
          <span>Upgrade 2</span> - 15 Pi
          <button>Buy</button>
        </li>
      </ul>
    </div>
  );
};

export default Shop;
import React, { useState, useEffect } from 'react';
import { getShopItems, purchaseItem } from '../../services/api';

const Shop = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItems = async () => {
      const itemsData = await getShopItems();
      setItems(itemsData);
      setLoading(false);
    };

    fetchItems();
  }, []);

  const handlePurchase = async (itemId) => {
    try {
      await purchaseItem(itemId);
      alert('Item purchased successfully!');
    } catch (error) {
      alert('Purchase failed! Please try again.');
    }
  };

  if (loading) {
    return <div>Loading items...</div>;
  }

  return (
    <div className="shop">
      <h2>Shop</h2>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <h3>{item.name}</h3>
            <p>{item.price} Pi</p>
            <button onClick={() => handlePurchase(item.id)}>Buy</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Shop;