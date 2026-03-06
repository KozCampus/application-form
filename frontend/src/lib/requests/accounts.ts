import axios from '$lib/axiosConfig';
import type { API } from '$lib/api-specs';

export const getClientAccount = async () => {
	const response = await axios.get<API.GetClientAccount.Http200.ResponseBody>('/accounts/me');
	return response.data;
};

export const createClientAccount = async (body: API.CreateClientAccount.RequestBody) => {
	const response = await axios.post<API.CreateClientAccount.Http201.ResponseBody>(
		'/accounts/me',
		body
	);
	return response.data;
};

export const listAccounts = async (params?: API.ListAccounts.QueryParameters) => {
	const response = await axios.get<API.ListAccounts.Http200.ResponseBody>('/accounts/', {
		params,
	});
	return response.data;
};

export const createAccount = async (body: API.CreateAccount.RequestBody) => {
	const response = await axios.post<API.CreateAccount.Http201.ResponseBody>('/accounts/', body);
	return response.data;
};

export const getAccount = async (account_id: string) => {
	const response = await axios.get<API.GetAccount.Http200.ResponseBody>(
		`/accounts/${account_id}`
	);
	return response.data;
};

export const updateAccount = async (account_id: string, body: API.UpdateAccount.RequestBody) => {
	const response = await axios.put<API.UpdateAccount.Http200.ResponseBody>(
		`/accounts/${account_id}`,
		body
	);
	return response.data;
};

export const deleteAccount = async (account_id: string) => {
	const response = await axios.delete<API.DeleteAccount.Http204.ResponseBody>(
		`/accounts/${account_id}`
	);
	return response.data;
};
