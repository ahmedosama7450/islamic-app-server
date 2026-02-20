# Frontend Integration Guide — Islamic App API

## Base URL

```
http://localhost:8000/api/v1
```

> [!NOTE]
> Interactive API docs are available at `http://localhost:8000/docs` (Swagger UI).

---

## Endpoints

### 1. Search Hadiths

```
GET /hadiths
```

**Query Parameters**

| Param               | Type    | Default | Description                                                            |
| ------------------- | ------- | ------- | ---------------------------------------------------------------------- |
| `full_text_plain`   | string  | —       | Case-insensitive text search on the hadith body                        |
| `book_id`           | integer | —       | Filter by exact book ID                                                |
| `narrators`         | string  | —       | Comma-separated narrator IDs (e.g. `1557,4757,1254`)                   |
| `narrators_ordered` | boolean | `false` | When `true`, narrators must appear in the given order within the chain |
| `skip`              | integer | `0`     | Offset for pagination (≥ 0)                                            |
| `limit`             | integer | `20`    | Page size (1–100)                                                      |

All filters are optional and can be combined. When multiple filters are provided, they are ANDed together.

**Example Requests**

```js
// Search by text
fetch("/api/v1/hadiths?full_text_plain=صلاة");

// Filter by book + narrators (unordered — any arrangement)
fetch("/api/v1/hadiths?book_id=1&narrators=1557,4757");

// Filter by narrators (ordered — must appear in this exact chain order)
fetch("/api/v1/hadiths?narrators=1557,4757,1254&narrators_ordered=true");

// Pagination
fetch("/api/v1/hadiths?book_id=1&skip=20&limit=10");
```

**Response** — `200 OK`

```json
{
  "items": [
    {
      "id": "6789abcdef012345abcdef01",
      "book_id": 1,
      "page_number": 42,
      "full_text": "حدثنا ...",
      "full_text_plain": "حدثنا ...",
      "matn": "...",
      "matn_plain": "...",
      "narrators": [
        { "id": 1557, "name": "...", "name_plain": "..." },
        { "id": 4757, "name": "...", "name_plain": "..." }
      ]
    }
  ],
  "total": 134
}
```

> `total` is the total count of matching documents (before `skip`/`limit`), useful for pagination controls.

---

### 2. Get Hadith by ID

```
GET /hadiths/{hadith_id}
```

**Path Parameters**

| Param       | Type   | Description      |
| ----------- | ------ | ---------------- |
| `hadith_id` | string | MongoDB ObjectId |

**Example**

```js
fetch("/api/v1/hadiths/6789abcdef012345abcdef01");
```

**Response** — `200 OK`

Same shape as a single item in the search response above.

**Error** — `404 Not Found`

```json
{ "detail": "Hadith not found." }
```

---

### 3. Search Narrators

```
GET /narrators
```

**Query Parameters**

| Param        | Type    | Default | Description                              |
| ------------ | ------- | ------- | ---------------------------------------- |
| `name_plain` | string  | —       | Case-insensitive search on narrator name |
| `kunya`      | string  | —       | Case-insensitive search on kunya         |
| `nasab`      | string  | —       | Case-insensitive search on nasab         |
| `skip`       | integer | `0`     | Offset for pagination (≥ 0)              |
| `limit`      | integer | `20`    | Page size (1–100)                        |

All filters are ANDed together when multiple are provided.

**Example Requests**

```js
// Search by name
fetch("/api/v1/narrators?name_plain=مالك");

// Combine filters
fetch("/api/v1/narrators?name_plain=مالك&kunya=أبو");
```

**Response** — `200 OK`

```json
{
  "items": [
    {
      "id": "6789abcdef012345abcdef02",
      "narrator_id": 1557,
      "name": "...",
      "name_plain": "...",
      "kunya": "...",
      "nasab": "...",
      "death_date": "...",
      "tabaqa": "...",
      "rank_ibn_hajar": "...",
      "rank_dhahabi": "...",
      "relations": "...",
      "jarh_wa_tadil": [
        {
          "scholar": "ابن حجر",
          "quotes": ["ثقة", "حافظ"]
        }
      ]
    }
  ],
  "total": 23
}
```

