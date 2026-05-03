# VenueIQ — Design Structure Document
## Layout and Component Architecture Only

---

## APPLICATION SHELL

The application is a single-page React app with client-side routing.
It has five pages: Landing, Dashboard, Chat, Community, and Staff Portal.

The shell renders two persistent elements on every page: the navigation
bar fixed to the top of the viewport, and the alert notification container
fixed to the top-right of the viewport below the navbar. Everything else
is page-specific content that mounts and unmounts on navigation.

---

## NAVIGATION BAR

Height: 64px
Position: fixed, top 0, full viewport width, z-index 100

Layout: horizontal flex row, space between, vertically centered
Left side padding: 32px
Right side padding: 32px

Left region contains:
- Logo mark: 32px square with 8px border radius
- Wordmark: single text element immediately right of logo mark
- Gap between logo mark and wordmark: 10px

Right region contains:
- Navigation pills in a horizontal flex row with 8px gap
- Pills in order: Home, Live Status, Concierge, Community
- Primary CTA button to the right of the pills with 8px left margin

Each navigation pill:
- Padding: 8px vertical, 16px horizontal
- Border radius: 100px

Primary CTA button:
- Padding: 9px vertical, 20px horizontal
- Border radius: 100px

Scroll behaviour: on initial render the navbar background is transparent.
After the user scrolls past 40px the navbar gains a frosted background.
Transition duration: 400ms.

On the Staff Portal page the primary CTA button is hidden.

Mobile behaviour: below 768px viewport width the navigation pills collapse.
Only the logo and a hamburger menu icon remain visible. The hamburger
opens a full-width drawer from the right containing the navigation items
stacked vertically.

---

## ALERT NOTIFICATION CONTAINER

Position: fixed, top 72px, right 16px, z-index 200
Width: 320px
Layout: vertical flex column with 8px gap between alert cards
Maximum alerts visible simultaneously: 5

Each alert card:
- Width: 100%
- Padding: 14px vertical, 16px horizontal
- Border radius: 14px
- Layout: vertical flex column

Inside each alert card top row:
- Left: severity icon, 20px square
- Right: dismiss button, 24px square, flex centered
- Space between layout

Below top row:
- Alert title: single line text
- Alert message: multi-line text, maximum 3 lines
- Action button (conditional, only if action label exists): pill shape

Entry animation: slides in from right. Starts at translateX(340px) opacity 0.
Arrives at translateX(0) opacity 1. Duration 400ms.
Exit animation: slides out to right. Duration 250ms.

---

## LANDING PAGE

### Page Container
Min height: 100vh
Overflow-x: hidden
Layout: vertical flex column

### Hero Section
Min height: 100vh
Layout: vertical flex column, centered both axes
Padding top: 120px (clears navbar)
Padding bottom: 80px
Padding left and right: 24px
Text alignment: center
Position: relative (contains absolutely positioned background layers)

Background layer order bottom to top:
1. Grid texture (absolutely positioned, fills section)
2. Radial glow (absolutely positioned, centered at 50% horizontal 30% vertical)
3. Content (positioned in normal flow)

Content stack top to bottom with these spacing gaps:
- Badge pill: inline-flex, auto width, margin bottom 32px
- H1 headline: max width 800px, centered, margin bottom 24px
- Paragraph: max width 520px, centered, margin bottom 48px
- Button row: horizontal flex, centered, gap 12px, flex wrap
- Stat row: horizontal flex, centered, gap 48px, margin top 80px, flex wrap

Badge pill:
- Padding: 6px top and bottom, 8px left, 14px right
- Border radius: 100px
- Internal layout: horizontal flex, gap 8px, vertically centered
- Contains: pulsing dot (6px circle) + text

Button row contains two buttons side by side.
Stat row contains four stat items.
Each stat item: vertical flex, text alignment center, gap 4px between value and label.

### Story Section
Padding bottom: 80px

Section header:
- Centered, max width 800px, margin 0 auto
- Padding bottom: 56px
- Contains: section label above heading, gap 16px

Horizontal scroll container:
- Full viewport width, no max width
- Padding: 0 32px 32px
- Overflow-x: auto, scroll-snap-type x mandatory
- Scrollbar hidden
- Horizontal flex row, gap 16px, no wrap

Each story card:
- Width: 340px, flex shrink 0
- Height: 460px
- Border radius: 24px
- Scroll snap align: start
- Position: relative, overflow hidden
- Cursor: pointer

