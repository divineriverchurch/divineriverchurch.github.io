# Divine River Church Website

## Version 1 Data and Content Model

Document Version: 1.0
Project: Divine River Church Website
Scope: Version 1 Public Website

## Purpose

Version 1 stores structured church content in JSON files.

The JSON files contain content only. HTML templates control presentation.

Content that has not yet been received should normally use:

* `null` for an unknown single value;
* `[]` for an empty collection;
* `false` for content that should not yet be published.

Approved content may be populated directly into the corresponding JSON files.

The developer must not invent missing church information.

---

# 1. General Data-Modelling Rules

The Version 1 content model should follow these rules:

1. Content and presentation must remain separate.
2. Shared information should be stored once and reused by templates.
3. Repeated content should use arrays rather than duplicate HTML.
4. Multiple records may share the same day, category or content type.
5. Optional values should use `null` where no approved value exists.
6. Content that is not ready for publication should use `published: false`.
7. Telephone numbers should retain their international format.
8. Telephone and WhatsApp capability must not be assumed to be the same.
9. Dates should use ISO format where applicable.
10. IDs should be stable, unique and machine-readable.

---

# 2. site.json

`site.json` stores information that may be reused across several pages.

Main sections:

* site identity;
* welcome information;
* vision;
* mission;
* history;
* values;
* leadership;
* branches;
* contact information;
* service times;
* location;
* social links;
* livestream information;
* giving information.

A recommended overall structure is:

```json
{
  "site": {},
  "leadership": [],
  "branches": [],
  "contact": {},
  "service_times": [],
  "location": {},
  "social_links": [],
  "livestream": {},
  "giving": {}
}
```

---

# 3. Site Identity Structure

The `site` object may contain:

* `name`
* `tagline`
* `description`
* `welcome_message`
* `vision`
* `vision_reference`
* `mission`
* `history`
* `values`

Recommended structure:

```json
{
  "site": {
    "name": "Divine River Church",
    "tagline": null,
    "description": null,
    "welcome_message": null,
    "vision": "To Bring people back to God, Disciple and equip them for the Ministry",
    "vision_reference": "Mathew 28:19 - 20",
    "mission": null,
    "history": null,
    "values": []
  }
}
```

The currently approved vision can therefore be stored centrally and reused on:

* Home;
* About;
* other approved areas where required.

The wording should not be duplicated manually in several templates.

---

# 4. Leadership Structure

Leadership must support multiple pastors.

Each leadership record may contain:

* `id`
* `name`
* `title`
* `mobile`
* `whatsapp`
* `biography`
* `image`
* `published`
* `sort_order`

The `title` field is optional because no leadership titles have currently been supplied.

The `whatsapp` field should explicitly state whether the number is approved for WhatsApp use.

Recommended structure:

```json
{
  "leadership": [
    {
      "id": "pr-pasteur-kavuma",
      "name": "Pr Pasteur Kavuma",
      "title": null,
      "mobile": "+256 754 275036",
      "whatsapp": false,
      "biography": null,
      "image": null,
      "published": true,
      "sort_order": 1
    },
    {
      "id": "pr-noah-mubiru",
      "name": "Pr Noah Mubiru",
      "title": null,
      "mobile": "+256 782 576969",
      "whatsapp": null,
      "biography": null,
      "image": null,
      "published": true,
      "sort_order": 2
    },
    {
      "id": "pr-lamech-sebbuunza",
      "name": "Pr Lamech Sebbuunza",
      "title": null,
      "mobile": "+256 773 213404",
      "whatsapp": null,
      "biography": null,
      "image": null,
      "published": true,
      "sort_order": 3
    },
    {
      "id": "pr-anthony-mubiru",
      "name": "Pr Anthony Mubiru",
      "title": null,
      "mobile": "+256 757 255619",
      "whatsapp": null,
      "biography": null,
      "image": null,
      "published": true,
      "sort_order": 4
    }
  ]
}
```

`false` means a number has been explicitly confirmed as not being a WhatsApp number.

`null` means WhatsApp use has not yet been confirmed.

