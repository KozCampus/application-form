import type { RouteGroup } from '$lib/types/routing';

type RoutingState = {
	isAuthenticating: boolean | undefined;
	groups: RouteGroup[];
};

let state: RoutingState = $state({
	isAuthenticating: undefined,
	groups: [], // updated in root +layout
});

const routing = {
	get state() {
		return state;
	},
	set state(value: RoutingState) {
		state = value;
	},
};

export default routing;
