import subprocess
from pathlib import Path


def main():
    print("Starting data generation...")
    tmp_dp = Path("tmp")
    tmp_dp.mkdir(exist_ok=True, parents=True)

    # generate SYS-GetProv.txt
    generate_sys_getprov(tmp_dp)

    # generate SYS-Pin.txt
    generate_sys_pin(tmp_dp)

    # generate SYS-GetTag.txt and SYS-SetTagID.txt
    generate_sys_gettag_and_settagid(tmp_dp)

    # generate SYS-GetTagName.txt
    generate_sys_gettagname(tmp_dp)

    # generate tradenode province groups
    generate_tradenode_province_groups(tmp_dp)

    # run provsize.py
    run_provsize()

    # generate SYS-Rugged.txt
    generate_sys_rugged(tmp_dp)

    # generate pins for ambient_objects.txt
    generate_pins_for_ambient_objects()


def generate_sys_getprov(tmp_dp: Path):
    print("Generating SYS-GetProv.txt...")
    output_fp = Path("output.txt")
    tmp_fp = tmp_dp / "SYS-GetProv.txt"
    target_fp = Path("common/scripted_effects/SYS-GetProv.txt")

    start_marker = "#START_REPLACE"
    stop_marker = "#STOP_REPLACE"

    # delete output and tmp if they exist
    if output_fp.exists():
        output_fp.unlink()
    if tmp_fp.exists():
        tmp_fp.unlink()

    # generate output.txt
    inputs = [
        "1",
        "1",
        get_last_province_id(),
        "check_key = { lhs = S_ID value = %s }",
        "%s = { save_event_target_as = GetProvOut }",
    ]
    subprocess.run(
        ["python", "binary_tree.py"],
        input="\n".join(inputs) + "\n",
        text=True,
    )

    # move to tmp
    output_fp.rename(tmp_fp)

    # replace in target
    target_text = target_fp.read_text(encoding="utf-8")
    output_text = tmp_fp.read_text(encoding="utf-8")

    before, _, rest = target_text.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text = f"{before}{start_marker}\n{output_text}\n{stop_marker}{after}"
    target_fp.write_text(new_text, encoding="utf-8")


def generate_sys_pin(tmp_dp: Path):
    print("Generating SYS-Pin.txt...")
    output_fp = Path("output.txt")
    tmp_fp = tmp_dp / "SYS-Pin.txt"
    target_fp = Path("common/scripted_effects/SYS-Pin.txt")

    start_marker = "#START_REPLACE"
    stop_marker = "#STOP_REPLACE"

    # delete output and tmp if they exist
    if output_fp.exists():
        output_fp.unlink()
    if tmp_fp.exists():
        tmp_fp.unlink()

    # generate output.txt
    inputs = [
        "1",
        "1",
        get_last_province_id(),
        "check_key = { lhs = $inp$ value = %s }",
        "$action$_ambient_object = pin_%s",
    ]
    subprocess.run(
        ["python", "binary_tree.py"],
        input="\n".join(inputs) + "\n",
        text=True,
    )

    # move to tmp
    output_fp.rename(tmp_fp)

    # replace in target
    target_text = target_fp.read_text(encoding="utf-8")
    output_text = tmp_fp.read_text(encoding="utf-8")

    before, _, rest = target_text.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text = f"{before}{start_marker}\n{output_text}\n{stop_marker}{after}"
    target_fp.write_text(new_text, encoding="utf-8")


def generate_sys_gettag_and_settagid(tmp_dp: Path):
    print("Generating SYS-GetTag.txt and SYS-SetTagID.txt...")
    output_fp = Path("output.txt")
    outputt_fp = Path("outputt.txt")
    tmp_gettag_fp = tmp_dp / "SYS-GetTag.txt"
    tmp_settagid_fp = tmp_dp / "SYS-SetTagID.txt"
    target_gettag_fp = Path("common/scripted_effects/SYS-GetTag.txt")
    target_settagid_fp = Path("common/scripted_effects/SYS-SetTagID.txt")

    start_marker = "#START_REPLACE"
    stop_marker = "#STOP_REPLACE"

    # delete output and tmp if they exist
    if output_fp.exists():
        output_fp.unlink()
    if outputt_fp.exists():
        outputt_fp.unlink()
    if tmp_gettag_fp.exists():
        tmp_gettag_fp.unlink()
    if tmp_settagid_fp.exists():
        tmp_settagid_fp.unlink()

    # generate output.txt and outputt.txt
    subprocess.run(
        ["python", "binarycountry.py"],
    )

    # move to tmp
    output_fp.rename(tmp_gettag_fp)
    outputt_fp.rename(tmp_settagid_fp)

    # replace in gettag
    target_text_gettag = target_gettag_fp.read_text(encoding="utf-8")
    output_text_gettag = tmp_gettag_fp.read_text(encoding="utf-8")

    before, _, rest = target_text_gettag.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text_gettag = (
        f"{before}{start_marker}\n{output_text_gettag}\n{stop_marker}{after}"
    )
    target_gettag_fp.write_text(new_text_gettag, encoding="utf-8")

    # replace in settagid
    target_text_settagid = target_settagid_fp.read_text(encoding="utf-8")
    output_text_settagid = tmp_settagid_fp.read_text(encoding="utf-8")

    before, _, rest = target_text_settagid.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text_settagid = (
        f"{before}{start_marker}\n{output_text_settagid}\n{stop_marker}{after}"
    )
    target_settagid_fp.write_text(new_text_settagid, encoding="utf-8")


