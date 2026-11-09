import UserProfilePage from './pages/UserProfilePage.vue'

export const user_router = [
  {
    path: '/users/:id',
    name: 'user_profile',
    component: UserProfilePage,
  },
]
