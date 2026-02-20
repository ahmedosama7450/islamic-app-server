# Islamic App - Product Requirements Document

## Home Page

User can search for a hadith using the following filters:

- the hadith's `full_text_plain` fields
- the book id of the hadith
- the narrators of the hadith

> the narrator is searched using the narrator's `name_plain`, `kunya`, `nasab` fields

## Hadith Page

- The hadith page will display the full information about the hadith, and its narrators

## Schemas

### Hadith Schema

- \_id: mongoDB ObjectId
- book_id: number
- page_number: number
- full_text: string
- full_text_plain: string
- matn: string
- matn_plain: string
- narrators: array of objects with the following fields:
  - id: number
  - name: string
  - name_plain: string

### Narrator Schema

- \_id: mongoDB ObjectId
- narrator_id: number
- name: string
- name_plain: string
- kunya: string
- nasab: string
- death_date: string
- tabaqa: string
- rank_ibn_hajar: string
- rank_dhahabi: string
- relations: string
- jarh_wa_tadil: array of objects with the following fields:
  - scholar: string
  - quotes: array of strings

## Endpoints

- GET /hadiths
  - query parameters:
    - full_text_plain
    - book_id
    - narrators
      - unordered_narrators
        - e.g. `narrators=1557,4757,1254&narrators_ordered=false`
        - hadiths where the narrator's id is in the list of narrators
      - ordered_narrators
        - e.g. `narrators=1557,4757,1254&narrators_ordered=true`
        - hadiths where the narrator's id is in the list of narrators and the narrator's id is in the same order as the list
- GET /hadiths/{id}
- GET /narrators
  - query parameters:
    - name_plain
    - kunya
    - nasab
- GET /narrators/{id}
