import sys
sys.dont_write_bytecode = True

import argparse
from climate_resilience import downloader


def parse_arguments() -> argparse.Namespace:
    """Reads commandline arguments and returns the parsed object.
    
    Returns:
        argparse.Namespace: parsed object containing all the input arguments.
    """
    parser = argparse.ArgumentParser(
        description="Sample usage of download functions.",
        fromfile_prefix_chars="@",  # helps read the arguments from a file.
    )
    
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument(
        "-s",
        "--site_json",
        type=str,
        required=True,
        help="Path to the json file containing all the sites information.",
    )
    
    required_named.add_argument(
        "-y",
        "--yaml_path",
        type=str,
        required=True,
        help="Path to the yaml file containing all the download parameters.",
    )
    
    parser.add_argument(
        "-o",
        "--drive_output_dir",
        type=str,
        default="gee_downloader_testing",
        help="Name of a folder located in Google Drive. Will be created if not \
            already present.",
    )
    
    args, unknown = parser.parse_known_args()

    # print("--- args ---")
    # print(args)

    return args


def main():
    args = parse_arguments()
    
    output_dir = args.drive_output_dir
    site_json_file_path = args.site_json     # Path to the data directory within this git repo '../../../data/LMsites.json'.
    yaml_path = args.yaml_path               # Path to the data directory within this git repo './download_params.yml'.
    
    sd_obj = downloader.SitesDownloader(
        folder=output_dir,
        site_json_file_path=site_json_file_path,
    )
    
    sd_obj.download_samples(params_yaml_file=yaml_path, mode="daily")


if __name__ == "__main__":
    main()
