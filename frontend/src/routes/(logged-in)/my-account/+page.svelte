<script lang="ts">
	import clientAccount from '$lib/stores/clientAccount.svelte';
</script>

{#if clientAccount.state}
	<div class="flex flex-col gap-4 p-6 md:p-10">
		<h1 class="text-2xl font-bold">My Account</h1>
		<p><strong>Name:</strong> {clientAccount.state.name}</p>
		<p><strong>Email:</strong> {clientAccount.state.email}</p>
		<p><strong>Role:</strong> {clientAccount.state.role}</p>
	</div>
{/if}
