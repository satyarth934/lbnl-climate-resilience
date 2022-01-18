import sys
sys.dont_write_bytecode = True

from climate_resilience import downloader


def main():
    output_dir = "gee_downloader_testing"    # Folder located in Google Drive. Will be created if not already present.
    site_json_file_path = "/global/scratch/satyarth/Projects/lbnl-zexuan-code/src/zexuan_pkg/LMsites.json"
    yaml_path = "download_params.yml"
    
    sd_obj = downloader.SitesDownloader(
        folder=output_dir,
        site_json_file_path=site_json_file_path,
    )
    
    sd_obj.download_samples(params_yaml_file=yaml_path, mode="daily")


if __name__ == "__main__":
    main()
