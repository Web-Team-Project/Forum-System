import React from "react";


const UserContext = React.createContext({
    user: {
      username: "",
      userId: "",
      token: "",
      role: "",
    },
    setUser: () => {},
  });
  
  export default UserContext;