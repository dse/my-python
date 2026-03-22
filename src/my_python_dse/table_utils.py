def table(field_names, rows):
    if type(field_names) == list and type(rows) == list:
        strs = []
        max_lengths = [max([len(field_name), *[ len(row[field_name]) for row in rows ]]) for field_name in field_names]
        field_tuples = list(zip(max_lengths, field_names))
        strs.append(" | ".join([("%-*s" % (tuple[0], tuple[1])) for tuple in field_tuples]))
        strs.append("-|-".join([("-" * tuple[0]) for tuple in field_tuples]))
        for row in rows:
            strs.append(" | ".join(["%-*s" % (tuple[0], row[tuple[1]]) for tuple in field_tuples]))
        return "\n".join(strs)
    raise Exception("invalid arguments")

def table_keys(rows):
    field_names = []
    for row in list(rows):
        for key in row.keys():
            if key not in field_names:
                field_names.append(key)
    return field_names

def table_dict(rows):
    field_names = table_keys(rows)
    return table(field_names, rows)

def flatten(values):
    result = []
    for item in values:
        if type(item) == list:
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def tsv_value_escape(str):
    str = str.replace("\\", "\\\\")
    str = str.replace("\t", "\\t")
    str = str.replace("\r", "\\r")
    str = str.replace("\n", "\\n")
    return str

# excel dialect
def csv_value_escape(str):
    if '"' not in str and ',' not in str and '\r' not in str and '\n' not in str:
        return str
    str = str.replace('"', '""')
    return '"' + str + '"'

def camel_case(str):
    str = re.sub(r'^[^A-Za-z0-9]+', '', str)
    str = re.sub(r'[^A-Za-z0-9]+$', '', str)
    str = re.sub(r'\'+', '', str)
    words = re.split(r'[^A-Za-z0-9]+', str)
    words = [words[i].lower() if i == 0 else words[i][0].upper() + words[i][1:] for i in range(0, len(words))]
    return "".join(words)
