import { api, requireData } from '../../../api/openapi'
import type { CreateTopicDTO, ReplyCreateDTO, ReplyDTO, TopicDTO, UpdateTopicDTO } from './dto'

export async function create_topic(dto: CreateTopicDTO): Promise<TopicDTO> {
  return requireData(await api.POST('/topics/', { body: dto }))
}

export async function get_topic_by_id(
  id: number,
  offset: number = 0,
  limit: number = 10,
): Promise<TopicDTO> {
  return requireData(
    await api.GET('/topics/{topic_id}', {
      params: {
        path: { topic_id: id },
        query: { offset, limit },
      },
    }),
  )
}

export async function update_topic(id: number, dto: UpdateTopicDTO): Promise<TopicDTO> {
  return requireData(
    await api.PUT('/topics/{topic_id}', {
      params: { path: { topic_id: id } },
      body: dto,
    }),
  )
}

export async function create_reply(dto: ReplyCreateDTO): Promise<ReplyDTO> {
  return requireData(await api.PUT('/replies/', { body: dto }))
}