Inside each card position absolute layers bottom to top:
1. Background image: fills card, object-fit cover
2. Gradient overlay: fills card
3. Content layer: fills card, padding 28px

Content layer layout: vertical flex, space between
Top of content: tag label
Bottom of content: headline, subtitle (gap 16px below headline),
stat chip (gap 24px below subtitle)

Stat chip:
- Display: inline-flex, flex direction column
- Padding: 12px vertical, 20px horizontal
- Border radius: 16px

Slide dots row:
- Horizontal flex, centered, gap 8px
- Margin top: 8px
- Each dot: height 8px, border radius 4px
- Active dot width: 24px
- Inactive dot width: 8px

### How It Works Section
Padding: 80px 32px
Max width: 1100px, centered

Section header: centered, margin bottom 56px

Agent cards grid:
- Display: grid
- Grid template columns: repeat auto-fit, minimum 280px
- Gap: 16px

Each agent card:
- Padding: 28px
- Border radius: 20px

Inside each agent card top to bottom:
- Icon container: 48px square, 14px border radius, margin bottom 20px
- Tech label: single line, margin bottom 8px
- Agent name heading: margin bottom 12px
- Description paragraph

### CTA Section
Margin: 40px 32px 80px
Border radius: 28px
Padding: 72px 40px
Text alignment: center
Position: relative (contains radial glow layer)

Content inside: heading, paragraph (max width 480px, centered, margin top 16px),
single button (margin top 40px)

---

## LIVE STATUS DASHBOARD PAGE

Page padding: 96px top, 32px sides, 60px bottom
Max width: 1100px, centered

### Page Header
Horizontal flex row, space between, align items flex-end
Margin bottom: 48px
Flex wrap, gap 16px

Left side: section label above heading, gap 8px between them
Right side: live dot + timestamp text, horizontal flex, gap 8px, align center

### Predictions Card
Full width
Margin bottom: 32px
Padding: 24px
Border radius: 20px

Internal layout: two-column grid on desktop, single column on mobile
Left column: card title + subtitle
Right column: four data rows stacked vertically, gap 12px

Each data row: horizontal flex, space between
Left: label text
Right: value text

Card has a pulsing border animation when surge is under 5 minutes.
Small attribution line below card, centered.

### Summary Cards Row
Display: grid
Grid template columns: repeat auto-fit, minimum 200px
Gap: 12px
Margin bottom: 32px

Each summary card:
- Padding: 20px vertical, 24px horizontal
- Border radius: 16px

Inside each card top to bottom:
- Micro label: uppercase, margin bottom 8px
- Value: large text, margin bottom 4px
- Status line: small text

### Zone Sections
Three sections stacked vertically, gap 32px between sections.

Each section:
- Section title: margin bottom 12px
- Zone cards grid below title

Zone cards grid:
- Display: grid
- Grid template columns: repeat auto-fit, minimum 240px
- Gap: 12px

Each zone card:
- Padding: 20px vertical, 24px horizontal
- Border radius: 16px
- Horizontal flex row, space between, align center

Left side of zone card: zone name above wait time, gap 6px
Right side of zone card: status pill

Status pill:
- Padding: 6px vertical, 14px horizontal
- Border radius: 100px

### Ask AI Banner
Margin top: 32px
Padding: 24px vertical, 28px horizontal
Border radius: 20px
Horizontal flex row, space between, align center, flex wrap, gap 16px

Left side: heading above subtext, gap 4px
Right side: single CTA button

---

## CHAT CONCIERGE PAGE

Page layout: vertical flex column, min height 100vh
Padding top: 64px (navbar height)
Background: same as app shell

Background grid texture: fixed position, fills viewport, pointer events none, z-index 0

### Chat Header Bar
Position: sticky, top 64px, z-index 10
Padding: 24px top, 20px bottom, 32px sides
Border bottom: 1px
Background: semi-transparent with backdrop blur

Internal container: max width 720px, centered, horizontal flex row, gap 12px, align center

Left: agent avatar container, 40px square, 12px border radius
Right of avatar: two lines stacked
  Top line: agent name
  Bottom line: horizontal flex row, gap 6px — pulsing dot + status text

### Message Thread Container
Flex: 1 (fills available height)
Overflow-y: auto
Padding: 24px all sides
Max width: 720px, centered
Display: vertical flex column, gap 16px
Position: relative, z-index 1