The system must not interpret `null` as `true`.

---

# 5. Contact Structure

Centralising contact information prevents telephone numbers, email addresses and other details from being duplicated across multiple HTML files.

The contact object may contain:

* `phone`
* `whatsapp`
* `email`
* `address`
* `postal_address`
* `general_enquiry`
* `prayer_contact`

Recommended structure:

```json
{
  "contact": {
    "phone": null,
    "whatsapp": null,
    "email": null,
    "address": null,
    "postal_address": null,
    "general_enquiry": null,
    "prayer_contact": null
  }
}
```

Pastor mobile numbers should remain in the leadership structure unless one is explicitly approved as the main church contact.

A pastor's mobile number must therefore not automatically populate:

* main church telephone;
* WhatsApp;
* prayer contact;
* giving contact.

---

# 6. Service Times Structure

Service times should represent regular worship services specifically.

Each service-time record may contain:

* `id`
* `name`
* `day`
* `start_time`
* `end_time`
* `display_time`
* `venue`
* `published`
* `sort_order`

The approved Sunday services can be represented as:

```json
{
  "service_times": [
    {
      "id": "sunday-first-service",
      "name": "First Sunday Service",
      "day": "Sunday",
      "start_time": "08:00",
      "end_time": "10:00",
      "display_time": "8 am to 10:00 am",
      "venue": null,
      "published": true,
      "sort_order": 1
    },
    {
      "id": "sunday-second-service",
      "name": "Second Sunday Service",
      "day": "Sunday",
      "start_time": "10:30",
      "end_time": "13:00",
      "display_time": "10:30 am to 1:00 pm",
      "venue": null,
      "published": true,
      "sort_order": 2
    }
  ]
}
```

The structured start and end times can later support sorting and display logic.

`display_time` preserves the approved human-readable wording.

---

# 7. Location Structure

Location information should be stored separately from general contact information.

The location object may contain:

* `address`
* `google_maps_url`
* `directions_url`
* `embed_url`
* `landmark`

Recommended structure:

```json
{
  "location": {
    "address": null,
    "google_maps_url": "https://maps.app.goo.gl/1zDh24Ci9dNc55Hf6",
    "directions_url": "https://maps.app.goo.gl/1zDh24Ci9dNc55Hf6",
    "embed_url": null,
    "landmark": null
  }
}
```

The supplied Google Maps URL is approved.

A textual physical address remains unknown and should remain `null` until supplied.

The system must not invent an address based only on the Google Maps link.

---

# 8. Social Link Structure

Each social link may contain:

* `platform`
* `url`
* `label`
* `published`
* `sort_order`

The approved social links can be represented as:

```json
{
  "social_links": [
    {
      "platform": "youtube",
      "url": "https://www.youtube.com/@divineriverchurch",
      "label": "YouTube",
      "published": true,
      "sort_order": 1
    },
    {
      "platform": "facebook",
      "url": "https://www.facebook.com/Divine-River-Church-Ministries",
      "label": "Facebook",
      "published": true,
      "sort_order": 2
    }
  ]
}
```

Instagram, TikTok, X or other platforms should not be added until official URLs are supplied.

---

# 9. Livestream Structure

Livestream information may contain:

* `youtube_channel_url`
* `youtube_live_url`
* `button_label`
* `offline_message`
* `published`

Current approved information supports the YouTube channel as the destination.

Recommended structure:

```json
{
  "livestream": {
    "youtube_channel_url": "https://www.youtube.com/@divineriverchurch",
    "youtube_live_url": "https://www.youtube.com/@divineriverchurch",
    "button_label": null,
    "offline_message": null,
    "published": true
  }
}
```

A dedicated livestream URL may replace the channel URL later if one is supplied.

---

# 10. Giving Structure

The giving object may contain:

* `introduction`
* `methods`
* `enquiry_contact`

Each giving method may contain:

* `id`
* `type`
* `name`
* `details`
* `instructions`
* `published`

Recommended initial structure:

