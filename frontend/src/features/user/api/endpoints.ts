import { api, requireData } from '../../../api/openapi'
import type { UserTopicsDTO } from './dto'

export async function get_user_topics(
  user_id: number,
  offset = 0,
  limit = 10,
): Promise<UserTopicsDTO> {
  return requireData(
    await api.GET('/users/{user_id}/topics/', {
      params: { path: { user_id }, query: { offset, limit } },
    }),
  )
}
