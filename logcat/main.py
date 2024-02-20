import argparse
import json

from logcat.parser import LogcatParser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', metavar='path', type=str, help='filepath')
    parser.add_argument("-o", '--output_filepath', type=str, help='output filepath', default=None)
    parser.add_argument("-f", "--log_format", type=str, help="provide log format", default="threadtime", choices=['threadtime'])
    parser.add_argument("-of", "--output_format", type=str, help="output file format", choices=["json"])
    parser.add_argument("-i", "--include_logs", help="includes parsed logs in output", action='store_true')
    args = parser.parse_args()
    parser = LogcatParser(args.log_format)
    parser.parse_file(args.path)
    if args.output_filepath:
        parser.save_results(args.output_filepath, include_logs=args.include_logs)
    else:
        print(json.dumps(parser.get_parser_resume(include_logs=args.include_logs), indent=1))


if __name__ == "__main__":
    main()
