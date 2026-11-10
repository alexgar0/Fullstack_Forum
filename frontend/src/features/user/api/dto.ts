import type { paths } from '../../../api/schema.generated'

export type UserTopicsDTO =
  paths['/users/{user_id}/topics/']['get']['responses'][200]['content']['application/json']
