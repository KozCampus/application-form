<script lang="ts">
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { findRouteTitle } from '$lib/types/routing';
	import { page } from '$app/state';
	import { Button } from '$lib/components/ui/button';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import ArrowLeftIcon from '@lucide/svelte/icons/arrow-left';
	import type { Pathname } from '$app/types';

	let title = $derived(findRouteTitle(page.url.pathname));

	let isBackButton = $derived(page.url.searchParams.size > 0);

	function goBack() {
		// go back (e.g. from /accounts?id=123 to /accounts)
		goto(resolve(page.url.pathname as Pathname));
	}
</script>

<header
	class="h-(--header-height) group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height) flex shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear select-none"
>
	<div class="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
		<Sidebar.Trigger class="-ms-1 cursor-pointer" />
		{#if isBackButton}
			<Button variant="ghost" onclick={goBack}>
				<!-- stronger left arrow -->
				<ArrowLeftIcon class="size-4" />
				<h1 class="text-base font-medium">{title}</h1>
			</Button>
		{:else if title}
			<Separator orientation="vertical" class="mx-2 data-[orientation=vertical]:h-4" />
			<h1 class="text-base font-medium">{title}</h1>
		{/if}
	</div>
</header>
