import type { BaseEntityDTO, CreatedAtDTO, OwnableDTO, ViewsDTO } from "../../common/dto";
import type { SmallTopicDTO } from "../../topic/api/dto";

export interface BranchDTO extends BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO {
    title: string;
    description?: string;
    is_active: boolean;
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