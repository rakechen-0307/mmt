import os
import json
import argparse
import pathlib
import tqdm

import utils

@utils.resolve_paths
def parse_args(args=None, namespace=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Process music JSON files of POP909 Dataset."
    )
    parser.add_argument(
        "-t",
        "--target_dir",
        default="data/pop909/processed/json",
        type=pathlib.Path,
        help="target directory",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default="data/pop909/processed/new_json",
        type=pathlib.Path,
        help="output directory",
    )
    return parser.parse_args(args=args, namespace=namespace)


def main():
    """Main function."""
    # Parse the command-line arguments
    args = parse_args()

    # Make sure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)

    in_files = sorted(os.listdir(args.target_dir))
    for i in tqdm.tqdm(range(len(in_files))):
        with open(os.path.join(args.target_dir, in_files[i]), 'rb') as in_f:
            data = json.load(in_f)
        tracks = data['tracks']
        new_tracks = []
        for j in range(len(tracks)):
            if (tracks[j]['name'] != 'BRIDGE'):
                if (tracks[j]['name'] == 'MELODY'):
                    tracks[j]['program'] = 4
                elif (tracks[j]['name'] == 'PIANO'):
                    tracks[j]['program'] = 0
                new_tracks.append(tracks[j])
        data['tracks'] = new_tracks

        out_file = os.path.join(args.output_dir, in_files[i])
        with open(out_file, 'w') as out_f:
            json.dump(data, out_f)

if __name__ == "__main__":
    main()