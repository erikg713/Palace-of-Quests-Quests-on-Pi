import { useSelector } from "react-redux";

function UserProfile() {
  const user = useSelector((state) => state.auth.user);

  return <div>{user ? `Hello, ${user.username}` : "Not logged in"}</div>;
}
