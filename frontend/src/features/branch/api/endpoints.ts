import http from '../../../api/http'
import type { components } from '../../../api/schema.generated'
import type { PaginationQuery } from '../../../api/query'

type BranchCreateDTO = components['schemas']['BranchCreateDTO']
type BranchDTO = components['schemas']['BranchDTO']
type BranchWithSmallTopicsDTO = components['schemas']['BranchWithSmallTopicsDTO']

export async function create_branch(new_branch: BranchCreateDTO): Promise<BranchDTO> {
  const response = await http.post<BranchDTO>('/branches/', new_branch)
  return response.data
}

export async function get_all_branches(): Promise<BranchDTO[]> {
  const response = await http.get<BranchDTO[]>('/branches/')
  return response.data
}

export async function get_branch(
  branch_id: number,
  pagination?: PaginationQuery,
): Promise<BranchWithSmallTopicsDTO> {
  const response = await http.get<BranchWithSmallTopicsDTO>(`/branches/${branch_id}`, {
    params: pagination,
  })
  return response.data
}
