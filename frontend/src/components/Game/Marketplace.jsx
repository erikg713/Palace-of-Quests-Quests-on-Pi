import React, { useState, useEffect } from 'react';
import { getMarketplaceItems } from '../../api/api';

const Marketplace = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchItems = async () => {
      const { data } = await getMarketplaceItems();
      setItems(data);
    };
    fetchItems();
  }, []);

  return (
    <div>
      <h1>Marketplace</h1>
      {items.map((item) => (
        <div key={item.id}>
          <h3>{item.item_name}</h3>
          <p>Price: {item.price} Pi</p>
          <button>Buy</button>
        </div>
      ))}
    </div>
  );
};

export default Marketplace;
