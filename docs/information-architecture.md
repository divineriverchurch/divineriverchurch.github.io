# Divine River Church Website

## Version 1 Information Architecture

Document Version: 1.0
Project: Divine River Church Website
Scope: Version 1 Public Website

## 1. Purpose

This document defines the structure of the Divine River Church Version 1 website, including:

* primary navigation;
* page responsibilities;
* URL structure;
* relationships between pages;
* location of approved church content;
* external destinations such as YouTube, Facebook and Google Maps.

The objective is to ensure that visitors can reach important church information quickly without unnecessary navigation.

The approved church information currently includes:

* church vision;
* four pastors and their mobile numbers;
* weekly church programme;
* Sunday service times;
* official YouTube channel;
* official Facebook page;
* official Google Maps destination.

This information strengthens the existing Version 1 architecture but does not require additional top-level pages.

---

## 2. Primary Navigation

The website will contain eight primary pages:

1. Home
2. About
3. Ministries
4. Sermons
5. Programmes
6. Events
7. Give
8. Contact

The same primary information architecture will be used on:

* mobile;
* tablet;
* desktop.

Desktop may display navigation horizontally.

Mobile devices may use a collapsible navigation menu.

No additional top-level page is required for:

* pastors;
* weekly programme;
* YouTube;
* Facebook;
* Google Maps.

These functions belong within the existing eight-page architecture.

---

## 3. URL Structure

The recommended public URLs are:

| Page       | URL            |
| ---------- | -------------- |
| Home       | `/`            |
| About      | `/about/`      |
| Ministries | `/ministries/` |
| Sermons    | `/sermons/`    |
| Programmes | `/programmes/` |
| Events     | `/events/`     |
| Give       | `/give/`       |
| Contact    | `/contact/`    |

URLs should remain:

* short;
* readable;
* predictable;
* consistent.

---

## 4. Site Structure

```text
Divine River Church
│
├── Home
│
├── About
│
├── Ministries
│
├── Sermons
│
├── Programmes
│
├── Events
│
├── Give
│
└── Contact
```

Version 1 will remain intentionally shallow.

Important information should normally require no more than one primary navigation action from Home.

---

## 5. Home Page Responsibility

The Home page is the primary entry point to the website.

Its purpose is to:

* introduce Divine River Church;
* communicate the church vision;
* expose important weekly information;
* provide access to sermons and livestreams;
* promote upcoming events;
* provide paths to ministries;
* provide giving access;
* make location and contact actions easy to find.

Recommended structure:

```text
Home
│
├── Hero
│
├── Welcome
│
├── Vision
│
├── Latest Sermon
│      └── View Sermons
│
├── Watch Live
│      └── Official YouTube Channel / Live
│
├── Upcoming Events
│      └── Events
│
├── Ministries Preview
│      └── Ministries
│
├── Weekly Programme Preview
│      └── Programmes
│
├── Testimonials
│
├── Give
│      └── Give
│
├── Visit Us
│      └── Contact / Google Maps
│
└── Social Media
       ├── YouTube
       └── Facebook
```

The Home page should provide selected highlights rather than duplicate the full content of deeper pages.

---

## 6. Home Vision Section

The approved church vision is:

“To Bring people back to God, Disciple and equip them for the Ministry”

Scripture reference:

`Mathew 28:19 - 20`

The Home page should contain a dedicated vision section because the vision is a central statement of church identity.

The Home page may display:

* the full vision;
* its scripture reference;
* a link to About where broader church identity content is available.

The vision should not be rewritten independently on different pages.

It should originate from shared structured content.

---

## 7. About Page Responsibility

The About page explains the identity, history, purpose and leadership of Divine River Church.

Primary content should include:

* church history;
* vision;
* mission;
* core values;
* pastors;
* leadership information;
* branch information where applicable.

The About page should answer:

* Who is Divine River Church?
* What is the church's vision?
* What is the church's mission?
* What values guide the church?
* Who are the pastors?
* Where applicable, what branches exist?

Detailed weekly schedules should remain on Programmes rather than About.

---

## 8. Confirmed Pastor Information

The About page now has confirmed pastor information available.

Current approved pastors are:

* Pr Pasteur Kavuma;
* Pr Noah Mubiru;
* Pr Lamech Sebbuunza;
* Pr Anthony Mubiru.

Approved mobile numbers:

