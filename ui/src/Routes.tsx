import {
    createBrowserRouter,
} from "react-router-dom";
import Login from './components/login/Login';
import SignUp from './components/sign-up/SignUp';
import App from './App';

const routes = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                path: "login",
                element: <Login />,
            },
            {
                path: "sign-up",
                element: <SignUp />,
            }
        ],
    }
]);

export default routes;