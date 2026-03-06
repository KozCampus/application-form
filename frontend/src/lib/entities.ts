export type UUIDAuditBase = {
	id: string;
	createdAt: string;
	updatedAt: string;
};

export type AccountFields = {
	name: string;
	email: string;
	isActive: boolean;
	role: 'admin' | 'moderator' | 'member';
};

export type Account = UUIDAuditBase & AccountFields;
