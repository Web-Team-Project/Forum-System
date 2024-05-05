import React from "react";


const UserContext = React.createContext({
	user: {
		username: "",
		userId: "",
		token: "",
	},
});

export default UserContext;