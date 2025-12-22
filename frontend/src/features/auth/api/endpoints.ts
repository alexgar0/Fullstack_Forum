import http from "../../../api/http";
import type { RegisterDTO, UserDTO } from "./dto";


export async function login(username: string, password: string) {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);

    const response = await http.post(
        "/users/login",
        body,
        {
            // withCredentials: true,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
    );
    return response.data;
}


export async function register(username: string, email: string, password: string, password_check: string) {
    if (password != password_check) {
        throw new Error("Passwords don't match");
    }

    const body: RegisterDTO = {
        username: username,
        email: email,
        password: password
    };
    const response = await http.post(
        "/users/register",
        body,
    );

    return response.data;
}


export async function me() : Promise<UserDTO> {
    const response = await http.get<UserDTO>('/users/me');
    return response.data
}

export async function logout() {
    await http.post('/users/logout');
}