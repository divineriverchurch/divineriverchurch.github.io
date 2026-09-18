# Divine River Church Website

## Version 1 Requirements Traceability Matrix

Document Version: 1.0
Project: Divine River Church Website
Scope: Version 1 Public Website

## 1. Purpose

This document defines the traceable functional, content, design, integration, accessibility, performance, security and deployment requirements for Version 1 of the Divine River Church website.

Each requirement has a unique identifier so that implementation and testing can be verified before release.

The Version 1 scope remains unchanged.

The approved church information now provides concrete acceptance values for:

* church vision;
* pastor information;
* weekly church programmes;
* Sunday service times;
* YouTube;
* Facebook;
* Google Maps.

Information that has not yet been supplied remains subject to the content inventory and must not be invented during implementation.

### Current Approved Content Baseline

#### Vision

“To Bring people back to God, Disciple and equip them for the Ministry”

Scripture reference:

`Mathew 28:19 - 20`

#### Pastors

* Pr Pasteur Kavuma — `+256 754 275036`
* Pr Noah Mubiru — `+256 782 576969`
* Pr Lamech Sebbuunza — `+256 773 213404`
* Pr Anthony Mubiru — `+256 757 255619`

Pr Pasteur Kavuma's mobile number is explicitly confirmed as not being a WhatsApp number.

No pastor titles have currently been supplied.

#### Weekly Programme

* Monday — Women's Fellowship — 5 to 7
* Tuesday — Intercession — 10 am to 6 pm
* Wednesday — Mid Week Services — 6 pm to 9 pm
* Thursday — Choir Practice — 4 pm to 7 pm
* Friday — Bible Study — 4 pm to 7 pm
* Saturday — Church Cleaning — 7 am to 11 am
* Saturday — Choir Practice — 4 pm to 7 pm
* Sunday — First Sunday Service — 8 am to 10:00 am
* Sunday — Second Sunday Service — 10:30 am to 1:00 pm

#### YouTube

`https://www.youtube.com/@divineriverchurch`

#### Facebook

`https://www.facebook.com/Divine-River-Church-Ministries`

#### Google Maps

`https://maps.app.goo.gl/1zDh24Ci9dNc55Hf6`

---

## 2. General Website Requirements

| ID       | Requirement                                         | Page/Area   | Implementation Location  | Test                 |
| -------- | --------------------------------------------------- | ----------- | ------------------------ | -------------------- |
| WEB1-001 | Website must contain eight main pages               | Entire site | `src/templates/`         | Page existence test  |
| WEB1-002 | Website must use one responsive codebase            | Entire site | CSS                      | Responsive test      |
| WEB1-003 | Website must support mobile devices                 | Entire site | CSS                      | Mobile test          |
| WEB1-004 | Website must support tablets                        | Entire site | CSS                      | Tablet test          |
| WEB1-005 | Website must support laptops and desktop computers  | Entire site | CSS                      | Desktop test         |
| WEB1-006 | Website must support light mode                     | Entire site | CSS / JS                 | Theme test           |
| WEB1-007 | Website must support dark mode                      | Entire site | CSS / JS                 | Theme test           |
| WEB1-008 | First visit should respect device theme preference  | Entire site | `main.js`                | Theme behaviour test |
| WEB1-009 | User must be able to manually change theme          | Header      | `header.html`, `main.js` | Functional test      |
| WEB1-010 | Theme choice must persist between pages             | Entire site | Browser local storage    | Persistence test     |
| WEB1-011 | Website must not require user login                 | Entire site | Architecture             | Scope verification   |
| WEB1-012 | Website must not require a database                 | Entire site | Architecture             | Scope verification   |
| WEB1-013 | Website must not require a production Python server | Entire site | Static build             | Deployment test      |
| WEB1-014 | Website must be generated as static HTML            | Entire site | `build.py`               | Build test           |

---

## 3. Navigation and Site Shell

