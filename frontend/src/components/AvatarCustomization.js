import React, { useState, useEffect } from "react";
import { getAvatar, customizeAvatar } from "../api/avatarAPI";

const AvatarCustomization = () => {
  const [avatar, setAvatar] = useState(null);
  const [customizationOptions, setCustomizationOptions] = useState({
    outfit: "default",
    helmet: "none",
    hairstyle: "default",
    weapon_skin: "standard",
    background_theme: "plain"
  });

  useEffect(() => {
    const fetchAvatar = async () => {
      const data = await getAvatar();
      setAvatar(data);
      setCustomizationOptions({
        outfit: data.outfit,
        helmet: data.helmet,
        hairstyle: data.hairstyle,
        weapon_skin: data.weapon_skin,
        background_theme: data.background_theme
      });
    };
    fetchAvatar();
  }, []);

  const handleCustomization = async (attribute, value) => {
    const updatedAvatar = await customizeAvatar({ [attribute]: value });
    setAvatar(updatedAvatar);
  };

  return (
    <div className="container">
      <h2>Customize Your Avatar</h2>
      <div>
        <label>Outfit:
          <select value={customizationOptions.outfit} onChange={(e) => handleCustomization("outfit", e.target.value)}>
            <option value="default">Default</option>
            <option value="warrior">Warrior</option>
            <option value="mage">Mage</option>
          </select>
        </label>
        <label>Hairstyle:
          <select value={customizationOptions.hairstyle} onChange={(e) => handleCustomization("hairstyle", e.target.value)}>
            <option value="default">Default</option>
            <option value="spiky">Spiky</option>
            <option value="long">Long</option>
          </select>
        </label>
        <label>Weapon Skin:
          <select value={customizationOptions.weapon_skin} onChange={(e) => handleCustomization("weapon_skin", e.target.value)}>
            <option value="standard">Standard</option>
            <option value="flame">Flame</option>
            <option value="ice">Ice</option>
          </select>
        </label>
        <label>Background Theme:
          <select value={customizationOptions.background_theme} onChange={(e) => handleCustomization("background_theme", e.target.value)}>
            <option value="plain">Plain</option>
            <option value="forest">Forest</option>
            <option value="castle">Castle</option>
          </select>
        </label>
      </div>
    </div>
  );
};

export default AvatarCustomization;
