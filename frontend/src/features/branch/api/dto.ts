export interface BranchDTO {
    id: number;
    title: string;
    description: string | undefined;
    creator_id: number;
    is_active: boolean;
    created_at: Date;
    parent_id: number | undefined;
    children_ids: number[];
    topic_ids: number[];
}

export interface BranchCreateDTO {
    title: string;
    description: string | undefined;
    parent_id: number | undefined;
}