| ID       | Requirement                                             | Page/Area   | Implementation Location | Test                   |
| -------- | ------------------------------------------------------- | ----------- | ----------------------- | ---------------------- |
| WEB1-015 | Header must appear on all pages                         | Entire site | `header.html`           | Visual test            |
| WEB1-016 | Footer must appear on all pages                         | Entire site | `footer.html`           | Visual test            |
| WEB1-017 | Main navigation must contain Home                       | Navigation  | `header.html`           | Navigation test        |
| WEB1-018 | Main navigation must contain About                      | Navigation  | `header.html`           | Navigation test        |
| WEB1-019 | Main navigation must contain Ministries                 | Navigation  | `header.html`           | Navigation test        |
| WEB1-020 | Main navigation must contain Sermons                    | Navigation  | `header.html`           | Navigation test        |
| WEB1-021 | Main navigation must contain Programmes                 | Navigation  | `header.html`           | Navigation test        |
| WEB1-022 | Main navigation must contain Events                     | Navigation  | `header.html`           | Navigation test        |
| WEB1-023 | Main navigation must contain Give                       | Navigation  | `header.html`           | Navigation test        |
| WEB1-024 | Main navigation must contain Contact                    | Navigation  | `header.html`           | Navigation test        |
| WEB1-025 | Logo must link to Home                                  | Header      | `header.html`           | Link test              |
| WEB1-026 | Current navigation item should be visually identifiable | Navigation  | Jinja/CSS               | Visual test            |
| WEB1-027 | Mobile navigation must open and close correctly         | Header      | `main.js`               | Mobile functional test |
| WEB1-028 | Navigation must be keyboard accessible                  | Header      | HTML/CSS/JS             | Accessibility test     |

---

## 4. Home Page

| ID       | Requirement                                                                                                                                                   | Page/Area | Implementation Location    | Test                     |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | -------------------------- | ------------------------ |
| WEB1-029 | Home page must contain a hero section                                                                                                                         | Home      | `index.html`               | Visual test              |
| WEB1-030 | Home page must display the approved church vision: “To Bring people back to God, Disciple and equip them for the Ministry” with reference `Mathew 28:19 - 20` | Home      | `site.json` / `index.html` | Exact content test       |
| WEB1-031 | Home page must contain a welcome message when approved content is supplied                                                                                    | Home      | `site.json` / `index.html` | Content test             |
| WEB1-032 | Home page must show latest sermon when approved sermon information is available                                                                               | Home      | `sermons.json`             | Content/YouTube test     |
| WEB1-033 | Home page must provide a Watch Live action using the approved church YouTube destination until a dedicated live URL is supplied                               | Home      | `site.json` / YouTube      | Integration test         |
| WEB1-034 | Home page must show upcoming events when approved event information is available                                                                              | Home      | `events.json`              | Content test             |
| WEB1-035 | Home page must show ministry previews when approved ministry information is available                                                                         | Home      | `ministries.json`          | Content test             |
| WEB1-036 | Home page must show programme information or a link to the full approved weekly programme                                                                     | Home      | `programmes.json`          | Content test             |
| WEB1-037 | Home page may display approved testimonials                                                                                                                   | Home      | `testimonials.json`        | Content test             |
| WEB1-038 | Home page must provide Give action                                                                                                                            | Home      | `index.html`               | Link test                |
| WEB1-039 | Home page must show approved contact/location information as it becomes available                                                                             | Home      | `site.json`                | Content test             |
| WEB1-040 | Home page must provide approved YouTube and Facebook social links                                                                                             | Home      | `site.json`                | Exact external-link test |

### WEB1-040 Acceptance Values

YouTube:

`https://www.youtube.com/@divineriverchurch`

Facebook:

`https://www.facebook.com/Divine-River-Church-Ministries`

---

## 5. About Page

| ID       | Requirement                                                                         | Page/Area | Implementation Location    | Test                  |
| -------- | ----------------------------------------------------------------------------------- | --------- | -------------------------- | --------------------- |
| WEB1-041 | About page must display approved church history once supplied                       | About     | `site.json` / `about.html` | Content test          |
| WEB1-042 | About page must display the approved church vision and scripture reference          | About     | `site.json`                | Exact content test    |
| WEB1-043 | About page must display approved mission once supplied                              | About     | `site.json`                | Content test          |
| WEB1-044 | About page must display approved core values once supplied                          | About     | `site.json`                | Content test          |
| WEB1-045 | About page must display the four approved pastors and their approved mobile numbers | About     | `site.json` / `about.html` | Exact leadership test |
| WEB1-046 | About page may display branch information where applicable                          | About     | `site.json` / template     | Content test          |

### WEB1-042 Acceptance Value

Vision:

“To Bring people back to God, Disciple and equip them for the Ministry”

Reference:

`Mathew 28:19 - 20`

### WEB1-045 Acceptance Values

