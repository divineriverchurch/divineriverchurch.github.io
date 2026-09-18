# Divine River Church Website

## Version 1 Design System

Document Version: 1.0
Project: Divine River Church Website
Scope: Version 1 Public Website

## 1. Purpose

This document defines the shared visual and responsive rules for Version 1 of the Divine River Church website.

The design system provides a consistent foundation for all pages and reusable components.

Individual pages should use these shared rules rather than defining unrelated visual styles.

The design system must also accommodate the approved Version 1 content, including:

* the church vision;
* multiple pastors;
* pastor mobile-number actions;
* a weekly programme with multiple activities on the same day;
* two Sunday services;
* YouTube;
* Facebook;
* Google Maps.

These content requirements influence component behaviour but do not alter the overall visual architecture.

---

## 2. Design Principles

The website should be:

* clear and easy to navigate;
* respectful of the church identity;
* readable on mobile, tablet and desktop;
* visually consistent;
* suitable for both light and dark modes;
* accessible using keyboard navigation;
* sufficiently flexible for future content;
* simple enough to maintain without a large frontend framework;
* capable of displaying recurring church information without visual clutter;
* capable of distinguishing important actions such as Watch Live, Call, Facebook and Get Directions.

Version 1 will use custom CSS rather than a CSS framework.

---

## 3. Brand Colours

The current logo-derived colours are provisional until official church branding values are provided.

| Role             | Colour     | Starting Value |
| ---------------- | ---------- | -------------- |
| Primary brand    | Blue       | `#374994`      |
| Light background | White      | `#FFFFFF`      |
| Dark background  | Near black | `#161617`      |
| Secondary accent | Red        | `#902F3A`      |
| Highlight        | Yellow     | `#F4ED39`      |

Blue will remain the dominant brand colour.

Red should be used selectively.

Yellow should be used only for small highlights and emphasis.

The newly approved content does not change the current colour system.

---

## 4. Semantic Colour System

Components should use semantic colour variables instead of repeatedly using raw colour values.

Primary semantic variables include:

| Variable                | Purpose                      |
| ----------------------- | ---------------------------- |
| `--color-bg`            | Main page background         |
| `--color-surface`       | Cards and secondary surfaces |
| `--color-surface-alt`   | Alternate section background |
| `--color-text`          | Main text                    |
| `--color-text-muted`    | Secondary text               |
| `--color-border`        | Borders and separators       |
| `--color-primary`       | Main church blue             |
| `--color-primary-hover` | Primary hover state          |
| `--color-secondary`     | Church red                   |
| `--color-highlight`     | Church yellow                |
| `--color-link`          | Link colour                  |
| `--color-focus`         | Keyboard focus indicator     |

This allows light and dark themes to use the same components without rewriting component-specific styles.

---

## 5. Light Mode

The light theme should approximately use:

| Element          | Treatment          |
| ---------------- | ------------------ |
| Main background  | White              |
| Surface/card     | Very light grey    |
| Main text        | Near black         |
| Secondary text   | Dark grey          |
| Primary actions  | Church blue        |
| Secondary accent | Church red         |
| Highlight        | Church yellow      |
| Borders          | Light neutral grey |

The design should avoid excessive coloured backgrounds.

White and neutral space should remain prominent.

Approved church information such as the vision, weekly programme and leadership should remain easy to scan without competing background colours.

---

## 6. Dark Mode

The dark theme should approximately use:

| Element           | Treatment                                        |
| ----------------- | ------------------------------------------------ |
| Main background   | Near black                                       |
| Surface/card      | Dark grey                                        |
| Alternate surface | Slightly lighter dark grey                       |
| Main text         | White / off-white                                |
| Secondary text    | Light grey                                       |
| Primary action    | Lighter variation of church blue where necessary |
| Secondary accent  | Controlled red                                   |
| Highlight         | Controlled yellow                                |
| Borders           | Low-contrast grey                                |

Dark mode must preserve the same content hierarchy as light mode.

Dark mode must not require separate HTML templates.

Leadership mobile actions, programme times, social links and Maps actions must remain clearly visible in dark mode.

---

## 7. Typography

Version 1 should initially use a system font stack rather than depending on an external font provider.

Recommended stack:

`Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

If Inter is not locally available, the browser will use the next available system font.

Recommended hierarchy:

| Element | Relative Importance             |
| ------- | ------------------------------- |
| H1      | Main page title / hero          |
| H2      | Major section heading           |
| H3      | Card/subsection heading         |
| H4      | Minor subsection                |
| Body    | Normal reading text             |
| Small   | Metadata and supplementary text |

Body text should normally use a minimum size around `1rem`.

Long paragraphs should use comfortable line-height.

The church vision is short enough to be given prominent typographic treatment on the Home page without becoming difficult to read.

---

## 8. Typography Scale

Initial scale:

| Token              | Starting Size |
| ------------------ | ------------- |
| `--font-size-xs`   | `0.75rem`     |
| `--font-size-sm`   | `0.875rem`    |
| `--font-size-base` | `1rem`        |
| `--font-size-lg`   | `1.125rem`    |
| `--font-size-xl`   | `1.25rem`     |
| `--font-size-2xl`  | `1.5rem`      |
| `--font-size-3xl`  | `2rem`        |
| `--font-size-4xl`  | `2.5rem`      |
| `--font-size-5xl`  | `3.25rem`     |

Large headings may use responsive sizing.

The vision section may use `--font-size-2xl` or larger depending on viewport width and surrounding layout.

---

## 9. Spacing System

Use a shared spacing scale.

| Token       | Value     |
| ----------- | --------- |
| `--space-1` | `0.25rem` |
| `--space-2` | `0.5rem`  |
| `--space-3` | `0.75rem` |
| `--space-4` | `1rem`    |
| `--space-5` | `1.5rem`  |
| `--space-6` | `2rem`    |
| `--space-7` | `3rem`    |
| `--space-8` | `4rem`    |
| `--space-9` | `6rem`    |

Components should use this scale rather than arbitrary spacing wherever possible.

Programme rows and leadership cards should use enough internal spacing to keep names, times and actions visually separate.

---

## 10. Page Width

Content should not stretch indefinitely across large screens.

Initial maximum content width:

`1200px`

A reusable `.container` class should:

* center content;
* provide horizontal padding;
* respect the maximum width;
* adapt to smaller screens.

Dense sections such as weekly programmes should remain within the shared container rather than spanning the full viewport.

---

## 11. Section Spacing

Major page sections should use generous vertical separation.

Recommended starting rule:

Mobile: approximately `3rem` vertical padding.

Desktop: approximately `4rem` to `6rem` depending on section importance.

Hero and vision sections may use larger spacing.

Programme and leadership sections may use slightly tighter internal spacing because they contain repeated structured content.

---

## 12. Border Radius

Use a small consistent radius system.

| Token           | Value      |
| --------------- | ---------- |
| `--radius-sm`   | `0.375rem` |
| `--radius-md`   | `0.75rem`  |
| `--radius-lg`   | `1.25rem`  |
| `--radius-pill` | `999px`    |

Buttons may use medium or pill-shaped radius depending on final visual review.

Cards should generally use medium or large radius.

---

## 13. Shadows

Shadows should remain subtle.

Cards should rely primarily on:

* background contrast;
* borders;
* spacing;

rather than strong drop shadows.

Dark mode shadows should be especially restrained.

---

## 14. Buttons

Two primary button types will be supported.

### Primary Button

Used for important actions such as:

* Watch Live;
* Give;
* View Sermon;
* Get Directions;
* Call where appropriate.

Primary buttons should use the church blue with readable contrasting text.

### Secondary Button

Used for lower-priority navigation and supporting actions.

Secondary buttons may use:

* transparent background;
* border;
* primary-colour text.

Buttons must include:

* hover state;
* focus state;
* active state;
* disabled state where relevant.

External-service buttons should use meaningful text such as:

* Watch on YouTube;
* Visit Facebook;
* Get Directions;
* Call Pastor.

---

## 15. External Links and Actions

The approved Version 1 external destinations include:

* YouTube;
* Facebook;
* Google Maps.

These links should use a consistent visual treatment.

Where icons are used, they should support the text rather than replace it.

Recommended labels include:

* `Watch on YouTube`
* `Visit Facebook`
* `Get Directions`

External links should remain clearly identifiable in both themes.

Links should not use vague labels such as:

`Click here`

where a descriptive label is available.

---

## 16. Links

Links must be identifiable without relying only on colour where possible.

Navigation links may use visual treatment appropriate to the header.

Inline text links should have clear hover and keyboard-focus states.

Telephone links should use the `tel:` action only where a number has been approved for publication.

WhatsApp actions must only be shown where WhatsApp use has been explicitly confirmed.

Pr Pasteur Kavuma's approved mobile number must not be styled or labelled as a WhatsApp action because it has explicitly been confirmed as not being a WhatsApp number.

---

## 17. Cards

Reusable cards will support:

* ministries;
* sermons;
* programmes;
* events;
* testimonials;
* leadership.

A card may include:

* image;
* category or metadata;
* heading;
* description;
* supplementary information;
* action.

Cards should share:

* border treatment;
* radius;
* spacing;
* typography hierarchy.

Cards must adapt naturally to the amount of available content.

---

## 18. Leadership Cards

Leadership cards should support the approved pastor information.

Current pastors are:

* Pr Pasteur Kavuma;
* Pr Noah Mubiru;
* Pr Lamech Sebbuunza;
* Pr Anthony Mubiru.

A leadership card should be capable of displaying:

* pastor name;
* optional title;
* optional photograph;
* optional short biography;
* mobile number;
* telephone action.

The title field must remain optional because no approved leadership titles have currently been supplied.

The layout must not leave an awkward empty area when no title, photograph or biography exists.

Mobile numbers should wrap safely on small screens.

Telephone actions should remain visually secondary to the pastor's name.

Leadership cards should not assume that every mobile number supports WhatsApp.

---

## 19. Programme Cards and Weekly Schedule

The weekly programme contains activities from Monday through Sunday and must support multiple activities on the same day.

The design must therefore handle:

* one activity on a day;
* multiple activities on the same day;
* varying programme-name lengths;
* long time ranges;
* two separate Sunday services.

Approved schedule:

* Monday — Women's Fellowship — 5 to 7;
* Tuesday — Intercession — 10 am to 6 pm;
* Wednesday — Mid Week Services — 6 pm to 9 pm;
* Thursday — Choir Practice — 4 pm to 7 pm;
* Friday — Bible Study — 4 pm to 7 pm;
* Saturday — Church Cleaning — 7 am to 11 am;
* Saturday — Choir Practice — 4 pm to 7 pm;
* Sunday — First Sunday Service — 8 am to 10:00 am;
* Sunday — Second Sunday Service — 10:30 am to 1:00 pm.

The programme interface should visually distinguish:

* day;
* programme name;
* time.

Saturday must show Church Cleaning and Choir Practice as separate activities.

Sunday must clearly distinguish:

* First Sunday Service;
* Second Sunday Service.

The design should not merge both Sunday services into one ambiguous block.

---

## 20. Vision Section

The approved church vision is:

“To Bring people back to God, Disciple and equip them for the Ministry”

Scripture reference:

`Mathew 28:19 - 20`

The Home page should support a dedicated vision section.

The visual treatment may include:

* prominent heading or statement;
* supporting scripture reference;
* restrained decorative accent;
* sufficient whitespace.

The vision should remain readable and should not be placed over a visually busy image unless contrast is demonstrably sufficient.

The reference should be visually secondary to the main vision statement.

---

## 21. Images

Images should:

* preserve appropriate aspect ratio;
* avoid unintended stretching;
* use `object-fit` where required;
* include appropriate alternative text;
* use optimised web versions.

Recommended presentation types:

Hero image: wide landscape.

Leadership photograph: portrait.

Ministry image: landscape or square.

Event poster: preserve poster proportions.

Sermon thumbnail: approximately 16:9.

Leadership cards must also work when no pastor photograph has yet been supplied.

---

## 22. Reusable Components

The design system will support:

| Component              | Main Usage              |
| ---------------------- | ----------------------- |
| Header                 | All pages               |
| Navigation             | All pages               |
| Footer                 | All pages               |
| Hero                   | Home                    |
| Vision Block           | Home / About            |
| Primary Button         | Multiple                |
| Secondary Button       | Multiple                |
| Leadership Card        | About                   |
| Ministry Card          | Home / Ministries       |
| Sermon Card            | Home / Sermons          |
| Event Card             | Home / Events           |
| Programme Card         | Home / Programmes       |
| Weekly Programme Group | Programmes              |
| Testimonial Card       | Home                    |
| Contact Block          | Home / Contact          |
| YouTube Block          | Home / Sermons          |
| Social Link Block      | Home / Contact / Footer |
| Map Block              | Contact                 |
| Section Header         | Multiple                |

---

## 23. Responsive Strategy

The website will use a mobile-first responsive strategy.

Base CSS should represent the smallest practical screen.

Additional layout behaviour should be introduced as viewport width increases.

Initial breakpoint guidance:

| Range     | Purpose                               |
| --------- | ------------------------------------- |
| `< 640px` | Small/mobile layout                   |
| `640px+`  | Larger phone/small tablet adjustments |
| `768px+`  | Tablet                                |
| `1024px+` | Laptop/desktop                        |
| `1280px+` | Large desktop refinement              |

Breakpoints should be driven by layout requirements rather than device brand names.

---

## 24. Grid Behaviour

Mobile:

Primarily one-column layouts.

Tablet:

One or two columns depending on content.

Desktop:

Two, three or four columns where appropriate.

Examples:

Ministries: 1 → 2 → 3 columns.

Events: 1 → 2 → 3 columns.

Sermons: 1 → 2 → 3 columns.

Leadership: 1 → 2 → 4 columns where space allows.

Programmes: 1 → 2 or 3 columns where card layout is appropriate.

For the full weekly programme, a grouped day-by-day layout may be preferable to a simple card grid.

The exact layout should depend on available content.

---

## 25. Weekly Programme Responsive Behaviour

On mobile:

* each day should remain clearly separated;
* programme name and time should stack where necessary;
* multiple activities on Saturday and Sunday should remain visibly grouped under the correct day.

On tablet:

* programme name and time may appear side by side where space allows.

On desktop:

* the weekly schedule may use a structured multi-column layout;
* repeated activities on the same day must remain visually associated.

No programme time should be truncated because of viewport width.

---

## 26. Leadership Responsive Behaviour

On mobile:

* leadership cards should normally use one column;
* pastor name should appear first;
* phone action should be easy to tap;
* long numbers must not overflow.

On tablet:

* two-column layout may be used.

On desktop:

* up to four leadership cards may appear in one row where spacing remains comfortable.

Cards should remain usable even when photographs are unavailable.

---

## 27. Accessibility and Focus

All keyboard-interactive elements must have visible focus states.

Focus indicators should remain visible in both light and dark themes.

Interactive targets should be comfortably large for touch devices.

Colour must not be the only method used to communicate important state.

Telephone, YouTube, Facebook and Maps actions must have meaningful accessible labels.

Examples:

* `Call Pr Pasteur Kavuma`
* `Open Divine River Church on YouTube`
* `Open Divine River Church on Facebook`
* `Get directions to Divine River Church`

---

## 28. Motion

Animation should remain limited.

Use motion only where it improves understanding, such as:

* mobile menu transitions;
* button interaction;
* theme transition where appropriate.

Animations should not interfere with usability.

The design should respect the visitor's reduced-motion preference.

---

## 29. Theme Implementation

Theme selection will eventually use the root HTML element.

Example:

`<html data-theme="light">`

or:

`<html data-theme="dark">`

CSS variables will then determine the theme.

JavaScript will later:

* inspect the device preference on first visit;
* apply the selected theme;
* store manual preference in local storage;
* restore the preference on subsequent visits.

Theme JavaScript will be implemented during the common-site-shell stage.

---

## 30. Contact and Action Hierarchy

External actions should have a clear hierarchy.

High-priority visitor actions may include:

* Watch Live;
* Get Directions;
* Give;
* Contact the Church.

Supporting actions may include:

* YouTube;
* Facebook;
* Call a pastor where appropriate.

Pastor telephone numbers should not automatically become the church's main contact action.

The absence of a confirmed general church WhatsApp number means a global WhatsApp button should not be introduced yet.

---

## 31. Content-Length Resilience

Components must be designed to accommodate future real content.

Examples include:

* longer pastor names;
* future leadership titles;
* ministry descriptions;
* event titles;
* longer programme names;
* sermon titles;
* additional service times.

No card should rely on every item having the same amount of text.

Layouts should not break when optional fields are `null`.

---

## 32. Design Constraints

Version 1 should avoid unnecessary frontend complexity.

The project should not require:

* Bootstrap;
* Tailwind;
* React;
* Vue;
* Angular;
* large animation libraries;

unless the architecture is formally changed.

HTML, custom CSS and minimal vanilla JavaScript are sufficient for Version 1.

---

## 33. Stage 6 Acceptance Gate

Stage 6 passes when:

* brand colours are represented as reusable variables;
* light theme is defined;
* dark theme is defined;
* typography rules are defined;
* spacing scale is defined;
* page-width rules are defined;
* reusable button styles are defined;
* reusable card styles are defined;
* leadership cards support pastor names and mobile-number actions;
* leadership cards work without titles, biographies or photographs;
* programme components support multiple activities on the same day;
* Saturday can display Church Cleaning and Choir Practice distinctly;
* Sunday can clearly distinguish First Service and Second Service;
* the approved vision has an appropriate prominent visual treatment;
* YouTube actions have a defined design treatment;
* Facebook actions have a defined design treatment;
* Google Maps/Get Directions actions have a defined design treatment;
* telephone actions do not imply WhatsApp capability;
* focus-state requirements are defined;
* responsive strategy is defined;
* mobile-first behaviour is established;
* blue remains the primary church colour;
* red and yellow remain controlled accents;
* future pages can use the same visual system without independently redefining basic styles.

Once these conditions are satisfied, the project may proceed to Stage 7: Static Build System.
