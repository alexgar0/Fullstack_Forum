import type { SmallTopicDTO } from "../../topic/api/dto";

export interface BranchDTO {
    id: number;
    title: string;
    description?: string;
    creator_id: number;
    is_active: boolean;
    created_at: Date;
    parent_id?: number;
    topic_count: number;
    children_ids: number[];
    topic_ids: number[];
}

export interface BranchWithSmallTopicsDTO extends BranchDTO {
    small_topics: SmallTopicDTO[];
}

export interface BranchCreateDTO {
    title: string;
    description?: string;
    parent_id?: number;
}