---

### 4. Get Narrator by ID

```
GET /narrators/{narrator_id}
```

**Path Parameters**

| Param         | Type   | Description      |
| ------------- | ------ | ---------------- |
| `narrator_id` | string | MongoDB ObjectId |

**Example**

```js
fetch("/api/v1/narrators/6789abcdef012345abcdef02");
```

**Response** — `200 OK`

Same shape as a single item in the narrator search response above.

**Error** — `404 Not Found`

```json
{ "detail": "Narrator not found." }
```

---

## Response Type Reference

### HadithNarrator (embedded in Hadith)

| Field        | Type    | Description                                                               |
| ------------ | ------- | ------------------------------------------------------------------------- |
| `id`         | integer | Narrator ID (use this to look up full narrator details or filter hadiths) |
| `name`       | string  | Narrator name (formatted)                                                 |
| `name_plain` | string  | Narrator name (plain text)                                                |

### Hadith

| Field             | Type             | Description                               |
| ----------------- | ---------------- | ----------------------------------------- |
| `id`              | string           | MongoDB ObjectId                          |
| `book_id`         | integer          | Book identifier                           |
| `page_number`     | integer          | Page number in the book                   |
| `full_text`       | string           | Full hadith text (formatted)              |
| `full_text_plain` | string           | Full hadith text (plain, used for search) |
| `matn`            | string           | Hadith matn (formatted)                   |
| `matn_plain`      | string           | Hadith matn (plain)                       |
| `narrators`       | HadithNarrator[] | Chain of narrators                        |

### Narrator

| Field            | Type          | Description                       |
| ---------------- | ------------- | --------------------------------- |
| `id`             | string        | MongoDB ObjectId                  |
| `narrator_id`    | integer       | Unique narrator identifier        |
| `name`           | string        | Full name (formatted)             |
| `name_plain`     | string        | Full name (searchable plain text) |
| `kunya`          | string        | Kunya                             |
| `nasab`          | string        | Lineage / nasab                   |
| `death_date`     | string        | Date of death                     |
| `tabaqa`         | string        | Scholar generation/layer          |
| `rank_ibn_hajar` | string        | Ranking by Ibn Hajar              |
| `rank_dhahabi`   | string        | Ranking by Al-Dhahabi             |
| `relations`      | string        | Relations info                    |
| `jarh_wa_tadil`  | JarhWaTadil[] | Scholar evaluations               |

### JarhWaTadil

| Field     | Type     | Description                    |
| --------- | -------- | ------------------------------ |
| `scholar` | string   | Name of the evaluating scholar |
| `quotes`  | string[] | Evaluation quotes              |

---

## Common Patterns

### Pagination

All list endpoints return `{ items, total }`. Build pagination with:

```js
const page = 1;
const pageSize = 20;

const res = await fetch(
  `/api/v1/hadiths?skip=${(page - 1) * pageSize}&limit=${pageSize}`,
);
const { items, total } = await res.json();
const totalPages = Math.ceil(total / pageSize);
```

### Linking Hadiths ↔ Narrators

Each hadith contains embedded `narrators[].id` values. Use these to:

1. **Filter hadiths by narrator chain** — pass IDs to `GET /hadiths?narrators=1557,4757`
2. **Fetch full narrator profile** — the embedded `narrators[].id` is the `narrator_id` field in the narrators collection. First search `GET /narrators` to find the narrator's MongoDB `id`, then use `GET /narrators/{id}` for the full profile.

### Error Handling

| Status | Meaning                                                       |
| ------ | ------------------------------------------------------------- |
| `200`  | Success                                                       |
| `404`  | Resource not found (invalid or non-existent ID)               |
| `422`  | Validation error (bad query param types, out-of-range values) |
