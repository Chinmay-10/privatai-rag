# API Documentation

Base URL:
```

[http://localhost:8000](http://localhost:8000)

```

---

## Authentication

### Signup
```

POST /api/auth/signup

````

**Request Body (JSON):**
```json
{
  "username": "string",
  "password": "string",
  "tenant_id": "default"
}
````

---

### Login

```
POST /api/auth/login
```

**Request Body (form-data):**

```
username=your_username
password=your_password
```

**Response:**

```json
{
  "access_token": "jwt_token"
}
```

---

## Document Upload

```
POST /api/upload/
```

**Headers:**

```
Authorization: Bearer <token>
```

**Body:**

* Multipart form-data
* File upload (PDF / text)

---

## Query Documents

```
POST /api/query/
```

**Headers:**

```
Authorization: Bearer <token>
```

**Request Body (JSON):**

```json
{
  "question": "What is the document about?",
  "top_k": 3
}
```

**Response:**

```json
{
  "answer": "Generated response from the LLM"
}
```

---

## Notes

* Lower `top_k` improves performance on CPU
* First query may be slow due to model warm-up

