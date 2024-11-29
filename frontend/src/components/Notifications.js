import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

const Notifications = ({ userId }) => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    socket.on(`notification_${userId}`, (data) => {
      setNotifications((prev) => [...prev, data.message]);
    });
    return () => {
      socket.off(`notification_${userId}`);
    };
  }, [userId]);

  return (
    <div className="notifications">
      <h3>Notifications</h3>
      <ul>
        {notifications.map((message, index) => (
          <li key={index}>{message}</li>
        ))}
      </ul>
    </div>
  );
};

export default Notifications;