User message row:
- Horizontal flex, justify flex-end

User message bubble:
- Max width: 76% of thread width
- Padding: 12px vertical, 18px horizontal
- Border radius: 20px top-left, 20px top-right, 20px bottom-left, 6px bottom-right

AI message row:
- Horizontal flex, justify flex-start, align items flex-start

AI avatar:
- 28px square, 8px border radius
- Margin right: 10px
- Margin top: 4px
- Flex shrink: 0

AI message bubble:
- Max width: 76% of thread width
- Padding: 16px vertical, 20px horizontal
- Border radius: 6px top-left, 20px top-right, 20px bottom-right, 20px bottom-left

Timestamp line inside every bubble:
- Margin top: 8px
- Right-aligned for user bubbles, left-aligned for AI bubbles

Typing indicator row:
- Same layout as AI message row
- Bubble contains three dots in horizontal flex row, gap 6px

### Quick Prompt Pills Row
Padding: 12px top, 32px sides, 0 bottom
Max width: 720px, centered
Horizontal flex row, gap 8px, overflow-x auto, scrollbar hidden, no wrap

Each pill:
- Padding: 8px vertical, 14px horizontal
- Border radius: 100px
- Horizontal flex row, gap 6px, align center
- White space: nowrap
- Contains: emoji + label text

### Input Area
Padding: 16px top, 32px sides, 32px bottom
Max width: 720px, centered, relative positioned, z-index 10

Input container:
- Horizontal flex row, align items flex-end, gap within padding
- Padding: 8px top, 8px right, 8px bottom, 20px left
- Border radius: 16px

Inside container:
- Left: textarea, flex 1, transparent background, no border, no outline
- Right: send button, 40px square, 10px border radius, flex shrink 0

Attribution line below input:
- Centered
- Margin top: 10px

---

## COMMUNITY PAGE

Page padding: 96px top, 32px sides, 60px bottom
Max width: 900px, centered

### Page Header
Section label above heading, gap 16px
Margin bottom: 40px

### Post Composer
Full width
Margin bottom: 32px
Padding: 20px
Border radius: 20px

Inside composer top to bottom:
- Textarea: min height 80px, full width, no resize
- Bottom row (horizontal flex, space between, align center):
  - Left: type selector (horizontal flex row of pill buttons, gap 8px)
  - Right: post button (pill shape)

### Feed Layout
Vertical flex column, gap 12px

Each community post card:
- Padding: 20px
- Border radius: 16px
- Vertical flex column, gap 12px

Post card top row:
- Horizontal flex, space between, align flex-start
- Left: author name + location tag (horizontal flex, gap 8px, align center)
- Right: timestamp + type tag (horizontal flex, gap 8px, align center)

Post card body:
- Post text, full width

Post card bottom row:
- Horizontal flex, space between, align center
- Left: helpful vote button (horizontal flex, gap 6px) + vote count
- Right: optional AI reviewed badge (if post was cross-referenced)

Organizer advisory card uses same structure but has a verified badge in
the top row and is visually distinguished from community posts. Pinned
advisories appear above all community posts regardless of timestamp.

---

## STAFF PORTAL PAGE

Page padding: 96px top, 32px sides, 60px bottom
Max width: 700px, centered

### Page Header
Section label above heading above subheading
Gaps: 8px between label and heading, 16px between heading and subheading
Margin bottom: 40px

### Staff ID Input
Full width
Height: 48px
Border radius: 12px
Margin bottom: 24px

### Report Textarea
Full width
Min height: 120px
Border radius: 12px
No resize handle
Padding: 16px
Margin bottom: 16px

### Submit Button
Full width
Height: 52px
Border radius: 12px
Margin bottom: 24px

Loading state: shows spinner centered in button
Success state: shows checkmark, held for 2 seconds, then resets

### Result Card (conditional, shown after submission)
Full width
Padding: 16px
Border radius: 12px
Margin bottom: 24px
Vertical flex column, gap 8px

Contains: success label, zone updated text, action taken text,
optional redirect suggestion text

### Incident Feed Section
Section heading: margin bottom 16px

Incident list: vertical flex column, gap 10px

Each incident card:
- Padding: 14px
- Border radius: 10px
- Horizontal flex row, space between, align flex-start, gap 16px

Left side of incident card:
- Issue summary text above timestamp and zone text, gap 4px

