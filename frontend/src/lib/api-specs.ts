export namespace API {
	export type Role = 'admin' | 'moderator' | 'member';

	export type AccountBody = {
		id: string;
		createdAt: string;
		updatedAt: string;
		name: string;
		email: string;
		isActive: boolean;
		role: API.Role;
	};

	export type PaginatedResponse<T> = {
		items: T[];
		total: number;
		limit: number;
		offset: number;
	};

	export type ErrorBody = {
		detail: string;
		extra?: Record<string, unknown> | null | unknown[];
		status_code: number;
	};

	export namespace Callback {
		export namespace Http200 {
			export type ResponseBody = {};
		}

		export namespace Http400 {
			export type ResponseBody = ErrorBody;
		}

		export interface QueryParameters {
			code: string;
			state: string;
		}
	}

	export namespace GetClientClaims {
		export namespace Http200 {
			export type ResponseBody = {
				sub: string;
				exp: number;
				iat: number;
				scope: string;
			} | null;
		}
	}

	export namespace Logout {
		export namespace Http201 {
			export type ResponseBody = null;
		}
	}

	export namespace GetClientAccount {
		export namespace Http200 {
			export type ResponseBody = AccountBody;
		}
	}

	export namespace CreateClientAccount {
		export namespace Http201 {
			export type ResponseBody = AccountBody;
		}

		export namespace Http400 {
			export type ResponseBody = ErrorBody;
		}

		export type RequestBody = {
			name: string;
			email: string;
		};
	}

	export namespace ListAccounts {
		export namespace Http200 {
			export type ResponseBody = PaginatedResponse<AccountBody>;
		}

		export interface QueryParameters {
			currentPage?: number;
			pageSize?: number;
			searchField?: string;
			searchString?: string;
		}
	}

	export namespace CreateAccount {
		export namespace Http201 {
			export type ResponseBody = AccountBody;
		}

		export namespace Http400 {
			export type ResponseBody = ErrorBody;
		}

		export type RequestBody = {
			name: string;
			email: string;
			isActive: boolean;
			role: API.Role;
		};
	}

	export namespace GetAccount {
		export namespace Http200 {
			export type ResponseBody = AccountBody;
		}
	}

	export namespace UpdateAccount {
		export namespace Http200 {
			export type ResponseBody = AccountBody;
		}

		export type RequestBody = {
			name: string;
			email: string;
			isActive: boolean;
			role: API.Role;
		};
	}

	export namespace DeleteAccount {
		export namespace Http204 {
			export type ResponseBody = null;
		}
	}
}
