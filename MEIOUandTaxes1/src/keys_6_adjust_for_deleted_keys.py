# by KJH, Phlopsi & JF

import os
import shutil
import ahocorasick
from concurrent.futures import ProcessPoolExecutor, as_completed

def load_keys(filename):
    result = {}
    if not os.path.exists(filename):
        return result
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, var = line.split(":", 1)
            result[key.strip()] = var.strip()
    return result


def build_automaton(replacement_map):
    A = ahocorasick.Automaton()
    for old_var, new_var in replacement_map.items():
        A.add_word(old_var, (old_var, new_var))
    A.make_automaton()
    return A


def replace_with_automaton(text, automaton):
    out = []
    last_end = 0
    for end_idx, (old_var, new_var) in automaton.iter(text):
        start_idx = end_idx - len(old_var) + 1
        if start_idx < last_end:
            continue  # overlaps a match already applied this pass, skip
        before_ok = start_idx == 0 or not (text[start_idx - 1].isalnum() or text[start_idx - 1] == "_")
        after_ok = end_idx + 1 == len(text) or not (text[end_idx + 1].isalnum() or text[end_idx + 1] == "_")
        if before_ok and after_ok:
            out.append(text[last_end:start_idx])
            out.append(new_var)
            last_end = end_idx + 1
    out.append(text[last_end:])
    return "".join(out)


def process_file(filename, base_dir, replacement_map):
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        return f"Missing: {filename}"

    # build INSIDE process, same reasoning as compiling regex per-process
    automaton = build_automaton(replacement_map)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = replace_with_automaton(text, automaton)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return f"Updated {filename}"


def update_localization_vars():
    old_keys = load_keys("keys_old.txt")
    new_keys = load_keys("keys.txt")

    if not old_keys:
        print("No oldkeys.txt found, skipping localization update.")
        shutil.copyfile("keys.txt", "keys_old.txt")
        return

    if old_keys == new_keys:
        print("No key changes detected. Skipping localization update.")
        shutil.copyfile("keys.txt", "keys_old.txt")
        return

    old_var_to_key = {v: k for k, v in old_keys.items()}
    files = [
        "DISP-Trade_Bought.txt",
        "DISP-Trade_Bought_2.txt",
        "DISP-Trade_Bought_3.txt",
        "DISP-Trade_Sold.txt",
        "DISP-Trade_Sold_2.txt",
        "DISP-Trade_Sold_3.txt",
        "SYS-LocPlague.txt",
        "SYS-Modifiers.txt",
    ]
    base_dir = os.path.join("customizable_localization")

    replacement_map = {}
    for old_var, key in old_var_to_key.items():
        if key in new_keys:
            replacement_map[old_var] = new_keys[key]

    if not replacement_map:
        print("No matching vars to replace.")
        shutil.copyfile("keys.txt", "keys_old.txt")
        return

    with ProcessPoolExecutor(max_workers=min(8, len(files))) as executor:
        futures = {
            executor.submit(process_file, filename, base_dir, replacement_map): filename
            for filename in files
        }
        for future in as_completed(futures):
            print(future.result())

    shutil.copyfile("keys.txt", "keys_old.txt")

if __name__ == "__main__":
    update_localization_vars()
