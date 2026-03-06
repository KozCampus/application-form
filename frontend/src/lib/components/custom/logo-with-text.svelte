<script lang="ts">
	import { cn } from '$lib/utils';

	type Props = { class?: string };
	let { class: className = '' }: Props = $props();
</script>

<div
	class={cn(
		'flex items-center gap-2 self-center font-medium select-none pointer-events-none',
		className
	)}
>
	közcampus
</div>
