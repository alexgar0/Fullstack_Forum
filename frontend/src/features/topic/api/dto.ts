import type { BaseEntityDTO, CreatedAtDTO, OwnableDTO, ViewsDTO } from "../../common/dto";

export interface SmallTopicDTO extends BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO {
    branch_id: number;
    title: string;
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

