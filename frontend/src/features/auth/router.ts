import CompleteRegistration from "./pages/CompleteRegistration.vue";
import LoginPage from "./pages/LoginPage.vue";
import RegistrationPage from "./pages/RegistrationPage.vue";

export const LOGIN_PATH = '/login';
export const REGISTER_PATH = '/register';
export const COMPLETE_REGISTRATION_PATH = '/complete_registration';

const auth_router = [{
    path: LOGIN_PATH,
    name: 'login',
    component: LoginPage,
},
{
    path: REGISTER_PATH,
    name: 'register',
    component: RegistrationPage
},
{
    path: COMPLETE_REGISTRATION_PATH,
    name: "complete_registration",
    component: CompleteRegistration
}
];

export default auth_router;