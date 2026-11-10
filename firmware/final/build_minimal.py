"""Minimal active extended-aspect build.

Starts from the last functional extended-aspect base (supplied by
sony-a7r5-custom-firmware), disables the bounded diagnostic hooks that are not
needed for the aspect-ratio feature, and leaves the dead diagnostic code
untouched (removing it would require a full re-link and is not provided).

No version number is assigned here. The firmware version is a container number
chosen at packaging time (any value newer than the installed one).
"""
from pathlib import Path
import hashlib, io, json, os, sys
H = Path(__file__).resolve().parent
P = H.parent
sys.path.insert(0, str(P.parent / "a7r5/direct-p1-read-20261031/analysis-deps"))
from elftools.elf.elffile import ELFFile

BASE_AP = P / "build-4.85-liveview-20261104/patched/appFw.so"
BASE_CP = P / "build-4.85-liveview-20261104/patched/cpapp-b.bin"
BASE_AP_SHA = "9f947f68bec0d6a5140a5d31078ed5cdda920c7b25c656fb619d953eb4833e7a"
FINAL_AP_SHA = "30f556e7c106b5aabb0b06127c08cbdc81229a02f440f1bf6b771038410beb6c"
FINAL_CP_SHA = "1bcdddcff45ac551d36f0992955e2ffb0c1c54c3d12d3f0c37d0cfb306146f84"
AF_AT = 0x16d82f0
AF_BEFORE = bytes.fromhex("01008052")
AF_AFTER = bytes.fromhex("815a40b9")

# (VA, expected current, original instruction, why)
RESTORE = [
    (0x35b858c, "3b7e8417", "fd7bbca9", "disable bounded fatal-signal recorder: assert hook"),
    (0x35b8564, "6c7e8417", "fd7bbfa9", "disable bounded fatal-signal recorder: fatal hook"),
    (0x8e974e4, "b3022116", "fd7bbea9", "disable bounded fatal-signal recorder: request hook"),
    (0x1c61d14, "ccd8e917", "fd7bb9a9", "disable bounded fatal-signal recorder: set hook"),
    (0x1c93d88, "d610e917", "fd7bbda9", "disable bounded fatal-signal recorder: sequence hook"),
    (0x1878128, "eb82f917", "ff0314d1", "disable AF RAM observer hook"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def off(elf, va):
    for s in elf.iter_segments():
        if s["p_type"] == "PT_LOAD" and s["p_vaddr"] <= va < s["p_vaddr"] + s["p_filesz"]:
            return va - s["p_vaddr"] + s["p_offset"]
    raise KeyError(hex(va))


def main():
    base = BASE_AP.read_bytes()
    cp = BASE_CP.read_bytes()
    assert sha(base) == BASE_AP_SHA
    assert sha(cp) == FINAL_CP_SHA
    elf = ELFFile(io.BytesIO(base))
    out = bytearray(base)
    for va, current, original, why in RESTORE:
        o = off(elf, va)
        assert out[o:o + 4].hex() == current, (hex(va), out[o:o + 4].hex(), current)
        out[o:o + 4] = bytes.fromhex(original)
    af_o = off(elf, AF_AT)
    assert out[af_o:af_o + 4] == AF_BEFORE
    out[af_o:af_o + 4] = AF_AFTER
    assert sha(out) == FINAL_AP_SHA
    (H / "ap-build").mkdir(exist_ok=True)
    (H / "ap-build/appFw-minimal.NONINSTALLABLE.so").write_bytes(out)
    (H / "ap-build/cpapp-minimal.NONINSTALLABLE.bin").write_bytes(cp)
    report = dict(
        container_version=os.environ.get("FIRMWARE_VERSION", ""),
        base_AP_sha256=BASE_AP_SHA,
        final_AP_sha256=FINAL_AP_SHA,
        final_CP_sha256=FINAL_CP_SHA,
        active_feature="extended aspect ratios 4..6, required restart/display fixes, and the final AF source fix",
        debug_hooks_disabled=[dict(va=hex(va), current=current, original=original, why=why) for va, current, original, why in RESTORE],
        dead_diagnostic_code_retained=True,
        full_relink_without_dead_code=False,
        af_frame_fix_included=True,
        raw_zoom_fix_included=False,
        physical_camera_tested=False,
        all_issues_fixed=False,
    )
    (H / "build-minimal.json").write_text(json.dumps(report, indent=2) + "\n")
    print(FINAL_AP_SHA)


if __name__ == "__main__":
    main()