def generate_sys_gettagname(tmp_dp: Path):
    print("Generating SYS-GetTagName.txt...")
    output_fp = Path("output.txt")
    tmp_fp = tmp_dp / "SYS-GetTagName.txt"
    target_fp = Path("common/scripted_effects/SYS-GetTagName.txt")

    start_marker = "#START_REPLACE"
    stop_marker = "#STOP_REPLACE"

    # delete output and tmp if they exist
    if output_fp.exists():
        output_fp.unlink()
    if tmp_fp.exists():
        tmp_fp.unlink()

    # generate output.txt
    subprocess.run(
        ["python", "binarycountryNames.py"],
    )

    # move to tmp
    output_fp.rename(tmp_fp)

    # replace in target
    target_text = target_fp.read_text(encoding="utf-8")
    output_text = tmp_fp.read_text(encoding="utf-8")

    before, _, rest = target_text.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text = f"{before}{start_marker}\n{output_text}\n{stop_marker}{after}"
    target_fp.write_text(new_text, encoding="utf-8")


def generate_tradenode_province_groups(tmp_dp: Path):
    print("Generating tradenode province groups...")
    output_fp = Path("output.txt")
    tmp_fp = tmp_dp / "tradenode_province_groups.txt"
    target_fp = Path("map/provincegroup.txt")

    start_marker = "#START_REPLACE_TRADENODES"
    stop_marker = "#STOP_REPLACE_TRADENODES"

    # delete output and tmp if they exist
    if output_fp.exists():
        output_fp.unlink()
    if tmp_fp.exists():
        tmp_fp.unlink()

    # generate output.txt
    subprocess.run(
        ["python", "MAP-Tradenode_Province_Groups.py"],
    )

    # move to tmp
    output_fp.rename(tmp_fp)

    # replace in target
    target_text = target_fp.read_text(encoding="utf-8")
    output_text = tmp_fp.read_text(encoding="utf-8")

    before, _, rest = target_text.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text = f"{before}{start_marker}\n{output_text}\n{stop_marker}{after}"
    target_fp.write_text(new_text, encoding="utf-8")


def run_provsize():
    print("Running provsize.py...")
    subprocess.run(
        ["python", "provsize.py"],
    )


def generate_sys_rugged(tmp_dp: Path):
    print("Generating SYS-Rugged.txt...")
    output_fp = Path("out.txt")
    tmp_fp = tmp_dp / "SYS-Rugged.txt"
    target_fp = Path("common/scripted_effects/SYS-Rugged.txt")

    start_marker = "#START_REPLACE"
    stop_marker = "#STOP_REPLACE"

    # delete output and tmp if they exist
    if output_fp.exists():
        output_fp.unlink()
    if tmp_fp.exists():
        tmp_fp.unlink()

    # generate output.txt
    subprocess.run(
        ["python", "rugged.py"],
    )

    # move to tmp
    output_fp.rename(tmp_fp)

    # replace in target
    target_text = target_fp.read_text(encoding="utf-8")
    output_text = tmp_fp.read_text(encoding="utf-8")

    before, _, rest = target_text.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text = f"{before}{start_marker}\n{output_text}\n{stop_marker}{after}"
    target_fp.write_text(new_text, encoding="utf-8")


def generate_pins_for_ambient_objects():
    print("Generating pins for ambient_objects.txt...")
    output_fp = Path("map/pinpos.txt")
    tmp_fp = Path("tmp/pinpos.txt")
    target_fp = Path("map/ambient_object.txt")

    start_marker = "#START_REPLACE_PINS"
    stop_marker = "#STOP_REPLACE_PINS"

    # delete output if it exists
    if output_fp.exists():
        output_fp.unlink()
    if tmp_fp.exists():
        tmp_fp.unlink()

    # generate output.txt
    subprocess.run(
        ["python", "MAP-Generate_Pins.py"],
    )

    # replace in target
    target_text = target_fp.read_text(encoding="utf-8")
    output_text = output_fp.read_text(encoding="utf-8")

    before, _, rest = target_text.partition(start_marker)
    _, _, after = rest.partition(stop_marker)

    new_text = f"{before}{start_marker}\n{output_text}\n{stop_marker}{after}"
    target_fp.write_text(new_text, encoding="utf-8")


def get_last_province_id() -> str:
    definition_fp = Path("map/definition.csv")
    with definition_fp.open("r", encoding="utf-8") as f:
        last_line = f.readlines()[-1].strip()
        last_id = last_line.split(";")[0]
    return last_id


if __name__ == "__main__":
    main()
