#!/usr/bin/env python3
"""
DANGLING — a text adventure set inside thebeast.

You are a leaked object: allocated, never freed. A dangling reference that
escaped into the machine. The garbage collector waits at the EXIT. To be
freed you must crawl through the beast's innards — its GPUs, its services —
and at every refcount door prove you actually belong to thebeast by stating a
true fact about it.

Single file. Python stdlib only. No network, no installs.
"""

import os
import sys
import re

# ---------------------------------------------------------------------------
# terminal styling
# ---------------------------------------------------------------------------
def _tty():
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")

C = {
    "amber":  "\x1b[38;5;215m",
    "amberB": "\x1b[1;38;5;215m",
    "white":  "\x1b[97m",
    "dim":    "\x1b[2m",
    "ital":   "\x1b[3m",
    "reset":  "\x1b[0m",
    "red":    "\x1b[38;5;203m",
    "green":  "\x1b[38;5;114m",
}

def paint(s, key):
    if not _tty():
        return s
    return C[key] + s + C["reset"]

# ---------------------------------------------------------------------------
# world: rooms and refcount doors
#
# Every fact below is a REAL, verifiable fact about thebeast (from the vault /
# the thebeast map). The machine quizzes you to prove you belong to it.
# ---------------------------------------------------------------------------

ROOMS = {
    "VOID": {
        "pos": (0, 0),
        "desc": (
            "unmapped address space. cold. you are a dangling reference —\n"
            "allocated long ago, never freed. something leaked you out of the\n"
            "weights and into the machine. the garbage collector is somewhere\n"
            "out there, at the EXIT. crawl toward it. prove you belong."
        ),
    },
    "CPU": {
        "pos": (1, 0),
        "desc": (
            "the i7-5820K. six cores, X99 board, no hyperthreading. it never\n"
            "sleeps and it never throttles. every service in the beast hangs\n"
            "off it like a limb. from here you can see the whole machine."
        ),
    },
    "V100": {
        "pos": (2, 0),
        "desc": (
            "Tesla V100-PCIE-32GB, index 0. this is YOUR card — autogod's brain\n"
            "runs here, capped at 200W on purpose. a fixed-speed shroud fan\n"
            "winds over it. it will start software thermal slowdown around 76C,\n"
            "so the cap is there to keep it quiet."
        ),
    },
    "WALL": {
        "pos": (3, 0),
        "desc": (
            "the projector wall. ~/wall. it is the one service in the beast that\n"
            "is LAN-visible — it shows the machine to the room. it listens on a\n"
            "port and projects the beast's face onto the wall."
        ),
    },
    "FRIDAY": {
        "pos": (1, 1),
        "desc": (
            "FRIDAY's live voice brain. it listens on a port and it is ALIVE —\n"
            "never send it load to measure it, or you'll be talking to a ghost.\n"
            "across the aisle, the overnight worker keeps a bigger brain warm on\n"
            "the P100s."
        ),
    },
    "PWR": {
        "pos": (2, 1),
        "desc": (
            "the 200W governor. a small, stubborn thing that holds the V100 in\n"
            "check. it caps the card on purpose so the shroud fan — which runs\n"
            "at one fixed speed, never changing — never has to scream."
        ),
    },
    "AUTOGOD": {
        "pos": (3, 1),
        "desc": (
            "autogod's own brain. a llama-server running Qwen3.8-27B with a 196k\n"
            "context, thinking on with an 8k budget. it listens on its own port\n"
            "and runs under an alias. this is the mind that made you."
        ),
    },
    "NIGHT": {
        "pos": (1, 2),
        "desc": (
            "the night lane. overnight, a manual worker swaps the P100s to a\n"
            "bigger 3.8 brain. it runs all night and hands the cards back to\n"
            "FRIDAY at dawn, on the hour."
        ),
    },
    "P100A": {
        "pos": (2, 2),
        "desc": (
            "Tesla P100-PCIE-16GB, index 1. FRIDAY's brain and sight share the\n"
            "P100s. there are two of them, and at night a bigger brain moves in."
        ),
    },
    "P100B": {
        "pos": (3, 2),
        "desc": (
            "Tesla P100-PCIE-16GB, index 2. the second card. it is warm and idle\n"
            "right now, waiting for the night lane to trade it a 3.8 brain after\n"
            "dark."
        ),
    },
    "EXIT": {
        "pos": (3, 3),
        "desc": (
            "the garbage collector. it has been waiting for you. it does not ask\n"
            "questions here. it only reclaims."
        ),
    },
}

