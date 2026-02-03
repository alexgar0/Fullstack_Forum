export interface SmallTopicDTO {
    id: number;
    branch_id: number;
    title: string;
    creator_id: number;
    creator_username: string;
    created_at: string;
    last_edited_at: string;
}

export interface TopicDTO extends SmallTopicDTO {
    description: string;
    is_active: boolean;
}

export interface CreateTopicDTO {
    title: string;
    description: string;
    branch_id: number
}

export interface UpdateTopicDTO {
    description: string;
}

