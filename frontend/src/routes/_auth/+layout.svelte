<script lang="ts">
	import routing from '$lib/stores/routing.svelte';
	import { onMount } from 'svelte';

	let { children } = $props();

	onMount(() => {
		routing.state.isAuthenticating = true;
		return () => (routing.state.isAuthenticating = false);
	});
</script>

{@render children()}