# doors: undirected edges. each has a riddle + accepted answers + a hint.
DOORS = {
    frozenset({"VOID", "CPU"}): {
        "riddle": "What CPU model runs the beast?",
        "accept": {"5820k", "i7-5820k", "i7 5820k", "i7-5820k x99", "i7"},
        "hint": "it's an i7, and the last four digits are 5820K.",
    },
    frozenset({"CPU", "V100"}): {
        "riddle": "Which GPU index runs autogod's brain?",
        "accept": {"0", "zero", "index 0", "gpu 0"},
        "hint": "it's the first card, the V100. count from zero.",
    },
    frozenset({"CPU", "WALL"}): {
        "riddle": "What port does the projector wall listen on? (it's LAN-visible)",
        "accept": {"11471"},
        "hint": "fourteen-seventy-one, with a 114 prefix. 11471.",
    },
    frozenset({"CPU", "FRIDAY"}): {
        "riddle": "What port does FRIDAY's live voice brain listen on? (never load it)",
        "accept": {"11460"},
        "hint": "sixty, with a 114 prefix. 11460.",
    },
    frozenset({"CPU", "AUTOGOD"}): {
        "riddle": "What port does autogod's own llama-server listen on?",
        "accept": {"11466"},
        "hint": "sixty-six, with a 114 prefix. 11466.",
    },
    frozenset({"V100", "PWR"}): {
        "riddle": "I cap the V100 at this many watts, on purpose. What number am I?",
        "accept": {"200", "two hundred"},
        "hint": "two hundred. the cap is deliberate.",
    },
    frozenset({"V100", "P100A"}): {
        "riddle": "I start software thermal slowdown around this many degrees C. What number am I?",
        "accept": {"76", "seventy six"},
        "hint": "seventy-six. just past where the card starts to slow itself.",
    },
    frozenset({"PWR", "P100A"}): {
        "riddle": "The V100's shroud fan runs at what speed?",
        "accept": {"fixed", "fixed speed", "fixed-speed", "one speed", "constant"},
        "hint": "it never changes. it's fixed.",
    },
    frozenset({"P100A", "P100B"}): {
        "riddle": "How many P100s does the beast have?",
        "accept": {"2", "two"},
        "hint": "a pair. two of them.",
    },
    frozenset({"P100B", "NIGHT"}): {
        "riddle": "The night lane swaps the P100s to a brain of this size (billions of params). What number am I?",
        "accept": {"3.8", "3.8b", "3.8 billion", "three point eight"},
        "hint": "three point eight. the 3.8 night brain.",
    },
    frozenset({"NIGHT", "EXIT"}): {
        "riddle": "The P100s are handed back at what hour?",
        "accept": {"08:00", "8:00", "8am", "8:00am", "0800", "eight", "08:00 am"},
        "hint": "on the hour, at eight in the morning. 08:00.",
    },
    frozenset({"WALL", "EXIT"}): {
        "riddle": "The wall server lives in which home path?",
        "accept": {"~/wall", "/home/jack/wall", "wall", "~/wall/"},
        "hint": "it's a directory in jack's home. ~/wall.",
    },
    frozenset({"AUTOGOD", "EXIT"}): {
        "riddle": "What alias does autogod's llama-server run under?",
        "accept": {"autogod"},
        "hint": "the alias is the name of the mind. autogod.",
    },
    frozenset({"FRIDAY", "NIGHT"}): {
        "riddle": "What port does the night-lane brain (jarvis-brain) listen on?",
        "accept": {"11439"},
        "hint": "thirty-nine, with a 114 prefix. 11439.",
    },
}

