<script lang="ts">
	import clientAccount from '$lib/stores/clientAccount.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import CopyIcon from '@tabler/icons-svelte/icons/copy';
	import { browser } from '$app/environment';
	import { toast } from 'svelte-sonner';

	type Props = { id: string };
	let { id }: Props = $props();

	async function copy(text: string) {
		if (!browser) return;
		try {
			await navigator.clipboard.writeText(text);
			toast.success('Másolva a vágólapra!');
		} catch {
			toast.error('Nem sikerült másolni. Próbáld manuálisan.');
		}
	}
</script>

<div class="flex items-center gap-2">
	<code class="text-sm break-all whitespace-pre-line">{id || '-'}</code>
	{#if id}
		<Button
			variant="ghost"
			size="icon"
			aria-label="Azonosító másolása"
			title="Azonosító másolása"
			onclick={() => {
				if (clientAccount.state?.id) copy(clientAccount.state.id);
			}}
		>
			<CopyIcon class="size-4" />
		</Button>
	{/if}
</div>
