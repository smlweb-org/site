# S—ML Web: Responsive Delivery Profiles for the Open Web

*Draft 0.2 — July 2026*

---

## The Manifesto (TL;DR)

Responsive design made the web fit the screen. S—ML makes the web fit the situation.

Today a single URL may be opened on a fast desktop connection, a phone on 5G, a handset connected through direct-to-device satellite, an aircraft seatback screen, an assistive reader, or by an AI agent that only needs the meaning of the page. These clients do not need the same weight of experience — yet the web has no common, testable way to request or publish a lighter one.

S—ML Web proposes a delivery-profile layer for the web we already have. Every important resource can expose the same canonical content in three weights:

- **S — Sparse.** The minimal trustworthy representation: text-first, server-rendered, no required JavaScript, machine-readable, resilient on constrained or high-latency links.
- **M — Medium.** The disciplined everyday mobile experience.
- **L — Luxe.** The full rich experience: media, interactivity, immersion.

The profiles are contracts with budgets, negotiated over ordinary HTTP, auditable by ordinary tools. And they compose: a page can travel Sparse and *hydrate* toward Medium or Luxe on the client — low fidelity on the wire, high fidelity on the screen.

One URL. Three weights. No separate internet.

---

## Abstract

Responsive web design made the web adapt to screens. It did not make the web adapt to networks, cost, latency, urgency, battery, accessibility needs, or machine consumption. Modern pages are routinely delivered as large, script-heavy applications even when the consumer needs only a small amount of critical information — a flight gate, a storm warning, a balance, a confirmation.

This paper proposes **S—ML Web**, a lightweight profile layer for the existing web. S—ML defines three delivery profiles — Sparse, Medium, and Luxe — for the same canonical resource, discoverable and negotiable over standard HTTP, with declared budgets that tooling can audit. It further proposes **hydration across profiles**: the Sparse representation acts as the durable wire format from which richer profiles can be reconstructed client-side when conditions allow.

S—ML is not a new protocol, not a replacement for HTML, and not a parallel internet. It is a delivery contract: one resource, multiple weights, negotiated by context.

---

## 1. Introduction

The web is the universal publishing and application platform. A single URL can point to a news story, a bank transaction, a government form, a boarding pass, an emergency alert, or a medical instruction.

Yet the representation delivered at that URL is usually optimized for abundance: fast networks, low latency, powerful devices, large batteries, modern browsers, cheap data, and continuous connectivity. These assumptions do not always hold. A user may be roaming, on a weak cell, connected via satellite, conserving battery, on an older device, relying on assistive technology, or reaching for information in an emergency. Increasingly, the consumer may not be a human at all, but an AI model, crawler, summarizer, agent, indexer, or archiver that needs the semantic core of a page far more than its visual shell.

The web can technically serve all of these cases. What it lacks is a common **delivery contract** for them: a named, testable way for a client to ask for — and a publisher to promise — the right weight of experience.

S—ML Web proposes that contract. This is not about creating a lesser web for constrained users. It is about making the web more reliable, more efficient, more machine-readable, and more context-aware for everyone.

## 2. The Problem

### 2.1 Responsive design solved layout, not delivery

Responsive web design changed development by making pages adapt to screen size. Fluid grids, flexible media, and media queries let one page serve desktops, tablets, and phones. That solved a presentation problem.

But a page can rearrange itself beautifully on a small screen while still requiring megabytes of JavaScript, multiple font files, third-party analytics, ad code, and long chains of client-side rendering before meaningful content appears.

The layout is responsive. The payload is not.

### 2.2 The web lacks a content-weight contract

A client can request a URL, but it cannot reliably say: *give me the smallest trustworthy version of this resource.* A publisher can optimize a page, but cannot declare in a standardized, verifiable way: *this URL has a Sparse representation that preserves the core meaning and critical actions.*

Existing mechanisms each address part of the problem: responsive design adapts layout; progressive enhancement protects baseline functionality; reader modes extract content after the fact; `Save-Data` expresses a reduced-data preference; Client Hints communicate some device and network context; structured data helps crawlers; feeds provide alternate representations for some content types. What none of them provides is a **general, named, testable delivery profile** — a shared vocabulary that humans, tools, and machines can all use.

The missing piece is not another framework. It is a contract.

### 2.3 Critical paths are hostage to rich delivery

