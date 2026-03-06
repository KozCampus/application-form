<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Field from '$lib/components/ui/field/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { type ComponentProps } from 'svelte';
	import { createClientAccount } from '$lib/requests/accounts';
	import * as Alert from '$lib/components/ui/alert/index.js';

	type Props = { email: string };
	let { email, ...restProps }: Props & ComponentProps<typeof Card.Root> = $props();

	let name: string = $state('');
	let alertMessage: string | null = $state(null);

	let preventSubmit = $derived(!name);

	async function submit(event: Event) {
		event.preventDefault();
		alertMessage = null;

		try {
			await createClientAccount({ name, email });
			window.location.href = '/';
		} catch {
			alertMessage = 'An unknown error occurred.';
		}
	}
</script>

<Card.Root {...restProps}>
	<Card.Header>
		<Card.Title>Request access</Card.Title>
		<Card.Description>Fill in the form below to create your account.</Card.Description>
	</Card.Header>
	<Card.Content>
		<form onsubmit={submit}>
			<Field.Group>
				<Field.Field>
					<Field.Label for="name">Full name</Field.Label>
					<Input
						id="name"
						type="text"
						bind:value={name}
						placeholder="Jane Doe"
						required
					/>
				</Field.Field>
				<Field.Field>
					<Field.Label for="email">Email address</Field.Label>
					<Input id="email" type="email" required bind:value={email} readonly />
				</Field.Field>
				<Field.Group class="mt-4">
					<Field.Field>
						<Button type="submit" disabled={preventSubmit}>Submit request</Button>
					</Field.Field>
				</Field.Group>
			</Field.Group>
		</form>
	</Card.Content>
</Card.Root>

{#if alertMessage}
	<Alert.Root variant="destructive" class="mb-4">
		<Alert.Title>{alertMessage}</Alert.Title>
	</Alert.Root>
{/if}
