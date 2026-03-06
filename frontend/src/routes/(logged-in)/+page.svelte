<script lang="ts">
	import clientAccount from '$lib/stores/clientAccount.svelte';
	import LoaderIcon from '@lucide/svelte/icons/loader';
</script>

{#if !clientAccount.state}
	<div class="flex flex-col items-center justify-center gap-6 p-6 md:p-10">
		<LoaderIcon role="status" aria-label="Loading" class="size-6 animate-spin " />
	</div>
{:else}
	<!-- Dashboard -->
	<div class="flex flex-col items-center justify-center gap-6 p-6 md:p-10">
		<h1 class="text-2xl font-bold text-center">
			Hello, {clientAccount.state.name}!
		</h1>
	</div>
{/if}
