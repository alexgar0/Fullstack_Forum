import http from '../../../api/http'
import type { components } from '../../../api/schema.generated'
// import type { CreateTopicDTO, ReplyCreateDTO, ReplyDTO, TopicDTO, UpdateTopicDTO } from './dto'

type TopicCreateDTO = components['schemas']['TopicCreateDTO']
type FullTopicDTO = components['schemas']['FullTopicDTO']
type TopicUpdateDTO = components['schemas']['TopicUpdateDTO']
type ReplyCreateDTO = components['schemas']['ReplyCreateDTO']
type ReplyDTO = components['schemas']['ReplyDTO']

export async function create_topic(dto: TopicCreateDTO): Promise<FullTopicDTO> {
  const response = await http.post<FullTopicDTO>('/topics/', dto, { withCredentials: true })
  return response.data
}

export async function get_topic_by_id(
  id: number,
  offset: number = 0,
  limit: number = 10,
): Promise<FullTopicDTO> {
  const response = await http.get<FullTopicDTO>(`/topics/${id}`, {
    params: {
      offset,
      limit,
    },
    withCredentials: true,
  })
  return response.data
}

export async function update_topic(id: number, dto: TopicUpdateDTO): Promise<FullTopicDTO> {
  const response = await http.put<FullTopicDTO>(`/topics/${id}`, dto, { withCredentials: true })
  return response.data
}

export async function create_reply(dto: ReplyCreateDTO): Promise<ReplyDTO> {
  const response = await http.put<ReplyDTO>(`/replies/`, dto, { withCredentials: true })
  return response.data
}
