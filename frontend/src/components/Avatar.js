import React, { useState, useEffect } from "react";
import { getAvatar, customizeAvatar } from "../api/avatarAPI";

const Avatar = () => {
  const [avatar, setAvatar] = useState(null);

  useEffect(() => {
    const fetchAvatar = async () => {
      const data = await getAvatar();
      setAvatar(data);
    };
    fetchAvatar();
  }, []);

  const handleCustomization = async (attribute, value) => {
    const updatedAvatar = await customizeAvatar(attribute, value);
    setAvatar(updatedAvatar);
  };

  return (
    <div className="container">
      <h2>{avatar?.name}'s Avatar</h2>
      <p>Level: {avatar?.level}</p>
      <div>
        <label>
          Outfit:
          <select onChange={(e) => handleCustomization("outfit", e.target.value)}>
            <option value="default">Default</option>
            <option value="warrior">Warrior</option>
            <option value="mage">Mage</option>
          </select>
        </label>
        <label>
          Helmet:
          <select onChange={(e) => handleCustomization("helmet", e.target.value)}>
            <option value="none">None</option>
            <option value="iron_helmet">Iron Helmet</option>
            <option value="golden_helmet">Golden Helmet</option>
          </select>
        </label>
      </div>
    </div>
  );
};

export default Avatar;
