import http from "../../../api/http";
import type { BranchCreateDTO, BranchDTO } from "./dto";

export async function create_branch(new_branch: BranchCreateDTO): Promise<BranchDTO> {
    const response = await http.post<BranchDTO>('/branches/', new_branch);
    return response.data;
}

export async function get_all_branches(): Promise<BranchDTO[]> {
    const response = await http.get<BranchDTO[]>('/branches/');
    return response.data;
}

export async function get_branch(branch_id: number): Promise<BranchDTO> {
    const response = await http.get<BranchDTO>(`/branches/${branch_id}`);
    return response.data;
}

