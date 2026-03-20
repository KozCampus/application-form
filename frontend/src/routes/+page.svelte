<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { createApplicant } from '$lib/requests/applicants';
	import { toast } from 'svelte-sonner';
	import CircleCheckBig from '@lucide/svelte/icons/circle-check-big';

	const TARGET = new Date('2026-08-07T00:00:00').getTime();

	let days = $state(0);
	let hours = $state(0);
	let minutes = $state(0);
	let seconds = $state(0);
	let tick: ReturnType<typeof setInterval>;

	function refresh() {
		const d = Math.max(0, TARGET - Date.now());
		days = Math.floor(d / 86_400_000);
		hours = Math.floor((d / 3_600_000) % 24);
		minutes = Math.floor((d / 60_000) % 60);
		seconds = Math.floor((d / 1000) % 60);
	}

	onMount(() => {
		refresh();
		tick = setInterval(refresh, 1000);
	});
	onDestroy(() => tick && clearInterval(tick));

	const pad = (n: number) => String(n).padStart(2, '0');

	// form
	let firstName = $state('');
	let lastName = $state('');
	let email = $state('');
	let phone = $state('');
	let submitting = $state(false);
	let submitted = $state(false);

	const INTERESTS = [
		'Eseményszervezés',
		'Kommunikáció',
		'Partnerkapcsolatok',
		'Média',
		'HR',
		'Jogi terület',
		'IT/Digitális infrastruktúra',
	] as const;

	let selectedInterests = $state<string[]>([]);

	function toggleInterest(interest: string) {
		if (selectedInterests.includes(interest)) {
			selectedInterests = selectedInterests.filter((i) => i !== interest);
		} else {
			selectedInterests = [...selectedInterests, interest];
		}
	}

	let valid = $derived(
		firstName.trim().length > 0 && lastName.trim().length > 0 && email.trim().includes('@')
	);

	async function submit(e: SubmitEvent) {
		e.preventDefault();
		if (!valid || submitting) return;
		submitting = true;
		try {
			await createApplicant({
				firstName: firstName.trim(),
				lastName: lastName.trim(),
				email: email.trim(),
				phone: phone.trim(),
				interests: selectedInterests as typeof INTERESTS[number][],
			});
			submitted = true;
			toast.success('Sikeres jelentkezés!');
		} catch {
			// axios interceptor handles error toasts
		} finally {
			submitting = false;
		}
	}
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=DM+Serif+Display&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<main class="landing">
	<!-- ───── HERO ───── -->
	<section class="hero">
		<div class="hero-fog"></div>
		<div class="hero-inner">
			<img src="/logo-white.svg" alt="KözCampus" class="logo" />

			<h2 class="tagline">
				A fiatal magyar értelmiség<br />közös nevezője
			</h2>

			<p class="blurb">
				Csatlakozz a közösséghez, amely nemcsak kapcsolatokat épít,
				hanem jellemet és jövőt.
			</p>

			<!-- countdown -->
			<div class="countdown" aria-label="Visszaszámlálás 2026. augusztus 7-ig">
				<div class="cd-box cd-green">
					<span class="cd-num">{days}</span>
					<span class="cd-lbl">nap</span>
				</div>
				<div class="cd-box cd-amber">
					<span class="cd-num">{pad(hours)}</span>
					<span class="cd-lbl">óra</span>
				</div>
				<div class="cd-box cd-rose">
					<span class="cd-num">{pad(minutes)}</span>
					<span class="cd-lbl">perc</span>
				</div>
				<div class="cd-box cd-lime">
					<span class="cd-num">{pad(seconds)}</span>
					<span class="cd-lbl">mp</span>
				</div>
			</div>
		</div>
	</section>

	<!-- ───── FORM ───── -->
	<section class="form-section">
		<div class="form-card">
			{#if submitted}
				<div class="success">
					<CircleCheckBig class="success-icon" />
					<h3 class="success-title">Köszönjük, {firstName}!</h3>
					<p class="success-desc">
						Jelentkezésedet rögzítettük.<br />
						Hamarosan felvesszük veled a kapcsolatot!
					</p>
				</div>
			{:else}
				<h3 class="form-heading">
					Légy része a 40 fős szervezői csapatnak!
				</h3>

				<form onsubmit={submit} class="form">
					<div class="field">
						<label for="fn">Keresztnév</label>
						<Input
							id="fn"
							type="text"
							placeholder="Add meg a keresztneved"
							bind:value={firstName}
							class="h-11"
						/>
					</div>

					<div class="field">
						<label for="ln">Vezetéknév</label>
						<Input
							id="ln"
							type="text"
							placeholder="Add meg a vezetékneved"
							bind:value={lastName}
							class="h-11"
						/>
					</div>

					<div class="field">
						<label for="em">E-mail cím</label>
						<Input
							id="em"
							type="email"
							placeholder="pelda@email.hu"
							bind:value={email}
							class="h-11"
						/>
					</div>

					<div class="field">
						<label for="ph">Telefonszám</label>
						<Input
							id="ph"
							type="tel"
							placeholder="+36 30 123 4567"
							bind:value={phone}
							class="h-11"
						/>
					</div>

					<div class="field">
						<label>Érdeklődési terület</label>
						<div class="interests">
							{#each INTERESTS as interest}
								<button
									type="button"
									class="chip"
									class:selected={selectedInterests.includes(interest)}
									onclick={() => toggleInterest(interest)}
								>
									{interest}
								</button>
							{/each}
						</div>
					</div>

					<Button
						type="submit"
						size="lg"
						disabled={!valid || submitting}
						class="mt-2 h-12 w-full rounded-lg text-sm font-bold uppercase tracking-widest"
					>
						{submitting ? 'Küldés…' : 'Csatlakozom a küldetéshez!'}
					</Button>
				</form>
			{/if}
		</div>
	</section>
</main>

<style>
	/* ── page-scoped tokens ── */
	.landing {
		--hero-bg: #253a25;
		--cd-green: #7a9a3a;
		--cd-amber: #d4a832;
		--cd-rose: #c24d5d;
		--cd-lime: #8fb32a;
		font-family: 'DM Sans', ui-sans-serif, system-ui, sans-serif;
		min-height: 100svh;
		display: flex;
		flex-direction: column;
		overflow-x: hidden;
	}

	/* ── HERO ── */
	.hero {
		position: relative;
		background: radial-gradient(ellipse 120% 100% at 50% 20%, #3a5c3a 0%, var(--hero-bg) 70%);
		color: #fff;
		text-align: center;
		padding: 4rem 1.5rem 6rem;
		flex-shrink: 0;
	}

	/* atmospheric noise layer */
	.hero-fog {
		position: absolute;
		inset: 0;
		background:
			radial-gradient(circle at 30% 35%, rgba(120, 160, 80, 0.18) 0%, transparent 55%),
			radial-gradient(circle at 70% 60%, rgba(60, 100, 60, 0.15) 0%, transparent 50%);
		pointer-events: none;
	}

	.hero-inner {
		position: relative;
		max-width: 460px;
		margin: 0 auto;
	}

	.logo {
		width: 360px;
		height: auto;
		margin: 0 auto 2.5rem;
	}

	.tagline {
		font-size: 1rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		line-height: 1.45;
		margin-bottom: 0.75rem;
	}

	.blurb {
		font-size: 0.85rem;
		line-height: 1.55;
		opacity: 0.75;
		max-width: 340px;
		margin: 0 auto 2rem;
	}

	/* ── COUNTDOWN ── */
	.countdown {
		display: flex;
		justify-content: center;
		gap: 0.625rem;
	}

	.cd-box {
		width: 66px;
		border-radius: 14px;
		padding: 0.65rem 0 0.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
	}

	.cd-green {
		background: var(--cd-green);
	}
	.cd-amber {
		background: var(--cd-amber);
	}
	.cd-rose {
		background: var(--cd-rose);
	}
	.cd-lime {
		background: var(--cd-lime);
	}

	.cd-num {
		font-size: 1.65rem;
		font-weight: 800;
		line-height: 1;
		font-variant-numeric: tabular-nums;
	}

	.cd-lbl {
		font-size: 0.6rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		margin-top: 0.2rem;
		opacity: 0.85;
	}

	/* ── FORM SECTION ── */
	.form-section {
		flex: 1;
		background: var(--color-background, #fff);
		border-radius: 1.75rem 1.75rem 0 0;
		margin-top: -1.75rem;
		position: relative;
		z-index: 1;
		padding: 2.5rem 1.5rem 3.5rem;
		box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.06);
	}

	.form-card {
		max-width: 400px;
		margin: 0 auto;
	}

	.form-heading {
		font-size: 1.05rem;
		font-weight: 800;
		text-transform: uppercase;
		text-align: center;
		letter-spacing: 0.03em;
		line-height: 1.4;
		margin-bottom: 1.75rem;
		color: var(--color-foreground);
	}

	.form {
		display: flex;
		flex-direction: column;
		gap: 1.15rem;
	}

	.field {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}

	.field label {
		font-size: 0.78rem;
		font-weight: 600;
		color: var(--color-muted-foreground);
		padding-left: 0.05rem;
	}

	/* ── INTERESTS ── */
	.interests {
		display: flex;
		flex-wrap: wrap;
		gap: 0.45rem;
	}

	.chip {
		font-size: 0.78rem;
		font-weight: 500;
		padding: 0.35rem 0.75rem;
		border-radius: 9999px;
		border: 1.5px solid var(--color-border, #e0e0e0);
		background: transparent;
		color: var(--color-foreground);
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.chip:hover {
		border-color: var(--cd-green);
	}

	.chip.selected {
		background: var(--cd-green);
		border-color: var(--cd-green);
		color: #fff;
	}

	/* ── SUCCESS STATE ── */
	.success {
		text-align: center;
		padding: 2rem 0 1rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
	}

	:global(.success-icon) {
		width: 48px;
		height: 48px;
		color: var(--cd-green);
	}

	.success-title {
		font-family: 'DM Serif Display', serif;
		font-size: 1.4rem;
		font-weight: 400;
		color: var(--color-foreground);
	}

	.success-desc {
		font-size: 0.875rem;
		line-height: 1.6;
		color: var(--color-muted-foreground);
	}
</style>
