### pandas‗sqlite.py
# 作成日：2023/01/30
# 更新日：2023/08/25
#
# 更新内容：
# v1   … 初回リリース
#

import sqlite3
import os
import pandas as pd
import numpy as np
import yaml
import logging
import glob

def main():
    """
    実行部

    """
    ### 基本変数
    cdir = os.path.dirname(__file__)
    logger = logging.getLogger(__name__)
    conf_path = "settings\\settings_v2.yml"
    log_path = "logs\\"
    out_path = "out\\"
    conf = os.path.join(cdir,conf_path)
    # 設定ファイル(settings.yaml)読み込み
    with open(conf, 'r', encoding="utf-8") as yml:
        config = yaml.safe_load(yml)
    # DB生成/接続用変数
    dbpath = config['COMMONS']['PATH']
    dbfs = config['DATABASES']['NAME']
    db_dir = os.path.join(cdir,dbpath)
    db = os.path.join(db_dir,dbfs)
    datadir = config['COMMONS']['DATA']
    data_path = os.path.join(cdir,datadir)
    dbname = db
    # logger用変数
    log = config['COMMONS']['LOG']
    log_fs = os.path.join(cdir,log_path,log)
    filehandler = logging.FileHandler(filename=log_fs, encoding='utf-8')
    streamhandler = logging.StreamHandler()
    format = '[%(asctime)s][%(levelname)s][%(message)s]'
    datefmt='%Y/%m/%d %I:%M:%S'
    formatter = logging.Formatter(format, datefmt)
    streamhandler.setFormatter(formatter)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.setLevel(logging.DEBUG)
    logger.debug('---- py_Analysis Start ----')

    ## DB/テーブル生成処理
    # DB生成処理
    if glob.glob(dbname,  recursive=True):
        logger.info('DB生成処理…Skip')
    else:
        logger.info('DB生成処理')
        db_create = create_db(logger,dbname)

    # DB接続処理
    conn = connect_db(logger,dbname)

    # テーブル生成処理
    ck_file = data_path + "\\*.csv"
    ck_files = glob.glob(ck_file)
    if ck_files:
        for datafs in os.listdir(data_path):
            if datafs.endswith('.csv'):
                fs = os.path.join(cdir,datadir,datafs)
                tbl_name = config['DATABASES']['TBLNAME']
                if tbl_name:
                    tabls_create = create_tbls(logger,fs,tbl_name,conn)
                    conn.commit()
                else:
                    status = "dataディレクトリ内にCSVファイルが存在しません"
                    msg= status
                    logger.info(msg)

    ## DB操作処理
    act_dict = config['QUERYS']['actions']
    acts = act_dict
    for act in acts:
        # insert処理
        if act in "insert":
            in_csv = data_path + "\\INSERT_FS\\**\\*.csv"
            in_fs = glob.glob(in_csv,recursive=True)
            print(in_fs)
            for fs in in_fs:
                tbl_name = config['QUERYS']['insert']["TBLNAME"]
                i_tabls = insert_tbl(logger,tbl_name,fs,conn)
                logger.info(i_tabls)
        # concat結合処理
        elif act in "concat":
            l_tbl_name = config['QUERYS']['concat']["L_TBLNAME"]
            r_tbl_name = config['QUERYS']['concat']["R_TBLNAME"]
            i_l_tbl = select_tbl(logger,l_tbl_name,conn)
            i_r_tbl = select_tbl(logger,r_tbl_name,conn)
            i_tabls = concat_tbls(logger,i_l_tbl,i_r_tbl)
            logger.info(i_tabls)
        # merge結合処理
        elif act in "merge":
            how = config['QUERYS']['merge']['HOW']
            l_tbl_name = config['QUERYS']['merge']["L_TBLNAME"]
            r_tbl_name = config['QUERYS']['merge']["R_TBLNAME"]
            l_key = config['QUERYS']['merge']["L_KEY"]
            r_key = config['QUERYS']['merge']["R_KEY"]
            i_l_tbl = select_tbl(logger,l_tbl_name,conn)
            i_r_tbl = select_tbl(logger,r_tbl_name,conn)
            i_tabls = inner_tbls(logger,how,i_l_tbl,i_r_tbl,l_key,r_key)
            logger.info(i_tabls)
        elif act in "outer":
            how = "outer"
            l_tbl_name = config['QUERYS']['outer']["L_TBLNAME"]
            r_tbl_name = config['QUERYS']['outer']["R_TBLNAME"]
            l_key = config['QUERYS']['outer']["L_KEY"]
            r_key = config['QUERYS']['outer']["R_KEY"]
            i_l_tbl = select_tbl(logger,l_tbl_name,conn)
            i_r_tbl = select_tbl(logger,r_tbl_name,conn)
            i_tabls = inner_tbls(logger,how,i_l_tbl,i_r_tbl,l_key,r_key)
    conn.close()



def connect_db(logger,dbname):
    """ SQLiteデータベース接続

    Parameters
    ----------
    logger :
        ログパーサー
    dbname : string
        データベースファイル生成ファイル名(パス含む)

    Returns
    -------
    conn : string
        DB接続用パス
    """
    try:
        conn = sqlite3.connect(dbname)
    except Exception as e:
        logger.error(e)
    else:
        status = "…接続OK"
        msg= dbname + status
        logger.info(msg)
        return conn

