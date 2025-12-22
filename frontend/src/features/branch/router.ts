import CreateBranchPage from "./pages/CreateBranchPage.vue"

export const CREATE_BRANCH_PATH = '/branch/create'

export const branch_router = [
    {
        path: CREATE_BRANCH_PATH,
        name: 'create_branch',
        component: CreateBranchPage
    }
]