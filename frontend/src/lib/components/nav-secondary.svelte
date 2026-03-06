<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import type { WithoutChildren } from '$lib/utils.js';
	import type { ComponentProps } from 'svelte';
	import { useSidebar } from '$lib/components/ui/sidebar/index.js';
	import type { Route } from '$lib/types/routing';

	type Props = { items: Route[] } & WithoutChildren<ComponentProps<typeof Sidebar.Group>>;
	let { items, ...restProps }: Props = $props();

	const sidebar = useSidebar();

	function closeSidebar() {
		sidebar.setOpenMobile(false);
	}
</script>

<Sidebar.Group {...restProps}>
	<Sidebar.GroupContent>
		<Sidebar.Menu>
			{#each items as item (item.name)}
				<Sidebar.MenuItem>
					<Sidebar.MenuButton>
						{#snippet child({ props })}
							<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
							<a href={item.url} {...props} onclick={closeSidebar}>
								<item.icon />
								<span>{item.name}</span>
							</a>
						{/snippet}
					</Sidebar.MenuButton>
				</Sidebar.MenuItem>
			{/each}
		</Sidebar.Menu>
	</Sidebar.GroupContent>
</Sidebar.Group>
