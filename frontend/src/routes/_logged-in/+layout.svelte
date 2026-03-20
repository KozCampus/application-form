<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/app-sidebar.svelte';
	import SiteHeader from '$lib/components/site-header.svelte';

	import routing from '$lib/stores/routing.svelte';
	import { onMount } from 'svelte';
	import clientAccount from '$lib/stores/clientAccount.svelte';

	let { children } = $props();

	onMount(() => {
		routing.state.isAuthenticating = false;
	});
</script>

<Sidebar.Provider
	style="--sidebar-width: calc(var(--spacing) * 66); --header-height: calc(var(--spacing) * 12);"
>
	<AppSidebar />
	<Sidebar.Inset class="mb-12">
		<SiteHeader />
		{#if clientAccount.state}
			{@render children()}
		{/if}
	</Sidebar.Inset>
</Sidebar.Provider>
