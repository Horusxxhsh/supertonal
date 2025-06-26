# -*- coding: gbk -*-
import sys
import json
import sqlite3
from openai import OpenAI
import os

# ʹ�þ���·�����ӵ����ݿ�
db_path = os.path.join(os.getcwd(), 'music_info.db')
print(f"Database path: {db_path}")  # ��ӡ���ݿ��ļ�·��
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ɾ����
'''
try:
    cursor.execute("DROP TABLE IF EXISTS music_responses")
    conn.commit()
    print("Table 'music_responses' has been dropped successfully.")
except sqlite3.Error as e:
    print(f"An error occurred while dropping the table: {e}")
'''
# ��������������ڣ�
cursor.execute('''
CREATE TABLE IF NOT EXISTS music_responses (
    SongName TEXT PRIMARY KEY,
    Style TEXT,
    Parameters TEXT
)
''')
conn.commit()


client = OpenAI(api_key="sk-1b73586fde854a329ec187dc371f53ef", base_url="https://api.deepseek.com")

if len(sys.argv) > 1:
    chat_message = sys.argv[1]  # ��ȡ�����в�����c++�������ĸ�������
else:
    chat_message = "Don't cry"

print(f"Chat message: {chat_message}")

# ������һ����ʾ��
system_prompt1 = f'���Ǽ���Ч������ʦ������Ҫ��ȡ�û������еĸ��������жϸø���ԭ��������ЩЧ����ģ�飬��Щģ��������أ�ʧ�棬�ӳ٣����죬ѹ������λ���ϳ�����ߣ������Լ������ţ��ظ���������Ч�� JSON ��ʽ�Ĳ����б�����: {{"overload": "yes", "distortion": "yes", "delay": "yes", "reverb": "yes", "compression": "no", "phase": "no", "chorus": "no", "flanger": "no", "equalization": "yes", "noise_gate": "no"}}���û�����ĸ����ǣ�{chat_message}'
user_prompt1 = chat_message
response1 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt1},
        {"role": "user", "content": user_prompt1},
    ],
    stream=False
)

# ��ȡ response1 �����ݲ�����Ϊ JSON
response_content1 = response1.choices[0].message.content
# ȥ��������Ǻͻ��з�
cleaned_content1 = response_content1.replace("```json", "").replace("```", "").strip()
try:
    result1 = json.loads(cleaned_content1)
    # print(json.dumps(result1, ensure_ascii=False, indent=2))
except json.JSONDecodeError:
    print(f"Error: ��Ч��JSON��Ӧ: {cleaned_content1}")
    sys.exit(1)

# �����ڶ�����ʾ��
system_prompt2 = f'�������ִ�ʦ������Ҫ�����û�����ĸ������жϸø����ķ��(�����ж���)���ظ���������Ч�� JSON ��ʽ�Ĳ����б�����: {{"tags": ["tag_1",..."tag_n"]}}��'
user_prompt2 = f'����������{chat_message}�ķ��'
response2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt2},
        {"role": "user", "content": user_prompt2},
    ],
    stream=False
)

# ��ȡ response2 �����ݲ�����Ϊ JSON
response_content2 = response2.choices[0].message.content
# ȥ��������Ǻͻ��з�
cleaned_content2 = response_content2.replace("```json", "").replace("```", "").strip()
try:
    result2 = json.loads(cleaned_content2)
    result2_str = json.dumps(result2, ensure_ascii=False)
    #print(result2_str)
except json.JSONDecodeError:
    print(f"Error: ��Ч��JSON��Ӧ: {cleaned_content2}")
    sys.exit(1)


