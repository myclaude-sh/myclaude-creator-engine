"""
mode_select.py — Heavy-think deliberation mode classifier.

USE: python scripts/mode_select.py --answers "ans1,ans2,ans3,ans2,ans1"
                                   [--verifiable]

Computes agreement_ratio across K trajectory final answers and selects
deliberation mode per SKILL.md §Stage-2 mode selection.

Stdlib only.
"""
import argparse
from collections import Counter

VERIFICATION_THRESHOLD = 0.75
SYNTHESIS_THRESHOLD = 0.50


def classify(answers: list[str], verifiable: bool) -> dict:
    if not answers:
        return {"mode": "ABORT", "reason": "no answers provided"}

    K = len(answers)
    counts = Counter(a.strip() for a in answers)
    most_common, freq = counts.most_common(1)[0]
    agreement = freq / K

    if agreement >= VERIFICATION_THRESHOLD and verifiable:
        mode = "VERIFICATION"
        focus = ("Validate consensus correctness. Check whether any "
                 "dissenting trajectory exposes a flaw the majority missed.")
    elif agreement < SYNTHESIS_THRESHOLD:
        mode = "SYNTHESIS"
        focus = ("Genuine cross-trajectory synthesis. Identify partial "
                 "truths, resolve contradictions, cross-pollinate insights. "
                 "May re-derive from scratch.")
    else:
        mode = "HYBRID"
        focus = ("Verify the leading answer; mine minority trajectories "
                 "for missed insights or edge cases.")

    return {
        "mode": mode,
        "focus": focus,
        "K": K,
        "distribution": dict(counts),
        "leading_answer": most_common,
        "agreement_ratio": round(agreement, 3),
        "verifiable": verifiable,
    }


def main():
    p = argparse.ArgumentParser(description="Heavy-think mode classifier")
    p.add_argument("--answers", type=str, required=True,
                   help="Comma-separated final answers from K trajectories")
    p.add_argument("--verifiable", action="store_true",
                   help="Task has verifiable correctness criteria "
                        "(required for VERIFICATION mode)")
    args = p.parse_args()

    answers = [a for a in args.answers.split(",") if a.strip()]
    result = classify(answers, args.verifiable)

    print(f"Mode: {result['mode']}")
    if "focus" in result:
        print(f"Focus: {result['focus']}")
        print(f"K: {result['K']}")
        print(f"Agreement ratio: {result['agreement_ratio']}")
        print(f"Leading answer: {result['leading_answer']}")
        print(f"Distribution: {result['distribution']}")
        if not result["verifiable"] and result["mode"] != "SYNTHESIS":
            print("\nNote: --verifiable not set. Even at high agreement, "
                  "task non-verifiability may warrant SYNTHESIS over "
                  "VERIFICATION.")
    else:
        print(f"Reason: {result['reason']}")


if __name__ == "__main__":
    main()
