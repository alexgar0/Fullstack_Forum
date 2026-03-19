import type { BaseEntityDTO, CreatedAtDTO, OwnableDTO, PaginationDTO, ViewsDTO } from "../../common/dto";

export interface SmallTopicDTO extends BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO {
    branch_id: number;
    title: string;
    last_edited_at: Date;
}

export interface TopicDTO extends SmallTopicDTO {
    description: string;
    is_active: boolean;
    replies: ReplyDTO[];
    pagination: PaginationDTO;
}

export interface CreateTopicDTO {
    title: string;
    description: string;
    branch_id: number
}

export interface UpdateTopicDTO {
    description: string;
}

export interface ReplyDTO extends BaseEntityDTO, ViewsDTO, OwnableDTO, CreatedAtDTO {
    content: string;
    topic_id: number;
}

export interface ReplyCreateDTO {
    content: string;
    topic_id: number;
}

