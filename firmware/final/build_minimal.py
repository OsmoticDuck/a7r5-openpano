"""Minimal active extended-aspect build.

Uses the last full functional baseline that already includes the custom
2:1 / 65:24 menu and playback icons (the 4.92 quality-menu base supplied by
sony-a7r5-custom-firmware). That baseline already has the AF fixes and the
bounded diagnostic hooks restored to the original instructions, so no binary
patching is needed here.

No version number is assigned here. The firmware version is a container number
chosen at packaging time (any value newer than the installed one).
"""
from pathlib import Path
import hashlib, json, os, shutil

H = Path(__file__).resolve().parent
P = H.parent
BASE_AP = P / "build-4.92-quality-menu-20261105/patched/appFw.so"
BASE_CP = P / "build-4.92-quality-menu-20261105/patched/cpapp-b.bin"
BASE_AP_SHA = "d17861657b062d4228ea74b31844bf7476cd82e3530c36b9b201f930c3df432f"
BASE_CP_SHA = "feececdcfdfff740324327eadedc863fc293e136b9b1db91cc8bc4e222f550c4"
FINAL_AP_SHA = BASE_AP_SHA
FINAL_CP_SHA = BASE_CP_SHA


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = BASE_AP.read_bytes()
    cp = BASE_CP.read_bytes()
    assert sha(ap) == BASE_AP_SHA
    assert sha(cp) == BASE_CP_SHA
    (H / "ap-build").mkdir(exist_ok=True)
    (H / "ap-build/appFw-minimal.NONINSTALLABLE.so").write_bytes(ap)
    (H / "ap-build/cpapp-minimal.NONINSTALLABLE.bin").write_bytes(cp)
    report = dict(
        container_version=os.environ.get("FIRMWARE_VERSION", ""),
        base_AP_sha256=BASE_AP_SHA,
        final_AP_sha256=FINAL_AP_SHA,
        final_CP_sha256=FINAL_CP_SHA,
        base_is_final=True,
        active_feature="extended aspect ratios 4..6, custom icons, AF and required restart/display fixes",
        icons_installed=True,
        af_frame_fix_included=True,
        debug_hooks_already_absent=True,
        dead_diagnostic_code_retained=False,
        raw_zoom_fix_included=False,
        physical_camera_tested=False,
        all_issues_fixed=False,
    )
    (H / "build-minimal.json").write_text(json.dumps(report, indent=2) + "\n")
    print(FINAL_AP_SHA)


if __name__ == "__main__":
    main()
