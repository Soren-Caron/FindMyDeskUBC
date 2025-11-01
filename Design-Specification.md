The problem is discussed in the readme.md

Here we will discuss a high level overview of what the solution would look like:

The UBC Smart Study-Space Finder is a responsive web application (desktop + mobile) that helps UBC students easily locate ideal study spaces across campus. It focuses on simplicity, accessibility, and fast development while delivering meaningful, data-driven recommendations.

- Core User Features

- Search or browse an interactive campus map for study spaces.

- Filter by preferred features:

Quiet | Plugs | Whiteboard | Group | Natural Light | 24/7 Access

- View availability indicators for each spot:

Status: Available / Busy / Unknown

Availability Score (0–100) — an easy-to-read metric based on recent data.

- Check in to a spot (crowdsourced presence) and optionally:

Report missing features

Leave a short status note (e.g., “too noisy,” “lots of outlets”)

- See short-term predicted availability (next 2 hours) using lightweight statistical prediction.

- Bookmark favorite spots and optionally set simple alerts (stretch feature).

- MVP (Minimum Viable Product) Approach

Data Sources:

Real-time and predictive availability derived from crowdsourced check-ins and historical time-of-day patterns.

No reliance on campus hardware sensors or paid APIs.

Design Principles:

Minimal number of screens and simple, intuitive user flows.

Mobile-first responsive layout.

Lightweight, fast-loading interface that allows the development team to ship quickly while maintaining a polished experience.
