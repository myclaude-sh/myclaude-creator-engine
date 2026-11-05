"""
pre_iteration.py — Heavy-think pre-iteration diagnostic gate.

USE: python scripts/pre_iteration.py --N <iteration-number>
                                     --hm <mean-quality 0-10>
                                     --hp <best-quality 0-10>
                                     --prev-answer <str>
                                     --new-answer <str>
                                     --reasoning-strength <prev,new>

Implements Checks 1-4 from SKILL.md §Iteration. Returns ITERATE or STOP
with reason. Catches contamination cascade by monitoring reasoning
strength delta, not just answer stability.

Stdlib only.
"""
import argparse
import sys

CEILING_GAP_EPSILON = 0.5  # HM/HP within this = ceiling reached
ITER_CAP = 3


def diagnose(N: int, hm: float, hp: float,
             prev_answer: str, new_answer: str,
             prev_reasoning: float, new_reasoning: float) -> dict:

    # Check 4 first: hard cap
    if N >= ITER_CAP:
        return {"decision": "STOP",
                "check": 4,
                "reason": f"Iteration cap reached (N={N} >= {ITER_CAP}). "
                          "Empirically, returns are negative past N=3."}

    # Check 1: ceiling
    if abs(hm - hp) <= CEILING_GAP_EPSILON:
        return {"decision": "STOP",
                "check": 1,
                "reason": f"Ceiling reached (HM={hm} ~ HP={hp}, "
                          f"gap <= {CEILING_GAP_EPSILON}). Further iteration "
                          "trades potential for consistency."}

    # Check 3: reasoning weakening (cascade) — checked before Check 2
    # so cascade is named even when answer stays same.
    same_answer = prev_answer.strip() == new_answer.strip()
    if same_answer and new_reasoning < prev_reasoning:
        return {"decision": "STOP",
                "check": 3,
                "reason": f"CONTAMINATION CASCADE detected. Same answer, "
                          f"weaker reasoning ({prev_reasoning} -> "
                          f"{new_reasoning}). Stop immediately. v1 "
                          "deliberation likely better than degraded vN."}

    # Check 2: no new resolution (consistency-without-insight decay)
    if same_answer and new_reasoning <= prev_reasoning:
        return {"decision": "STOP",
                "check": 2,
                "reason": f"Consistency-without-insight decay. Same answer "
                          f"as N-1 with no stronger supporting reasoning "
                          f"({prev_reasoning} -> {new_reasoning})."}

    return {"decision": "ITERATE",
            "reason": f"All checks passed at N={N}. Proceed with iteration."}


def main():
    p = argparse.ArgumentParser(description="Heavy-think pre-iteration gate")
    p.add_argument("--N", type=int, required=True,
                   help="Iteration number to consider (the N you are about to run)")
    p.add_argument("--hm", type=float, required=True,
                   help="Mean deliberation quality 0-10")
    p.add_argument("--hp", type=float, required=True,
                   help="Best deliberation quality 0-10")
    p.add_argument("--prev-answer", type=str, required=True,
                   help="Answer from previous iteration")
    p.add_argument("--new-answer", type=str, required=True,
                   help="Answer from current iteration")
    p.add_argument("--reasoning-strength", type=str, required=True,
                   help="Comma-separated 'prev,new' reasoning strength scores 0-10")
    args = p.parse_args()

    parts = [s.strip() for s in args.reasoning_strength.split(",")]
    if len(parts) != 2:
        print("ERROR: --reasoning-strength must be 'prev,new'", file=sys.stderr)
        sys.exit(1)
    prev_reasoning, new_reasoning = float(parts[0]), float(parts[1])

    result = diagnose(args.N, args.hm, args.hp,
                      args.prev_answer, args.new_answer,
                      prev_reasoning, new_reasoning)

    print(f"Decision: {result['decision']}")
    if "check" in result:
        print(f"Triggered check: #{result['check']}")
    print(f"Reason: {result['reason']}")

    sys.exit(0 if result["decision"] == "ITERATE" else 2)


if __name__ == "__main__":
    main()
