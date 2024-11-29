import { useState, useEffect } from "react";

const useAuth = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem("authToken");
            if (token) {
                // Simulate API call to fetch user details
                const userDetails = await fetch("/api/user", {
                    headers: { Authorization: `Bearer ${token}` },
                }).then((res) => res.json());
                setUser(userDetails);
            }
        };
        fetchUser();
    }, []);

    return user;
};

export default useAuth;
