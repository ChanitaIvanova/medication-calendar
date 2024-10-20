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
import NewTimesheet from './components/timesheet/NewTimesheet';
import TimesheetList from './components/timesheet/TimesheetList'; // Add this import
import TimesheetCalendar from './components/timesheet/TimesheetCalendar'; // Add this import
import EditTimesheet from './components/timesheet/EditTimesheet'; // Add this import

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
            },
            {
                path: "profile",
                element: <Profile />,
            },
            {
                path: "medications",
                element: <MedicationList />,
            },
            {
                path: "new-medication",
                element: <Medication />,
            },
            {
                path: "medications/:id",
                element: <MedicationView />,
            },
            {
                path: "edit-medication/:id",
                element: <EditMedication />,
            },
            {
                path: "new-timesheet",
                element: <NewTimesheet />,
            },
            {
                path: "timesheets",
                element: <TimesheetList />,
            },
            {
                path: "timesheet/:id",
                element: <TimesheetCalendar />,
            },
            {
                path: "edit-timesheet/:id",
                element: <EditTimesheet />,
            },
        ],
    }
]);

export default routes;
