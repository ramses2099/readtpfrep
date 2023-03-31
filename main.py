import os
import re

dir: str = os.path.dirname(os.path.abspath(__file__))
file: str = dir + "\data\TPFREP_CGM.edi"
file_report: str = "report.txt"


def isCMV_HCV_TMV(cadena: str) -> bool:
    rs: bool = False
    if cadena[0:3] == 'CMV':
        rs = True
    elif cadena[0:3] == 'HCV':
        rs = True
    elif cadena[0:3] == 'TMV':
        rs = True
    return rs


def isDIS_LOD(cadena: str) -> bool:
    rs: bool = False
    if cadena[0:3] == 'DIS':
        rs = True
    elif cadena[0:3] == 'LOD':
        rs = True
    return rs


def valDIS_LOD(cadena: str) -> int:
    op = cadena.split(':')
    rs: int = 0
    if op[0] == 'DIS':
        rs = int(op[1].replace("'", ""))
    elif op[0] == 'LOD':
        rs = int(op[1].replace("'", ""))
    return rs


def main() -> None:
    """
    MAIN FUNCTION
    """
    arr_data_header: list = []
    arr_data_details: list = []

    eqd: list = []

    file_write = open(file_report, "w")

    if os.path.isfile(file):
        # OPEN FILE
        tpfrep_file = open(file, "r")

        for each in tpfrep_file:
            line = each.rstrip()
            line = line.split('+')

            if line[0] == 'TDT':
                arr_data_header.append(line)
            # print(line)

            if line[0] == 'EQD' and line[1] == 'GC':
                arr_data_header.append(line)

            if line[0] == 'QTY' and isCMV_HCV_TMV(line[1]):
                arr_data_header.append(line)

            if line[0] == 'EQD' and line[1] == 'CN':
                arr_data_details.append(line)

            if line[0] == 'QTY' and not isCMV_HCV_TMV(line[1]):
                arr_data_details.append(line)

    print("===========================================")
    file_write.writelines("===========================================\n")
    cn_length: str = ''
    cn_fcl_empty: str = ''
    print("==============TPFREP=======================")
    file_write.writelines("==============TPFREP=======================\n")
    print("===========================================")
    file_write.writelines("===========================================\n")

    # HEADER
    if len(arr_data_header) > 0:
        for dt in arr_data_header:
            # print(dt)
            if dt[0] == 'TDT':
                print(f"Vessel Visit Id: {dt[2]}")
                file_write.writelines(f"Vessel Visit Id: {dt[2]}\n")
                value = dt[8].split(":")
                if len(value) > 0:
                    vesselname = value[3].replace("'", "")
                    print(f"Vessel Name: {vesselname}")
                    file_write.writelines(f"Vessel Name: {vesselname}\n")

            if dt[0] == 'EQD' and dt[1] == 'GC':
                crane_name = dt[2].replace("'", "")
                print("================================")
                file_write.writelines("================================\n")
                print(f"Crane Name:{crane_name}")
                file_write.writelines(f"Crane Name:{crane_name}\n")
                print("================================")
                file_write.writelines("================================\n")

            if dt[0] == 'QTY' and isCMV_HCV_TMV(dt[1]):
                value = dt[1].split(":")
                if value[0] == 'CMV':
                    cn_mov = value[1].replace("'", "")
                    print(f"Container Move:{cn_mov}")
                    file_write.writelines(f"Container Move:{cn_mov}\n")
                if value[0] == 'HCV':
                    hc_mov = value[1].replace("'", "")
                    print(f"Hatch Cover Move:{hc_mov}")
                    file_write.writelines(f"Hatch Cover Move:{hc_mov}\n")
                if value[0] == 'TMV':
                    cn_mov = value[1].replace("'", "")
                    print(f"Total Container Move:{cn_mov}")
                    file_write.writelines(f"Total Container Move:{cn_mov}\n")

    # DETAILS
    if len(arr_data_details) > 0:
        for dt in arr_data_details:
            # print(dt)

            if dt[0] == 'EQD' and dt[1] == 'CN' and dt[3] == '20FT' and dt[len(dt)-1] == "5'":
                cn_length = '20FT'
                cn_fcl_empty = 'FCL'
                continue
            elif dt[0] == 'EQD' and dt[1] == 'CN' and dt[3] == '20FT' and dt[len(dt)-1] == "4'":
                cn_length = '20FT'
                cn_fcl_empty = 'EMPTY'
                continue
            elif dt[0] == 'EQD' and dt[1] == 'CN' and dt[3] == '40FT' and dt[len(dt)-1] == "5'":
                cn_length = '40FT'
                cn_fcl_empty = 'FCL'
                continue
            elif dt[0] == 'EQD' and dt[1] == 'CN' and dt[3] == '40FT' and dt[len(dt)-1] == "4'":
                cn_length = '40FT'
                cn_fcl_empty = 'EMPTY'
                continue
            elif dt[0] == 'EQD' and dt[1] == 'CN' and dt[3] == '45FT' and dt[len(dt)-1] == "5'":
                cn_length = '45FT'
                cn_fcl_empty = 'FCL'
                continue
            elif dt[0] == 'EQD' and dt[1] == 'CN' and dt[3] == '45FT' and dt[len(dt)-1] == "4'":
                cn_length = '40FT'
                cn_fcl_empty = 'EMPTY'
                continue

            if cn_length == '20FT' and cn_fcl_empty == 'FCL':
                if dt[0] == 'QTY':
                    row = dt[1].split(':')
                    val = int(row[1].replace("'", ""))
                    eqd.append(['20FT', 'FCL', row[0], val])
            if cn_length == '20FT' and cn_fcl_empty == 'EMPTY':
                if dt[0] == 'QTY':
                    row = dt[1].split(':')
                    val = int(row[1].replace("'", ""))
                    eqd.append(['20FT', 'EMPTY', row[0], val])
            if cn_length == '40FT' and cn_fcl_empty == 'FCL':
                if dt[0] == 'QTY':
                    row = dt[1].split(':')
                    val = int(row[1].replace("'", ""))
                    eqd.append(['40FT', 'FCL', row[0], val])
            if cn_length == '40FT' and cn_fcl_empty == 'EMPTY':
                if dt[0] == 'QTY':
                    row = dt[1].split(':')
                    val = int(row[1].replace("'", ""))
                    eqd.append(['40FT', 'EMPTY', row[0], val])
            if cn_length == '45FT' and cn_fcl_empty == 'FCL':
                if dt[0] == 'QTY':
                    row = dt[1].split(':')
                    val = int(row[1].replace("'", ""))
                    eqd.append(['45FT', 'FCL', row[0], val])
            if cn_length == '45FT' and cn_fcl_empty == 'EMPTY':
                if dt[0] == 'QTY':
                    row = dt[1].split(':')
                    val = int(row[1].replace("'", ""))
                    eqd.append(['45FT', 'EMPTY', row[0], val])

    if len(eqd) > 0:
        # 20FT
        total20ft_dis_empty: int = 0
        total20ft_lod_empty: int = 0
        total20ft_dis_full: int = 0
        total20ft_lod_full: int = 0

        # 40FT
        total40ft_dis_empty: int = 0
        total40ft_lod_empty: int = 0
        total40ft_dis_full: int = 0
        total40ft_lod_full: int = 0

        # 45FT
        total45ft_dis_empty: int = 0
        total45ft_lod_empty: int = 0
        total45ft_dis_full: int = 0
        total45ft_lod_full: int = 0

        for e in eqd:
            # print(e)

            # 20ft empty dis lod
            if e[0] == '20FT' and e[1] == 'EMPTY' and e[2] == 'DIS':
                total20ft_dis_empty += e[3]
            elif e[0] == '20FT' and e[1] == 'EMPTY' and e[2] == 'LOD':
                total20ft_lod_empty += e[3]
            # 20ft full dis lod
            if e[0] == '20FT' and e[1] == 'FCL' and e[2] == 'DIS':
                total20ft_dis_full += e[3]
            elif e[0] == '20FT' and e[1] == 'FCL' and e[2] == 'LOD':
                total20ft_lod_full += e[3]

            # 40ft empty dis lod
            if e[0] == '40FT' and e[1] == 'EMPTY' and e[2] == 'DIS':
                total40ft_dis_empty += e[3]
            elif e[0] == '40FT' and e[1] == 'EMPTY' and e[2] == 'LOD':
                total40ft_lod_empty += e[3]
            # 40ft full dis lod
            if e[0] == '40FT' and e[1] == 'FCL' and e[2] == 'DIS':
                total40ft_dis_full += e[3]
            elif e[0] == '40FT' and e[1] == 'FCL' and e[2] == 'LOD':
                total40ft_lod_full += e[3]

            # 45ft empty dis lod
            if e[0] == '45FT' and e[1] == 'EMPTY' and e[2] == 'DIS':
                total45ft_dis_empty += e[3]
            elif e[0] == '45FT' and e[1] == 'EMPTY' and e[2] == 'LOD':
                total45ft_lod_empty += e[3]
            # 45ft full dis lod
            if e[0] == '45FT' and e[1] == 'FCL' and e[2] == 'DIS':
                total45ft_dis_full += e[3]
            elif e[0] == '45FT' and e[1] == 'FCL' and e[2] == 'LOD':
                total45ft_lod_full += e[3]

        print("===========================================")
        file_write.writelines("===========================================\n")
        print("=================DETAILS===================")
        file_write.writelines("=================DETAILS===================\n")
        print("===========================================")
        file_write.writelines("===========================================\n")

        # 20 FT
        print(f'Total 20FT EMPTY DIS {total20ft_dis_empty}')
        file_write.writelines(f'Total 20FT EMPTY DIS {total20ft_dis_empty}\n')
        print(f'Total 20FT EMPTY LOAD {total20ft_lod_empty}')
        file_write.writelines(f'Total 20FT EMPTY LOAD {total20ft_lod_empty}\n')
        print(f'Total 20FT FULL DIS {total20ft_dis_full}')
        file_write.writelines(f'Total 20FT FULL DIS {total20ft_dis_full}\n')
        print(f'Total 20FT FULL LOAD {total20ft_lod_full}')
        file_write.writelines(f'Total 20FT FULL LOAD {total20ft_lod_full}\n')

        # 40 FT
        print(f'Total 40FT EMPTY DIS {total40ft_dis_empty}')
        file_write.writelines(f'Total 40FT EMPTY DIS {total40ft_dis_empty}\n')
        print(f'Total 40FT EMPTY LOAD {total40ft_lod_empty}')
        file_write.writelines(f'Total 40FT EMPTY LOAD {total40ft_lod_empty}\n')
        print(f'Total 40FT FULL DIS {total40ft_dis_full}')
        file_write.writelines(f'Total 40FT FULL DIS {total40ft_dis_full}\n')
        print(f'Total 40FT FULL LOAD {total40ft_lod_full}')
        file_write.writelines(f'Total 40FT FULL LOAD {total40ft_lod_full}\n')

        # 45 FT
        print(f'Total 45FT EMPTY DIS {total45ft_dis_empty}')
        file_write.writelines(f'Total 45FT EMPTY DIS {total45ft_dis_empty}\n')
        print(f'Total 45FT EMPTY LOAD {total45ft_lod_empty}')
        file_write.writelines(f'Total 45FT EMPTY LOAD {total45ft_lod_empty}\n')
        print(f'Total 45FT FULL DIS {total45ft_dis_full}')
        file_write.writelines(f'Total 45FT FULL DIS {total45ft_dis_full}\n')
        print(f'Total 45FT FULL LOAD {total45ft_lod_full}')
        file_write.writelines(f'Total 45FT FULL LOAD {total45ft_lod_full}\n')

        print("===========================================")
        file_write.writelines("===========================================\n")
        print("===========================================")
        file_write.writelines("===========================================\n")

    file_write.close()


if __name__ == "__main__":
    main()
