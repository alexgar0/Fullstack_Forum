export interface Topic {
    id: number;
    branch_id: number;
    title: string;
    description: string;
    creator_id: number;
    is_active: boolean;
    created_at: string;
    last_edited_at: string;
};

export interface CreateTopicDto {
    title: string;
    description: string;
}

export interface UpdateTopicDto {
    description: string;
}

