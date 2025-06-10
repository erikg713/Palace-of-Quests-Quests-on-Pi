import React, { useState, useCallback } from "react";
import { PiSDK } from "@pi-network/pi-sdk";

const App = () => {
  const [userData, setUserData] = useState(null);
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState("");

  const authenticatePiUser = useCallback(async () => {
    setAuthLoading(true);
    setAuthError("");
    try {
      const authData = await PiSDK.auth({ permissions: ["payments", "username"] });
      setUserData(authData);
    } catch (error) {
      console.error("Pi Authentication Error:", error);
      setAuthError("Authentication failed. Please try again.");
    } finally {
      setAuthLoading(false);
    }
  }, []);

  return (
    <main style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #2d2e6e 0%, #7e54f5 100%)",
      color: "#fff",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "Inter, Segoe UI, Arial, sans-serif"
    }}>
      <h1 style={{
        fontWeight: 700,
        fontSize: "2.5rem",
        marginBottom: "1.5rem",
        letterSpacing: "2px"
      }}>
        Palace of Quests
      </h1>
      {user
