<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { toast } from 'svelte-sonner';
	import LoaderIcon from '@lucide/svelte/icons/loader';
	import { fade } from 'svelte/transition';
	import { Textarea } from '$lib/components/ui/textarea/index.js';
	import { createTicket } from '$lib/requests/tickets';
	import clientAccount from '$lib/stores/clientAccount.svelte';

	type Props = { open: boolean };
	let { open = $bindable(false) }: Props = $props();

	let message: string = $state('');
	let preventSubmit = $derived(!message.trim());
	let isLoading = $state(false);

	async function handleSubmit() {
		if (!message.trim()) {
			toast.error('Üres üzenet nem küldhető el.');
			return;
		}
		if (!clientAccount.state?.id) {
			toast.error('Visszajelzés küldése előtt jelentkezz be.');
			return;
		}

		isLoading = true;
		try {
			await createTicket({ accountId: clientAccount.state?.id, description: message });
			toast.success('Visszajelzés rögzítve.');
			open = false;
			message = '';
		} catch {
			toast.error('Hiba történt a visszajelzés küldésekor.');
		} finally {
			isLoading = false;
		}
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title>Visszajelzés</Dialog.Title>
		</Dialog.Header>

		<Textarea bind:value={message} class="w-full min-h-32" placeholder="Üzenet" />

		<Dialog.Footer>
			<Button variant="secondary" onclick={handleSubmit} disabled={preventSubmit || isLoading}
				>Küldés
			</Button>
		</Dialog.Footer>

		{#if isLoading}
			<div
				class="absolute top-0 left-0 w-full h-full flex items-center justify-center bg-background/50 select-none"
				transition:fade={{ duration: 200 }}
			>
				<LoaderIcon
					role="status"
					aria-label="Loading"
					class="size-6 animate-spin absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
				/>
			</div>
		{/if}
	</Dialog.Content>
</Dialog.Root>
