import http from "../../../api/http";
import type { CreateTopicDto, Topic, UpdateTopicDto } from "./types";

export const createTopic = (dto: CreateTopicDto) =>
    http.post<Topic>("/topics", dto, { withCredentials: true });

export const getTopicById = (id: number) =>
    http.get<Topic>(`/topics/${id}`, { withCredentials: true });

export const updateTopic = (id: number, dto: UpdateTopicDto) =>
    http.put<Topic>(`/topics/${id}`, dto, { withCredentials: true });