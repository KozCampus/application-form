<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import LoaderIcon from '@lucide/svelte/icons/loader';
	import RefreshCcwIcon from '@lucide/svelte/icons/refresh-ccw';
	import { toast } from 'svelte-sonner';

	type Props = { onRefresh: () => Promise<void>; class?: string };
	let { onRefresh, class: className }: Props = $props();

	let refreshing = $state(false);

	async function handleRefresh() {
		if (refreshing) return;
		refreshing = true;
		try {
			await onRefresh();
			toast.success('Adatok frissítve.');
		} finally {
			refreshing = false;
		}
	}
</script>

<Button variant="outline" onclick={handleRefresh} disabled={refreshing} class={className}>
	{#if refreshing}
		<LoaderIcon class="size-4 animate-spin" />
	{:else}
		<RefreshCcwIcon class="size-4" />
	{/if}
	Frissítés
</Button>
