import axios, { AxiosError } from 'axios';
import { PUBLIC_API_URL } from '$env/static/public';
import { toast } from 'svelte-sonner';
import routing from './stores/routing.svelte';
import clientAccount from './stores/clientAccount.svelte';

function normalizeApiOrigin(raw: string | undefined): string {
	if (!raw) return '';
	let url = raw.trim();
	if (!url) return '';
	// Remove trailing slashes to stabilize joining behavior.
	url = url.replace(/\/+$/, '');
	// Some environments may set PUBLIC_API_URL to include `/api`.
	// Requests in this app already prefix paths with `/api`, so strip it here.
	if (url.endsWith('/api')) url = url.slice(0, -4);
	return url;
}

const axiosInstance = axios.create({
	baseURL: normalizeApiOrigin(PUBLIC_API_URL),
	headers: {
		'Content-Type': 'application/json',
	},
	withCredentials: true,
});

const codeMap: Record<string, string | ((error: unknown) => string | undefined)> = {
	inactive_account: () => {
		if (window.location.pathname === '/') {
			return undefined;
		}
		return 'Your account is inactive. Please contact an administrator.';
	},
};

// Status message: constant string OR generator function
const statusMap: Record<number, string | ((error: unknown) => string | undefined)> = {
	400: 'Bad request. Please check your input and try again.',
	401: () => {
		// if we're sure that the user's not authenticating, redirect to login
		if (routing.state.isAuthenticating === false) {
			clientAccount.state = null; // this brings the user to login
			return 'You are not logged in. Please log in again.';
		}
		return undefined; // else, skip toast
	},
	403: 'You do not have permission to perform this action.',
	404: (error) => {
		// ignore message if the error came from a /accounts/me request
		if (error instanceof AxiosError && error.config?.url?.includes('/accounts/me')) {
			return undefined;
		}
		return 'The requested resource was not found.';
	},
	409: 'A conflict occurred. Please check your input and try again.',
	500: 'An unknown error occurred. Please try again later.',
	502: 'An error occurred while communicating with the server. Please try again later.',
};

axiosInstance.interceptors.response.use(undefined, (error) => {
	const status = error.response?.status;
	const code = error.response?.data?.error;

	if (code && Object.hasOwn(codeMap, code)) {
		const message = codeMap[code];
		error.message = typeof message === 'string' ? message : message(error);
	} else if (status && Object.hasOwn(statusMap, status)) {
		const message = statusMap[status];
		error.message = typeof message === 'string' ? message : message(error);
	} else {
		error.message = 'An unknown error occurred. Please try again later.';
	}

	if (error.message) toast.error(error.message);

	return Promise.reject(error);
});

export default axiosInstance;
