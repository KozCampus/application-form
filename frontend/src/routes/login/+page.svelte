<script lang="ts">
	import LoginForm from '$lib/components/login-form.svelte';
	import LogoWithText from '$lib/components/custom/logo-with-text.svelte';
	import ModeToggle from '$lib/components/mode-toggle.svelte';
</script>

<div class="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
	<div class="flex w-full max-w-sm flex-col gap-6">
		<LogoWithText />
		<LoginForm />
	</div>
	<div class="fixed bottom-4 right-4">
		<ModeToggle />
	</div>
</div>
