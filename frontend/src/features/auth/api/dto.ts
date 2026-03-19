import type { BaseEntityDTO, CreatedAtDTO, ViewsDTO } from "../../common/dto";

export type Role = "admin" | "premium" | "user" | "guest";

export interface UserDTO extends BaseEntityDTO, ViewsDTO, CreatedAtDTO {
    username: string;
    role: Role;
    bio: string;
    lats_login: Date;
    last_activity: Date;
}

export interface RegisterDTO {
    username: string,
    email: string,
    password: string
}