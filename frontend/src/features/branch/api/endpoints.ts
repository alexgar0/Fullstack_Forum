import http from "../../../api/http";
import type { PaginationQuery } from "../../../api/query";
import type { BranchCreateDTO, BranchDTO, BranchWithSmallTopicsDTO } from "./dto";

export async function create_branch(new_branch: BranchCreateDTO): Promise<BranchDTO> {
    const response = await http.post<BranchDTO>('/branches/', new_branch);
    return response.data;
}

export async function get_all_branches(): Promise<BranchDTO[]> {
    const response = await http.get<BranchDTO[]>('/branches/');
    return response.data;
}

export async function get_branch(
    branch_id: number,
    pagination?: PaginationQuery
): Promise<BranchWithSmallTopicsDTO> {
    const response = await http.get<BranchWithSmallTopicsDTO>(`/branches/${branch_id}`, {
        params: pagination
    });
    return response.data;
}
