import pandas as pd
import random
import sys


def get_prev_matches(df: pd.DataFrame) -> dict:
    pairing_dict = {}
    for index, row in df.iterrows():
        member = row["Members"]
        prev_matches = set(row.iloc[1:])
        pairing_dict[member] = prev_matches
    return pairing_dict


def create_matches(members: list, old_pairs: dict) -> list:
    n = len(members)
    matches = [None] * n
    unmatched_indices = list(range(n))

    while unmatched_indices:
        idx = random.choice(unmatched_indices)
        unmatched_indices.remove(idx)
        member = members[idx]

        possible_matches = [i for i in unmatched_indices if members[i] not in old_pairs[member]]

        if possible_matches:
            match_idx = random.choice(possible_matches)
            match_member = members[match_idx]

            matches[idx] = match_member
            matches[match_idx] = member

            unmatched_indices.remove(match_idx)

        else:
            print(f"NO VALID MATCHES FOR {member}")

    return matches


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    instructions = """
    -------- INSTRUCTIONS --------
    
    (1) Generate Pairs -> python3 main.py generate <file-to-read> <date>  
    
        Creates new pairs for <date> based on <file-to-read>    
            
        Arg Examples:
            Example for <file-to-read>: "Donut Dates.csv"
            Example for <date>: "April 30"
            
        Returns:
            Creates file with the name: "<date> Donut Dates.csv"
            
    (2) Shuffle Last Matching -> python3 main.py shuffle <file-to-read>
        
        Replaces the last column of matches in <file-to-read>  
            
        Arg Examples:
            Example for <date>: "April 30"
            Example for <file-to-read>: "Donut Dates.csv"
            
        Returns:
            Replaces file with same name of <file-to-read> 
    """

    if len(sys.argv) < 3:
        print(instructions)
        sys.exit(1)

    command = sys.argv[1]
    csv_path = sys.argv[2]

    if (command == "generate" and len(sys.argv) != 4) or (command == "shuffle" and len(sys.argv) != 3):
        print(instructions)
        sys.exit(1)

    # df = pd.read_csv(csv_path, header=0, index_col=0)

    date, df = None, None
    # date = None
    if command == "generate":
        df = pd.read_csv(csv_path, header=0)
        print(df)

        date = sys.argv[3]
    elif command == "shuffle":
        df = pd.read_csv(csv_path, header=0)

        # Grab last date and drop the last col
        date = df.columns.values[-1]
        df = df.drop(date, axis=1)

    all_members = df["Members"]

    pairing_dict = get_prev_matches(df)

    new_matches = create_matches(all_members, pairing_dict)

    df[date] = new_matches

    print(df)

    df.to_csv(f"{date} Donut Dates.csv", index=False)