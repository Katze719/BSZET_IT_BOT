from table2ascii import table2ascii as t2a, PresetStyle, Alignment

def parse_table(table):

    _datum = 0
    _tag = 1
    _stunde = 2
    _lehrer_name = 3
    _fach = 4
    _raum_nummer = 5
    _klasse = 6
    _mitteilung = 7
    _vlehrer_kurzel = 8



    result = []
    for index in table.axes[0]:
        tmp = [
            table.iat[index, 2],
            table.iat[index, 3],
            table.iat[index, 4],
            table.iat[index, 5],
            table.iat[index, 7],
        ]

        for s in range(len(tmp)):
            tmp[s] = tmp[s].replace('.', '')
            tmp[s] = tmp[s].replace('+', '')
        result.append(tmp)

    output = t2a(
        header=["Stunde", "Lehrer", "Fach", "Raum", "Info"],
        body=result,
        style=PresetStyle.thin_compact,
        cell_padding=0
    )

    return f"```\n{output}\n```"
