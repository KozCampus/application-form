<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { FieldGroup, Field } from '$lib/components/ui/field/index.js';
	import { cn } from '$lib/utils.js';
	import type { HTMLAttributes } from 'svelte/elements';
	import BrandGoogle from '@tabler/icons-svelte/icons/brand-google';
	import LoaderIcon from '@tabler/icons-svelte/icons/loader';

	let { class: className, ...restProps }: HTMLAttributes<HTMLDivElement> = $props();

	let isLoading = $state(false);

	function handleGoogleLogin() {
		if (isLoading) return;
		isLoading = true;
		window.location.href = new URL('/auth/redirect', PUBLIC_API_URL).toString();
	}
</script>

<div class={cn('flex flex-col gap-6', className)} {...restProps}>
	<Card.Root>
		<Card.Header class="text-center">
			<Card.Title class="text-xl">Üdvözlünk!</Card.Title>
			<Card.Description>Jelentkezz be a Google fiókoddal.</Card.Description>
		</Card.Header>
		<Card.Content>
			<form>
				<FieldGroup>
					<Field>
						<Button
							variant="outline"
							type="button"
							onclick={handleGoogleLogin}
							disabled={isLoading}
						>
							{#if isLoading}
								<LoaderIcon class="size-5 animate-spin" />
							{:else}
								<BrandGoogle class="size-5 fill-current stroke-none" />
							{/if}
							Bejelentkezés Google-lel
						</Button>
					</Field>
				</FieldGroup>
			</form>
		</Card.Content>
	</Card.Root>
</div>
