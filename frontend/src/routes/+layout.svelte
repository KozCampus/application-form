<script lang="ts">
	import '../app.css';
	import clientAccount from '$lib/stores/clientAccount.svelte';
	import clientClaims from '$lib/stores/clientClaims.svelte';
	import { getClientAccount } from '$lib/requests/accounts';
	import { getClientClaims } from '$lib/requests/auth';
	import { onMount } from 'svelte';
	import { ModeWatcher } from 'mode-watcher';
	import ModeToggle from '$lib/components/mode-toggle.svelte';
	import LoaderIcon from '@lucide/svelte/icons/loader';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import routing from '$lib/stores/routing.svelte';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import RegistrationPending from '$lib/components/custom/registration-pending.svelte';
	import {
		ADMIN_ROUTE_GROUPS,
		MODERATOR_ROUTE_GROUPS,
		MEMBER_ROUTE_GROUPS,
	} from '$lib/types/routing';
	import { browser } from '$app/environment';
	import FeedbackButton from '$lib/components/feedback-button.svelte';

	let { children } = $props();

	onMount(async () => {
		// try fetching client account
		try {
			clientAccount.state = await getClientAccount();
		} catch {
			clientAccount.state = null;
			// stop loading, nothing else would load
			return;
		}

		try {
			clientClaims.state = await getClientClaims();
		} catch {
			clientClaims.state = null;
		}
	});

	$effect(() => {
		if (!browser || clientAccount.state === undefined) return;

		if (clientAccount.state === null) {
			// Redirect to login page if not authenticating already
			if (routing.state.isAuthenticating === false) goto(resolve('/login'));
		} else {
			// Redirect to root if stuck on an authentication page
			if (routing.state.isAuthenticating === true) goto(resolve('/'));
		}
	});

	// Update groups based on client account role
	$effect(() => {
		switch (clientAccount.state?.role) {
			case 'admin':
				routing.state.groups = ADMIN_ROUTE_GROUPS;
				break;
			case 'moderator':
				routing.state.groups = MODERATOR_ROUTE_GROUPS;
				break;
			default:
				routing.state.groups = MEMBER_ROUTE_GROUPS;
				break;
		}
	});
</script>

{#if clientAccount.state === undefined}
	<LoaderIcon
		role="status"
		aria-label="Loading"
		class="size-6 animate-spin fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
	/>
{:else if clientAccount.state && !clientAccount.state.isActive}
	<!-- Registration pending message -->
	<RegistrationPending />
{:else}
	{@render children()}
{/if}

<ModeWatcher />

<div class="fixed bottom-4 right-4 z-50 flex gap-2">
	<FeedbackButton />
	<ModeToggle />
</div>

<Toaster position="top-center" />