def create_db(logger,dbname):
    """ SQLiteデータベース生成関数

    Parameters
    ----------
    logger :
        ログパーサー
    dbname : string
        データベースファイル生成ファイル名(パス含む)

    Returns
    -------
    dbname : string
        DB接続用パス

    """
    try:
        con = sqlite3.connect(dbname)
    except Exception as e:
        logger.error(e)
    else:
        status = "…生成OK"
        msg= dbname + status
        logger.info(msg)
        return con

## テーブル作成処理
def create_tbls(logger,fs,tbl_name,conn):
    """ SQLiteテーブル生成関数

    Parameters
    ----------
    logger :
        ログパーサー
    fs : string
        CSVファイル格納ディレクトリパス
    tbl_name : string
        テーブル名
    conn : string
        DB接続コネクション

    Returns
    -------
    なし

    """
    try:
        start = "テーブル生成処理開始"
        start_msg = tbl_name + start
        logger.info(start_msg)
        logger.info(fs)
        if fs == "":
            logger.info("--- testテーブル生成:" + tbl_name + "---")
            df = pd.DataFrame({"A":["test", "test2"],"B":[1, 2],"C":[1.0, 2.0]})
            df.to_sql(tbl_name, con=conn,  if_exists='replace')
            conn.commit()
            return
        data = pd.read_csv(fs, encoding="utf-8-sig")
        data.drop_duplicates(subset=None, keep='first',inplace=True,ignore_index=True)
        print(data.describe())
        print(data.value_counts())
        print(data)
        data.to_sql(tbl_name, con=conn,  if_exists='replace')
        conn.commit()
    except Exception as e:
        logger.error(e)
    else:
        status = "…生成OK"
        msg= tbl_name + status
        logger.info(msg)
        return


## 内部結合用テーブル読込処理
def select_tbl(logger,tbl_name,conn):
    """ SQLiteテーブル_内部結合用左テーブル読込

    Parameters
    ----------
    logger :
        ログパーサー
    tbl_name : string
        読み取り対象テーブル名
    conn : string
        DB接続コネクション

    Returns
    -------
    df : DataFrame

    """
    try:
        start = ":テーブル取得処理開始"
        start_msg = tbl_name + start
        logger.info(start_msg)
        sql = "select * from " + tbl_name + ";"
        df = pd.read_sql(sql, con=conn)
    except Exception as e:
        logger.error(e)
    else:
        status = ":データフレーム抽出"
        msg= tbl_name + status
        logger.info(msg)
        return df

## テーブルレコード追加処理
def insert_tbl(logger,tbl_name,fs,conn):
    """ SQLiteテーブル_レコード追加処理

    Parameters
    ----------
    logger :
        ログパーサー
    tbl_name : string
        読み取り対象テーブル名
    conn : string
        DB接続コネクション

    Returns
    -------
    df : DataFrame

    """
    try:
        start = "：レコード追加処理開始"
        start_msg = tbl_name + start
        logger.info(start_msg)
        act_msg = "追加レコードファイル："
        act_info = act_msg + fs
        logger.info(act_info)
        data = pd.read_csv(fs, encoding="utf-8-sig")
        print(data)
        data.drop_duplicates(subset=None, keep='first',inplace=True,ignore_index=True)
        print(data)
        sql = "select * from " + tbl_name + ";"
        df = pd.read_sql(sql, con=conn)
        print(df)
        data.to_sql(tbl_name, conn,  if_exists='append')
        conn.commit()
        sql = "select * from " + tbl_name + ";"
        df = pd.read_sql(sql, con=conn)
        print(df)
        print(df.describe())
        print(df.value_counts())
    except Exception as e:
        logger.error(e)
    else:
        status = "…レコード追加処理OK"
        msg= tbl_name + status
        logger.info(msg)
        return

def concat_tbls(logger,i_l_tbl,i_r_tbl):
    """ SQLiteテーブル_内部結合処理

    Parameters
    ----------
    logger :
        ログパーサー
    i_l_tbl : string
        テーブル名
    i_r_tbl : string
        テーブル名

    Returns
    -------
    concat_outer : DataFrame


    """
    try:
        start = "テーブル結合処理開始"
        start_msg = start
        logger.info(start_msg)
        concat_outer = pd.concat([i_l_tbl, i_r_tbl])
        print(concat_outer)
    except Exception as e:
        logger.error(e)
    else:
        status = "テーブル結合処理完了"
        msg= status
        logger.info(msg)
        return concat_outer


def inner_tbls(logger,how,i_l_tbl,i_r_tbl,l_key,r_key):
    """ SQLiteテーブル_内部結合処理

    Parameters
    ----------
    logger :
        ログパーサー
    how : string
        結合種別
    i_l_tbl : string
        テーブル名
    i_r_tbl : string
        テーブル名
    l_key : string
        左テーブル検索Key
    r_key : string
        右テーブル検索Key

    Returns
    -------
    merged_inner : DataFrame


    """
    try:
        start = "テーブル結合処理開始"
        start_msg = start
        logger.info(start_msg)
        merged_inner = pd.merge(how=how , left=i_l_tbl, right=i_r_tbl, left_on=l_key, right_on=r_key)
        merged_inner.shape
        print(merged_inner)
    except Exception as e:
        logger.error(e)
    else:
        status = "テーブル結合処理完了"
        msg= status
        logger.info(msg)
        return merged_inner

if __name__ == '__main__':
    main()
