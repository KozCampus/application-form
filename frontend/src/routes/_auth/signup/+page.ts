import { redirect } from '@sveltejs/kit';
import { resolve } from '$app/paths';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ url }) => {
	const email = url.searchParams.get('email')?.trim() ?? '';
	if (!email) throw redirect(302, resolve('/login'));

	return { email };
};
