import BranchDetailPage from "./pages/BranchDetailPage.vue"
import CreateBranchPage from "./pages/CreateBranchPage.vue"

export const CREATE_BRANCH_PATH = '/branch/create'
export const BRANCH_DETAIL_PATH = '/branch/:id'

export const branch_router = [
    {
        path: CREATE_BRANCH_PATH,
        name: 'create_branch',
        component: CreateBranchPage
    },
    {
        path:BRANCH_DETAIL_PATH,
        name: 'branch_detail',
        component: BranchDetailPage

    }
]