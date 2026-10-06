import importlib.util
from pathlib import Path
import random
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "source" / "main.py"
spec = importlib.util.spec_from_file_location("dispatcher", PROGRAM)
dispatcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dispatcher)


def run_program(text):
    return subprocess.run(
        [sys.executable, str(PROGRAM)], input=text, text=True,
        capture_output=True, timeout=10, encoding="utf-8",
    )


class CommandTests(unittest.TestCase):
    def assert_output(self, text, expected):
        result = run_program(text)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, expected)

    def test_documented_examples(self):
        document = (ROOT / "TESTS.md").read_text(encoding="utf-8")
        pattern = (
            r"## Test (\d+).*?Input:\s*```text\n(.*?)\n```"
            r".*?Expected:\s*```text\n(.*?)\n```"
            r".*?Actual:\s*```text\n(.*?)\n```"
        )
        cases = re.findall(pattern, document, re.S)
        self.assertGreaterEqual(len(cases), 8)
        for number, source, expected, actual in cases:
            with self.subTest(test=number):
                expected_output = expected + "\n" if expected else ""
                self.assert_output(source + "\n", expected_output)
                self.assertEqual(actual, expected)

    def test_eof(self):
        self.assert_output("", "")
        self.assert_output("CONFIG 0", "")
        self.assert_output("CONFIG 0\nADD 1 3 SW", "ADDED 1 P=33\n")
        self.assert_output("CONFIG\n", "INVALID\n")

    def test_invalid_config_then_valid_config(self):
        invalid = [
            "", "CONFIG", "CONFIG 0 extra", "WRONG 0", "CONFIG -1",
            "CONFIG 10", "CONFIG x", "CONFIG 1.5", "CONFIG +1",
            "CONFIG ²", "CONFIG ١", "CONFIG " + "9" * 5000,
        ]
        self.assert_output(
            "\n".join(invalid + ["CONFIG 0", "ADD 1 1 SW", "END"]) + "\n",
            "INVALID\n" * len(invalid) + "ADDED 1 P=13\n",
        )

    def test_all_configs(self):
        # Expected values are independent of getConfig().
        configs = [(3, 1, 2), (1, 2, 3), (2, 3, 1), (3, 2, 1), (2, 1, 3)] * 2
        for variant, bonuses in enumerate(configs):
            with self.subTest(variant=variant):
                commands = [f"CONFIG {variant}"]
                expected = []
                for ticket_id, (category, bonus) in enumerate(zip(("SW", "HW", "ACC"), bonuses), 1):
                    commands.append(f"ADD {ticket_id} 1 {category}")
                    expected.append(f"ADDED {ticket_id} P={10 + bonus}")
                self.assert_output("\n".join(commands), "\n".join(expected) + "\n")

    def test_invalid_arguments_do_not_change_state(self):
        invalid = [
            "", "UNKNOWN", "ADD", "ADD 2", "ADD 2 3",
            "ADD 2 3 SW extra", "FIND", "FIND 1 extra", "CANCEL",
            "CANCEL 1 extra", "TRIAGE extra", "SERVE extra", "END extra",
            "CONFIG 1", "ADD 1 0 SW", "ADD 1 6 SW", "ADD 1 3 OTHER",
        ]
        for bad_id in ("0", "-1", "+1", "1000000001", "x", "1.0", "²", "١", "9" * 5000):
            invalid.extend((f"ADD {bad_id} 3 SW", f"FIND {bad_id}", f"CANCEL {bad_id}"))
        for severity in ("-1", "+1", "x", "1.5", "²", "١", "9" * 5000):
            invalid.append(f"ADD 2 {severity} SW")
        commands = ["CONFIG 0", "ADD 1 3 SW"]
        expected = ["ADDED 1 P=33"]
        for command in invalid:
            commands.extend((command, "FIND 1"))
            expected.extend(("INVALID", "FOUND 1 WAITING P=33"))
        commands.extend(("TRIAGE", "SERVE", "TRIAGE", "SERVE", "END"))
        expected.extend(("TRIAGED 1 P=33", "SERVED 1", "EMPTY WAITING", "EMPTY READY"))
        self.assert_output("\n".join(commands) + "\n", "\n".join(expected) + "\n")

    def test_end_stops_only_without_arguments(self):
        self.assert_output(
            "CONFIG 0\nEND extra\nADD 1 1 SW\nEND\nADD 2 1 SW\n",
            "INVALID\nADDED 1 P=13\n",
        )

    def test_invalid_commands_preserve_ready_heap(self):
        self.assert_output(
            "CONFIG 0\nADD 1 5 SW\nTRIAGE\nSERVE extra\n"
            "CANCEL 1 extra\nCONFIG 1\nFIND 1\nSERVE\nSERVE\n",
            "ADDED 1 P=53\nTRIAGED 1 P=53\nINVALID\nINVALID\nINVALID\n"
            "FOUND 1 READY P=53\nSERVED 1\nEMPTY READY\n",
        )

    def test_id_boundaries(self):
        self.assert_output(
            "CONFIG 0\nADD 1 1 SW\nADD 1000000000 5 ACC\n"
            "ADD 0000000001 2 HW\nFIND 1000000000\nEND\n",
            "ADDED 1 P=13\nADDED 1000000000 P=52\nDUPLICATE 1\n"
            "FOUND 1000000000 WAITING P=52\n",
        )

    def test_reused_ready_id_does_not_serve_old_record(self):
        self.assert_output(
            "CONFIG 0\nADD 5 5 SW\nTRIAGE\nCANCEL 5\nADD 5 1 HW\n"
            "SERVE\nFIND 5\nTRIAGE\nSERVE\nEND\n",
            "ADDED 5 P=53\nTRIAGED 5 P=53\nCANCELLED 5\nADDED 5 P=11\n"
            "EMPTY READY\nFOUND 5 WAITING P=11\nTRIAGED 5 P=11\nSERVED 5\n",
        )

    def test_random_commands_against_simple_model(self):
        for variant in range(10):
            rng = random.Random(100 + variant)
            bonuses = [(3, 1, 2), (1, 2, 3), (2, 3, 1), (3, 2, 1), (2, 1, 3)][variant % 5]
            category_bonus = dict(zip(("SW", "HW", "ACC"), bonuses))
            active = {}
            arrival = 0
            commands = [f"CONFIG {variant}"]
            expected = []
            for _ in range(300):
                action = rng.choice(("ADD", "ADD", "TRIAGE", "SERVE", "FIND", "CANCEL"))
                ticket_id = rng.choice((1, 8, 15, 22, 29, 36, 43, 50))
                if action == "ADD":
                    severity = rng.randint(1, 5)
                    category = rng.choice(("SW", "HW", "ACC"))
                    commands.append(f"ADD {ticket_id} {severity} {category}")
                    if ticket_id in active:
                        expected.append(f"DUPLICATE {ticket_id}")
                    else:
                        arrival += 1
                        priority = severity * 10 + category_bonus[category]
                        active[ticket_id] = ["WAITING", priority, arrival]
                        expected.append(f"ADDED {ticket_id} P={priority}")
                elif action == "TRIAGE":
                    commands.append(action)
                    candidates = [key for key, value in active.items() if value[0] == "WAITING"]
                    if not candidates:
                        expected.append("EMPTY WAITING")
                    else:
                        key = min(candidates, key=lambda key: active[key][2])
                        active[key][0] = "READY"
                        expected.append(f"TRIAGED {key} P={active[key][1]}")
                elif action == "SERVE":
                    commands.append(action)
                    candidates = [key for key, value in active.items() if value[0] == "READY"]
                    if not candidates:
                        expected.append("EMPTY READY")
                    else:
                        key = min(candidates, key=lambda key: (-active[key][1], active[key][2]))
                        del active[key]
                        expected.append(f"SERVED {key}")
                elif action == "FIND":
                    commands.append(f"FIND {ticket_id}")
                    if ticket_id in active:
                        status, priority, _ = active[ticket_id]
                        expected.append(f"FOUND {ticket_id} {status} P={priority}")
                    else:
                        expected.append(f"NOT FOUND {ticket_id}")
                else:
                    commands.append(f"CANCEL {ticket_id}")
                    if ticket_id in active:
                        del active[ticket_id]
                        expected.append(f"CANCELLED {ticket_id}")
                    else:
                        expected.append(f"NOT FOUND {ticket_id}")
            with self.subTest(variant=variant):
                self.assert_output("\n".join(commands), "\n".join(expected) + "\n")


class HashTableTests(unittest.TestCase):
    def test_put_replaces_each_position_in_collision_chain(self):
        for replaced_id in (1, 8, 15):
            with self.subTest(ticket_id=replaced_id):
                table = dispatcher.TicketHashTable(7)
                originals = {key: dispatcher.Ticket(key, 1, "SW", 13, key) for key in (1, 8, 15)}
                for key, ticket in originals.items():
                    table.put(key, ticket)
                replacement = dispatcher.Ticket(replaced_id, 5, "HW", 51, 4)
                table.put(replaced_id, replacement)
                self.assertIs(table.get(replaced_id), replacement)
                node = table.buckets[1]
                ids = []
                while node is not None:
                    ids.append(node.id)
                    node = node.next
                self.assertCountEqual(ids, (1, 8, 15))
                self.assertIs(table.remove(replaced_id), replacement)
                self.assertIsNone(table.get(replaced_id))
                for key in originals:
                    if key != replaced_id:
                        self.assertIs(table.get(key), originals[key])


if __name__ == "__main__":
    unittest.main()
