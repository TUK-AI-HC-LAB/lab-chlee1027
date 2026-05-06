"""Apply our local modification to upstream patchcore-inspection's bin/run_patchcore.py.

Single change: in `image_transform()`, replace dataset-attribute access with
hardcoded ImageNet mean/std. Upstream code does
``dataloaders["testing"].dataset.transform_std/_mean`` but the MVTec dataset
class in the version we use doesn't expose those attributes, so segmentation
visualization fails. We hardcode the ImageNet standard values instead.

Idempotent — running twice is a no-op.
"""
import re
import sys
from pathlib import Path


# Match the unique pair of lines that reference dataset.transform_std/_mean.
# We capture the leading indent so we preserve it in the replacement.
PATTERN = re.compile(
    r"^(?P<indent>[ \t]+)in_std = np\.array\(\s*"
    r"dataloaders\[\"testing\"\]\.dataset\.transform_std\s*"
    r"\)\.reshape\(-1, 1, 1\)\s*"
    r"(?P=indent)in_mean = np\.array\(\s*"
    r"dataloaders\[\"testing\"\]\.dataset\.transform_mean\s*"
    r"\)\.reshape\(-1, 1, 1\)",
    re.MULTILINE,
)

ALREADY_PATCHED = re.compile(
    r"in_std = np\.array\(\[0\.229, 0\.224, 0\.225\]\)\.reshape\(-1, 1, 1\)"
)


def main(target: str) -> None:
    path = Path(target)
    if not path.exists():
        sys.exit(f"[apply_modifications] file not found: {path}")

    text = path.read_text()

    if ALREADY_PATCHED.search(text):
        print(f"[apply_modifications] already patched: {path}")
        return

    def repl(m: "re.Match[str]") -> str:
        ind = m.group("indent")
        return (
            f"{ind}in_std = np.array([0.229, 0.224, 0.225]).reshape(-1, 1, 1)\n"
            f"{ind}in_mean = np.array([0.485, 0.456, 0.406]).reshape(-1, 1, 1)"
        )

    new_text, n = PATTERN.subn(repl, text)
    if n == 0:
        sys.exit(
            f"[apply_modifications] could not locate the original block in {path}. "
            "Upstream may have changed; please apply the modification manually "
            "(see method1_patchcore/source/README.md '수정 내역')."
        )

    path.write_text(new_text)
    print(f"[apply_modifications] patched {path} ({n} substitution)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: apply_modifications.py <path-to-bin/run_patchcore.py>")
    main(sys.argv[1])
