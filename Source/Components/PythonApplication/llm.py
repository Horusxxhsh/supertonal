# -*- coding: gbk -*-
import sys
import json
import sqlite3
from openai import OpenAI
import os

# 使用绝对路径连接到数据库
db_path = os.path.join(os.getcwd(), 'music_info.db')
print(f"Database path: {db_path}")  # 打印数据库文件路径
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 删除表
'''
try:
    cursor.execute("DROP TABLE IF EXISTS music_responses")
    conn.commit()
    print("Table 'music_responses' has been dropped successfully.")
except sqlite3.Error as e:
    print(f"An error occurred while dropping the table: {e}")
'''
# 创建表（如果不存在）
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
    chat_message = sys.argv[1]  # 获取命令行参数（c++传过来的歌曲名）
else:
    chat_message = "Don't cry"

print(f"Chat message: {chat_message}")

# 构建第一个提示词
system_prompt1 = f'你是吉他效果器大师，你需要提取用户输入中的歌曲名来判断该歌曲原作中有哪些效果器模块，这些模块包括过载，失真，延迟，混响，压缩，相位，合唱，镶边，均衡以及噪声门，回复必须是有效的 JSON 格式的参数列表，例如: {{"overload": "yes", "distortion": "yes", "delay": "yes", "reverb": "yes", "compression": "no", "phase": "no", "chorus": "no", "flanger": "no", "equalization": "yes", "noise_gate": "no"}}。用户输入的歌曲是：{chat_message}'
user_prompt1 = chat_message
response1 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt1},
        {"role": "user", "content": user_prompt1},
    ],
    stream=False
)

# 提取 response1 的内容并解析为 JSON
response_content1 = response1.choices[0].message.content
# 去除代码块标记和换行符
cleaned_content1 = response_content1.replace("```json", "").replace("```", "").strip()
try:
    result1 = json.loads(cleaned_content1)
    # print(json.dumps(result1, ensure_ascii=False, indent=2))
except json.JSONDecodeError:
    print(f"Error: 无效的JSON响应: {cleaned_content1}")
    sys.exit(1)

# 构建第二个提示词
system_prompt2 = f'你是音乐大师，你需要根据用户输入的歌曲名判断该歌曲的风格(可以有多种)，回复必须是有效的 JSON 格式的参数列表，例如: {{"tags": ["tag_1",..."tag_n"]}}。'
user_prompt2 = f'分析歌曲：{chat_message}的风格'
response2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt2},
        {"role": "user", "content": user_prompt2},
    ],
    stream=False
)

# 提取 response2 的内容并解析为 JSON
response_content2 = response2.choices[0].message.content
# 去除代码块标记和换行符
cleaned_content2 = response_content2.replace("```json", "").replace("```", "").strip()
try:
    result2 = json.loads(cleaned_content2)
    result2_str = json.dumps(result2, ensure_ascii=False)
    #print(result2_str)
except json.JSONDecodeError:
    print(f"Error: 无效的JSON响应: {cleaned_content2}")
    sys.exit(1)


