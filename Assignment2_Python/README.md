# Assignment 2 — Campus IT Ticket Dispatcher

- Student name: Borodin Danila
- Student ID: SE-2514
- Language: Python

The program keeps new tickets in a FIFO queue, moves triaged tickets to a
max-heap, and uses a hash table to find active tickets by ID. Higher priority
is served first. Tickets with the same priority are served in arrival order.

Run from this directory with `python source/main.py`. Send commands through
standard input. There is no menu or input prompt; standard output contains
only command responses.

Input checks:

- Start with `CONFIG d`, where `d` is a single digit from 0 to 9. Invalid
  configuration lines print `INVALID`; the program waits for a valid CONFIG.
  Once configured, a second CONFIG is invalid and does not reset the data.
- IDs use 1–10 ASCII digits and must have a numeric value from 1 to 1000000000.
  Leading zeros are allowed within that length; IDs are compared numerically.
- Severity is one of `1`, `2`, `3`, `4`, `5`. Categories are `SW`, `HW`, `ACC`.
- ADD requires three arguments; FIND and CANCEL require one. TRIAGE, SERVE,
  and END take no arguments. Commands and categories are case-sensitive.
- A blank line, unknown command, missing argument, extra argument, or invalid
  value prints `INVALID` without changing any ticket or its arrival order.
  This check happens before checking for a duplicate ID.
- `END` stops without printing a response. `END extra` prints `INVALID` and
  processing continues. End of input also stops normally, including before
  CONFIG and after a last line without a newline.

Complexity:

Let A be the number of active tickets, M the number of hash buckets, H the
number of stored heap records, Q the number of stored queue records, and L the
longest hash chain. H and Q include cancelled records that have not yet been
discarded. Let k be the number of stale records skipped by one command.
The bounds below describe data-structure work. Reading and checking a line
additionally costs O(B), where B is the number of characters in that line.

| Command | Cost using the longest collision chain L |
| --- | --- |
| ADD | O(1 + L): duplicate lookup and table insertion scan a chain; queue enqueue is Θ(1). |
| TRIAGE | O((k + 1)(1 + L) + log(H + 2)): each dequeued record needs a table lookup; an accepted ticket is inserted into the heap. |
| SERVE | O((k + 1)(log(H + 2) + 1 + L)): each popped heap record needs a lookup, and the accepted ticket is removed from the table. |
| FIND | O(1 + L). |
| CANCEL | O(1 + L); the queue and heap are not scanned. |

In the worst case L = A because all IDs can collide. With uniformly distributed
IDs, expected chain work is O(1 + A/M), not automatically O(1). The bucket count
is fixed by CONFIG and the table does not resize, so constant expected lookup
time requires a bounded load factor A/M.

One heap sift takes O(log(H + 2)). The heap uses a Python list, whose occasional
growth or shrink can copy elements; bounds involving insertion/removal use
amortized list costs. One command can still skip many stale records. Each stale
queue node or heap record is discarded at most once overall, but discarding it
also costs a hash lookup and, for the heap, heap removal.

Data-structure memory is O(M + A + Q + H). If S tickets have been successfully added over the
whole run, it is bounded by O(M + S). Memory is not necessarily O(A), since
cancellation can leave old references in the queue and heap. The current input
line and its tokens additionally use O(B) memory.

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
- `put` replaces the value of an existing key without adding another node.

Stale-record solution:
CANCEL removes a ticket only from the hash table; it does not scan the queue or heap. Old queue/heap references are therefore lazy stale records. Before TRIAGE or SERVE accepts a record, the program looks up the same ID in the hash table and checks object identity (`current is ticket`) and the required status. This prevents an old cancelled ticket from being mistaken for a newly added ticket that reuses the same ID.

AI usage:
AI was used to review the code, fix input validation, add regression tests,
and check the complexity explanation. The queue, heap, and chained hash table
remain handwritten. I need to be able to explain these structures and the
lazy-deletion checks during the defense.

Tests:

Run `python -m unittest discover -s tests -v` from this directory. The suite
checks the examples in TESTS.md, malformed commands, all ten CONFIG values,
EOF, ID reuse, and hash-table updates at every position in a collision chain.
It also compares 3000 generated commands with a simple independent model.
The Actual blocks in TESTS.md are captured from real program runs.