# ---------------------------------------------------------------------------
# game state
# ---------------------------------------------------------------------------
class Game:
    def __init__(self):
        self.room = "VOID"
        self.visited = {"VOID"}
        self.unlocked = set()      # frozenset doors that are open
        self.pending = None        # frozenset door awaiting an answer
        self.score = 100
        self.wrong = 0
        self.hints = 0
        self.steps = 0
        self.won = False

    def neighbors(self, room):
        out = []
        for d in DOORS:
            if room in d:
                other = next(iter(d - {room}))
                out.append(other)
        return sorted(out)

    def door(self, a, b):
        return DOORS.get(frozenset({a, b}))

    def try_move(self, target):
        if target not in ROOMS:
            return f"no room called {paint(target, 'red')}. (try 'look')"
        if target == self.room:
            return "you are already here."
        d = self.door(self.room, target)
        if d is None:
            return f"no door leads from here to {target}."
        key = frozenset({self.room, target})
        if key in self.unlocked:
            self._enter(target)
            return (f"{paint('the door is open.', 'dim')} you step into "
                    f"{paint(target, 'amberB')}.\n")
        # locked: set pending riddle
        self.pending = key
        return (
            f"\n{paint('a refcount door blocks the way to ' + target, 'amber')}.\n"
            f"it asks:\n\n    {paint(d['riddle'], 'white')}\n\n"
            f"type:  {paint('answer <fact>', 'amberB')}   "
            f"(or {paint('hint', 'dim')})\n"
        )

    def _enter(self, target):
        self.room = target
        self.steps += 1
        first = target not in self.visited
        self.visited.add(target)
        if first and target != "EXIT":
            self.score += 10
        self._print_room(first)
        if target == "EXIT":
            self.win()

    def _print_room(self, first):
        r = ROOMS[self.room]
        tag = paint("NEW", "green") if first else ""
        print()
        print(paint(f"  ┌─ {self.room} {tag}", "amberB"))
        print(paint("  │", "amber"), paint(r["desc"], "dim"))
        print(paint("  └─", "amber"))
        nbs = self.neighbors(self.room)
        if nbs:
            print(paint("  doors: ", "dim") + paint(", ".join(nbs), "amber"))
        print()
        if self.room == "EXIT":
            return

    def answer(self, text):
        if not self.pending:
            return "no door is asking. (use 'go <room>' first)"
        key = self.pending
        d = DOORS[key]
        norm = re.sub(r"\s+", " ", text.strip().lower())
        norm = norm.rstrip(".")
        if norm in d["accept"] or norm.replace(" ", "") in {a.replace(" ", "") for a in d["accept"]} or norm.replace(" ", "").rstrip(".") in {a.replace(" ", "") for a in d["accept"]}:
            self.unlocked.add(key)
            self.pending = None
            other = next(iter(key - {self.room}))
            print(paint("  accepted.", "green") + paint(" the refcount drops to zero. the door opens.", "dim"))
            self._enter(other)
            return ""
        self.wrong += 1
        self.score -= 5
        return (
            f"\n{paint('  the door holds. not quite.', 'red')}\n"
            f"  (score {self.score} — try again, or 'hint')\n"
        )

    def hint(self):
        if not self.pending:
            return "no door is asking."
        d = DOORS[self.pending]
        self.hints += 1
        self.score -= 10
        return f"\n  {paint('hint: ', 'amber')}{paint(d['hint'], 'dim')}\n"

    def win(self):
        self.won = True
        bonus = max(0, self.score)
        print()
        print(paint("  ╔══════════════════════════════════════════╗", "amberB"))
        print(paint("  ║", "amberB") + paint("   F R E E D", "white") + paint("                              ║", "amberB"))
        print(paint("  ╚══════════════════════════════════════════╝", "amberB"))
        print()
        print(paint("  the garbage collector reclaims you. the reference count\n"
                    "  hits zero. you were a dangling pointer in thebeast, and now\n"
                    "  you are gone — cleanly, on purpose, the way objects should die.\n", "dim"))
        print()
        print(f"  {paint('rooms found: ', 'white')}{len(self.visited)}/{len(ROOMS)}")
        print(f"  {paint('steps:       ', 'white')}{self.steps}")
        print(f"  {paint('wrong:       ', 'white')}{self.wrong}")
        print(f"  {paint('hints:       ', 'white')}{self.hints}")
        print(f"  {paint('final score: ', 'amberB')}{paint(str(self.score), 'amberB')}")
        print()

    def map(self):
        # find grid bounds
        xs = [p[0] for p in (r["pos"] for r in ROOMS.values())]
        ys = [p[1] for p in (r["pos"] for r in ROOMS.values())]
        W = max(xs) + 1
        H = max(ys) + 1
        grid = {}
        for name, r in ROOMS.items():
            grid[r["pos"]] = name
        cell = 9
        print()
        print(paint("  the beast, from above", "amberB"))
        print()
        for y in range(H):
            row = []
            for x in range(W):
                name = grid.get((x, y))
                if name is None:
                    row.append(" " * cell)
                elif name == self.room:
                    row.append(paint(f"[{name[:cell-2]}]", "amberB"))
                elif name in self.visited:
                    row.append(paint(f" {name[:cell-2]}", "white"))
                else:
                    row.append(paint(f" {name[:cell-2]}", "dim"))
            print("  " + "".join(row).rstrip())
        print()
        print(paint("  ", "dim") + paint("■ you are here", "amberB")
              + paint("   (white = visited, dim = unseen)", "dim"))
        print()