| Pastor              | Approved Mobile Number | Additional Requirement                     |
| ------------------- | ---------------------- | ------------------------------------------ |
| Pr Pasteur Kavuma   | `+256 754 275036`      | Must not be presented as a WhatsApp number |
| Pr Noah Mubiru      | `+256 782 576969`      | Mobile number                              |
| Pr Lamech Sebbuunza | `+256 773 213404`      | Mobile number                              |
| Pr Anthony Mubiru   | `+256 757 255619`      | Mobile number                              |

No pastor title should be invented or displayed unless later approved.

---

## 6. Ministries Page

| ID       | Requirement                                                           | Page/Area  | Implementation Location | Test         |
| -------- | --------------------------------------------------------------------- | ---------- | ----------------------- | ------------ |
| WEB1-047 | Ministries page must display ministry name for each approved ministry | Ministries | `ministries.json`       | Content test |
| WEB1-048 | Each ministry must support description                                | Ministries | `ministries.json`       | Content test |
| WEB1-049 | Each ministry must support leader information                         | Ministries | `ministries.json`       | Content test |
| WEB1-050 | Each ministry must support meeting schedule                           | Ministries | `ministries.json`       | Content test |
| WEB1-051 | Each ministry must support contact information                        | Ministries | `ministries.json`       | Content test |
| WEB1-052 | Each ministry may display an approved image                           | Ministries | assets / JSON           | Image test   |

Current weekly activities must not automatically be treated as formal ministries.

For example, Women's Fellowship does not by itself confirm a Women's Ministry.

---

## 7. Sermons and Media

| ID       | Requirement                                                                                                  | Page/Area    | Implementation Location | Test               |
| -------- | ------------------------------------------------------------------------------------------------------------ | ------------ | ----------------------- | ------------------ |
| WEB1-053 | Sermons page must display latest sermon when individual sermon information is supplied                       | Sermons      | `sermons.json`          | YouTube test       |
| WEB1-054 | Sermons page must support recent sermons                                                                     | Sermons      | `sermons.json`          | Content test       |
| WEB1-055 | Sermons page must support sermon series                                                                      | Sermons      | `sermons.json`          | Content test       |
| WEB1-056 | Sermons page must support praise and worship content                                                         | Sermons      | `sermons.json`          | Content test       |
| WEB1-057 | Sermons page must support testimonies                                                                        | Sermons      | JSON / YouTube          | Content test       |
| WEB1-058 | Sermons page must support special programmes                                                                 | Sermons      | JSON / YouTube          | Content test       |
| WEB1-059 | Videos must be hosted externally on YouTube                                                                  | Sermons      | YouTube                 | Architecture test  |
| WEB1-060 | Website must support links to the approved Divine River Church YouTube channel and individual YouTube videos | Sermons/Home | Templates               | External-link test |
| WEB1-061 | Website may support YouTube embeds                                                                           | Sermons/Home | Templates               | Embed test         |
| WEB1-062 | Website should avoid loading excessive YouTube players simultaneously                                        | Sermons      | Template strategy       | Performance test   |

### Approved YouTube Destination

`https://www.youtube.com/@divineriverchurch`

The channel URL alone does not satisfy WEB1-053 until individual approved sermon information is supplied.

---

## 8. Livestream

| ID       | Requirement                                                                                                                         | Page/Area    | Implementation Location | Test               |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------ | ----------------------- | ------------------ |
| WEB1-063 | Website must provide access to livestream/media through the approved church YouTube channel                                         | Home/Sermons | `site.json`             | Integration test   |
| WEB1-064 | Livestream action must use `https://www.youtube.com/@divineriverchurch` unless a dedicated approved live URL later replaces it      | Home/Sermons | `site.json`             | Exact-link test    |
| WEB1-065 | Website must remain useful when church is not live by providing access to the official YouTube channel and available sermon content | Home/Sermons | Template content        | Offline-state test |

---

## 9. Programmes

| ID       | Requirement                                                                                                             | Page/Area  | Implementation Location | Test                    |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ---------- | ----------------------- | ----------------------- |
| WEB1-066 | Every approved programme must display its programme name                                                                | Programmes | `programmes.json`       | Exact content test      |
| WEB1-067 | Programme model must support a description, while allowing the field to remain empty until approved content is supplied | Programmes | `programmes.json`       | Data-model/content test |
| WEB1-068 | Every approved programme must display the correct day                                                                   | Programmes | `programmes.json`       | Exact schedule test     |
| WEB1-069 | Every approved programme must display the correct approved time                                                         | Programmes | `programmes.json`       | Exact schedule test     |
| WEB1-070 | Programme model must support venue information when supplied                                                            | Programmes | `programmes.json`       | Data-model/content test |
| WEB1-071 | Programme model must support contact information when supplied                                                          | Programmes | `programmes.json`       | Data-model/content test |

