export interface BaseEntityDTO {
    id: number;
}

export interface ViewsDTO {
    view_count: number;
}

export interface OwnableDTO {
    creator_id: number;
    creator_username: string;
}

export interface CreatedAtDTO {
    created_at: Date;
}