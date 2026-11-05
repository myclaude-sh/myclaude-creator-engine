"""
constraint_check.py — Heavy-think pre-execution constraint gate.

USE: python scripts/constraint_check.py --context <tokens> --K <K>
                                        [--per-traj <tokens>]
                                        [--latency-target <s>]
                                        [--per-traj-latency <s>]

Computes whether the chosen K is viable given context window and (optional)
latency budget. Implements rules R1-R4 from SKILL.md §Constraint-aware
execution. Outputs adjusted K + reason, or ABORT signal.

Stdlib only.
"""
import argparse
import sys

CACHE_RATIO_MAX = 0.60
DELIB_BUDGET_MIN = 2000
K_MIN = 3
DEFAULT_PER_TRAJ_TOKENS = 1200


def evaluate(context: int, K: int, per_traj: int,
             latency_target: float | None,
             per_traj_latency: float | None) -> dict:
    notes = []
    adjusted_K = K

    while adjusted_K >= K_MIN:
        cache_est = adjusted_K * per_traj
        delib_budget = context - cache_est

        # R1: cache must not exceed 60% of available context
        if cache_est > CACHE_RATIO_MAX * context:
            adjusted_K -= 1
            notes.append(f"R1 violated at K={adjusted_K + 1}: cache "
                         f"({cache_est}) > 60% of context ({int(CACHE_RATIO_MAX * context)}). "
                         f"Reducing K.")
            continue

        # R2: minimum viable deliberation budget
        if delib_budget < DELIB_BUDGET_MIN:
            adjusted_K -= 1
            notes.append(f"R2 violated at K={adjusted_K + 1}: deliberation "
                         f"budget ({delib_budget}) < {DELIB_BUDGET_MIN}. "
                         f"Reducing K.")
            continue

        # R4: latency budget (if applicable)
        if latency_target is not None and per_traj_latency is not None:
            total_latency = adjusted_K * per_traj_latency
            if total_latency > latency_target:
                adjusted_K -= 1
                notes.append(f"R4 violated at K={adjusted_K + 1}: "
                             f"{total_latency:.1f}s > target {latency_target:.1f}s. "
                             f"Reducing K.")
                continue

        # All constraints satisfied at this K
        return {
            "status": "OK",
            "K": adjusted_K,
            "cache_estimate": cache_est,
            "deliberation_budget": delib_budget,
            "notes": notes,
        }

    # R3: K dropped below minimum viable
    return {
        "status": "ABORT",
        "K": adjusted_K,
        "reason": (f"K reduced below minimum ({K_MIN}). Heavy thinking with "
                   f"K<3 is empirically worse than good single-pass. "
                   f"FALLBACK: enriched single-pass + structured self-critique."),
        "notes": notes,
    }


def main():
    p = argparse.ArgumentParser(description="Heavy-think constraint gate")
    p.add_argument("--context", type=int, required=True,
                   help="Available context budget in tokens (window - system - convo)")
    p.add_argument("--K", type=int, required=True,
                   help="Desired number of parallel trajectories")
    p.add_argument("--per-traj", type=int, default=DEFAULT_PER_TRAJ_TOKENS,
                   help=f"Estimated tokens per pruned trajectory (default {DEFAULT_PER_TRAJ_TOKENS})")
    p.add_argument("--latency-target", type=float, default=None,
                   help="Optional latency budget in seconds")
    p.add_argument("--per-traj-latency", type=float, default=None,
                   help="Optional per-trajectory latency in seconds")
    args = p.parse_args()

    result = evaluate(args.context, args.K, args.per_traj,
                      args.latency_target, args.per_traj_latency)

    print(f"Status: {result['status']}")
    print(f"K (final): {result['K']}")
    if result["status"] == "OK":
        print(f"Cache estimate: {result['cache_estimate']} tokens")
        print(f"Deliberation budget: {result['deliberation_budget']} tokens")
    else:
        print(f"Reason: {result['reason']}")

    if result["notes"]:
        print("\nAdjustments:")
        for n in result["notes"]:
            print(f"  - {n}")

    sys.exit(0 if result["status"] == "OK" else 2)


if __name__ == "__main__":
    main()
