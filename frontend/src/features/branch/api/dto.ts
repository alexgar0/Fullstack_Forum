export interface BranchDTO {
    id: number;
    title: string;
    description?: string;
    creator_id: number;
    is_active: boolean;
    created_at: Date;
    parent_id?: number;
    children_ids: number[];
    topic_ids: number[];
}

export interface BranchCreateDTO {
    title: string;
    description?: string ;
    parent_id?: number;
}