# 定义效果器模块和对应的配置
effectors = [
    {
        "name": "compression",
        "example_with": '{"CompressorOn": {"Threshold": "0.00", "Ratio": "2", "Attack": 68.12, "Release": "154.34", "Makeup": "21.49", "Mix": "0.25"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中压缩的参数，我的压缩模块中所有可调节参数为Ratio、Attack、Release和Makeup，其中Threshold的可调节范围是-128.00db~0.00db，Ratio的可调节范围是1~100，Attack的可调节范围是0.00ms~1.00ms，Release的可调节范围是0.00ms~1.00ms，Makeup的可调节范围是-128.00db~64.00db,Mix的可调节范围是0.00~1.00。输出格式严格参照',
    },
    {
        "name": "distortion",
        "example_with": '{"DriverOn":{"Distortion":"0.68","Volume":-18.4352685}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中失真的参数，我的失真模块中所有可调节参数为Distortion(Gain)和Volume，其中Distortion(Gain)的可调节范围是0.00~1.00，Volume的可调节范围是-64.0000000~0.0000000。输出格式严格参照',
    },
    {
        "name": "overload",
        "example_with": '{"ScreamerOn":{"Drive":"0.81","Tone":"0.52","Level":"-24.3199567"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中过载的参数，我的过载模块中所有可调节参数为Drive、Tone和Level，其中Drive的可调节范围是0.00~1.00，Tone的可调节范围是0.00~1.00，Level的可调节范围是-64.0000000~0.0000000。输出格式严格参照',
    },
    {
        "name": "delay",
        "example_with": ' {"DelayOn":{"Feedback":"0.25","Delay":724.89,"Mix":"0.52"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中延迟的参数，我的延迟模块中所有可调节参数为Feedback、Delay和Mix，其中Feedback的可调节范围是0.00~1.00，Delay(Time)的可调节范围是1.00ms~10000.00ms，Mix的可调节范围是0.00~1.00。输出格式严格参照',
    },
    {
        "name": "reverb",
        "example_with": ' {"ReverbOn":{"Size":"0.25","Damping":0.25,"Width":"0.52","Mix":"0.56"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中混响的参数，我的混响模块中所有可调节参数为Size、Damping、Width和Mix，其中Size的可调节范围是0.00~1.00，Damping的可调节范围是0.00~1.00，Width的可调节范围是0.00~1.00，Mix的可调节范围是0.00~1.00。输出格式严格参照',
    },
    {
        "name": "chorus",
        "example_with": ' {"ChorusOn":{"Delay":"0.025","Depth":0.25,"Frequency":"0.51","Width":"0.024"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中合唱的参数，我的合唱模块中所有可调节参数为Delay、Depth、Frequency和Width，其中Delay的可调节范围是0.010~0.050，Depth的可调节范围是0.00~1.00，Frequency的可调节范围是0.05~2.00，Width的可调节范围是0.010~0.050。输出格式严格参照',
    },
    {
        "name": "flanger",
        "example_with": ' {"FlangerOn":{"Delay":"0.01179","Depth":0.38,"Feedback":"0.25","Frequency":"1.26","Width":"0.011"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中镶边的参数，我的镶边模块中所有可调节参数为Delay、Depth、Feedback、Frequency和Width，其中Delay的可调节范围是0.00100~0.02000，Depth的可调节范围是0.00~1.00，Feedback的可调节范围是0.00~0.50，Frequency的可调节范围是0.05~2.00，Width的可调节范围是0.001~0.020。输出格式严格参照',
    },
    {
        "name": "equalization",
        "example_with": '{"EqualiserOn":{"100hz":"0.00","200hz":"0.00","400hz":"0.00","800hz":"0.00","1600hz":"0.00","3200hz":"0.00","6400hz":"0.00","Level":"0.00"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中均衡的参数，我的均衡模块中所有可调节参数为100hz、200hz、400hz、800hz、1600hz、3200hz、6400hz和Level，其中100hz的可调节范围是-15.00~15.00，200hz的可调节范围是-15.00~15.00，400hz的可调节范围是-15.00~15.00，800hz的可调节范围是-15.00~15.00，1600hz的可调节范围是-15.00~15.00，3200hz的可调节范围是-15.00~15.00，6400hz的可调节范围是-15.00~15.00，Level的可调节范围是-15.00~15.00。输出格式严格参照',
    },
    {
        "name": "phase",
        "example_with": ' {"PhaserOn":{"Depth":"1.00","Feedback":"0.70","Frequency":"0.51","Width":"1366"}}',
        "prompt_with": f'我想演奏{chat_message}该怎么调节我的效果器模块中相位的参数，我的相位模块中所有可调节参数为Depth、Feedback、Frequency和Width，其中Depth的可调节范围是0.00~1.00，Feedback的可调节范围是0.00~0.90，Frequency的可调节范围是0.05~2.00，Width的可调节范围是50~3000。输出格式严格参照',
    }
]

final_result = {}

# 使用 for 循环处理不同的效果器模块
for effector in effectors:
    effector_name = effector["name"]
    if result1.get(effector_name) == "yes":
        system_prompt = f'你是一个吉他效果器参数调节大师，回复必须是有效的 JSON 格式的参数列表，例如: {effector["example_with"]}，务必不要回答参数列表之外的任何内容。'
        user_prompt = effector["prompt_with"] + effector["example_with"]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )

        # 提取响应内容并解析为 JSON
        response_content = response.choices[0].message.content
        # 去除代码块标记和换行符
        cleaned_content = response_content.replace("```json", "").replace("```", "").strip()
        try:
            result = json.loads(cleaned_content)
            final_result.update(result)
        except json.JSONDecodeError:
            print(f"Error: 无效的JSON响应: {cleaned_content}")
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


# 将最终结果转换为字符串
result_str = json.dumps(final_result, ensure_ascii=False)

# 检查 chat_message 是否已经存在于数据库中
cursor.execute("SELECT SongName FROM music_responses WHERE SongName =?", (chat_message,))
existing_song = cursor.fetchone()

if existing_song:
    # 如果存在，更新 Style 和 Parameters
    cursor.execute("UPDATE music_responses SET Style =?, Parameters =? WHERE SongName =?", (result2_str, result_str, chat_message))
else:
    # 如果不存在，插入新数据
    cursor.execute("INSERT INTO music_responses (SongName, Style, Parameters) VALUES (?,?,?)", (chat_message, result2_str, result_str))

conn.commit()

# 将结果字符串写入文件
with open(r"C:\Users\Lenovo56\Desktop\result.txt", 'w', encoding='utf-8') as f:
    f.write(result_str)

# 定义 Jaccard 相似度函数
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# 检索时根据歌曲风格的相似度来检索
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
        print(f"Error: 无效的JSON响应: {style_str}")

# 按相似度排序
similar_songs.sort(key=lambda x: x[1], reverse=True)

# 打印响应结果
print(f"处理的歌曲名称: {chat_message}")
print(f"响应的风格:{result2_str}")
print(f"响应参数:{result_str}")
print("-" * 50)

# 输出相似歌曲
for song in similar_songs:
    song_name = song[0]
    similarity = song[1]
    style = json.loads(song[2])
    resu = json.loads(song[3])
    print(f"获取到的相似歌曲数量: {len(similar_songs)}")
    print(f"SongName: {song_name}")
    print(f"Similarity: {similarity}")
    print(f"Style: {json.dumps(style, ensure_ascii=False, indent=2)}")
    print(f"Parameters: {json.dumps(resu, ensure_ascii=False, indent=2)}")
    print("-" * 50)

# 关闭数据库连接
conn.close()

