import CreateTopicPage from "./pages/CreateTopicPage.vue"
import ViewTopicPage from "./pages/ViewTopicPage.vue"

export const CREATE_TOPIC_PATH = "/topic/create/:id"
export const VIEW_TOPIC_PATH = "/topic/:id"
export const topic_router = [
    {
        path: CREATE_TOPIC_PATH,
        name: 'topic_create',
        component: CreateTopicPage
    },
    {
        path: VIEW_TOPIC_PATH,
        name: 'topic_view',
        component: ViewTopicPage
    }
]