<script lang="ts">
	import { onMount } from 'svelte';
	import { listApplicants, updateApplicant } from '$lib/requests/applicants';
	import type { API } from '$lib/api-specs';
	import { toast } from 'svelte-sonner';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Table from '$lib/components/ui/table/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import LoaderIcon from '@lucide/svelte/icons/loader';
	import RefreshCw from '@lucide/svelte/icons/refresh-cw';
	import Users from '@lucide/svelte/icons/users';

	type Applicant = API.ListApplicants.Http200.ResponseBody['items'][number];

	let applicants = $state<Applicant[]>([]);
	let total = $state(0);
	let loading = $state(true);
	let updatingId = $state<string | null>(null);

	async function fetchApplicants() {
		loading = true;
		try {
			const data = await listApplicants({ pageSize: 100 });
			applicants = data.items;
			total = data.total;
		} catch {
			// error toast handled by axios interceptor
		} finally {
			loading = false;
		}
	}

	onMount(fetchApplicants);

	async function handleStatusChange(id: string, status: 'received' | 'in_progress' | 'accepted') {
		updatingId = id;
		try {
			const updated = await updateApplicant(id, { status });
			applicants = applicants.map((a) => (a.id === id ? updated : a));
			toast.success('Státusz frissítve.');
		} catch {
			// error toast handled by axios interceptor
		} finally {
			updatingId = null;
		}
	}

	function decodeBase64Utf8(b64: string): string {
		const bytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
		return new TextDecoder().decode(bytes);
	}

	function parseInterests(raw: unknown): string[] {
		if (Array.isArray(raw)) return raw;
		if (typeof raw === 'string') {
			try {
				const decoded = JSON.parse(decodeBase64Utf8(raw));
				if (Array.isArray(decoded)) return decoded;
			} catch {
				// not base64/json
			}
			try {
				const parsed = JSON.parse(raw);
				if (Array.isArray(parsed)) return parsed;
			} catch {
				// not json
			}
		}
		return [];
	}

	function formatDate(iso: string) {
		return new Date(iso).toLocaleDateString('hu-HU', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
		});
	}
</script>

<div class="space-y-6">
	<div class="flex items-center justify-between">
		<div class="flex items-center gap-3">
			<Users class="text-muted-foreground size-5" />
			<div>
				<h1 class="text-xl font-semibold">Jelentkezők</h1>
				<p class="text-muted-foreground text-sm">
					{total} jelentkező összesen
				</p>
			</div>
		</div>
		<Button variant="outline" size="sm" onclick={fetchApplicants} disabled={loading}>
			<RefreshCw class="size-4 {loading ? 'animate-spin' : ''}" />
			Frissítés
		</Button>
	</div>

	{#if loading && applicants.length === 0}
		<div class="flex items-center justify-center py-16">
			<LoaderIcon class="size-6 animate-spin" />
		</div>
	{:else if applicants.length === 0}
		<div class="bg-background rounded-lg border py-16 text-center">
			<p class="text-muted-foreground">Még nincsenek jelentkezők.</p>
		</div>
	{:else}
		<div class="bg-background rounded-lg border">
			<Table.Root>
				<Table.Header>
					<Table.Row>
						<Table.Head>Név</Table.Head>
						<Table.Head>E-mail</Table.Head>
						<Table.Head>Telefon</Table.Head>
						<Table.Head>Érdeklődés</Table.Head>
						<Table.Head>Jelentkezett</Table.Head>
						<Table.Head class="w-[160px]">Státusz</Table.Head>
					</Table.Row>
				</Table.Header>
				<Table.Body>
					{#each applicants as applicant (applicant.id)}
						<Table.Row>
							<Table.Cell class="font-medium">
								{applicant.lastName} {applicant.firstName}
							</Table.Cell>
							<Table.Cell>
								<a href="mailto:{applicant.email}" class="text-sm hover:underline">
									{applicant.email}
								</a>
							</Table.Cell>
							<Table.Cell class="text-sm">
								{applicant.phone || '-'}
							</Table.Cell>
							<Table.Cell>
								{@const interests = parseInterests(applicant.interests)}
								<div class="flex flex-wrap gap-1">
									{#each interests as interest}
										<Badge variant="secondary" class="text-xs">
											{interest}
										</Badge>
									{/each}
									{#if interests.length === 0}
										<span class="text-muted-foreground text-xs">-</span>
									{/if}
								</div>
							</Table.Cell>
							<Table.Cell class="text-muted-foreground text-sm">
								{formatDate(applicant.createdAt)}
							</Table.Cell>
							<Table.Cell>
								{#if updatingId === applicant.id}
									<LoaderIcon class="size-4 animate-spin" />
								{:else}
									<Select.Root
										type="single"
										value={applicant.status}
										onValueChange={(v) => {
											if (v && v !== applicant.status) {
												handleStatusChange(applicant.id, v as 'received' | 'in_progress' | 'accepted');
											}
										}}
									>
										<Select.Trigger class="h-8 w-[140px] text-xs">
											{#if applicant.status === 'received'}
												Beérkezett
											{:else if applicant.status === 'in_progress'}
												Folyamatban
											{:else}
												Elfogadva
											{/if}
										</Select.Trigger>
										<Select.Content>
											<Select.Item value="received">Beérkezett</Select.Item>
											<Select.Item value="in_progress">Folyamatban</Select.Item>
											<Select.Item value="accepted">Elfogadva</Select.Item>
										</Select.Content>
									</Select.Root>
								{/if}
							</Table.Cell>
						</Table.Row>
					{/each}
				</Table.Body>
			</Table.Root>
		</div>
	{/if}
</div>