* Pr Pasteur Kavuma — `+256 754 275036`
* Pr Noah Mubiru — `+256 782 576969`
* Pr Lamech Sebbuunza — `+256 773 213404`
* Pr Anthony Mubiru — `+256 757 255619`

Pr Pasteur Kavuma's number has explicitly been identified as not being a WhatsApp number.

No leadership titles have currently been supplied.

The About page should therefore support pastor cards containing:

* name;
* optional title;
* optional photograph;
* optional biography;
* mobile number.

The interface must not imply WhatsApp availability where it has not been confirmed.

---

## 9. Ministries Page Responsibility

The Ministries page explains the major ministries operating within the church.

Each ministry may contain:

* ministry name;
* description;
* leader;
* meeting schedule;
* contact;
* image.

Possible examples may include, only where later confirmed:

* Children's Ministry;
* Youth Ministry;
* Women's Ministry;
* Men's Ministry;
* Worship Ministry;
* Media Ministry;
* Evangelism Ministry;
* Prayer Ministry.

The church's actual ministry structure will determine the final list.

The existence of a related programme does not automatically establish an official ministry.

For example:

`Women's Fellowship`

does not by itself confirm that an official:

`Women's Ministry`

should be created.

---

## 10. Sermons Page Responsibility

The Sermons page is the main media destination.

Its content may be organised into:

* Latest Sermon;
* Recent Sermons;
* Sermon Series;
* Praise and Worship;
* Testimonies;
* Special Programmes.

YouTube remains the primary external media platform.

The confirmed official YouTube destination is:

`https://www.youtube.com/@divineriverchurch`

The Sermons page should generally provide:

* sermon title;
* preacher;
* date;
* thumbnail;
* category;
* YouTube destination.

Where appropriate, a selected video may be embedded directly.

The page should avoid loading a large number of YouTube players simultaneously.

Individual sermon information remains separate from the channel information and will be added as it becomes available.

---

## 11. Livestream Navigation

Livestream access should be visible from at least:

* Home;
* Sermons;
* website header where appropriate.

The preferred primary action is:

```text
Watch Live
```

Current approved destination:

```text
Website
   ↓
Watch Live
   ↓
Official Divine River Church YouTube Channel
```

Approved YouTube destination:

`https://www.youtube.com/@divineriverchurch`

If a dedicated YouTube Live URL is later supplied, it may replace the general channel URL for the Watch Live action.

When the church is not live, visitors should still be able to reach:

* the church YouTube channel;
* latest sermons when available;
* relevant service information.

---

## 12. Programmes Page Responsibility

The Programmes page is the main destination for recurring church activities.

The church now has an approved weekly programme.

The page must therefore support actual Monday-to-Sunday content rather than generic placeholder programme cards.

Approved programme:

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

Each programme record may additionally support:

* description;
* venue;
* contact.

These remain pending where they have not yet been supplied.

---

## 13. Multiple Activities on the Same Day

The information architecture must support more than one programme on the same day.

Saturday contains:

```text
Saturday
├── Church Cleaning — 7 am to 11 am
└── Choir Practice — 4 pm to 7 pm
```

Sunday contains:

```text
Sunday
├── First Sunday Service — 8 am to 10:00 am
└── Second Sunday Service — 10:30 am to 1:00 pm
```

The Programmes page should preserve this relationship.

The two activities must not be merged into one ambiguous programme.

---

## 14. Sunday Service Information

Sunday service times are important enough to appear outside the Programmes page.

Approved service times:

* First Sunday Service — 8 am to 10:00 am;
* Second Sunday Service — 10:30 am to 1:00 pm.

Service times may also appear on:

* Home;
* Contact;
* Footer.

The Programmes page remains the primary source for the complete weekly schedule.

---

## 15. Events Page Responsibility

The Events page is for dated or special church activities.

Examples may include:

* conferences;
* crusades;
* special services;
* retreats;
* seminars;
* youth events;
* worship nights;
* church celebrations.

Each event may provide:

* event name;
* poster;
* description;
* date;
* time;
* venue;
* speaker;
* contact or registration destination.

Registration remains external in Version 1.

No current event information has yet been supplied.

The page remains part of Version 1 and may use clearly identified development placeholders until approved content is received.

---

## 16. Give Page Responsibility

The Give page provides church-approved giving information.

Possible content:

* short introduction;
* Mobile Money;
* bank details;
* other approved giving methods;
* giving instructions;
* giving enquiry contact.

