import http from "../../../api/http";
import type { CreateTopicDTO, TopicDTO, UpdateTopicDTO } from "./dto";

export async function create_topic(dto: CreateTopicDTO): Promise<TopicDTO> {
    const response = await http.post<TopicDTO>("/topics/", dto, { withCredentials: true });
    return response.data;
}

export async function get_topic_by_id(id: number): Promise<TopicDTO> {
    const response = await http.get<TopicDTO>(`/topics/${id}`, { withCredentials: true });
    return response.data;
}
export async function update_topic(id: number, dto: UpdateTopicDTO): Promise<TopicDTO> {
    const response = await http.put<TopicDTO>(`/topics/${id}`, dto, { withCredentials: true });
    return response.data;
}