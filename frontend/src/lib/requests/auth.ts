import axios from '$lib/axiosConfig';
import type { API } from '$lib/api-specs';
import { PUBLIC_API_URL } from '$env/static/public';

export const getClientClaims = async () => {
	const response = await axios.get<API.GetClientClaims.Http200.ResponseBody>('/auth/claims');
	return response.data;
};

export const logout = async () => {
	const response = await axios.post<API.Logout.Http201.ResponseBody>('/auth/logout');
	return response.data;
};

export const callback = async (params: API.Callback.QueryParameters) => {
	const response = await axios.get<API.Callback.Http200.ResponseBody>('/auth/callback', {
		params,
	});
	return response.data;
};

export const getAuthRedirectUrl = () => {
	return new URL('/auth/redirect', PUBLIC_API_URL).toString();
};
