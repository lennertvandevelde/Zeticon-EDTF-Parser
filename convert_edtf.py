import argparse

import pandas as pd
import pyparsing as pp

yyyy_mm_dd = pp.Word(pp.nums) + "-" + pp.Word(pp.nums) + "-" + pp.Word(pp.nums)
yyyy_mm = pp.Word(pp.nums) + "-" + pp.Word(pp.nums) + "-" + pp.Word(pp.alphas)
yyyy = pp.Word(pp.nums) + "-" + pp.Word(pp.alphas) + "-" + pp.Word(pp.alphas)
unk = pp.Word(pp.alphas) + "-" + pp.Word(pp.alphas) + "-" + pp.Word(pp.alphas)

yyyy_mm_dd_timeinterval_yyyy_mm_dd = yyyy_mm_dd + "/" + yyyy_mm_dd
yyyy_mm_dd_timeinterval_yyyy_mm = yyyy_mm_dd + "/" + yyyy_mm
yyyy_mm_dd_timeinterval_yyyy = yyyy_mm_dd + "/" + yyyy
yyyy_mm_dd_timeinterval_unk = yyyy_mm_dd + "/" + unk
yyyy_mm_timeinterval_yyyy_mm_dd = yyyy_mm + "/" + yyyy_mm_dd
yyyy_mm_timeinterval_yyyy_mm = yyyy_mm + "/" + yyyy_mm
yyyy_mm_timeinterval_yyyy = yyyy_mm + "/" + yyyy
yyyy_mm_timeinterval_unk = yyyy_mm + "/" + unk
yyyy_timeinterval_yyyy_mm_dd = yyyy + "/" + yyyy_mm_dd
yyyy_timeinterval_yyyy_mm = yyyy + "/" + yyyy_mm
yyyy_timeinterval_yyyy = yyyy + "/" + yyyy
yyyy_timeinterval_unk = yyyy + "/" + unk
unk_timeinterval_yyyy_mm_dd = unk + "/" + yyyy_mm_dd
unk_timeinterval_yyyy_mm = unk + "/" + yyyy_mm
unk_timeinterval_yyyy = unk + "/" + yyyy
unk_timeinterval_unk = unk + "/" + unk

def detect_natural_lang(date):
    if "after" in date:
        return True, "/" + convert_to_EDTF(date.replace("after", ""))
    elif "before" in date:
        return True, convert_to_EDTF(date.replace("before", "")) + "/"
    else:
        return False, ""

def convert_to_EDTF(date):
    natural_lang_detected, converted_date = detect_natural_lang(date)
    if natural_lang_detected:
        return converted_date
    if "/" in date:
        converted_date = yyyy_mm_dd_timeinterval_yyyy_mm_dd.search_string(date)
        if converted_date:
            return date
        elif yyyy_mm_dd_timeinterval_yyyy_mm.search_string(date):
            converted_date = yyyy_mm_dd_timeinterval_yyyy_mm.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "-" + converted_date[4] + "/" + converted_date[6] + "-" + converted_date[8]
        elif yyyy_mm_dd_timeinterval_yyyy.search_string(date):
            converted_date = yyyy_mm_dd_timeinterval_yyyy.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "-" + converted_date[4] + "/" + converted_date[6]
        elif yyyy_mm_dd_timeinterval_unk.search_string(date):
            converted_date = yyyy_mm_dd_timeinterval_unk.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "-" + converted_date[4] + "/"
        elif yyyy_mm_timeinterval_yyyy_mm_dd.search_string(date):
            converted_date = yyyy_mm_timeinterval_yyyy_mm_dd.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "/" + converted_date[6] + "-" + converted_date[8] + "-" + converted_date[10]
        elif yyyy_mm_timeinterval_yyyy_mm.search_string(date):
            converted_date = yyyy_mm_timeinterval_yyyy_mm.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "/" + converted_date[6] + "-" + converted_date[8]
        elif yyyy_mm_timeinterval_yyyy.search_string(date):
            converted_date = yyyy_mm_timeinterval_yyyy.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "/" + converted_date[6]
        elif yyyy_mm_timeinterval_unk.search_string(date):
            converted_date = yyyy_mm_timeinterval_unk.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "/"
        elif yyyy_timeinterval_yyyy_mm_dd.search_string(date):
            converted_date = yyyy_timeinterval_yyyy_mm_dd.search_string(date)[0]
            return converted_date[0] + "/" + converted_date[6] + "-" + converted_date[8] + "-" + converted_date[10]
        elif yyyy_timeinterval_yyyy_mm.search_string(date):
            converted_date = yyyy_timeinterval_yyyy_mm.search_string(date)[0]
            return converted_date[0] + "/" + converted_date[6] + "-" + converted_date[8]
        elif yyyy_timeinterval_yyyy.search_string(date):
            converted_date = yyyy_timeinterval_yyyy.search_string(date)[0]
            return converted_date[0] + "/" + converted_date[6]
        elif yyyy_timeinterval_unk.search_string(date):
            converted_date = yyyy_timeinterval_unk.search_string(date)[0]
            return converted_date[0] + "/"
        elif unk_timeinterval_yyyy_mm_dd.search_string(date):
            converted_date = unk_timeinterval_yyyy_mm_dd.search_string(date)[0]
            return  "/" + converted_date[6] + "-" + converted_date[8] + "-" + converted_date[10]
        elif unk_timeinterval_yyyy_mm.search_string(date):
            converted_date = unk_timeinterval_yyyy_mm.search_string(date)[0]
            return  "/" + converted_date[6] + "-" + converted_date[8]
        elif unk_timeinterval_yyyy.search_string(date):
            converted_date = unk_timeinterval_yyyy.search_string(date)[0]
            return  "/" + converted_date[6]
        elif unk_timeinterval_unk.search_string(date):
            converted_date = unk_timeinterval_unk.search_string(date)[0]
            return  "uuuu-uu-uu"
        else:
            return date
    else:
        if yyyy_mm_dd.search_string(date):
            converted_date = yyyy_mm_dd.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2] + "-" + converted_date[4]
        elif yyyy_mm.search_string(date):
            converted_date = yyyy_mm.search_string(date)[0]
            return converted_date[0] + "-" + converted_date[2]
        elif yyyy.search_string(date):
            converted_date = yyyy.search_string(date)[0]
            return converted_date[0]
        elif unk.search_string(date):
            converted_date = unk.search_string(date)[0]
            return "uuuu-uu-uu"
        else:
            return date



def main(args):
    for file in args.files:
        df = pd.read_csv(file, delimiter=args.delimiter)
        df["dcterms_created"] = df["dcterms_created"].fillna("lege datum")
        converted_dates = []
        for date in df["dcterms_created"]:
            converted_dates.append(convert_to_EDTF(date))
        df["converted_dates"] = converted_dates
        df.to_csv("converted_" + file)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
       "files",
        metavar="inputFile",
        nargs="+",
        help="CSV file(s) to be processed",
    )
    parser.add_argument(
       "--delimiter",
        metavar="delimiter",
        type=str,
        default=",",
        required=False,
        help="delimiter to be used in the CSV file(s), default is ','",
    )
    args = parser.parse_args()
    main(args)