Version 1 must not process payments directly.

No approved giving information has yet been supplied.

The architecture should therefore provide the page without inventing payment details.

The Give page should clearly distinguish official giving information from general contact information.

---

## 17. Contact Page Responsibility

The Contact page is the main destination for church contact and location information.

The page should ultimately provide:

* main church telephone;
* WhatsApp where confirmed;
* email;
* physical address;
* service times;
* Google Maps;
* Get Directions;
* social media;
* prayer request contact route.

Currently confirmed contact-related information includes:

* Google Maps destination;
* YouTube;
* Facebook;
* Sunday service times;
* pastor mobile numbers.

Main church telephone, WhatsApp, email and textual address remain pending.

Pastor mobile numbers should not automatically be treated as the church's general contact details.

---

## 18. Google Maps and Location

The confirmed Google Maps destination is:

`https://maps.app.goo.gl/1zDh24Ci9dNc55Hf6`

The Contact page should provide a clear action such as:

`Get Directions`

Navigation relationship:

```text
Contact
   ↓
Get Directions
   ↓
Google Maps
```

The same location action may also appear on Home.

A textual physical church address has not yet been supplied and should not be invented from the Maps URL.

---

## 19. Social Media Architecture

Confirmed official social destinations are:

### YouTube

`https://www.youtube.com/@divineriverchurch`

### Facebook

`https://www.facebook.com/Divine-River-Church-Ministries`

These do not require separate website pages.

They should be exposed through appropriate links from:

* Home;
* Contact;
* Footer.

YouTube additionally belongs prominently on:

* Sermons;
* livestream actions.

Navigation relationship:

```text
Website
├── YouTube
└── Facebook
```

Other social platforms should not be introduced until approved URLs are supplied.

---

## 20. Prayer Request Navigation

Version 1 will not store prayer requests.

Recommended future flow:

```text
Visitor
   ↓
Prayer Request
   ↓
Approved Contact Method
   ├── WhatsApp, if approved
   ├── Telephone, if approved
   ├── Email, if approved
   └── External form, if approved
```

The prayer request action may appear on:

* Home;
* Contact;
* Footer.

No prayer-specific contact method has yet been supplied.

Pastor mobile numbers must not automatically be assigned to prayer requests.

---

## 21. Global Header

The global header should contain:

* church logo;
* church name where appropriate;
* primary navigation;
* Watch Live action where appropriate;
* theme control;
* mobile menu control.

The logo should link to Home.

The currently selected page should be visually identifiable.

The Watch Live action may link to the confirmed YouTube channel until a dedicated livestream URL is provided.

---

## 22. Global Footer

The global footer may contain:

* church name;
* short church description;
* primary navigation;
* approved contact information;
* Sunday service times;
* YouTube;
* Facebook;
* Give link;
* Get Directions;
* prayer/contact shortcut when approved;
* copyright information.

The footer should remain consistent across all pages.

Only approved information should be shown.

---

## 23. Mobile Navigation

Mobile navigation should contain the same eight major destinations as desktop:

```text
Home
About
Ministries
Sermons
Programmes
Events
Give
Contact
```

The mobile version may use a menu button to conserve screen space.

The menu should:

* open and close predictably;
* be keyboard accessible;
* show all major pages;
* not hide important destinations;
* close appropriately after navigation.

No separate mobile information architecture will be maintained.

---

## 24. Cross-Page Navigation

Important relationships now include:

```text
Home
├── About
├── Sermons
├── Watch Live → YouTube
├── Events
├── Ministries
├── Programmes
├── Give
├── Contact
├── Google Maps
├── YouTube
└── Facebook

About
└── Pastor information

Sermons
└── YouTube

Programmes
├── Monday programme
├── Tuesday programme
├── Wednesday programme
├── Thursday programme
├── Friday programme
├── Saturday programmes
└── Sunday services

Events
└── External registration/contact where required

Contact
├── Google Maps
├── YouTube
├── Facebook
├── Telephone when approved
├── WhatsApp when approved
└── Email when approved

Give
└── Approved giving information

Footer
├── Contact
├── Programmes / service times
├── YouTube
├── Facebook
├── Maps
└── Give
```

---

## 25. Content Ownership Rules

Each content type should have one primary location.

