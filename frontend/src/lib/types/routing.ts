import type { Component } from 'svelte';
import type { Icon } from '@tabler/icons-svelte';
import HomeIcon from '@lucide/svelte/icons/home';
import UsersIcon from '@lucide/svelte/icons/users';
import UserIcon from '@lucide/svelte/icons/user';
import routing from '$lib/stores/routing.svelte';

export type Route = {
	name: string;
	url: string;
	icon: Component | Icon;
};

export type RouteGroup = {
	title: string | null;
	routes: Route[];
};

export const MEMBER_ROUTE_GROUPS: RouteGroup[] = [
	{
		title: null,
		routes: [
			{
				name: 'Home',
				url: '/',
				icon: HomeIcon,
			},
		],
	},
];

export const MODERATOR_ROUTE_GROUPS: RouteGroup[] = MEMBER_ROUTE_GROUPS.concat([]);

export const ADMIN_ROUTE_GROUPS: RouteGroup[] = MODERATOR_ROUTE_GROUPS.concat([
	{
		title: 'Administration',
		routes: [
			{
				name: 'Accounts',
				url: '/accounts',
				icon: UsersIcon,
			},
		],
	},
]);

export function findRouteTitle(route: string): string | undefined {
	// remove all slashes
	const normalRoute = '/' + route.replace(/\//g, '');

	// special case for /my-account
	if (normalRoute === '/my-account') return 'My Account';

	for (const group of routing.state.groups) {
		const found = group.routes.find((r) => r.url === normalRoute);
		if (found) return found.name;
	}

	return undefined;
}
