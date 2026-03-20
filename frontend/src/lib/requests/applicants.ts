import axios from '$lib/axiosConfig';
import type { API } from '$lib/api-specs';

export const createApplicant = async (body: API.CreateApplicant.RequestBody) => {
	const response = await axios.post<API.CreateApplicant.Http201.ResponseBody>(
		'/applicants/',
		body
	);
	return response.data;
};

export const listApplicants = async (params?: API.ListApplicants.QueryParameters) => {
	const response = await axios.get<API.ListApplicants.Http200.ResponseBody>('/applicants/', {
		params,
	});
	return response.data;
};

export const updateApplicant = async (
	applicant_id: string,
	body: API.UpdateApplicant.RequestBody
) => {
	const response = await axios.put<API.UpdateApplicant.Http200.ResponseBody>(
		`/applicants/${applicant_id}`,
		body
	);
	return response.data;
};