Many of the web's most important tasks should never depend on a full rich application: reading an emergency alert, checking a flight gate, viewing a bank balance, receiving a one-time code, confirming a medical instruction, submitting a government form. Yet these critical paths are routinely delivered through the same heavyweight pipeline used for immersive experiences.

Nobody wants to defend "our flood-warning page requires four megabytes of JavaScript and a tracker to load." S—ML gives teams the vocabulary to prevent it: *this page needs an S profile.*

The waste is not only experiential. Transferred bytes are the web's most direct energy proxy: every redundant megabyte is powered at the data center, across the network, and on the device — multiplied by billions of page loads a day. Payload discipline is digital sustainability by another name, and a meaningful share of the web's carbon footprint is, at root, a delivery-profile problem.

## 3. Proposal: S—ML Web

S—ML Web defines three delivery profiles for a single canonical resource:

| Profile | Name | Purpose |
|---|---|---|
| **S** | Sparse | Minimal, resilient, low-bandwidth, high-latency-tolerant, AI/crawler-friendly |
| **M** | Medium | Normal mobile and everyday connected experience |
| **L** | Luxe | Full rich experience with advanced media and interactivity |

The same resource is delivered in different profiles depending on the user's context, network conditions, device capabilities, accessibility requirements, or machine-consumption needs. The principle:

> **One URL. Three weights. No separate internet.**

S—ML works with the existing web: URLs, HTML, HTTP, TLS, CSS, structured metadata, service workers, caching, and progressive enhancement. It is best understood as **responsive delivery infrastructure**. Where responsive design asks *how should this page adapt to the screen?*, S—ML asks *how should this resource adapt to the situation?*

## 4. Profile Definitions

A note on emphasis before the definitions: two of the three profiles largely exist already. L is today's default maximalist web — turn everything up. M is established mobile-first practice: responsive CSS, media queries, optimized images. S—ML names them so they become *declared, auditable* weights rather than accidents of whatever shipped. But the standard's center of gravity is S — the profile the web is missing, and the one this specification spends its effort on.

### 4.1 S — Sparse

The Sparse profile is the minimal trustworthy representation of a resource. It is designed to survive the worst conditions — direct-to-device satellite, intermittent links, expensive or metered data, emergencies, low-power and embedded devices — and to serve the readers that never needed the interface at all: assistive technologies, crawlers, AI models, summarizers, archives, and agents.

Latency tolerance is a consequence here, not the definition. Sparse is not a "high-latency mode": on a fast, low-latency connection the same representation is simply *instant*. The benefit scales with how bad the link is — but it never disappears when the link is good. That is the kick: Sparse is the profile that wins everywhere and merely wins biggest where the network is worst.

A conforming S representation should:

- expose the canonical title, a concise summary, and the primary content or current state;
- expose critical actions;
- work without required client-side JavaScript for core content;
- avoid third-party scripts, custom fonts, and heavy media by default;
- minimize network requests and round trips;
- use semantic HTML and include machine-readable metadata;
- be server-rendered and available from the initial response;
- support caching and preserve end-to-end security.

The S profile is not a degraded page. It is the page's **durable semantic core** — fast, legible, accessible, cacheable, inspectable, and reliable. Sparse is not broken; sparse is resilient.

### 4.2 M — Medium

The Medium profile is the disciplined everyday experience: smartphones and tablets on ordinary cellular or Wi-Fi, touch-friendly layout, optimized images, moderate interactivity, progressive enhancement. JavaScript and personalization are welcome, but core content and critical actions must not be buried behind client-side complexity. M is the default for most connected use.

### 4.3 L — Luxe

The Luxe profile is the full expression: large screens, fast networks, powerful devices, high-resolution media, animation, realtime collaboration, complex visualization, immersive and application-like interfaces. Luxe is where the web can be cinematic. But Luxe is an enhancement — it must never be the *only* representation of important content.

## 5. Hydration: LoFi on the Wire, HiFi on the Screen

A natural objection to profiles is that they sound like three separate builds of every page. They are not — and the reason is hydration.

The insight is familiar from MDX and from modern rendering architectures: a document can travel as something small and declarative, and be **hydrated after transfer** into something richer. Markdown crosses the wire as plain text; on the client it becomes live components. Server-rendered HTML crosses the wire inert; islands of it wake up into interactive applications.

S—ML generalizes this: **the Sparse profile is the wire format; Medium and Luxe are hydration states.** Content is transferred LoFi and rendered HiFi — informally, *HyFi*: hydratable fidelity.

