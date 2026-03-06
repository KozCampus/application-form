<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import LinkIcon from '@tabler/icons-svelte/icons/external-link';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import type { Pathname } from '$app/types';

	type Props = { text: string; url: string | null | undefined };
	let { text, url }: Props = $props();
</script>

<div class="flex items-center gap-2">
	<p class="text-sm">{text || '-'}</p>
	{#if url}
		<Button variant="ghost" size="icon" onclick={() => goto(resolve(url as Pathname))}>
			<LinkIcon class="size-4" />
		</Button>
	{/if}
</div>
