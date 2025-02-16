import {
    createBrowserRouter,
} from "react-router-dom";
import Login from './components/login/Login';
import SignUp from './components/sign-up/SignUp';
import Profile from './components/profile/Profile';
import App from './App';
import Medication from './components/medication/Medication';
import MedicationList from './components/medication/MedicationList';
import MedicationView from './components/medication/MedicationView';
import EditMedication from './components/medication/EditMedication';
import Timesheet from './components/timesheet/Timesheet';
import Home from './components/home/Home';
import ProtectedRoute from './components/common/ProtectedRoute';

const routes = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                path: "",
                element: <Home />,
            },
            {
                path: "login",
                element: <Login />,
            },
            {
                path: "sign-up",
                element: <SignUp />,
            },
            {
                path: "profile",
                element: <ProtectedRoute allowedRoles={['admin', 'user']}><Profile /></ProtectedRoute>,
            },
            {
                path: "medications",
                element: <ProtectedRoute allowedRoles={['admin']}><MedicationList /></ProtectedRoute>,
            },
            {
                path: "new-medication",
                element: <ProtectedRoute allowedRoles={['admin']}><Medication /></ProtectedRoute>,
            },
            {
                path: "medications/:id",
                element: <ProtectedRoute allowedRoles={['admin']}><MedicationView /></ProtectedRoute>,
            },
            {
                path: "edit-medication/:id",
                element: <ProtectedRoute allowedRoles={['admin']}><EditMedication /></ProtectedRoute>,
            },
            {
                path: "timesheet",
                element: <ProtectedRoute allowedRoles={['user']}><Timesheet /></ProtectedRoute>,
            }
        ],
    }
]);

export default routes;