Concretely, a client on a constrained link fetches the S representation — the semantic core, a few kilobytes, meaningful immediately. If and when conditions allow (bandwidth appears, the cache warms, the user opts in), the client hydrates upward: pulling optimized media to reach M, or the full interactive layer to reach L. The upgrade is incremental and interruptible. If the link drops mid-hydration, the user still has a complete, usable page — because S was complete on arrival.

This inverts the failure mode of today's web. A modern SPA that loses its connection mid-load leaves the user with a blank shell: HiFi on the wire, nothing on the screen. An S—ML page that loses its connection mid-hydration leaves the user with the whole story, minus decoration.

### 5.1 Doesn't hydration make M and L redundant?

If S can hydrate all the way to Luxe, why define M and L at all? And conversely — islands architecture, server components, and resumability frameworks already do partial hydration, so what does S—ML add?

The answer to both is the same: **hydration is a technique; S—ML is the contract.**

Today's hydration strategies are private implementation details of individual frameworks. There is no way for a client to *request* the un-hydrated core, no way for a publisher to *promise* that the core is complete and self-sufficient, and no way for a tool to *verify* either claim. A framework can ship a beautiful islands architecture whose baseline HTML is still 900 KB and meaningless without JavaScript — and nothing calls that out.

S—ML names the layers and puts budgets on them. S is not "whatever happens to be in the initial response"; it is a certified representation with declared guarantees. M and L are not "whatever the bundle grows into"; they are declared weights a client can request directly — because many clients (a seatback screen, a crawler, an AI agent, a metered connection) will *never* want to hydrate past a given profile, and must be able to say so.

So hydration does not replace the profiles. It is the preferred way to *implement* them from a single source: author the semantic core once, and let M and L be enhancement layers over it rather than separate products. The contract makes the technique legible, requestable, and testable — which is precisely what the technique alone has never had.

### 5.2 The everyday analogy: progressive image loading

For anyone who has watched a progressive JPEG load — a recognizable image appearing immediately, then sharpening as more bytes arrive — S—ML is that idea applied to entire pages: a useful first pass, refined by further passes when conditions allow.

But the analogy earns its keep only with its two differences stated. First, *completeness*: nobody wants a progressive image that stops after one pass, because an image's first pass is a preview — legible, but degraded. The Sparse pass is not a preview. It is the complete information of the page — everything the reader came for, minus the decoration. Stopping at Sparse is not settling for a blur; it is receiving the whole message at the lowest cost. Second, *negotiation*: a progressive image always refines to full resolution if the bytes keep coming — the client has no say. Under S—ML, refinement is a contract term: a client can request the first pass and stop there, a publisher promises that pass is genuinely complete, and a tool can verify both.

S—ML is progressive loading with a contract — and a complete first pass.

> Cache Sparse. Serve Medium. Enhance to Luxe.

## 6. S—ML and AI

The name reads three ways, and all are intended: **S**parse–**M**edium–**L**uxe; **S — ML**, the Sparse profile as the representation machine learning reads; and plain **sml** — "small" with the vowels compressed out, which is exactly what the Sparse profile does to a page.

S—ML is naturally AI-friendly. Models, crawlers, summarizers, and agents need the semantic meaning of a page more than its visual presentation — yet today they must parse large, noisy documents full of layout wrappers, scripts, navigation, cookie banners, and tracking code before reaching the content.

A useful analogy is Markdown front matter: a compact YAML header that tells the reader what a file is about before the body is parsed. A web resource should offer the same orientation layer. Example:

```yaml
profile: S
canonical: https://example.com/flight/BA123
title: "BA123 London to Lisbon"
summary: "Flight BA123 departs from Gate B12. Boarding begins at 14:35."
type: flight_status
updated: 2026-07-07T12:30:00Z
critical_state:
  status: boarding
  gate: B12
critical_actions:
  - text: "Show boarding pass"
    href: "/flight/BA123/boarding-pass?profile=s"
profiles: [s, m, l]
```

For AI systems, S—ML offers lower token and bandwidth cost, cleaner extraction and summarization, more reliable citation, clearer canonical identity, easier action discovery, and better alignment between what publishers intend and what machines infer. For publishers, it is a way to expose meaning deliberately rather than surrendering it to scraping heuristics.

The Sparse profile becomes the page's **public semantic minimum** — and, in hydration terms, the exact artifact a machine consumes is the same artifact a browser hydrates. One core, every reader.

