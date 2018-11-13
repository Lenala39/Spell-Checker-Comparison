import csv

def gold_eval(data):
    only_errors = data[data["Error"] == True]
    #print(only_errors)

    data_size = len(only_errors.index)

    hun_unrecognized = only_errors[only_errors["Original"] == only_errors["Hunspell"]]
    word_unrecognized = only_errors[only_errors["Original"] == only_errors["Word"]]

    hun_percent = round(len(hun_unrecognized.index) / data_size * 100,2)
    word_percent = round(len(word_unrecognized.index) / data_size * 100, 2)

    output_dict = {
        "All errors": data_size,
        "# hunspell unrecognized": len(hun_unrecognized.index),
        "# word unrecognized": len(word_unrecognized.index),
        "% hun unrecognized": hun_percent,
        "% word unrecognized": word_percent
    }

    with open("results.csv", "a") as file:
        writer = csv.writer(file)
        for key, value in output_dict.items():
            writer.writerow([key, value])