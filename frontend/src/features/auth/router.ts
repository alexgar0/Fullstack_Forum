import CompleteRegistration from "./pages/CompleteRegistration.vue";
import LoginPage from "./pages/LoginPage.vue";
import RegistrationPage from "./pages/RegistrationPage.vue";

const auth_router = [{
    path: '/login',
    name: 'login',
    component: LoginPage,
},
{
    path: '/register',
    name: 'register',
    component: RegistrationPage
},
{
    path: '/complete_registration',
    name: "complete_registration",
    component: CompleteRegistration
}
];

export default auth_router;