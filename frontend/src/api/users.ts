import http from "./http";

export async function login(username: string, password: string) {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);

    const response = await http.post(
        "/users/login", 
        body,
        {
            withCredentials: true,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
    );

    return response.data;
}