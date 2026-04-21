# Blog API

A small REST API for blog posts built with **FastAPI**, **SQLAlchemy 2**, and **MySQL** (via PyMySQL). Tables are created on startup from SQLAlchemy models.

## Requirements

- Python 3.10+
- MySQL server and a database the app can use

## Setup

```bash
git clone https://github.com/Numair6649/Blogging-Pattern-API
cd "Bloggin pattern API"
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create an empty database in MySQL (example):

```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Configuration

Set environment variables **before** starting the app (system/user variables, shell, or a `.env` loader if you add one). If `DATABASE_URL` is set, it is used as-is and the `MYSQL_*` variables below are ignored.

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Full SQLAlchemy URL, e.g. `mysql+pymysql://user:password@localhost:3306/blog_db` |
| `MYSQL_USER` | MySQL user (default: `root`) |
| `MYSQL_PASSWORD` | MySQL password |
| `MYSQL_HOST` | Host (default: `localhost`) |
| `MYSQL_PORT` | Port (default: `3306`) |
| `MYSQL_DATABASE` | Database name |

## Run

```bash
uvicorn main:app --reload
```

API base URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/db-health` | DB connectivity check |
| `GET` | `/blogs` | List all blogs |
| `GET` | `/blogs/{blog_id}` | Get one blog by id (`404` if not found) |
| `POST` | `/blogs` | Create a blog (`201` + body) |
| `PUT` | `/blogs/{blog_id}` | Replace a blog (`404` if not found) |
| `DELETE` | `/blogs/{blog_id}` | Delete a blog (`204`, `404` if not found) |

### Request body (create / update)

`POST /blogs` and `PUT /blogs/{blog_id}` expect JSON:

```json
{
  "title": "string",
  "content": "string",
  "category": "string",
  "tags": ["tag1", "tag2"]
}
```

All fields are required; `tags` must be a non-empty array.

### Response shape (blog object)

Includes `id`, `title`, `content`, `category`, `tags`, `created_at`, and `updated_at`.

## Project layout

| File | Role |
|------|------|
| `main.py` | FastAPI app, routes, lifespan |
| `app.py` | Pydantic models, CRUD helpers |
| `db.py` | Engine, `Blog` model, `get_db` dependency |

## License

Add a license file if you publish the repo publicly.
