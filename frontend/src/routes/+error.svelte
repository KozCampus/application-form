<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { onMount } from 'svelte';

	onMount(() => {
		// redirect to root on 404
		if (page.status === 404) goto(resolve('/'));
	});
</script>

{#if page.status !== 404}
	<h1>{page.status}: {page.error?.message}</h1>
{/if}
