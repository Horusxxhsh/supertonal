# -*- coding: gbk -*-
import sqlite3

# ���ӵ����ݿ�
conn = sqlite3.connect(r'E:\c++\juceproject\juceEffector\supertonal\Builds\VisualStudio2022\music_info.db')
#conn = sqlite3.connect(r'E:\c++\day11\day11\music_info.db')
cursor = conn.cursor()

# ִ�в�ѯ���
try:
    cursor.execute("SELECT * FROM music_responses")
    results = cursor.fetchall()
    for row in results:
        print(row)
except sqlite3.Error as e:
    print(f"ִ�� SQL ���ʱ����: {e}")

# �ر�����
conn.close()