### 6.1 AI as author: the vibe-coding web

AI is not only a reader of the web; it is rapidly becoming its principal author. A growing share of new websites is generated conversationally — "vibe coded" — by people with no background in performance engineering, and often no awareness that a page *has* a weight. The generation tools they use inherit their defaults from the existing web's norms, which means the bloat of the modern web is now being amplified at machine speed: every generated landing page ships the full framework, the font pack, the animation library, and the analytics snippet, because that is what the training distribution looks like. The people least equipped to notice the problem are now producing the most pages.

S—ML addresses this at the layer where it can actually be fixed: not the author, but the tooling. A generation tool, agent skill, or scaffold that targets the S—ML contract produces conformant pages regardless of what its user knows. The author says "make me a site"; the tooling authors the semantic core first, layers enhancements behind profile gates, sets the negotiation headers, and runs the audit — and the notion of hydration is *inferred*, not something the author ever needs to learn. The standard's most demanding concepts become implementation details of the tools.

This inverts the classic adoption problem. Web standards have historically spread at the speed of developer education — millions of humans individually persuaded to change their habits. In a vibe-coded web, conformance spreads at the speed of tooling updates: encode the contract into the handful of generation tools, skills, and templates people actually use, and every page they emit is born conforming. The vibe coder gets resilience, AI-readability, and performance without asking for them; the web gets a generation of new pages that are light by default. Vibe code at ease — the tooling knows the standard so the author doesn't have to.

## 7. Discovery and Negotiation

S—ML works with ordinary URLs. A basic implementation may use explicit parameters:

```
https://example.com/article/123?profile=s
```

A mature implementation negotiates over HTTP:

```
Client:  Accept-Profile: s
         Save-Data: on

Server:  Content-Profile: s
         Available-Profiles: s, m, l
         Content-Budget: 42kb
```

And declares alternates in HTML:

```html
<link rel="alternate" type="text/html" data-profile="s" href="?profile=s">
```

