import argparse
import logging

from src.core.parse_rss_feeds import parse_rss_feeds

logging.getLogger().setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resources', nargs='+', help='List of RSS feed', required=True)
args = parser.parse_args()
parse_rss_feeds(args.resources)
