import os
import re
import pandas as pd

dir: str = os.path.dirname(os.path.abspath(__file__))
file: str = dir + "\data\CMA CGM LIBRA 0PPF4W1MA-TPFREP.edi"


def isCMV_HCV_TMV(cadena: str) -> bool:
    rs: bool = False
    if cadena[0:3] == 'CMV':
        rs = True
    elif cadena[0:3] == 'HCV':
        rs = True
    elif cadena[0:3] == 'TMV':
        rs = True
    return rs


def main() -> None:
    """
    MAIN FUNCTION
    """

    if not os.path.exists(file):
        print("ERROR: Input file does not exist!!")
        return

    table: list = []
    tableDetails: list = []
    rows: list = []

    op: str = ''
    site: str = ''

    cn_length: str = ''
    cn_fcl_empty: str = ''
    """OP SITE COUNT 20'F 20'M 40'F 40'M 45'F """

    if os.path.isfile(file):
        # OPEN FILE
        tpfrep_file = open(file, "r")

        for each in tpfrep_file:
            line = each.rstrip()
            line = line.split('+')

            if line[0] == 'NAD' and line[1] == 'CF':
                table.append(line)
            if line[0] == 'EQD' and line[1] == 'CN':
                table.append(line)
            if line[0] == 'QTY' and not isCMV_HCV_TMV(line[1]):
                table.append(line)

            """ NAD+CF+CMA'
                EQD+CN++20FT+++5'
                QTY+IDI:0'
                QTY+DIS:1' Discharged Imports
                QTY+CDI:0' Discharged Costals
                QTY+TDI:1' Discharged Transships
                QTY+ELD:0'
                QTY+TLD:0' Loaded Transships
                QTY+RES:0' Restow Terminal
                QTY+LOD:0' Loaded Export """

        if len(table) > 0:
            for row in table:
                if row[0] == 'NAD':
                    op = row[2].replace("'", "")
                    continue
                if row[0] == 'EQD' and row[1] == 'CN' and row[3] == '20FT' and row[len(row)-1] == "5'":
                    cn_length = '20FT'
                    cn_fcl_empty = 'FCL'
                    continue
                if row[0] == 'EQD' and row[1] == 'CN' and row[3] == '20FT' and row[len(row)-1] == "4'":
                    cn_length = '20FT'
                    cn_fcl_empty = 'EMPTY'
                    continue
                if row[0] == 'EQD' and row[1] == 'CN' and row[3] == '40FT' and row[len(row)-1] == "5'":
                    cn_length = '40FT'
                    cn_fcl_empty = 'FCL'
                    continue
                if row[0] == 'EQD' and row[1] == 'CN' and row[3] == '40FT' and row[len(row)-1] == "4'":
                    cn_length = '40FT'
                    cn_fcl_empty = 'EMPTY'
                    continue
                if row[0] == 'EQD' and row[1] == 'CN' and row[3] == '45FT' and row[len(row)-1] == "5'":
                    cn_length = '45FT'
                    cn_fcl_empty = 'FCL'
                    continue

                if cn_length == '20FT' and cn_fcl_empty == 'FCL':
                    if row[0] == 'QTY':
                        col = row[1].split(':')
                        val = int(col[1].replace("'", ""))
                        if col[0] == 'DIS' or col[0] == 'TDI' or col[0] == 'TLD' or col[0] == 'LOD' or col[0] == 'RES':
                            rows.append([op, '20FT', 'FCL', col[0], val])
                if cn_length == '20FT' and cn_fcl_empty == 'EMPTY':
                    if row[0] == 'QTY':
                        col = row[1].split(':')
                        val = int(col[1].replace("'", ""))
                        if col[0] == 'DIS' or col[0] == 'TDI' or col[0] == 'TLD' or col[0] == 'LOD' or col[0] == 'RES':
                            rows.append([op, '20FT', 'EMPTY', col[0], val])
                if cn_length == '40FT' and cn_fcl_empty == 'FCL':
                    if row[0] == 'QTY':
                        col = row[1].split(':')
                        val = int(col[1].replace("'", ""))
                        if col[0] == 'DIS' or col[0] == 'TDI' or col[0] == 'TLD' or col[0] == 'LOD' or col[0] == 'RES':
                            rows.append([op, '40FT', 'FCL', col[0], val])
                if cn_length == '40FT' and cn_fcl_empty == 'EMPTY':
                    if row[0] == 'QTY':
                        col = row[1].split(':')
                        val = int(col[1].replace("'", ""))
                        if col[0] == 'DIS' or col[0] == 'TDI' or col[0] == 'TLD' or col[0] == 'LOD' or col[0] == 'RES':
                            rows.append([op, '40FT', 'EMPTY', col[0], val])
                if cn_length == '45FT' and cn_fcl_empty == 'FCL':
                    if row[0] == 'QTY':
                        col = row[1].split(':')
                        val = int(col[1].replace("'", ""))
                        if col[0] == 'DIS' or col[0] == 'TDI' or col[0] == 'TLD' or col[0] == 'LOD' or col[0] == 'RES':
                            rows.append([op, '45FT', 'FCL', col[0], val])

        if len(rows) > 0:
            df = pd.DataFrame(rows)
            df.to_excel('output.xlsx')

            print(df.head(len(rows)))


if __name__ == "__main__":
    main()
