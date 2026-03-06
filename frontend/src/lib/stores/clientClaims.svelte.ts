import type { API } from '$lib/api-specs';

let state: API.GetClientClaims.Http200.ResponseBody | null | undefined = $state(undefined);

const clientClaims = {
	get state() {
		return state;
	},
	set state(value: API.GetClientClaims.Http200.ResponseBody | null | undefined) {
		state = value;
	},
};

export default clientClaims;