```json
{
  "giving": {
    "introduction": null,
    "methods": [],
    "enquiry_contact": null
  }
}
```

No giving information should be invented.

The Give page may remain structurally available while the underlying content remains unpublished or incomplete.

---

# 11. ministries.json

`ministries.json` stores confirmed church ministries.

Each ministry may contain:

* `id`
* `name`
* `description`
* `leader`
* `schedule`
* `contact`
* `image`
* `published`
* `sort_order`

Example structure:

```json
{
  "id": "youth-ministry",
  "name": "Youth Ministry",
  "description": null,
  "leader": null,
  "schedule": null,
  "contact": null,
  "image": null,
  "published": false,
  "sort_order": 1
}
```

`id` should be unique and machine-readable.

Example:

`youth-ministry`

No ministries should be created merely because a related activity appears in the weekly programme.

For example, the existence of Women's Fellowship does not automatically confirm an official Women's Ministry.

The current file may remain:

```json
{
  "ministries": []
}
```

until ministry information is supplied.

---

# 12. programmes.json

`programmes.json` stores recurring church activities.

Each programme may contain:

* `id`
* `name`
* `description`
* `day`
* `start_time`
* `end_time`
* `display_time`
* `venue`
* `contact`
* `published`
* `sort_order`

Programmes represent recurring activities.

Multiple programme records are allowed on the same day.

This is required because:

* Saturday contains Church Cleaning and Choir Practice;
* Sunday contains First Service and Second Service.

The programme model must therefore never assume that each day has only one activity.

The approved programme data can be represented as:

```json
{
  "programmes": [
    {
      "id": "womens-fellowship",
      "name": "Women's Fellowship",
      "description": null,
      "day": "Monday",
      "start_time": "17:00",
      "end_time": "19:00",
      "display_time": "5 to 7",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 1
    },
    {
      "id": "intercession",
      "name": "Intercession",
      "description": null,
      "day": "Tuesday",
      "start_time": "10:00",
      "end_time": "18:00",
      "display_time": "10 am to 6 pm",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 2
    },
    {
      "id": "mid-week-services",
      "name": "Mid Week Services",
      "description": null,
      "day": "Wednesday",
      "start_time": "18:00",
      "end_time": "21:00",
      "display_time": "6 pm to 9 pm",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 3
    },
    {
      "id": "thursday-choir-practice",
      "name": "Choir Practice",
      "description": null,
      "day": "Thursday",
      "start_time": "16:00",
      "end_time": "19:00",
      "display_time": "4 pm to 7 pm",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 4
    },
    {
      "id": "bible-study",
      "name": "Bible Study",
      "description": null,
      "day": "Friday",
      "start_time": "16:00",
      "end_time": "19:00",
      "display_time": "4 pm to 7 pm",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 5
    },
    {
      "id": "church-cleaning",
      "name": "Church Cleaning",
      "description": "Ushers cleaning the church",
      "day": "Saturday",
      "start_time": "07:00",
      "end_time": "11:00",
      "display_time": "7 am to 11 am",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 6
    },
    {
      "id": "saturday-choir-practice",
      "name": "Choir Practice",
      "description": null,
      "day": "Saturday",
      "start_time": "16:00",
      "end_time": "19:00",
      "display_time": "4 pm to 7 pm",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 7
    },
    {
      "id": "sunday-first-service",
      "name": "First Sunday Service",
      "description": null,
      "day": "Sunday",
      "start_time": "08:00",
      "end_time": "10:00",
      "display_time": "8 am to 10:00 am",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 8
    },
    {
      "id": "sunday-second-service",
      "name": "Second Sunday Service",
      "description": null,
      "day": "Sunday",
      "start_time": "10:30",
      "end_time": "13:00",
      "display_time": "10:30 am to 1:00 pm",
      "venue": null,
      "contact": null,
      "published": true,
      "sort_order": 9
    }
  ]
}
```

The two Sunday services may appear in both:

* `programmes.json`, because they are recurring activities;
* the `service_times` section of `site.json`, because service times are reused globally.

The shared values should remain consistent.

---

# 13. sermons.json

