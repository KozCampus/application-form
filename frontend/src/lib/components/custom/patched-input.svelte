<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';
	import { cn, type WithElementRef } from '$lib/utils.js';
	import ChevronDownIcon from '@lucide/svelte/icons/chevron-down';

	type ExtraProps = {
		containerClass?: string;
	};

	type Props = WithElementRef<
		Omit<HTMLInputAttributes, 'type'> & { type?: 'date' | 'time'; files?: undefined }
	> &
		ExtraProps;

	let {
		ref = $bindable(null),
		value = $bindable(),
		type,
		containerClass,
		class: className,
		'data-slot': dataSlot = 'input',
		...restProps
	}: Props = $props();

	// determine whether we're running chrome
	const isChrome = navigator.userAgent.toLowerCase().includes('chrome');
</script>

<div class={cn('relative w-full', containerClass)}>
	<input
		bind:this={ref}
		data-slot={dataSlot}
		class={cn(
			'border-input bg-background selection:bg-primary dark:bg-input/30 selection:text-primary-foreground ring-offset-background placeholder:text-muted-foreground shadow-xs flex h-9 w-full min-w-0 rounded-md border px-3 py-1 text-base outline-none transition-[color,box-shadow] disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
			'focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]',
			'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive',
			isChrome ? 'input-custom-picker' : '',
			className
		)}
		{type}
		bind:value
		{...restProps}
	/>

	<!-- Cover the native indicator area and render our own icon -->
	<div
		class={cn(
			'pointer-events-none absolute inset-y-px right-px z-10 w-10 items-center justify-center rounded-r-md hidden',
			isChrome ? 'input-custom-picker-arrow' : ''
		)}
	>
		<ChevronDownIcon aria-hidden="true" class="size-4 text-muted-foreground" />
	</div>
</div>

<style>
	@media (max-width: 768px) {
		/* Workaround for Android Chrome: native date/time indicator can be unstyleable. */
		:global(input.input-custom-picker[type='date']),
		:global(input.input-custom-picker[type='time']) {
			-webkit-appearance: none;
			appearance: none;
		}

		:global(.input-custom-picker-arrow) {
			display: flex !important;
		}
	}
</style>
