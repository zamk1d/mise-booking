# mise-booking

## Description
Mise-booking - is a test task, that realizing a REST API for book a table at a restaurants.

## Task
REST API must realize endpoints for creating a book, getting books list, getting book by id and cancel books.

### Endpoints
- `POST` **/bookings:** *creates a book*
- `GET` **/bookings:** *books list, filter by date*
- `GET` **/bookings/{id}:** *get book by id*
- 'DELETE' **/bookings/{id}:** *cancel the book*

### Book data
- `name` **guest name**
- `phone` **guest phone, RU format**
- `booking_date` **book date**
- `booking_time` **book time by slots**
- `guests` **only digits from 1 to 12**

## Stack
- **python 3.11**
- **FastAPI**
- **Pydantic v2**
- **SQLAlchemy 2.0**
- **Uvicorn**
- **Alembic**
- **Pytest**
- **httpx**
- **Dockerfile**
- **docker-compose**
- **Poetry**