# Meeting Request and Founder Notification Policy

## Purpose

Make role-requested and scheduled meetings visible to the founder without allowing agents to create calendar events, invent appointments or generate meeting noise. Pepper owns the daily meeting horizon; the approved calendar and ALM or controlled fallback remain the sources of truth.

## Sources

Pepper may use only:

- connected calendars explicitly authorised for the founder brief;
- approved ALM meeting-request records or the controlled outage fallback;
- the controlled meeting-request contract defined here;
- evidence-backed immediate escalations;
- existing meeting definitions from `VIRTUAL_MEETING_CATALOG.json`.

If a source is unavailable, Pepper states `SOURCE UNAVAILABLE`. Calendar silence is not proof that no meeting exists. A role recommendation is not a scheduled appointment.

## Role Request Flow

```text
role identifies a decision, conflict, risk or collaborative design need
  -> structured meeting request in ALM or controlled fallback
  -> asynchronous-resolution check
  -> deduplication and smallest-participant review
  -> meeting-scaler recommendation
  -> authorised human schedule/decline/redirect decision
  -> calendar reference when actually scheduled
  -> Pepper daily horizon and immediate escalation where required
```

Roles may request a meeting but may not schedule it, invite external parties, reserve budget or imply founder approval. A request identifies the decision question, why asynchronous resolution is insufficient, deadline, evidence, smallest participant set, cost/time cap and consequence of delay.

## Daily Pepper Meeting Horizon

The 09:00 Europe/Budapest founder brief contains:

1. **Today — confirmed meetings:** local start/end, title, decision purpose, preparation, founder role and missing context;
2. **Next seven days — material meetings:** decision deadline and preparation lead time;
3. **New role requests:** requester, decision question, urgency, asynchronous attempt, proposed minimum participants and recommendation;
4. **Founder decisions:** approve scheduling, redirect asynchronously, merge, delegate, decline or request evidence;
5. **Conflicts and gaps:** overlaps, missing owner/evidence, unscheduled urgent request, unavailable calendar/ALM source;
6. **No-action statement:** explicit statement when no evidenced meeting action exists.

Do not list every low-value event. Personal event details, private descriptions and attendees are minimised. Read full event details only when required for meeting preparation and authorised by the connected calendar scope.

## Notification Priority

| Priority | Route |
| --- | --- |
| `IMMEDIATE` | evidence-backed material safety, security, privacy, legal, delivery or continuity risk supersedes the routine brief |
| `TODAY` | place at the top of the daily brief and founder decision list |
| `NEXT_7_DAYS` | show in the preparation horizon until resolved or scheduled |
| `ROUTINE` | bundle; redirect asynchronously when no meeting decision is justified |

An immediate request is not automatically a crisis. Pepper must state severity, known facts, uncertainty, containment, owner and deadline. The relevant human incident or governance authority decides the route.

## Meeting Economy

- Default to an asynchronous decision record.
- Merge requests with the same decision question and evidence baseline.
- Use the smallest authorised active participant set; observers receive minutes.
- Reject requests that contain no decision, conflict, risk, design collaboration or unique evidence need.
- Apply the meeting model-call cap and duration as ceilings, not targets.
- A scheduled meeting must retain its calendar reference; a calendar event must not be fabricated from a proposed request.

## Ownership

- Requesting role owns the evidence and decision question.
- Communication Operations and Scrum Master check async resolution, deduplication and meeting design.
- Pepper curates the founder-visible horizon and urgency.
- Jarvis reviews technical decision preparation and automation provenance.
- The calendar owner or delegated human schedules, changes or cancels meetings.
- The founder decides only the material items requiring founder authority.
