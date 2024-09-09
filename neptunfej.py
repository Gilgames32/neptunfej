import argparse
import sys
from generate import neptunfej

parser = argparse.ArgumentParser(description="Neptunfej")

parser.add_argument("-t", "--text", help="Caption text", required=True)
parser.add_argument("-o", "--output", help="Output file name", default=None)
parser.add_argument("-s", "--scale", help="Scale factor", type=int, default=2)
parser.add_argument("-m", "--margin", help="Margin", type=int, nargs=2, default=(10, 10))
parser.add_argument("-r", "--reverse", help="Upside down emoji", action="store_true")

args = parser.parse_args()

neptunfej(args.text, scale=args.scale, margin=args.margin, reverse=args.reverse).save(args.output if args.output else sys.stdout.buffer, "png")