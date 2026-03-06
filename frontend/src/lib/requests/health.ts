import axios from '$lib/axiosConfig';
import type { API } from '$lib/api-specs';

export const healthLivenessCheck = async () => {
	const response =
		await axios.get<API.HealthLivenessCheck.Http200.ResponseBody>('/health/liveness');
	return response.data;
};

export const healthReadinessCheck = async () => {
	const response =
		await axios.get<API.HealthReadinessCheck.Http200.ResponseBody>('/health/readiness');
	return response.data;
};
