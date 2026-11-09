import { api, requireData } from '../../../api/openapi'
import type { BranchCreateDTO, BranchDTO, BranchWithSmallTopicsDTO } from './dto'
import type { PaginationQuery } from '../../../api/query'

export async function create_branch(new_branch: BranchCreateDTO): Promise<BranchDTO> {
  return requireData(await api.POST('/branches/', { body: new_branch, credentials: 'same-origin' }))
}

export async function get_all_branches(): Promise<BranchDTO[]> {
  return requireData(await api.GET('/branches/', { credentials: 'same-origin' }))
}

export async function get_branch(
  branch_id: number,
  pagination?: PaginationQuery,
): Promise<BranchWithSmallTopicsDTO> {
  return requireData(
    await api.GET('/branches/{branch_id}', {
      credentials: 'same-origin',
      params: { path: { branch_id }, query: pagination },
    }),
  )
}