| Content                    | Primary Page     |
| -------------------------- | ---------------- |
| Church history             | About            |
| Vision                     | About            |
| Mission                    | About            |
| Leadership / pastors       | About            |
| Ministry details           | Ministries       |
| Sermons                    | Sermons          |
| Weekly church programme    | Programmes       |
| Sunday service schedule    | Programmes       |
| Special dated activities   | Events           |
| Giving details             | Give             |
| Address and church contact | Contact          |
| Google Maps                | Contact          |
| YouTube media              | Sermons          |
| Social destinations        | Contact / Footer |

The Home page may display summaries of these items but should link to their primary destination.

This reduces duplication and improves maintainability.

---

## 26. Shared Content Rules

Some information is sufficiently important to appear in several locations.

### Vision

Primary:

`About`

May also appear on:

`Home`

### Sunday Service Times

Primary:

`Programmes`

May also appear on:

* Home;
* Contact;
* Footer.

### YouTube

Primary media destination:

`Sermons`

May also appear on:

* Home;
* Header Watch Live action;
* Contact;
* Footer.

### Google Maps

Primary:

`Contact`

May also appear on:

`Home`

### Facebook

May appear on:

* Home;
* Contact;
* Footer.

The same underlying structured data should be reused rather than manually duplicating these values.

---

## 27. Navigation Depth

Version 1 should generally maintain:

```text
Home
  ↓
Primary Page
```

No visitor should have to navigate through several layers merely to access:

* service times;
* sermons;
* livestream;
* events;
* giving;
* church location;
* church contact information;
* pastor information.

---

## 28. Known Content Still Pending

The information architecture is complete even though some content remains outstanding.

Pending items currently include:

* mission;
* church history;
* core values;
* ministry details;
* individual sermon records;
* current events;
* giving information;
* main church telephone;
* WhatsApp number;
* email;
* textual physical address;
* prayer-request contact;
* final photographs;
* final logo assets.

Missing content should not be replaced with invented church information.

---

## 29. Future Expansion

The Version 1 information architecture should allow future versions to introduce features without redesigning the entire public website.

Potential future destinations may include:

* Devotionals;
* Search;
* Event Registration;
* Member Login;
* Member Dashboard;
* Prayer Request Form;
* Administration.

These are not part of Version 1.

They should not appear in the current main navigation unless formally added to scope.

---

## 30. Current Information Architecture Summary

The approved content confirms that the existing eight-page architecture remains appropriate.

```text
Home
│
├── Vision
├── Programme Preview
├── Sunday Service Times
├── Sermon / YouTube
├── Watch Live
├── Events Preview
├── Ministries Preview
├── Give
├── Maps / Visit Us
├── YouTube
└── Facebook

About
│
├── Vision
├── History
├── Mission
├── Values
└── Pastors
    ├── Pr Pasteur Kavuma
    ├── Pr Noah Mubiru
    ├── Pr Lamech Sebbuunza
    └── Pr Anthony Mubiru

Ministries
└── Confirmed ministries when supplied

Sermons
└── Official YouTube Channel

Programmes
│
├── Monday — Women's Fellowship
├── Tuesday — Intercession
├── Wednesday — Mid Week Services
├── Thursday — Choir Practice
├── Friday — Bible Study
├── Saturday
│   ├── Church Cleaning
│   └── Choir Practice
└── Sunday
    ├── First Sunday Service
    └── Second Sunday Service

Events
└── Current events when supplied

Give
└── Approved giving information when supplied

Contact
│
├── Sunday Service Times
├── Google Maps
├── YouTube
├── Facebook
└── Additional approved contact methods when supplied
```

---

## 31. Stage 4 Acceptance Gate

Stage 4 passes when:

* all eight required pages are represented;
* every page has a clear responsibility;
* Home routes users toward major functions;
* the approved vision has a defined location;
* confirmed pastors have a defined location under About;
* the weekly programme has a defined primary page;
* multiple activities on Saturday are supported;
* First and Second Sunday Services are represented separately;
* YouTube has a defined media and livestream role;
* Facebook has a defined social role;
* Google Maps has a defined location and directions role;
* every primary page is reachable from navigation;
* URLs use one consistent structure;
* mobile and desktop use the same information architecture;
* content ownership is defined;
* shared content rules are defined;
* unnecessary duplicate content is avoided;
* missing information is not invented;
* Version 2, Version 3 and Version 4 functions have not entered the Version 1 navigation without approval.

Once these conditions are satisfied, the project may proceed to Stage 5: Data and Content Model.