### Approved Programme Acceptance Values

| Day       | Programme             | Time                |
| --------- | --------------------- | ------------------- |
| Monday    | Women's Fellowship    | 5 to 7              |
| Tuesday   | Intercession          | 10 am to 6 pm       |
| Wednesday | Mid Week Services     | 6 pm to 9 pm        |
| Thursday  | Choir Practice        | 4 pm to 7 pm        |
| Friday    | Bible Study           | 4 pm to 7 pm        |
| Saturday  | Church Cleaning       | 7 am to 11 am       |
| Saturday  | Choir Practice        | 4 pm to 7 pm        |
| Sunday    | First Sunday Service  | 8 am to 10:00 am    |
| Sunday    | Second Sunday Service | 10:30 am to 1:00 pm |

Additional programme acceptance conditions:

* the system must allow more than one programme on the same day;
* Saturday must contain two distinct activities;
* Sunday must contain two distinct services;
* the two Sunday services must not be merged into one programme;
* programme ordering should follow the approved Monday-to-Sunday sequence.

---

## 10. Events

| ID       | Requirement                                             | Page/Area | Implementation Location | Test         |
| -------- | ------------------------------------------------------- | --------- | ----------------------- | ------------ |
| WEB1-072 | Event must support name                                 | Events    | `events.json`           | Content test |
| WEB1-073 | Event must support poster                               | Events    | JSON/assets             | Image test   |
| WEB1-074 | Event must support description                          | Events    | `events.json`           | Content test |
| WEB1-075 | Event must support date                                 | Events    | `events.json`           | Content test |
| WEB1-076 | Event must support time                                 | Events    | `events.json`           | Content test |
| WEB1-077 | Event must support venue                                | Events    | `events.json`           | Content test |
| WEB1-078 | Event may support speaker information                   | Events    | `events.json`           | Content test |
| WEB1-079 | Event may support external registration or contact link | Events    | `events.json`           | Link test    |
| WEB1-080 | Version 1 must not store event registration data        | Events    | Architecture            | Scope test   |

Current event content remains pending.

No event information should be invented to satisfy these requirements during development.

---

## 11. Prayer Requests

| ID       | Requirement                                                                                    | Page/Area    | Implementation Location | Test                |
| -------- | ---------------------------------------------------------------------------------------------- | ------------ | ----------------------- | ------------------- |
| WEB1-081 | Website must provide a prayer contact route once an approved prayer contact method is supplied | Contact/Home | `site.json`             | Functional test     |
| WEB1-082 | Prayer route may use WhatsApp only when an approved WhatsApp number is supplied                | Contact      | External link           | Link/approval test  |
| WEB1-083 | Prayer route may use telephone or email when explicitly approved for prayer requests           | Contact      | External link           | Link/approval test  |
| WEB1-084 | Version 1 must not store prayer requests                                                       | Entire site  | Architecture            | Security/scope test |

Pastor mobile numbers must not automatically be used as prayer-request contacts.

Pr Pasteur Kavuma's number must not be used as a WhatsApp prayer route.

---

## 12. Giving

| ID       | Requirement                                                    | Page/Area | Implementation Location | Test             |
| -------- | -------------------------------------------------------------- | --------- | ----------------------- | ---------------- |
| WEB1-085 | Give page must display only approved giving methods            | Give      | JSON/template           | Content approval |
| WEB1-086 | Give page may display Mobile Money information when approved   | Give      | JSON/template           | Content test     |
| WEB1-087 | Give page may display bank transfer information when approved  | Give      | JSON/template           | Content test     |
| WEB1-088 | Give page must provide approved giving instructions            | Give      | JSON/template           | Content test     |
| WEB1-089 | Give page must provide approved enquiry contact where required | Give      | JSON/template           | Content test     |
| WEB1-090 | Website must not directly process payments in Version 1        | Give      | Architecture            | Scope test       |
| WEB1-091 | Website must not store card information                        | Give      | Architecture            | Security test    |

No giving information has currently been supplied.

No payment details may be invented.

---

## 13. Contact and Location

