<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import PencilIcon from '@tabler/icons-svelte/icons/pencil';
	import CheckIcon from '@tabler/icons-svelte/icons/check';
	import LoaderIcon from '@tabler/icons-svelte/icons/loader';
	import type { Snippet } from 'svelte';

	type Props = {
		save: () => Promise<void>;
		enabled: boolean;
		children: Snippet<[{ isEditing: boolean }]>;
	};
	let { save, enabled, children }: Props = $props();

	let isEditing = $state(false);
	let isSaving = $state(false);

	async function handleClick() {
		if (!enabled) return;
		if (isEditing) {
			isSaving = true;
			try {
				await save();
				isEditing = false;
			} finally {
				isSaving = false;
			}
		} else {
			isEditing = true;
		}
	}
</script>

<div class="flex items-center gap-2">
	{@render children({ isEditing: enabled && isEditing })}
	{#if enabled}
		<Button variant="ghost" size="icon" onclick={handleClick} disabled={isSaving}>
			{#if isSaving}
				<LoaderIcon class="size-4 animate-spin" />
			{:else if isEditing}
				<CheckIcon class="size-4" />
			{:else}
				<PencilIcon class="size-4" />
			{/if}
		</Button>
	{/if}
</div>