Each sermon may contain:

* `id`
* `title`
* `preacher`
* `date`
* `youtube_id`
* `youtube_url`
* `series`
* `category`
* `description`
* `published`

Dates should use ISO format:

`YYYY-MM-DD`

Approved categories may include:

* `sermon`
* `sermon-series`
* `praise-worship`
* `testimony`
* `special-programme`

Where possible, the website should derive YouTube watch and embed URLs from `youtube_id`.

Example:

```json
{
  "id": "example-sermon",
  "title": null,
  "preacher": null,
  "date": null,
  "youtube_id": null,
  "youtube_url": null,
  "series": null,
  "category": "sermon",
  "description": null,
  "published": false
}
```

The latest published sermon may be determined using the sermon date.

The approved YouTube channel does not by itself provide sufficient information to create individual sermon records.

Until individual sermons are collected:

```json
{
  "sermons": []
}
```

is valid.

---

# 14. events.json

Each event may contain:

* `id`
* `name`
* `description`
* `date`
* `start_time`
* `end_time`
* `venue`
* `speaker`
* `poster`
* `registration`
* `published`

Dates should use:

`YYYY-MM-DD`

Registration remains external in Version 1.

The registration object may contain:

* `type`
* `label`
* `url`

Possible registration types include:

* `whatsapp`
* `phone`
* `external`
* `none`

Example:

```json
{
  "id": "example-event",
  "name": null,
  "description": null,
  "date": null,
  "start_time": null,
  "end_time": null,
  "venue": null,
  "speaker": null,
  "poster": null,
  "registration": {
    "type": "none",
    "label": null,
    "url": null
  },
  "published": false
}
```

No event information has yet been supplied.

The current file may remain:

```json
{
  "events": []
}
```

---

# 15. testimonials.json

Each testimonial may contain:

* `id`
* `name`
* `text`
* `image`
* `video_url`
* `permission_confirmed`
* `published`

Example:

```json
{
  "id": "testimonial-id",
  "name": null,
  "text": null,
  "image": null,
  "video_url": null,
  "permission_confirmed": false,
  "published": false
}
```

Testimonials must not be published unless:

```json
"permission_confirmed": true
```

and:

```json
"published": true
```

No testimonial information has yet been supplied.

The current file may remain:

```json
{
  "testimonials": []
}
```

---

# 16. Asset Paths

JSON should reference images relative to the generated website.

Example:

```text
assets/images/ministries/youth-ministry.jpg
```

Images themselves remain under:

```text
src/assets/images/
```

Recommended asset categories include:

* `branding/`
* `church/`
* `leadership/`
* `ministries/`
* `events/`

No JSON record should point to an image file that does not exist in the source asset directory unless the record remains unpublished.

---

# 17. Publishing Control

Structured records that may not yet be ready should use:

```json
"published": false
```

The build system should ignore unpublished records when creating public content.

Example:

```json
{
  "name": "Example Ministry",
  "published": false
}
```

This allows content to be prepared without accidentally publishing incomplete information.

For approved records such as the current pastors and weekly programme:

```json
"published": true
```

may be used.

---

# 18. Missing Values

Unknown values should normally use:

```json
null
```

Example:

```json
"email": null
```

An empty list should represent an unknown or currently empty collection:

```json
"values": []
```

Do not use invented information merely to make a page appear complete.

Examples of currently unknown information include:

* church mission;
* church history;
* core values;
* main church phone;
* WhatsApp number;
* church email;
* textual physical address;
* giving information;
* ministry details;
* individual sermon records;
* events;
* image paths.

---

# 19. Data Duplication Rules

Some information may need to appear in several parts of the website, but it should not be manually duplicated unnecessarily.

Examples:

Vision:

```text
site.json
   ↓
Home
About
```

Social links:

```text
site.json
   ↓
Header/Footer
Home
Contact
```

Pastor information:

```text
site.json leadership
   ↓
About
possibly Contact where specifically approved
```

Weekly programmes:

```text
programmes.json
   ↓
Programmes page
Home programme preview
```

