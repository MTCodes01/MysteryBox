# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Live event attendees anonymously uploading and rating design posters during a session. A secondary user is the Event Host who manages the live session, controls phases, and reveals leaderboards.

## Product Purpose
A real-time, WebSocket-driven live voting experience with host controls and live leaderboards. Designed to facilitate quick, engaging, and anonymous poster rating competitions during live events. Success means seamless real-time syncing between host and participants.

## Positioning
An ephemeral, live-synchronized design competition tool where the host controls the pacing and the audience rates submissions synchronously, unlike persistent gallery platforms.

## Operating Context
Used during live events, workshops, or classrooms where a presenter projects the host dashboard or QR code to an audience, and attendees participate simultaneously via their mobile or desktop devices.

## Capabilities and Constraints
- Built with FastAPI, WebSockets, and SQLite.
- Frontend uses static HTML/CSS (Tailwind via CDN) and vanilla JavaScript. No frontend build step or framework is used.
- Must remain highly responsive to handle simultaneous WebSocket state changes.

## Brand Commitments
The modern premium dark zinc theme (`bg-zinc-950`) with glassmorphism cards and vibrant indigo/violet gradients must be preserved. 
Fonts: `Outfit` for headings, `Inter` for body.

## Evidence on Hand
Current implementation has a functional upload flow, slider rating interface, and live leaderboard revealed by the host.

## Product Principles
- **Synchronicity:** The experience must stay tightly synced with the host's control phases.
- **Anonymity & Fairness:** Submissions and ratings are anonymous until the leaderboard reveal.
- **Premium Simplicity:** The UI must feel polished, modern, and reduce cognitive load for quick live interaction.