Right side of incident card:
- Status pill (open or resolved)

---

## RESPONSIVE BREAKPOINTS

Desktop: 1024px and above — all multi-column grid layouts active,
full navbar visible, side-by-side layouts in headers and cards.

Tablet: 768px to 1023px — grid minimum column widths cause natural
wrapping to fewer columns, horizontal flex rows wrap where needed.

Mobile: below 768px — all grids become single column, navbar collapses
to logo plus hamburger, horizontal story scroll cards shrink to 280px
width, chat interface fills full viewport height, input area sticks to
bottom with safe area inset padding for iOS home indicator.

---

## ANIMATION CATALOGUE

Page entrance: content starts at translateY(24px) opacity 0, arrives
at translateY(0) opacity 1, duration 600ms, stagger 100-150ms per element.

Page transition: incoming page from translateY(8px) opacity 0 to
translateY(0) opacity 1, duration 400ms.

Staggered section entrance: each section delays by 100ms after previous,
uses same translateY and opacity transition.

Story card active scale: active card at scale 1.02, inactive at scale 1,
transition 400ms.

Slide dot expansion: active dot width 24px, inactive 8px, transition 300ms.

Alert slide-in: from translateX(340px) opacity 0 to translateX(0) opacity 1,
duration 400ms.

Alert slide-out: to translateX(340px) opacity 0, duration 250ms.

Navbar background transition: transparent to frosted, duration 400ms,
triggered at 40px scroll depth.

Pulsing dot: opacity alternates 1 to 0.3, duration 2s, infinite ease-in-out.

Surge border pulse: border opacity alternates 0.4 to 1.0, duration 1s,
infinite, triggered when surge event under 5 minutes.

Chat message entrance: from translateY(10px) opacity 0 to translateY(0)
opacity 1, duration 300ms, triggers on each new message append.

Typing dots: each dot translateY -6px at midpoint of 1.2s loop,
staggered 200ms per dot.

Button press: scale to 0.97 on active/pressed state, duration 100ms.

Button hover brightness: brightness 1.1 on hover, duration 200ms.

Card hover: scale 1.01 or border brightening on hover, duration 200ms.

Zone card status transition: background and border color transition when
status changes, duration 300ms.

Demo mode activation: floating banner slides up from bottom, width auto,
centered horizontally, padding 12px 20px, border radius 100px.

---

## TYPOGRAPHY SCALE

Display large: used for hero headline, story card headlines, CTA headline.
Font size: fluid clamp from 48px to 88px.
Line height: 1.05.
Letter spacing: -2px.
Font: display font.

Display medium: used for page headings, section headings.
Font size: fluid clamp from 32px to 52px.
Line height: 1.1.
Letter spacing: -1.5px.
Font: display font.

Display small: used for agent card names, stat callout values.
Font size: 24px.
Letter spacing: -0.5px.
Font: display font.

Stat large: used for hero stat values.
Font size: 32px.
Letter spacing: -1px.
Font: display font.

Body large: used for hero paragraph, CTA paragraph.
Font size: 18px.
Line height: 1.7.
Font: body font.

Body default: used for card descriptions, chat messages, community posts.
Font size: 15px.
Line height: 1.65.
Letter spacing: -0.1px.
Font: body font.

Body small: used for labels, timestamps, captions, attribution lines.
Font size: 13px.
Line height: 1.5.
Font: body font.

Micro label: used for section labels, tech tags.
Font size: 11px to 12px.
Letter spacing: 1.5px to 3px.
Font weight: 600 to 700.
Font: body font.
Transform: uppercase.

---

## ICON AND EMOJI USAGE

Venue icons used as semantic identifiers:
Stadium emoji for the AI agent avatar and logo mark.
Pizza emoji for food agent and food-related UI elements.
Map emoji for navigation agent.
People silhouette emoji for crowd agent.
Cricket ball emoji for match agent.
Red cross emoji for medical facilities.
Warning triangle for busy status alerts.
Exclamation for critical status alerts.
Circle-i for info status alerts.
Check mark for success states.
Hourglass for loading states in chat send button.
Up arrow for ready-to-send state in chat send button.
Pulsing green dot for live status indicators.

All icons are either emoji or simple SVG path elements.
No external icon library required.
All SVG icons are inline within JSX, not imported from packages.

---

*VenueIQ Design Structure Document*
*Layout and component architecture reference only*
*No color values, theme tokens, or visual styling included*