Sunday service times:

```text
site.json service_times
   ↓
Home
Contact
Footer

programmes.json
   ↓
Programmes page
```

The build system and templates should ensure that duplicated displays remain consistent.

---

# 20. Sorting Rules

Repeated content should support deterministic ordering.

Use `sort_order` where editorial order is important.

Examples:

Leadership:

```text
1
2
3
4
```

Weekly programmes:

```text
Monday
Tuesday
Wednesday
Thursday
Friday
Saturday morning
Saturday afternoon
Sunday first service
Sunday second service
```

Chronological data such as sermons and events may additionally be sorted by date.

---

# 21. Identifier Rules

IDs should:

* be lowercase;
* use hyphens;
* contain no spaces;
* remain stable once published;
* describe the record sufficiently.

Examples:

```text
pr-pasteur-kavuma
womens-fellowship
intercession
mid-week-services
church-cleaning
sunday-first-service
sunday-second-service
```

Avoid IDs such as:

```text
programme1
pastor2
item3
```

where a meaningful stable identifier can be used.

---

# 22. Current Approved Data Summary

The following data is currently approved and can populate the Version 1 JSON files.

## Vision

```text
To Bring people back to God, Disciple and equip them for the Ministry
```

Reference:

```text
Mathew 28:19 - 20
```

## Pastors

```text
Pr Pasteur Kavuma
+256 754 275036
Not WhatsApp

Pr Noah Mubiru
+256 782 576969

Pr Lamech Sebbuunza
+256 773 213404

Pr Anthony Mubiru
+256 757 255619
```

## Weekly Programme

```text
Monday
Women's Fellowship
5 to 7

Tuesday
Intercession
10 am to 6 pm

Wednesday
Mid Week Services
6 pm to 9 pm

Thursday
Choir Practice
4 pm to 7 pm

Friday
Bible Study
4 pm to 7 pm

Saturday
Church Cleaning
7 am to 11 am

Saturday
Choir Practice
4 pm to 7 pm

Sunday
First Sunday Service
8 am to 10:00 am

Sunday
Second Sunday Service
10:30 am to 1:00 pm
```

## YouTube

```text
https://www.youtube.com/@divineriverchurch
```

## Facebook

```text
https://www.facebook.com/Divine-River-Church-Ministries
```

## Google Maps

```text
https://maps.app.goo.gl/1zDh24Ci9dNc55Hf6
```

---

# 23. Current JSON File Responsibilities

The Version 1 files have the following responsibilities:

| File                | Responsibility                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------------- |
| `site.json`         | Site identity, vision, leadership, contacts, service times, Maps, social links, livestream and giving |
| `ministries.json`   | Ministry records                                                                                      |
| `programmes.json`   | Recurring weekly church programmes                                                                    |
| `sermons.json`      | Individual sermon and media records                                                                   |
| `events.json`       | Upcoming and special event records                                                                    |
| `testimonials.json` | Approved testimonial records                                                                          |

The approved information currently affects primarily:

* `site.json`
* `programmes.json`

The remaining JSON files may stay empty until real content is supplied.

---

# 24. Stage 5 Acceptance

The data model passes Stage 5 when:

* all Version 1 content types can be represented;
* the approved vision can be represented centrally;
* multiple pastors can be represented;
* pastor titles remain optional;
* pastor mobile numbers can be represented without assuming WhatsApp availability;
* shared contact information is centralised;
* Google Maps information can be represented separately from textual address information;
* approved YouTube and Facebook links can be represented;
* multiple programmes can occur on the same day;
* Saturday can contain both Church Cleaning and Choir Practice;
* Sunday can contain both First Service and Second Service;
* new sermons can be added without changing HTML structure;
* new events can be added without changing HTML structure;
* new ministries can be added without changing HTML structure;
* new programmes can be added without changing HTML structure;
* no database is required;
* incomplete content can remain unpublished;
* missing values can remain `null`;
* all JSON files contain valid JSON.

Once these conditions are satisfied, Stage 5 is complete and the content model can be used by the Version 1 static build system.