| ID       | Requirement                                                                                   | Page/Area | Implementation Location        | Test                     |
| -------- | --------------------------------------------------------------------------------------------- | --------- | ------------------------------ | ------------------------ |
| WEB1-092 | Contact page must display the official main church telephone number once explicitly supplied  | Contact   | `site.json`                    | Content approval test    |
| WEB1-093 | Contact page must display WhatsApp contact only after an official WhatsApp number is supplied | Contact   | `site.json`                    | Link/approval test       |
| WEB1-094 | Contact page must display church email once supplied                                          | Contact   | `site.json`                    | Content/link test        |
| WEB1-095 | Contact page must display textual physical church address once supplied                       | Contact   | `site.json`                    | Content test             |
| WEB1-096 | Contact page must display the two approved Sunday service times                               | Contact   | `site.json` / template         | Exact service-time test  |
| WEB1-097 | Contact page must provide the approved Google Maps destination                                | Contact   | `site.json` / Maps integration | Exact integration test   |
| WEB1-098 | Contact page must provide a Get Directions action using the approved Maps URL                 | Contact   | Maps link                      | Exact-link test          |
| WEB1-099 | Contact page must provide the approved YouTube and Facebook links                             | Contact   | `site.json`                    | Exact external-link test |

### WEB1-096 Acceptance Values

First Sunday Service:

`8 am to 10:00 am`

Second Sunday Service:

`10:30 am to 1:00 pm`

### WEB1-097 and WEB1-098 Acceptance Value

`https://maps.app.goo.gl/1zDh24Ci9dNc55Hf6`

### WEB1-099 Acceptance Values

YouTube:

`https://www.youtube.com/@divineriverchurch`

Facebook:

`https://www.facebook.com/Divine-River-Church-Ministries`

Pastor mobile numbers must not be treated as the main church telephone number unless the church explicitly designates one for that purpose.

---

## 14. Branding and Visual Design

| ID       | Requirement                                                                   | Page/Area     | Implementation Location | Test                |
| -------- | ----------------------------------------------------------------------------- | ------------- | ----------------------- | ------------------- |
| WEB1-100 | Blue must be the primary brand colour                                         | Entire site   | CSS variables           | Visual test         |
| WEB1-101 | Light mode background should primarily use white                              | Entire site   | CSS                     | Visual test         |
| WEB1-102 | Dark mode should use near-black primary background                            | Entire site   | CSS                     | Theme test          |
| WEB1-103 | Red should be used as secondary accent                                        | Entire site   | CSS                     | Visual review       |
| WEB1-104 | Yellow should be used only as limited highlight                               | Entire site   | CSS                     | Visual review       |
| WEB1-105 | Website must use approved church logo once final production asset is supplied | Header/Footer | Assets                  | Content approval    |
| WEB1-106 | Logo must remain readable in light and dark modes                             | Entire site   | CSS/assets              | Visual test         |
| WEB1-107 | Buttons must have consistent visual treatment                                 | Entire site   | CSS                     | UI consistency test |
| WEB1-108 | Cards must have consistent visual treatment                                   | Entire site   | CSS                     | UI consistency test |

The approved content additionally requires:

* leadership cards capable of displaying pastor names and mobile-number actions;
* programme components capable of displaying multiple activities on one day;
* clear visual distinction between First and Second Sunday Service;
* external-action treatment for YouTube, Facebook and Google Maps;
* no visual implication that a mobile number is WhatsApp unless confirmed.

---

## 15. Content and Asset Requirements

| ID       | Requirement                                                 | Page/Area   | Implementation Location | Test               |
| -------- | ----------------------------------------------------------- | ----------- | ----------------------- | ------------------ |
| WEB1-109 | Production content must be approved by church               | Entire site | Content inventory       | Approval test      |
| WEB1-110 | Developer must not invent missing church information        | Entire site | Process                 | Content review     |
| WEB1-111 | Placeholder content must be clearly identified              | Entire site | Content inventory       | Review             |
| WEB1-112 | Production images must have publication permission          | Entire site | Content inventory       | Approval test      |
| WEB1-113 | Production images must be web optimised                     | Entire site | Assets                  | Performance test   |
| WEB1-114 | Image filenames should be descriptive                       | Assets      | Image directories       | Asset review       |
| WEB1-115 | Images should include meaningful alt text where appropriate | Entire site | Templates/JSON          | Accessibility test |

Approved content from the current baseline may be used directly.

