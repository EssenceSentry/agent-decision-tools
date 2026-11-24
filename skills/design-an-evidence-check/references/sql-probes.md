# Reconcile the grain before trusting a total

Example tables are `orders(id, amount_cents, deleted_at)` with one row per order and `events(order_id)` with zero or more rows per order. This portable query should return zero rows when an operation promises one output row per eligible order and an unchanged amount. Replace the candidate relation with the actual transformation. Two opposite errors can cancel in a global total.

```sql
WITH eligible AS (
    SELECT id, amount_cents FROM orders WHERE deleted_at IS NULL
), candidate AS (
    SELECT p.id, p.amount_cents FROM eligible AS p
    LEFT JOIN events AS e ON e.order_id = p.id
), by_key AS (
    SELECT id, COUNT(*) AS n, SUM(amount_cents) AS cents
    FROM candidate GROUP BY id
)
SELECT p.id, COALESCE(c.n, 0) AS rows_found, c.cents, p.amount_cents
FROM eligible AS p LEFT JOIN by_key AS c ON c.id = p.id
WHERE c.id IS NULL OR c.n <> 1 OR c.cents <> p.amount_cents
   OR c.cents IS NULL OR p.amount_cents IS NULL;
```

Separately check that the asserted parent keys are unique and non-NULL. In a real two-sided reconciliation check candidate-only keys as well.

```sql
SELECT id, COUNT(*) AS n FROM orders
GROUP BY id HAVING id IS NULL OR COUNT(*) <> 1;
```

Look for child rows with missing or deleted parents and decide whether the contract admits them. Preaggregate the many side or use an existence test if all the consumer needs is presence. Moving a right-side condition into WHERE after a left join can remove the zero-event parents.

```sql
SELECT e.order_id, COUNT(*) AS events_without_live_parent
FROM events AS e LEFT JOIN orders AS p
    ON p.id = e.order_id AND p.deleted_at IS NULL
WHERE p.id IS NULL GROUP BY e.order_id;
```

For production queries confirm catalog, source owner, refresh time, time zone, complete-day rule and eligibility for soft-deleted rows. Check NULL flags against the business rule, especially under negation, and compare integer minor units or decimal amounts at the intended precision. Search downstream jobs for removed columns and changed types or signs. Preserve the exact query, source revision, grain, counts and discrepancy, including a scoped zero.
