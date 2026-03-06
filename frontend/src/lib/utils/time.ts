// RFC 3339 full-time:
// - hh:mm:ss with optional fractional seconds
// - optional offset (Z or ±hh:mm)
//
// Browsers may also provide `H:MM` / `HH:MM` for `<input type="time">` values depending on platform,
// so we accept 1-2 digit hours and normalize to `HH:MM:SS`.
export const RFC3339_TIME_RE = /^(\d{1,2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?$/;

function pad2(n: number): string {
	return String(n).padStart(2, '0');
}

function parseTime(value: string): { hh: number; mm: number; ss: number } | null {
	const m = RFC3339_TIME_RE.exec(value);
	if (!m) return null;

	const hh = Number(m[1]);
	const mm = Number(m[2]);
	const ss = m[3] ? Number(m[3]) : 0;

	if ([hh, mm, ss].some((n) => Number.isNaN(n))) return null;
	if (hh < 0 || hh > 23) return null;
	if (mm < 0 || mm > 59) return null;
	if (ss < 0 || ss > 59) return null;

	return { hh, mm, ss };
}

export function hhmmFromRfc3339Time(time: string): string {
	const t = parseTime(time);
	if (!t) return '';
	return `${pad2(t.hh)}:${pad2(t.mm)}`;
}

// RFC 3339 full-time requires seconds; we send HH:MM:SS (no offset) since date is sent separately.
export function rfc3339TimeFromHHMM(hhmm: string): string {
	// Accept both HH:MM and HH:MM:SS (and also H:MM variants), normalize to HH:MM:SS.
	const t = parseTime(hhmm);
	if (!t) return '';
	return `${pad2(t.hh)}:${pad2(t.mm)}:${pad2(t.ss)}`;
}

export function timeStringToSeconds(time: string): number | null {
	const t = parseTime(time);
	if (!t) return null;
	return t.hh * 3600 + t.mm * 60 + t.ss;
}

export function mapDateToWeekday(dateStr: string): string {
	const date = new Date(dateStr);
	const options: Intl.DateTimeFormatOptions = { weekday: 'long' };
	return date.toLocaleDateString('hu-HU', options);
}

export function formatTimeRange(startTime: string, endTime: string): string {
	const start = startTime.slice(0, 5);
	const end = endTime.slice(0, 5);
	return `${start} - ${end}`;
}
