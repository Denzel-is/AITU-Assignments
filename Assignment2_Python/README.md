# Assignment 2 — Campus IT Ticket Dispatcher

Student name: REPLACE_WITH_YOUR_NAME  
Student ID: REPLACE_WITH_YOUR_STUDENT_ID  
Language: Python  
Variant: REPLACE_WITH_LAST_DIGIT_OF_STUDENT_ID  

Complexity:

- ADD: Queue enqueue is Θ(1). Hash-table insertion is expected O(1), worst-case O(n) because all active IDs may collide into one chain. No heap work is done in ADD.
- TRIAGE: Each queue node is dequeued at most once during the whole execution. A successful active WAITING ticket is inserted into the max-heap in O(log n). A single TRIAGE may skip stale queue nodes, so one call can take O(k + log n), where k is the number of stale nodes skipped. Amortized over all commands, stale queue nodes are discarded only once.
- SERVE: removeMax is O(log n) per heap record removed. SERVE may skip stale heap records; therefore one call can take O(k log n), where k is the number of stale heap records popped in that call. Each stale heap record is removed at most once overall.
- FIND: Expected O(1), worst-case O(n) because of hash collisions.
- CANCEL: Expected O(1), worst-case O(n) because removal scans one hash chain.
- Additional memory: O(n) for active table records plus queue/heap records. Lazy deletion can leave stale queue/heap references until they reach the front/root, so stored references are still O(number of successful ADD operations), bounded by the command limit.

Queue invariant:
- `head` points to the oldest not-yet-dequeued queue node and `tail` points to the newest node.
- If the queue is empty, both `head` and `tail` are `None`.
- Enqueue adds only at `tail`; dequeue removes only from `head`.

Heap invariant:
- For every child, its parent has higher or equal service order according to `(priority descending, arrival order ascending)`.
- Therefore the root is always the READY heap record that should be considered first.

Hash-table invariant:
- Every active ticket is stored in exactly one bucket `id % M`.
- Within a bucket, records form a singly linked collision chain.
- At most one active ticket exists for a given numeric ID.

Stale-record solution:
CANCEL removes a ticket only from the hash table; it does not scan the queue or heap. Old queue/heap references are therefore lazy stale records. Before TRIAGE or SERVE accepts a record, the program looks up the same ID in the hash table and checks object identity (`current is ticket`) and the required status. This prevents an old cancelled ticket from being mistaken for a newly added ticket that reuses the same ID.

AI usage:
AI was used to help explain the assignment, review the design, and assist with implementation/debugging. The final program should be tested by the student, and the student must be able to explain every structure, invariant, complexity bound, and command during the individual defense.
