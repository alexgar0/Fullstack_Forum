import CreateTopicPage from "./pages/CreateTopicPage.vue"

export const CREATE_TOPIC_PATH = "/topic/create/:id"
export const topic_router = [
    {
        path: CREATE_TOPIC_PATH,
        name: 'create_topic',
        component: CreateTopicPage
    }
]