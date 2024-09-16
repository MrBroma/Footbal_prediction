from utils.scraper import Scraper
from utils.merger import Merger
from utils.processor import Processor
from utils.loader import Loader


def run_scrape_and_download():
    scraper = Scraper('https://www.football-data.co.uk/belgiumm.php', '/opt/airflow/utils/csv_files')
    scraper.scrape_and_download()


def run_merge_csv_files():
    merger = Merger('/opt/airflow/utils/csv_files', '/opt/airflow/utils/one_csv_in_five')
    merger.merge_csv_files()

def run_process_and_save_csv():
    processor = Processor('/opt/airflow/utils/one_csv_in_five/Merged_file_common_columns.csv', '/opt/airflow/utils/New_csv_files')
    processor.process_and_save_csv()


def run_load_csv_to_sqlite():
    loader = Loader(
        '/opt/airflow/utils/New_csv_files/teams.csv',
        '/opt/airflow/utils/New_csv_files/matches.csv',
        '/opt/airflow/utils/New_csv_files/match_statistics.csv',
        '/opt/airflow/utils/football_prediction.db',
    )
    loader.load_csv_to_sqlite()