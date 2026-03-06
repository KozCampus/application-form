<script lang="ts">
	import FlagIcon from '@lucide/svelte/icons/flag';

	import { Button } from '$lib/components/ui/button/index.js';
	import FeedbackDialog from '$lib/components/custom/feedback-dialog.svelte';

	const action = 'Visszajelzés küldése';

	let isDialogOpen = $state(false);
</script>

<Button
	variant="outline"
	size="icon"
	class="h-10 w-10"
	title={action}
	onclick={() => (isDialogOpen = true)}
>
	<FlagIcon class="h-[1.2rem] w-[1.2rem]" />
	<span class="sr-only">{action}</span>
</Button>

<FeedbackDialog bind:open={isDialogOpen} />
