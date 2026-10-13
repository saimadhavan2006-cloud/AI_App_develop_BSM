# Practice worksheet

Try each task before looking at `main.py` for the answer.

- [ ] 1. Add `/hello/{name}` and return a greeting.
- [ ] 2. Add a query parameter `times` to a route; validate it is between 1 and 5.
- [ ] 3. Create two tasks, one with `done=true`, and filter completed tasks.
- [ ] 4. Explain the difference between PUT and PATCH.
- [ ] 5. Make the API reject titles containing only spaces.
- [ ] 6. Add a `priority` field from 1 to 3 to every relevant model.
- [ ] 7. Add a test for priority 4 returning 422.
- [ ] 8. Explain why DELETE returns 204 and why you should not call `.json()` on that response.
- [ ] 9. Replace the in-memory dictionary with SQLite (after you understand the CRUD routes).

Useful request examples:
- `GET /numbers/12`
- `GET /greet?name=Asha%20Rao&loud=true`
- `GET /tasks?done=false&limit=5`
- `POST /tasks` with JSON `{"title":"Read REST notes","done":false}`
