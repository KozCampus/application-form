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
		return 'A fiókod inaktív. Kérjük, vedd fel a kapcsolatot egy adminisztrátorral.';
	},
};

// Status message: constant string OR generator function
const statusMap: Record<number, string | ((error: unknown) => string | undefined)> = {
	400: 'Hibás kérés. Kérjük, ellenőrizd az adatokat és próbáld újra.',
	401: () => {
		// if we're sure that the user's not authenticating, redirect to login
		if (routing.state.isAuthenticating === false) {
			clientAccount.state = null; // this brings the user to login
			return 'Nem vagy bejelentkezve. Kérjük, jelentkezz be újra.';
		}
		return undefined; // else, skip toast
	},
	403: 'Nincs jogosultságod a művelet végrehajtásához.',
	404: (error) => {
		// ignore message if the error came from a /accounts/me request
		if (error instanceof AxiosError && error.config?.url?.includes('/accounts/me')) {
			return undefined;
		}
		return 'A keresett elem nem található.';
	},
	409: 'Ütközés történt. Kérjük, ellenőrizd az adatokat és próbáld újra.',
	500: 'Ismeretlen hiba történt. Kérjük, próbáld újra később.',
	502: 'Hiba történt a szerverrel való kommunikáció során. Kérjük, próbáld újra később.',
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
		error.message = 'Ismeretlen hiba történt. Kérjük, próbáld újra később.';
	}

	if (error.message) toast.error(error.message);

	return Promise.reject(error);
});

export default axiosInstance;