# ����Ч����ģ��Ͷ�Ӧ������
effectors = [
    {
        "name": "compression",
        "example_with": '{"CompressorOn": {"Threshold": "0.00", "Ratio": "2", "Attack": 68.12, "Release": "154.34", "Makeup": "21.49", "Mix": "0.25"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ����ѹ���Ĳ������ҵ�ѹ��ģ�������пɵ��ڲ���ΪRatio��Attack��Release��Makeup������Threshold�Ŀɵ��ڷ�Χ��-128.00db~0.00db��Ratio�Ŀɵ��ڷ�Χ��1~100��Attack�Ŀɵ��ڷ�Χ��0.00ms~1.00ms��Release�Ŀɵ��ڷ�Χ��0.00ms~1.00ms��Makeup�Ŀɵ��ڷ�Χ��-128.00db~64.00db,Mix�Ŀɵ��ڷ�Χ��0.00~1.00�������ʽ�ϸ����',
    },
    {
        "name": "distortion",
        "example_with": '{"DriverOn":{"Distortion":"0.68","Volume":-18.4352685}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ����ʧ��Ĳ������ҵ�ʧ��ģ�������пɵ��ڲ���ΪDistortion(Gain)��Volume������Distortion(Gain)�Ŀɵ��ڷ�Χ��0.00~1.00��Volume�Ŀɵ��ڷ�Χ��-64.0000000~0.0000000�������ʽ�ϸ����',
    },
    {
        "name": "overload",
        "example_with": '{"ScreamerOn":{"Drive":"0.81","Tone":"0.52","Level":"-24.3199567"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ���й��صĲ������ҵĹ���ģ�������пɵ��ڲ���ΪDrive��Tone��Level������Drive�Ŀɵ��ڷ�Χ��0.00~1.00��Tone�Ŀɵ��ڷ�Χ��0.00~1.00��Level�Ŀɵ��ڷ�Χ��-64.0000000~0.0000000�������ʽ�ϸ����',
    },
    {
        "name": "delay",
        "example_with": ' {"DelayOn":{"Feedback":"0.25","Delay":724.89,"Mix":"0.52"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ�����ӳٵĲ������ҵ��ӳ�ģ�������пɵ��ڲ���ΪFeedback��Delay��Mix������Feedback�Ŀɵ��ڷ�Χ��0.00~1.00��Delay(Time)�Ŀɵ��ڷ�Χ��1.00ms~10000.00ms��Mix�Ŀɵ��ڷ�Χ��0.00~1.00�������ʽ�ϸ����',
    },
    {
        "name": "reverb",
        "example_with": ' {"ReverbOn":{"Size":"0.25","Damping":0.25,"Width":"0.52","Mix":"0.56"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ���л���Ĳ������ҵĻ���ģ�������пɵ��ڲ���ΪSize��Damping��Width��Mix������Size�Ŀɵ��ڷ�Χ��0.00~1.00��Damping�Ŀɵ��ڷ�Χ��0.00~1.00��Width�Ŀɵ��ڷ�Χ��0.00~1.00��Mix�Ŀɵ��ڷ�Χ��0.00~1.00�������ʽ�ϸ����',
    },
    {
        "name": "chorus",
        "example_with": ' {"ChorusOn":{"Delay":"0.025","Depth":0.25,"Frequency":"0.51","Width":"0.024"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ���кϳ��Ĳ������ҵĺϳ�ģ�������пɵ��ڲ���ΪDelay��Depth��Frequency��Width������Delay�Ŀɵ��ڷ�Χ��0.010~0.050��Depth�Ŀɵ��ڷ�Χ��0.00~1.00��Frequency�Ŀɵ��ڷ�Χ��0.05~2.00��Width�Ŀɵ��ڷ�Χ��0.010~0.050�������ʽ�ϸ����',
    },
    {
        "name": "flanger",
        "example_with": ' {"FlangerOn":{"Delay":"0.01179","Depth":0.38,"Feedback":"0.25","Frequency":"1.26","Width":"0.011"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ������ߵĲ������ҵ����ģ�������пɵ��ڲ���ΪDelay��Depth��Feedback��Frequency��Width������Delay�Ŀɵ��ڷ�Χ��0.00100~0.02000��Depth�Ŀɵ��ڷ�Χ��0.00~1.00��Feedback�Ŀɵ��ڷ�Χ��0.00~0.50��Frequency�Ŀɵ��ڷ�Χ��0.05~2.00��Width�Ŀɵ��ڷ�Χ��0.001~0.020�������ʽ�ϸ����',
    },
    {
        "name": "equalization",
        "example_with": '{"EqualiserOn":{"100hz":"0.00","200hz":"0.00","400hz":"0.00","800hz":"0.00","1600hz":"0.00","3200hz":"0.00","6400hz":"0.00","Level":"0.00"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ���о���Ĳ������ҵľ���ģ�������пɵ��ڲ���Ϊ100hz��200hz��400hz��800hz��1600hz��3200hz��6400hz��Level������100hz�Ŀɵ��ڷ�Χ��-15.00~15.00��200hz�Ŀɵ��ڷ�Χ��-15.00~15.00��400hz�Ŀɵ��ڷ�Χ��-15.00~15.00��800hz�Ŀɵ��ڷ�Χ��-15.00~15.00��1600hz�Ŀɵ��ڷ�Χ��-15.00~15.00��3200hz�Ŀɵ��ڷ�Χ��-15.00~15.00��6400hz�Ŀɵ��ڷ�Χ��-15.00~15.00��Level�Ŀɵ��ڷ�Χ��-15.00~15.00�������ʽ�ϸ����',
    },
    {
        "name": "phase",
        "example_with": ' {"PhaserOn":{"Depth":"1.00","Feedback":"0.70","Frequency":"0.51","Width":"1366"}}',
        "prompt_with": f'��������{chat_message}����ô�����ҵ�Ч����ģ������λ�Ĳ������ҵ���λģ�������пɵ��ڲ���ΪDepth��Feedback��Frequency��Width������Depth�Ŀɵ��ڷ�Χ��0.00~1.00��Feedback�Ŀɵ��ڷ�Χ��0.00~0.90��Frequency�Ŀɵ��ڷ�Χ��0.05~2.00��Width�Ŀɵ��ڷ�Χ��50~3000�������ʽ�ϸ����',
    }
]

final_result = {}

