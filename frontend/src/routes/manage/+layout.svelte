<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import clientAccount from '$lib/stores/clientAccount.svelte';
	import { getClientAccount } from '$lib/requests/accounts';
	import { logout } from '$lib/requests/auth';
	import { Button } from '$lib/components/ui/button/index.js';
	import LogoWithText from '$lib/components/custom/logo-with-text.svelte';
	import LoaderIcon from '@lucide/svelte/icons/loader';
	import LogOut from '@lucide/svelte/icons/log-out';
	import ModeToggle from '$lib/components/mode-toggle.svelte';

	let { children } = $props();

	onMount(async () => {
		try {
			clientAccount.state = await getClientAccount();
		} catch {
			clientAccount.state = null;
		}
	});

	$effect(() => {
		if (clientAccount.state === null) {
			goto(resolve('/login'));
		}
	});

	let isModerator = $derived(
		clientAccount.state?.role === 'moderator' || clientAccount.state?.role === 'admin'
	);

	async function handleLogout() {
		await logout();
		clientAccount.state = null;
	}
</script>

{#if clientAccount.state === undefined}
	<div class="flex min-h-svh items-center justify-center">
		<LoaderIcon class="size-6 animate-spin" />
	</div>
{:else if clientAccount.state && !isModerator}
	<div class="flex min-h-svh flex-col items-center justify-center gap-4 p-6 text-center">
		<h1 class="text-xl font-semibold">Hozzáférés megtagadva</h1>
		<p class="text-muted-foreground text-sm">
			Nincs jogosultságod az oldal megtekintéséhez.
		</p>
		<Button variant="outline" onclick={handleLogout}>Kijelentkezés</Button>
	</div>
{:else if clientAccount.state}
	<div class="min-h-svh bg-muted/40">
		<header class="border-b bg-background">
			<div class="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
				<a href="/" class="no-underline">
					<LogoWithText />
				</a>
				<div class="flex items-center gap-3">
					<span class="text-muted-foreground text-sm">{clientAccount.state.name}</span>
					<ModeToggle />
					<Button variant="ghost" size="icon" onclick={handleLogout}>
						<LogOut class="size-4" />
					</Button>
				</div>
			</div>
		</header>
		<main class="mx-auto max-w-5xl px-6 py-8">
			{@render children()}
		</main>
	</div>
{/if}