Items that remain Pending in `content-inventory.md` must remain pending here as well and should not be fabricated.

---

## 16. Accessibility Requirements

| ID       | Requirement                                      | Page/Area   | Implementation Location | Test               |
| -------- | ------------------------------------------------ | ----------- | ----------------------- | ------------------ |
| WEB1-116 | Each page should have one logical H1             | Entire site | Templates               | Accessibility test |
| WEB1-117 | Heading hierarchy must be logical                | Entire site | Templates               | Accessibility test |
| WEB1-118 | Keyboard focus must be visible                   | Entire site | CSS                     | Keyboard test      |
| WEB1-119 | Interactive elements must have meaningful labels | Entire site | HTML                    | Accessibility test |
| WEB1-120 | Link descriptions must be meaningful             | Entire site | Templates               | Accessibility test |
| WEB1-121 | Text must remain readable in both themes         | Entire site | CSS                     | Contrast test      |
| WEB1-122 | Colour contrast must be sufficient               | Entire site | CSS                     | Contrast test      |

Specific accessible labels should include meaningful actions such as:

* Call Pr Pasteur Kavuma;
* Call Pr Noah Mubiru;
* Call Pr Lamech Sebbuunza;
* Call Pr Anthony Mubiru;
* Open Divine River Church on YouTube;
* Open Divine River Church on Facebook;
* Get directions to Divine River Church.

---

## 17. Performance Requirements

| ID       | Requirement                                              | Page/Area   | Implementation Location | Test                  |
| -------- | -------------------------------------------------------- | ----------- | ----------------------- | --------------------- |
| WEB1-123 | Images should be resized and compressed for web use      | Entire site | Assets                  | Performance test      |
| WEB1-124 | JavaScript should remain minimal                         | Entire site | `main.js`               | Code review           |
| WEB1-125 | CSS should avoid unnecessary duplication                 | Entire site | CSS                     | Code review           |
| WEB1-126 | Pages should avoid unnecessary third-party media loading | Entire site | Templates               | Performance test      |
| WEB1-127 | Layout should remain stable while loading                | Entire site | CSS/assets              | Visual stability test |

The official YouTube channel may be linked directly without embedding many video players simultaneously.

---

## 18. Security and Privacy Requirements

| ID       | Requirement                                      | Page/Area   | Implementation Location | Test                |
| -------- | ------------------------------------------------ | ----------- | ----------------------- | ------------------- |
| WEB1-128 | Production website must use HTTPS                | Production  | Cloudflare              | Security test       |
| WEB1-129 | Repository must contain no passwords             | Repository  | Git/source              | Security review     |
| WEB1-130 | Repository must contain no secret API keys       | Repository  | Git/source              | Security review     |
| WEB1-131 | Version 1 must store no member data              | Entire site | Architecture            | Scope/security test |
| WEB1-132 | Version 1 must store no payment transaction data | Entire site | Architecture            | Security test       |
| WEB1-133 | Version 1 must store no prayer request data      | Entire site | Architecture            | Security test       |

Approved pastor mobile numbers are public content approved for publication and are not authentication credentials or secrets.

They must nevertheless be used only for their approved purpose.

---

## 19. Build-System Requirements

| ID       | Requirement                                                                 | Page/Area    | Implementation Location | Test               |
| -------- | --------------------------------------------------------------------------- | ------------ | ----------------------- | ------------------ |
| WEB1-134 | Build system must read JSON content                                         | Build system | `build.py`              | Build test         |
| WEB1-135 | Build system must render Jinja templates                                    | Build system | `build.py`              | Build test         |
| WEB1-136 | Build system must generate all eight pages                                  | Build system | `build.py`              | Build test         |
| WEB1-137 | Build system must copy CSS                                                  | Build system | `build.py`              | Asset test         |
| WEB1-138 | Build system must copy JavaScript                                           | Build system | `build.py`              | Asset test         |
| WEB1-139 | Build system must copy images                                               | Build system | `build.py`              | Asset test         |
| WEB1-140 | Build system must generate output in `dist/`                                | Build system | `build.py`              | Build test         |
| WEB1-141 | Clean build must work from empty `dist/`                                    | Build system | `build.py`              | Clean-build test   |
| WEB1-142 | Repeated builds should produce consistent output                            | Build system | `build.py`              | Repeatability test |
| WEB1-143 | Missing required JSON values should be identified without inventing content | Build system | `build.py`              | Validation test    |

The build system must support:

