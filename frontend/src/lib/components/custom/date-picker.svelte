<script lang="ts">
	import CalendarIcon from '@lucide/svelte/icons/calendar';
	import type { DateRange } from 'bits-ui';
	import {
		CalendarDate,
		DateFormatter,
		type DateValue,
		getLocalTimeZone,
	} from '@internationalized/date';
	import { cn } from '$lib/utils.js';
	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import { RangeCalendar } from '$lib/components/ui/range-calendar/index.js';
	import * as Popover from '$lib/components/ui/popover/index.js';

	const df = new DateFormatter('hu-HU', {
		dateStyle: 'medium',
	});

	function calendarDateFromString(dateStr: string): CalendarDate {
		const parts = dateStr.split('-').map(Number);
		return new CalendarDate(parts[0], parts[1], parts[2]);
	}

	let {
		startDate,
		endDate,
		onValueChange = async (...args) => {},
	}: {
		startDate: string;
		endDate: string;
		onValueChange?: (startDate: string, endDate: string) => Promise<void>;
	} = $props();

	let value: DateRange = $state({
		// svelte-ignore state_referenced_locally
		start: calendarDateFromString(startDate),
		// svelte-ignore state_referenced_locally
		end: calendarDateFromString(endDate),
	});

	let startValue: DateValue | undefined = $state(undefined);

	function formatDate(date: DateValue): string {
		return `${date.year.toString().padStart(4, '0')}-${date.month
			.toString()
			.padStart(2, '0')}-${date.day.toString().padStart(2, '0')}`;
	}
</script>

<div class="grid gap-2">
	<Popover.Root
		onOpenChange={async () => {
			if (!value.start || !value.end) return;
			const startStr = formatDate(value.start);
			const endStr = formatDate(value.end);
			await onValueChange(startStr, endStr);
		}}
	>
		<Popover.Trigger
			class={cn(buttonVariants({ variant: 'outline' }), !value && 'text-muted-foreground')}
		>
			<CalendarIcon class="me-2 size-4" />
			{#if value && value.start}
				{#if value.end}
					{df.format(value.start.toDate(getLocalTimeZone()))} - {df.format(
						value.end.toDate(getLocalTimeZone())
					)}
				{:else}
					{df.format(value.start.toDate(getLocalTimeZone()))}
				{/if}
			{:else if startValue}
				{df.format(startValue.toDate(getLocalTimeZone()))}
			{:else}
				Pick a date
			{/if}
		</Popover.Trigger>
		<Popover.Content class="w-auto p-0" align="start">
			<RangeCalendar
				bind:value
				onStartValueChange={(v) => {
					startValue = v;
				}}
				numberOfMonths={2}
			/>
		</Popover.Content>
	</Popover.Root>
</div>
