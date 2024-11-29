import { useDispatch } from "react-redux";
import { login, logout } from "./authSlice";

function LoginButton() {
  const dispatch = useDispatch();

  const handleLogin = () => {
    dispatch(
      login({
        user: { id: 1, username: "testuser", email: "test@example.com" },
        token: "some.jwt.token",
      })
    );
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <div>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
