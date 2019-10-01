import os
import sysconsts
import shutil

def create_dir_sources():
    if not os.path.isdir(sysconsts.CONTABIL_SOURCE_PATH):
        os.mkdir(sysconsts.CONTABIL_SOURCE_PATH)

    if not os.path.isdir(sysconsts.FISCAL_SOURCE_PATH):
        os.mkdir(sysconsts.FISCAL_SOURCE_PATH)

    if not os.path.isdir(sysconsts.PESSOAL_SOURCE_PATH):
        os.mkdir(sysconsts.PESSOAL_SOURCE_PATH)

    if not os.path.isdir(sysconsts.COMMON_SOURCE_PATH):
        os.mkdir(sysconsts.COMMON_SOURCE_PATH)

def move_file(file_name, source_dir, dest_dir):
    file_path = "%s\\%s" % (source_dir, file_name)
    file_path_dest = "%s\\%s" % (dest_dir, file_name)
            
    if os.path.isfile(file_path):
        print("Moving: ", file_path, " To: ", file_path_dest)
        shutil.move(file_path, file_path_dest)                 

def copy_source_from_dpr(dpr_name, dest_dir):
    dpr = open(sysconsts.AC_SOURCE_PATH + dpr_name, "r")
    dpr_content = dpr.readlines()

    for line in dpr_content:       
        if line == "\n":
            continue

        if " in " in line:
            line_splited = line.split(" ")                                  

            # *.pas
            unit_name = "%s.pas" % line_splited[2]    
            move_file(unit_name, sysconsts.AC_SOURCE_PATH, dest_dir)

            # *.dfm            
            dfm_name = "%s.dfm" % line_splited[2]        
            move_file(dfm_name, sysconsts.AC_SOURCE_PATH, dest_dir)                

def copy_source_common_from_dpr(dirbase, dpr_base, dprs_compare):
    dpr = open(sysconsts.AC_SOURCE_PATH + dpr_base, "r")
    dpr_content = dpr.readlines()

    for compare in dprs_compare:
        dpr_compare = open(sysconsts.AC_SOURCE_PATH + compare, "r")
        dpr_compare_content = dpr_compare.readlines()

        for line in dpr_content:       
            if line == "\n":
                continue

            if " in " in line:
                line_splited = line.split(" ")
                unit_name = line_splited[2]        
                
                if any(unit_name in s for s in dpr_compare_content):
                    # *.pas
                    unit_name = "%s.pas" % line_splited[2]    
                    move_file(unit_name, dirbase, sysconsts.COMMON_SOURCE_PATH)

                    # *.dfm            
                    dfm_name = "%s.dfm" % line_splited[2]        
                    move_file(dfm_name, dirbase, sysconsts.COMMON_SOURCE_PATH)                

def run():
    create_dir_sources()

    copy_source_from_dpr(sysconsts.CONTABIL_DPR, sysconsts.CONTABIL_SOURCE_PATH)
    copy_source_from_dpr(sysconsts.PESSOAL_DPR, sysconsts.PESSOAL_SOURCE_PATH)
    copy_source_from_dpr(sysconsts.FISCAL_DPR, sysconsts.FISCAL_SOURCE_PATH)

    copy_source_common_from_dpr(sysconsts.CONTABIL_SOURCE_PATH, sysconsts.CONTABIL_DPR, [sysconsts.PESSOAL_DPR, sysconsts.FISCAL_DPR])
    copy_source_common_from_dpr(sysconsts.FISCAL_SOURCE_PATH, sysconsts.FISCAL_DPR, [sysconsts.CONTABIL_DPR, sysconsts.PESSOAL_DPR])
    copy_source_common_from_dpr(sysconsts.PESSOAL_SOURCE_PATH, sysconsts.PESSOAL_DPR, [sysconsts.CONTABIL_DPR, sysconsts.FISCAL_DPR])

    print("Success.")

run()