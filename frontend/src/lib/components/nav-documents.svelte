<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { useSidebar } from '$lib/components/ui/sidebar/index.js';
	import type { Route } from '$lib/types/routing';

	type Props = {
		title: string | null;
		items: Route[];
	};
	let { title, items }: Props = $props();

	const sidebar = useSidebar();
</script>

<Sidebar.Group class="group-data-[collapsible=icon]:hidden">
	{#if title}
		<Sidebar.GroupLabel>{title}</Sidebar.GroupLabel>
	{/if}
	<Sidebar.Menu>
		{#each items as item (item.name)}
			<Sidebar.MenuItem>
				<Sidebar.MenuButton>
					{#snippet child({ props })}
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
						<a {...props} href={item.url} onclick={() => sidebar.setOpenMobile(false)}>
							<item.icon />
							<span>{item.name}</span>
						</a>
					{/snippet}
				</Sidebar.MenuButton>
			</Sidebar.MenuItem>
		{/each}
	</Sidebar.Menu>
</Sidebar.Group>