# ʹ�� for ѭ������ͬ��Ч����ģ��
for effector in effectors:
    effector_name = effector["name"]
    if result1.get(effector_name) == "yes":
        system_prompt = f'����һ������Ч�����������ڴ�ʦ���ظ���������Ч�� JSON ��ʽ�Ĳ����б�����: {effector["example_with"]}����ز�Ҫ�ش�����б�֮����κ����ݡ�'
        user_prompt = effector["prompt_with"] + effector["example_with"]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        # ��ȡ��Ӧ���ݲ�����Ϊ JSON
        response_content = response.choices[0].message.content
        # ȥ��������Ǻͻ��з�
        cleaned_content = response_content.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(cleaned_content)
            final_result.update(result)
        except json.JSONDecodeError:
            print(f"Error: ��Ч��JSON��Ӧ: {cleaned_content}")
            sys.exit(1)
    elif result1.get(effector_name) == "no":
        if effector_name == "compression":
            final_result["CompressorOff"] = {"Threshold": "-128.00", "Ratio": "1", "Attack": "0.00", "Release": "0.00", "Makeup": "-12.00", "Mix": "0.00"}
        elif effector_name == "distortion":
            final_result["DriverOff"] = {"Distortion": "0.00", "Volume": "-64.0"}
        elif effector_name == "overload":
            final_result["ScreamerOff"] = {"Drive": "0.00", "Tone": "0.00", "Level": "-64.0000000"}
        elif effector_name == "delay":
            final_result["DelayOff"] = {"Feedback": "0.00", "Delay": "1.00", "Mix": "0.00"}
        elif effector_name == "reverb":
            final_result["ReverbOff"] = {"Size": "0.00", "Damping": "0.00", "Width": "0.00", "Mix": "0.00"}
        elif effector_name == "chorus":
            final_result["ChorusOff"] = {"Delay": "0.010", "Depth": "0.00", "Frequency": "0.05", "Width": "0.010"}
        elif effector_name == "flanger":
            final_result["FlangerOff"] = {"Delay": "0.00100", "Depth": "0.00", "Feedback": "0.00", "Frequency": "0.05", "Width": "0.001"}
        elif effector_name == "equalization":
            final_result["EqualiserOff"] = {"100hz": "0.00", "200hz": "0.00", "400hz": "0.00", "800hz": "0.00", "1600hz": "0.00", "3200hz": "0.00", "6400hz": "0.00", "Level": "0.00"}
        elif effector_name == "phase":
            final_result["PhaserOff"] = {"Depth": "0.00", "Feedback": "0.00", "Frequency": "0.05", "Width": "50"}


# �����ս��ת��Ϊ�ַ���
result_str = json.dumps(final_result, ensure_ascii=False)

# ��� chat_message �Ƿ��Ѿ����������ݿ���
cursor.execute("SELECT SongName FROM music_responses WHERE SongName =?", (chat_message,))
existing_song = cursor.fetchone()

if existing_song:
    # ������ڣ����� Style �� Parameters
    cursor.execute("UPDATE music_responses SET Style =?, Parameters =? WHERE SongName =?", (result2_str, result_str, chat_message))
else:
    # ��������ڣ�����������
    cursor.execute("INSERT INTO music_responses (SongName, Style, Parameters) VALUES (?,?,?)", (chat_message, result2_str, result_str))

conn.commit()

# ������ַ���д���ļ�
with open(r"C:\Users\Lenovo56\Desktop\result.txt", 'w', encoding='utf-8') as f:
    f.write(result_str)

# ���� Jaccard ���ƶȺ���
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# ����ʱ���ݸ����������ƶ�������
target_tags = set(result2.get("tags", []))
cursor.execute("SELECT SongName, Style, Parameters FROM music_responses")
rows = cursor.fetchall()
similar_songs = []
for row in rows:
    song_name = row[0]
    style_str = row[1]
    try:
        style = json.loads(style_str)
        tags = set(style.get("tags", []))
        similarity = jaccard_similarity(target_tags, tags)
        similar_songs.append((song_name, similarity, style_str, row[2]))
    except json.JSONDecodeError:
        print(f"Error: ��Ч��JSON��Ӧ: {style_str}")

# �����ƶ�����
similar_songs.sort(key=lambda x: x[1], reverse=True)

# ��ӡ��Ӧ���
print(f"����ĸ�������: {chat_message}")
print(f"��Ӧ�ķ��:{result2_str}")
print(f"��Ӧ����:{result_str}")
print("-" * 50)

# ������Ƹ���
for song in similar_songs:
    song_name = song[0]
    similarity = song[1]
    style = json.loads(song[2])
    resu = json.loads(song[3])
    print(f"��ȡ�������Ƹ�������: {len(similar_songs)}")
    print(f"SongName: {song_name}")
    print(f"Similarity: {similarity}")
    print(f"Style: {json.dumps(style, ensure_ascii=False, indent=2)}")
    print(f"Parameters: {json.dumps(resu, ensure_ascii=False, indent=2)}")
    print("-" * 50)

# �ر����ݿ�����
conn.close()

