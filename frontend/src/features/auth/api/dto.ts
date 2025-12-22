export type Role = "admin" | "premium" | "user" | "guest";

export interface UserDTO {
    id: Number;
    username: string;
    role: Role;
    created_at: Date;
    lats_login: Date;
    last_activity: Date;
}

export interface RegisterDTO {
    username: string,
    email: string,
    password: string
}