import { Outlet } from "react-router-dom";
import { useState } from "react";


const LayoutApp = () => {
    const [loggedIn, setLoggedIn] = useState(false);

    return <>
        <Outlet context={{ loggedIn, setLoggedIn }} />
    </>
}

export default LayoutApp