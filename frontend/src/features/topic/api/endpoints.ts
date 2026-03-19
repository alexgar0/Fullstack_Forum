import http from "../../../api/http";
import type { CreateTopicDTO, ReplyCreateDTO, ReplyDTO, TopicDTO, UpdateTopicDTO } from "./dto";

export async function create_topic(dto: CreateTopicDTO): Promise<TopicDTO> {
    const response = await http.post<TopicDTO>("/topics/", dto, { withCredentials: true });
    return response.data;
}

export async function get_topic_by_id(id: number, offset: number = 0, limit: number = 10): Promise<TopicDTO> {
    const response = await http.get<TopicDTO>(`/topics/${id}`, {
        params: {
            offset,
            limit
        },
        withCredentials: true 
    });
    return response.data;
}

export async function update_topic(id: number, dto: UpdateTopicDTO): Promise<TopicDTO> {
    const response = await http.put<TopicDTO>(`/topics/${id}`, dto, { withCredentials: true });
    return response.data;
}

export async function create_reply(dto: ReplyCreateDTO): Promise<ReplyDTO> {
    const response = await http.put<ReplyDTO>(`/replies/`, dto, { withCredentials: true });
    return response.data;
}