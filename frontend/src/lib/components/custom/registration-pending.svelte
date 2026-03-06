<script lang="ts">
	import { browser } from '$app/environment';
	import LogoWithText from '$lib/components/custom/logo-with-text.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { logout } from '$lib/requests/auth';

	async function handleLogout() {
		if (!browser) return;
		await logout();
		window.location.href = '/login';
	}
</script>

<div class="flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
	<div class="flex w-full max-w-sm flex-col gap-6">
		<LogoWithText />
	</div>
	<p class="text-muted-foreground text-sm text-center">
		Your registration has been received and is pending review.<br />
		Please wait or contact an administrator.
	</p>
	<Button variant="outline" onclick={handleLogout}>Log out</Button>
</div>