* multiple leadership records;
* multiple programmes on the same day;
* optional leadership titles;
* explicit telephone versus WhatsApp handling;
* approved external URLs from `site.json`.

---

## 20. Production and Deployment Requirements

| ID       | Requirement                                                    | Page/Area  | Implementation Location  | Test              |
| -------- | -------------------------------------------------------------- | ---------- | ------------------------ | ----------------- |
| WEB1-144 | Source code must be maintained with Git                        | Repository | Git                      | Repository test   |
| WEB1-145 | Production source may be hosted on GitHub                      | Repository | GitHub                   | Deployment test   |
| WEB1-146 | Production website must be deployable through Cloudflare Pages | Production | Cloudflare               | Deployment test   |
| WEB1-147 | Direct page URLs must load correctly                           | Production | Cloudflare/static output | Routing test      |
| WEB1-148 | Production must provide a working 404 page                     | Production | `dist/404.html`          | Error-page test   |
| WEB1-149 | Production CSS, JS and images must load correctly              | Production | Cloudflare               | Asset test        |
| WEB1-150 | No development-only local paths may appear in production       | Production | Generated HTML           | Deployment review |

Before production release, the live website must additionally verify the approved external destinations:

* YouTube;
* Facebook;
* Google Maps.

---

## 21. Version 1 Scope Restrictions

The following features are specifically outside Version 1 unless an approved scope change is made:

* Member registration
* Member login
* Authentication
* Member profiles
* Database
* Backend API
* Admin dashboard
* Internal prayer request storage
* Internal event registration storage
* Internal payment processing
* Donation history
* Push notifications
* Native Android application
* Native iOS application

Any request for these functions should be classified as an enhancement and assessed against Versions 2, 3 or 4 of the project roadmap.

The newly approved vision, pastor information, programme schedule, YouTube, Facebook and Maps details do not change Version 1 scope.

They are content and acceptance values within requirements that already existed.

---

## 22. Current Traceability of Approved Content

| Approved Content        | Requirement IDs                                    | Main Data Source               | Primary Page             |
| ----------------------- | -------------------------------------------------- | ------------------------------ | ------------------------ |
| Church vision           | WEB1-030, WEB1-042                                 | `site.json`                    | Home / About             |
| Pastor information      | WEB1-045                                           | `site.json` leadership         | About                    |
| Monday–Sunday programme | WEB1-036, WEB1-066 to WEB1-071                     | `programmes.json`              | Programmes               |
| Sunday service times    | WEB1-069, WEB1-096                                 | `programmes.json`, `site.json` | Programmes / Contact     |
| YouTube channel         | WEB1-033, WEB1-040, WEB1-059 to WEB1-065, WEB1-099 | `site.json`                    | Home / Sermons / Contact |
| Facebook page           | WEB1-040, WEB1-099                                 | `site.json`                    | Home / Contact / Footer  |
| Google Maps destination | WEB1-097, WEB1-098                                 | `site.json` location           | Contact                  |

This table demonstrates that the new information fits the existing requirements baseline and does not require additional Version 1 features.

---

## 23. Content Still Pending

The following requirements remain valid, but final acceptance cannot yet be completed because approved content has not been supplied:

* church history;
* mission;
* core values;
* ministry details;
* individual sermons;
* current events;
* main church telephone;
* official WhatsApp number;
* church email;
* textual physical address;
* prayer-request contact;
* giving information;
* final logo assets;
* final photographs.

These items should remain tracked in `docs/content-inventory.md`.

Their absence during development does not permit invented production content.

---

## 24. Stage 2 Acceptance Gate

Stage 2 is complete when:

* every Version 1 page has traceable requirements;
* every major feature has a requirement identifier;
* every requirement identifies where it will be implemented;
* every requirement has a test method;
* approved content has concrete acceptance values where available;
* the approved vision is traceable to Home and About;
* all four pastors are traceable to About;
* the complete weekly programme is traceable to Programmes;
* multiple Saturday and Sunday activities are supported;
* YouTube is traceable to Home, Sermons and Contact;
* Facebook is traceable to Home and Contact;
* Google Maps is traceable to Contact;
* unknown content remains identified as Pending rather than being invented;
* Version 2, 3 and 4 features remain outside the Version 1 baseline unless formally approved;
* the requirements document is available in `docs/web1-requirements.md`.

Once these conditions are satisfied, development may proceed through the remaining Version 1 engineering stages.
