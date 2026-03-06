import type { API } from '$lib/api-specs';

let state: API.GetClientAccount.Http200.ResponseBody | null | undefined = $state(undefined);

const clientAccount = {
	get state() {
		return state;
	},
	set state(value: API.GetClientAccount.Http200.ResponseBody | null | undefined) {
		state = value;
	},
};

export default clientAccount;
