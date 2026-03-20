export namespace API {
	export namespace Callback {
	export namespace Http200 {
	export type ResponseBody = {
	
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface QueryParameters {
	code: string;
	state: string;
};
};

	export namespace CreateAccount {
	export namespace Http201 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	id: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export type RequestBody = {
	email: string;
	isActive?: boolean;
	name: string;
	role?: "admin" | "member" | "moderator";
};
};

	export namespace CreateApplicant {
	export namespace Http201 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	firstName: string;
	id: string;
	interests: ("Eseményszervezés" | "HR" | "IT/Digitális infrastruktúra" | "Jogi terület" | "Kommunikáció" | "Média" | "Partnerkapcsolatok")[];
	lastName: string;
	privacyAccepted: boolean;
	status: "accepted" | "received";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export type RequestBody = {
	email: string;
	firstName: string;
	interests?: ("Eseményszervezés" | "HR" | "IT/Digitális infrastruktúra" | "Jogi terület" | "Kommunikáció" | "Média" | "Partnerkapcsolatok")[];
	lastName: string;
	privacyAccepted?: boolean;
};
};

	export namespace CreateClientAccount {
	export namespace Http201 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	id: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export type RequestBody = {
	email: string;
	isActive?: boolean;
	name: string;
	role?: "admin" | "member" | "moderator";
};
};

	export namespace DeleteAccount {
	export namespace Http204 {
	export type ResponseBody = undefined;
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface PathParameters {
	account_id: string;
};
};

	export namespace GetAccount {
	export namespace Http200 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	id: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface PathParameters {
	account_id: string;
};
};

	export namespace GetApplicant {
	export namespace Http200 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	firstName: string;
	id: string;
	interests: ("Eseményszervezés" | "HR" | "IT/Digitális infrastruktúra" | "Jogi terület" | "Kommunikáció" | "Média" | "Partnerkapcsolatok")[];
	lastName: string;
	privacyAccepted: boolean;
	status: "accepted" | "received";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface PathParameters {
	applicant_id: string;
};
};

	export namespace GetClientAccount {
	export namespace Http200 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	id: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
	updatedAt: string;
};
};
};

	export namespace GetClientClaims {
	export namespace Http200 {
	export type ResponseBody = null | {
	exp: number;
	iat: number;
	scope: string;
	sub: string;
};
};
};

	export namespace HealthLivenessCheck {
	export namespace Http200 {
	export type ResponseBody = undefined;
};
};

	export namespace HealthReadinessCheck {
	export namespace Http200 {
	export type ResponseBody = undefined;
};
};

	export namespace ListAccounts {
	export namespace Http200 {
	export type ResponseBody = {
	items: {
	createdAt: string;
	email: string;
	id: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
	updatedAt: string;
}[];
	limit: number;
	offset: number;
	total: number;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface QueryParameters {
	createdAfter?: null | string;
	createdBefore?: null | string;
	currentPage?: number;
	ids?: null | string[];
	orderBy?: null | string;
	pageSize?: number;
	searchField?: null | string;
	searchIgnoreCase?: boolean | null;
	searchString?: null | string;
	sortOrder?: "asc" | "desc" | null;
	updatedAfter?: null | string;
	updatedBefore?: null | string;
};
};

	export namespace ListApplicants {
	export namespace Http200 {
	export type ResponseBody = {
	items: {
	createdAt: string;
	email: string;
	firstName: string;
	id: string;
	interests: ("Eseményszervezés" | "HR" | "IT/Digitális infrastruktúra" | "Jogi terület" | "Kommunikáció" | "Média" | "Partnerkapcsolatok")[];
	lastName: string;
	privacyAccepted: boolean;
	status: "accepted" | "received";
	updatedAt: string;
}[];
	limit: number;
	offset: number;
	total: number;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface QueryParameters {
	createdAfter?: null | string;
	createdBefore?: null | string;
	currentPage?: number;
	ids?: null | string[];
	orderBy?: null | string;
	pageSize?: number;
	searchField?: null | string;
	searchIgnoreCase?: boolean | null;
	searchString?: null | string;
	sortOrder?: "asc" | "desc" | null;
	updatedAfter?: null | string;
	updatedBefore?: null | string;
};
};

	export namespace Logout {
	export namespace Http201 {
	export type ResponseBody = {
	
};
};
};

	export namespace Redirect {
	export namespace Http200 {
	export type ResponseBody = {
	
};
};
};

	export namespace UpdateAccount {
	export namespace Http200 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	id: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface PathParameters {
	account_id: string;
};

	export type RequestBody = {
	email: string;
	isActive: boolean;
	name: string;
	role: "admin" | "member" | "moderator";
};
};

	export namespace UpdateApplicant {
	export namespace Http200 {
	export type ResponseBody = {
	createdAt: string;
	email: string;
	firstName: string;
	id: string;
	interests: ("Eseményszervezés" | "HR" | "IT/Digitális infrastruktúra" | "Jogi terület" | "Kommunikáció" | "Média" | "Partnerkapcsolatok")[];
	lastName: string;
	privacyAccepted: boolean;
	status: "accepted" | "received";
	updatedAt: string;
};
};

	export namespace Http400 {
	export type ResponseBody = {
	detail: string;
	extra?: Record<string, unknown> | null | unknown[];
	status_code: number;
};
};

	export interface PathParameters {
	applicant_id: string;
};

	export type RequestBody = {
	status: "accepted" | "received";
};
};
};