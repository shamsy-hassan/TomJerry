// =======================================================
// File: AuthContext.jsx
// Description: Provides global authentication state and
//               functions (login, logout, register) to
//               all components across the app.
// =======================================================

import React, { createContext, useState, useEffect } from "react";
import { getToken, setToken, removeToken } from "../utils/api"; // helper to handle tokens

// -------------------------------------------------------
// 1️⃣ Create Auth Context
// -------------------------------------------------------
export const AuthContext = createContext();

// -------------------------------------------------------
// 2️⃣ Create Auth Provider Component
// -------------------------------------------------------
export const AuthProvider = ({ children }) => {
  // Store the authenticated user and token
  const [user, setUser] = useState(null);
  const [token, setAuthToken] = useState(getToken());
  const [loading, setLoading] = useState(true);

  // -----------------------------------------------------
  // 3️⃣ On App Mount — check if user already logged in
  // -----------------------------------------------------
  useEffect(() => {
    const savedToken = getToken();
    if (savedToken) {
      setAuthToken(savedToken);
      // Fetch user data from backend (optional)
      fetchUserData(savedToken);
    } else {
      setLoading(false);
    }
  }, []);

  // -----------------------------------------------------
  // 4️⃣ Fetch User Info using Token (optional)
  // -----------------------------------------------------
  const fetchUserData = async (token) => {
    try {
      const res = await fetch("http://localhost:5000/api/player/profile", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      }
    } catch (error) {
      console.error("❌ Failed to fetch user data:", error);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------------------------------
  // 5️⃣ Handle Login
  // -----------------------------------------------------
  const login = async (email, password) => {
    try {
      const res = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (res.ok && data.access_token) {
        setToken(data.access_token);
        setAuthToken(data.access_token);
        fetchUserData(data.access_token);
        return true;
      } else {
        alert(data.message || "Login failed");
        return false;
      }
    } catch (error) {
      console.error("❌ Login error:", error);
      return false;
    }
  };

  // -----------------------------------------------------
  // 6️⃣ Handle Logout
  // -----------------------------------------------------
  const logout = () => {
    removeToken();
    setAuthToken(null);
    setUser(null);
  };

  // -----------------------------------------------------
  // 7️⃣ Provide Context Values to the App
  // -----------------------------------------------------
  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        loading,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