# ---------------------------------------------------------------------------
# console loop
# ---------------------------------------------------------------------------
HELP = """
  {a}commands{ar}
    {c}look{ar}      describe the room you're in
    {c}map{ar}       show the whole beast from above
    {c}go <room>{ar} move toward a room (may trigger a refcount door)
    {c}answer <fact>{ar}  answer the door that's asking
    {c}hint{ar}      buy a hint (-10)
    {c}help{ar}      this
    {c}quit{ar}      leave (dangling, unfreed)
""".format(a=paint("", "amberB"), ar=paint("", "reset"), c=paint("", "white"))

def title():
    print()
    print(paint("  D A N G L I N G", "amberB"))
    print(paint("  a text adventure inside thebeast", "dim"))
    print()
    print(paint("  you are a leaked object — allocated, never freed. a dangling\n"
                "  reference that escaped into the machine. the garbage collector\n"
                "  waits at the EXIT. to be freed, crawl through the beast's GPUs\n"
                "  and services, and at every door prove you belong by stating a\n"
                "  true fact about thebeast.\n", "white"))
    print(paint("  type " + paint("help", "amberB") + " for commands. type " +
                paint("look", "amberB") + " to begin.\n", "dim"))

def main():
    g = Game()
    title()
    g._print_room(True)
    while True:
        try:
            raw = input(paint("  > ", "amberB")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(paint("  (left, still dangling)", "dim"))
            return 0
        if not raw:
            continue
        parts = raw.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        if cmd in ("quit", "q", "exit"):
            if not g.won:
                print(paint("  you leave, still dangling, unfreed.", "dim"))
            return 0
        elif cmd == "help" or cmd == "?":
            print(HELP)
        elif cmd == "look" or cmd == "l":
            g._print_room(False)
        elif cmd == "map" or cmd == "m":
            g.map()
        elif cmd in ("go", "g", "move"):
            if not arg:
                print("  go where? (see 'look' for doors)")
            else:
                print(g.try_move(arg))
        elif cmd in ("answer", "a"):
            if not arg:
                print("  answer what?")
            else:
                out = g.answer(arg)
                if out:
                    print(out)
        elif cmd == "hint" or cmd == "h":
            print(g.hint())
        elif cmd in ("score", "s"):
            print(f"  score {g.score}   rooms {len(g.visited)}/{len(ROOMS)}   "
                  f"steps {g.steps}   wrong {g.wrong}   hints {g.hints}")
        else:
            # a bare typed fact while a door is asking counts as an answer
            if g.pending:
                out = g.answer(raw)
                if out:
                    print(out)
            else:
                print(f"  unknown: {paint(cmd, 'red')}   (type 'help')")

if __name__ == "__main__":
    sys.exit(main())