(`data-profile` uses `data-*`, HTML's valid extension mechanism, and stays as plain as the header names it mirrors. A future standards-track version could graduate to an unprefixed `profile` attribute.)

The exact syntax should evolve through prototypes and standards discussion. The principles are fixed: clients can request a profile; servers declare what they delivered; crawlers and AI systems can discover the Sparse representation; audit tools can test conformance. Negotiation should build on existing mechanisms like `Save-Data`, and must prefer explicit user preference over silent device sniffing to avoid enlarging fingerprinting surface.

## 8. Conformance and Budgets

S—ML must be measurable. A page must not claim Sparse support while shipping a large application that hides content until hydration completes. A proposed early budget model:

| Requirement | S | M | L |
|---|---|---|---|
| Initial payload | ≤ 50 KB | ≤ 500 KB | Open |
| Core content without JS | Required | Recommended | Optional |
| Third-party scripts | None by default | Limited | Allowed |
| Custom fonts | Avoid | Optional | Allowed |
| Required round trips | ≤ 2 | ≤ 5 | Open |
| Machine-readable summary | Required | Recommended | Recommended |
| End-to-end TLS | Required | Required | Required |

A clarification on the JavaScript row, because it is the most debated: the rule measures **dependency, not presence**. Scripts are permitted in every profile and simply count against the payload budget — which weights them automatically, and rewards tree-shaken, profile-gated bundles. What Sparse requires is that core content and critical actions survive with scripting *unavailable*, because for many Sparse readers — e-ink browsers, crawlers, agents, embedded clients — JavaScript is not slow; it is absent. A pure weight limit on scripts would not protect those readers; the dependency rule does, and the byte budget handles the weight.

An audit tool makes the contract real:

```
$ npx sml-audit https://example.com/weather-alert

S Profile: FAIL
- Initial payload: 184 KB, budget: 50 KB
- Main content unavailable without JavaScript
- 7 third-party requests before main content
- Missing machine-readable summary

M Profile: PASS
L Profile: PASS
```

The exact thresholds should be debated. The existence of budgets should not. S—ML should feel like a missing Lighthouse category — a contract, not a vibe.

The budgets also read directly as carbon budgets. A page that declares and meets S has, in the same breath, declared and met a data-carbon ceiling — giving digital-sustainability teams the thing "green web" pledges have chronically lacked: a named, auditable unit of reduction.

## 9. Sector Perspectives

### 9.1 Satellite connectivity

Direct-to-device satellite is extending the web into places where terrestrial networks are unavailable, congested, damaged, or uneconomical. Satellite links are constrained not just in bandwidth but in latency, link availability, spectrum efficiency, power, beam capacity, and cost per delivered bit.

The cellular industry has already made the architectural move S—ML proposes — one layer down. 3GPP's Non-Terrestrial Networks (NTN) work, normative since Release 17, standardizes satellite access (LEO, MEO, GEO, high-altitude platforms) as an *extension of the 4G/5G architecture* rather than a proprietary parallel system: the cell tower is simply no longer on the ground. That is precisely the design decision S—ML makes at the application layer — extend the existing standard, never fork it:

> **3GPP NTN** — satellite-aware cellular connectivity.
> **S—ML Web** — satellite-aware web delivery.

The two are complementary, not competing. NTN solves access: cellular-grade connectivity over the satellite link. It cannot solve what applications push across that link. A standards-compliant NTN connection dutifully delivering an 8 MB script-heavy page is a solved network layer serving an unsolved application layer. S—ML completes the stack — and the pitch to operators writes itself: NTN made your satellites part of the cellular standard; S—ML makes the web's payloads worthy of the link.

S—ML gives operators and their partners a way to say **"this service is satellite-ready"** — not via a separate satellite web, but because it supports a Sparse profile designed for constrained delivery. Immediate applications include emergency messaging, weather and disaster information, lightweight government services, travel and logistics updates, maritime and remote field operations, and AI-assisted retrieval over limited links. Hydration fits this environment precisely: deliver S over the satellite link, hydrate toward M or L from cache or when a terrestrial network returns. And when a user needs only the Sparse representation, the network is never forced to carry the Luxe one — good for users, publishers, and operators alike.

### 9.2 Aviation and inflight entertainment

The aviation industry is moving toward web-based passenger, crew, and operational interfaces — IFE systems, passenger portals, onboard retail, safety information, crew tools. Aircraft cabins are a distinctive delivery environment: intermittent high-latency satellite backhaul shared across hundreds of passengers, embedded browsers on certified hardware lifecycles, offline operation, multilingual content, and strict reliability expectations.

S—ML maps directly onto this. The same resource serves the S profile for flight status, gate and connection information, safety content, and critical notices; the M profile for the seatback and passenger-device portal; the L profile for rich entertainment discovery, interactive maps, and commerce when bandwidth and hardware allow. The operational strategy is the hydration strategy: **cache Sparse, serve Medium, enhance to Luxe.**

### 9.3 Travelers, roaming, and data-constrained users

The most universal beneficiary of the Sparse profile needs no special hardware or industry at all: anyone whose data is expensive relative to their need. The traveler on a roaming plan where a single modern page load costs real money. The user in a remote area rationing a weak connection. The person on a metered or prepaid plan for whom data cost is a daily budgeting decision. For all of them, today's web offers a bad bargain: to read a train time, they must buy the whole application.

There is strong historical evidence of this demand. Initiatives such as Facebook's Lite clients and the Free Basics program demonstrated that lightweight delivery unlocks enormous audiences in connectivity-constrained and cost-constrained markets. But they also demonstrated the wrong architecture: a curated subset of the web, mediated by a single company, drew sustained net-neutrality criticism and regulatory rejection precisely because a gatekeeper decided which services deserved to be light. The demand was validated; the delivery model was not. S—ML answers the same demand as an open contract: *every* URL can carry a Sparse representation, no gatekeeper chooses the catalog, and the same standards and security apply everywhere.

The mechanism for these users is deliberately simple: a pinned browser preference. A user should be able to set "Sparse only" for a trip, a network, or permanently — one setting, sent as `Accept-Profile: s`, honored by every conforming site (the specification already requires user agents to support exactly this, and treats `Save-Data: on` as the same request). Operators can build on it too: a "roaming mode" that pins Sparse could be offered at the plan level, cutting subscriber bills and network load in the same gesture — data saving as a delivery contract rather than a compression proxy.

The same binding extends naturally to battery. Bytes cost energy twice — once at the radio, again in parsing, script execution, and rendering — so a device conserving power should also be conserving weight. Browsers already gesture at this: Safari, for example, stops videos auto-playing when Low Power Mode is on. S—ML turns that scattering of ad-hoc mitigations into one coherent behavior: **battery saver on → user agent requests `Accept-Profile: s`**, and the whole page arrives lighter, not just its videos. Done this way the signal is also privacy-preserving: the site never learns the battery level (a signal browsers have historically had to withdraw from page access precisely because it was abused for tracking) — it only receives a profile request, which the user agent mediates and the user can override.

## 10. The Human Argument: An Inhabited Internet Needs a Quiet Layer

The environmental historian Laura J. Martin observes that "the internet has stopped being a place we visit — it's now an environment we inhabit" ([Noema, 2026](https://www.noemamag.com/limiting-not-just-screen-time-but-screen-space/)): what began as a window fixed in domestic space has become weather, an ambient condition we move through and adapt our bodies to. That trajectory is real, and this paper does not argue against it. The immersive, spatial, inhabited internet is the honest destination of the L profile — Luxe exists precisely because some of the web's most valuable experiences are environments, and they deserve first-class support.

But Martin's deeper claim cuts the other way, and S—ML should answer it. We have learned to treat the internet, AI, and the "cloud" as placeless and infinite, when in fact the cloud is heavy industry and humans live in bodies, in shared physical rooms. An internet that is only environment offers no exit: today, even glancing at a train time means stepping into weather — pages engineered to extend the visit, feeds with no wings and no place to step off. The old web had an ethic of interruption ("brb" — the body in a room, waiting to return); the modern web deleted it, and with it the ability to *visit* the internet at all.

The S profile is that ability, restored as infrastructure. It is the information-only layer: get the fact, perform the action, return to the room. Its byte budgets double as attention budgets — no autoplay, no third-party engagement machinery, nothing whose economic job is to detain. S is the web's quiet room inside the inhabited house: not a retreat from the digital, but a lighter way of touching it, available at every URL rather than only at a "digital detox."

This also dignifies a class of hardware the heavy web has abandoned: deliberately minimal, "mono" devices — e-ink readers, distraction-free phones, wearables, single-purpose terminals. Under S—ML these are not degraded clients squinting at a desktop site; they are full citizens of the web, served a representation designed for them. Choosing a lighter relationship with the internet should not mean losing access to it.

S—ML does not moralize between immersion and restraint. It makes the weight of an experience the reader's choice rather than the publisher's default — which is precisely what a healthy physical–digital balance requires. Limit screen time, limit screen space — and let people choose their screen weight.

## 11. Relationship to Existing Practice — and What S—ML Is Not

S—ML aligns with, and packages, existing web principles: progressive enhancement, semantic HTML, accessibility, structured data, responsive design, performance budgets, sustainability, offline-first design, and privacy-preserving preferences. It replaces none of them; it gives them a shared, testable vocabulary.

History offers a caution here. Earlier attempts to serve constrained clients — separate mobile markup, operator gateways, parallel content ecosystems — failed because they built a second web beside the web. S—ML deliberately takes the opposite path: it never leaves the web's standards, URLs, or security model.

S—ML is **not**: a new browser, a replacement for HTML or responsive design, a new framework, a new transport protocol, a carrier gateway, a separate satellite internet, a stripped-down web for constrained users, or a revival of WAP.

S—ML **is**: a delivery-profile standard, a publishing discipline, a conformance target, an AI-readable content contract, and a vocabulary for context-aware web delivery.

## 12. Status and Roadmap

S—ML is a community specification and tooling effort, useful with today's web from day one — no browser changes required.

**Available now:** S—ML Web Profile 0.1, the draft specification, published as a standalone document (see Normative Specification below); `sml-audit`, an open-source, zero-dependency conformance CLI with CI-friendly output; and the project site — which itself conforms to the Sparse profile it describes.

**On the roadmap:** a reference demonstration of one URL rendered in all three profiles, including hydration across a degrading link; CI recipes and a GitHub Action; adapters and examples for content-first frameworks; conformance badges; and, as independent implementations appear, a W3C Community Group to carry the specification forward.

**How to participate:** implement a Sparse representation for one critical page and run the auditor against it. Bring the results — including disagreements with the budgets and edge cases the spec doesn't cover — back to the community. Teams operating under real delivery constraints (satellite and constrained-network services, aviation, emergency information, public sector, embedded web) are especially invited to pilot, because their conditions are the ones the Sparse profile must be proven against.

The premise anyone can act on today, no coordination required: **the critical path should work in Sparse mode.**

## 13. Design Decisions and Open Questions

### 13.1 Resolved for 0.1

1. **Naming.** The profiles are **Sparse**, **Medium**, and **Luxe** — one name per profile, used identically in prose, marketing, and spec text. No split between a technical term and a public term; the split itself would be a source of confusion. "Mobile" may be used informally to describe the Medium profile's typical context, but the profile's name is Medium.
2. **Budgets.** The default Sparse budget is 50 KB initial payload, expressed as the budget class `S-50`. Declared classes allow finer contracts where one threshold is too coarse: `S-14` (fits within a typical first TCP/QUIC congestion window — one round trip, content on screen), `S-50`, `S-100`, and `M-500`, `M-1000`. A page declares its class; the auditor holds it to it.
3. **JavaScript in Sparse.** Core content and critical actions must never *require* JavaScript. JavaScript itself is not banned: scripts are welcome within the byte budget, which in practice rewards tree-shaken, minimal, profile-gated bundles. The constraint is dependency, not presence.
4. **Negotiation privacy.** `Accept-Profile` is a single low-entropy header with three possible values, set by explicit user or user-agent preference, with no vendor extensions permitted. Servers must not infer profiles from fingerprinting-adjacent signals. This follows the precedent set by `Save-Data`.
5. **Machine-readable layer.** JSON-LD, complementing (not replacing) the meta description. It is already understood by crawlers, validators, and AI systems; inventing a parallel format would repeat the mistake this standard exists to avoid.
6. **Form state across hydration.** Resolved by construction: a critical form must be the *same element* across profiles — same action, same method, same field names. Hydration may enhance its presentation but never replaces it, so state entered at Sparse weight survives an upgrade to Medium or Luxe because the form never changed.
7. **Tooling integration.** Conformance auditing should live everywhere developers already look: CLI, CI, and eventually browser developer tools as a Lighthouse-class category. The measurement layer should be free and ubiquitous.
8. **Governance.** Staged. Now: a community specification with reference tooling, iterated through real deployments. Next: a W3C Community Group as adoption grows. Then: formal standards-track submission (the HTTP headers likely via the IETF) once multiple independent implementations exist. Standardizing before implementations exist would trade momentum for committee time.

### 13.2 Still open

1. **Content equivalence verification.** How should tooling verify that profiles agree on title, summary, state, and critical actions — particularly when Medium and Luxe are authored separately rather than hydrated from Sparse? A hierarchical correspondence (matching headings, sections, and actions across representations) is the likely direction.
2. **Authenticated and personalized resources.** How should Sparse representations of logged-in pages work — privacy-safe critical-state subsets, private cache scoping, prioritization of which personalized state belongs in the Sparse core? This needs prototyping with a real transactional service before it is specified.
3. **Advertising.** How do ad-supported publishers participate? Sparse's budgets exclude third-party ad tech by construction, but advertising itself is not banned: a first-party, inline, lightweight ad — closer to a print placement or a text ad than to programmatic display — fits within budget. Whether Sparse needs a standardized lightweight ad unit, and whether publishers will accept profile-dependent monetization, is open — and probably decisive for news adoption.
4. **Declarative profile syntax.** Should profiles get first-class CSS/HTML syntax, letting authors express delivery weight in the same idiom responsive design uses for screens — for example a media query like `@media (profile: sparse)`, aligned with the existing `prefers-reduced-data` proposal, or standardized attributes for profile-gated resources? This would make profile authoring feel native to web developers rather than bolted on.

## 14. Conclusion

The web should not assume abundance. A resource may be consumed on a fast desktop, a satellite-connected handset, an aircraft seatback, an assistive reader, or by an AI model trying to understand the page. These are no longer edge cases; they are normal conditions of a planetary web.

Responsive design made the web flexible at the level of layout. The next evolution is responsive delivery: one canonical resource, published once, delivered by constraint — small enough to survive any link, and hydratable to the richest experience the situation allows. A web that fits the situation is also a web that wastes less: fewer bytes moved is fewer joules burned, at planetary scale.

One URL. Three weights. No separate internet.

Sparse for resilience. Medium for mobility. Luxe for full expression.

That is S—ML.

---

## Normative Specification

The normative text of this proposal — **S—ML Web Profile 0.1 (Draft)** — is maintained as a standalone document so it can version independently of this paper. It defines the profile identifiers, discovery, negotiation rules, the Sparse representation's requirements, budgets and budget classes, content equivalence, hydration rules, conformance, and security and privacy considerations.

Read it at [**/spec/**](/spec/) (raw Markdown: [`/downloads/spec.md`](/downloads/spec.md)).
