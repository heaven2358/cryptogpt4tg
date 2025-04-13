import argparse, logging, signal, sys, os
from tgbot.runner import run_telegram_bot, run_input_loop
from utils.daemon import daemonize
from utils.usage import print_usage

def handle_sigterm(signum, frame):
    logging.info(f"Received signal {signum}, exiting.")
    sys.exit(0)

def handle_sighup(signum, frame):
    logging.info(f"Received signal {signum}, restarting.")
    os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-d", "--daemon", action="store_true")
    parser.add_argument("-t", "--telegram", action="store_true")
    parser.add_argument("-i", "--input", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(filename="bot.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGHUP, handle_sighup)

    if args.help or not (args.telegram or args.input):
        print_usage()
        sys.exit(0)

    if args.daemon:
        daemonize()

    if args.telegram:
        run_telegram_bot()
    elif args.input:
        run_input_loop()