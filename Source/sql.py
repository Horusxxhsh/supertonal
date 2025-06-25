# -*- coding: gbk -*-
import sys
import json
import sqlite3
import math


def get_ratio(value):
    mapping = {
        0.000000: 1,
        0.118416: 2,
        0.197404: 3,
        0.256761: 4,
        0.304328: 5,
        0.344022: 6,
        0.378081: 7,
        0.407910: 8,
        0.434443: 9,
        0.458337: 10,
    }
    return mapping.get(value)


try:
    # 连接到数据库
    conn = sqlite3.connect(r'E:\c++\juceproject\juceEffector\supertonal\Builds\VisualStudio2022\music_info.db')
    cursor = conn.cursor()

    # 获取index的值
    if len(sys.argv) > 2:
        chat_message = sys.argv[1]  # 获取命令行中c++程序传入的第一个参数
        print(f"Chat message: {chat_message}")
        parts = chat_message.split(',')
        if len(parts) < 48:
            print("命令行参数分割后列表长度不足 48，请检查输入。")
        else:
            first_47 = parts[:48]
            try:
                # 将 first_47[0] 到 first_47[8] 转换为浮点数
                for i in range(9):
                    first_47[i] = float(first_47[i])

                # 获取userMessageToSend的值并进行处理
                userMessageToSend = sys.argv[2]  # 获取命令行中c++程序传入的第二个参数
                print(f"userMessageToSend: {userMessageToSend}")

                # 查询匹配的记录
                cursor.execute("SELECT SongName, Style, Parameters FROM music_responses WHERE SongName =?",
                               (userMessageToSend,))
                row = cursor.fetchone()

                if row:
                    song_name = row[0]
                    try:
                        style = json.loads(row[1])
                        parameters = json.loads(row[2])

                        # 当 first_47[0] == 1.0 时，将 "CompressorOff" 替换为 "CompressorOn"
                        if first_47[0] == 1.0 and 'CompressorOff' in parameters:
                            compressor_settings = parameters.pop('CompressorOff')
                            parameters['CompressorOn'] = compressor_settings
                        # 当 first_47[1] == 1.0 时，将 "ScreamerOff" 替换为 "ScreamerOn"
                        if first_47[1] == 1.0 and 'ScreamerOff' in parameters:
                            compressor_settings = parameters.pop('ScreamerOff')
                            parameters['ScreamerOn'] = compressor_settings
                            # 当 first_47[2] == 1.0 时，将 "DriverOff" 替换为 "DriverOn"
                        if first_47[2] == 1.0 and 'DriverOff' in parameters:
                            compressor_settings = parameters.pop('DriverOff')
                            parameters['DriverOn'] = compressor_settings
                        # 当 first_47[3] == 1.0 时，将 "DelayOff" 替换为 "DelayOn"
                        if first_47[3] == 1.0 and 'DelayOff' in parameters:
                            compressor_settings = parameters.pop('DelayOff')
                            parameters['DelayOn'] = compressor_settings
                            # 当 first_47[4] == 1.0 时，将 "ReverbOff" 替换为 "ReverbOn"
                        if first_47[4] == 1.0 and 'ReverbOff' in parameters:
                            compressor_settings = parameters.pop('ReverbOff')
                            parameters['ReverbOn'] = compressor_settings
                        # 当 first_47[5] == 1.0 时，将 "ChorusOff" 替换为 "ChorusOn"
                        if first_47[5] == 1.0 and 'ChorusOff' in parameters:
                            compressor_settings = parameters.pop('ChorusOff')
                            parameters['ChorusOn'] = compressor_settings
                        # 当 first_47[6] == 1.0 时，将 "FlangerOff" 替换为 "FlangerOn"
                        if first_47[6] == 1.0 and 'FlangerOff' in parameters:
                            compressor_settings = parameters.pop('FlangerOff')
                            parameters['FlangerOn'] = compressor_settings
                        # 当 first_47[7] == 1.0 时，将 "PhaserOff" 替换为 "PhaserOn"
                        if first_47[7] == 1.0 and 'PhaserOff' in parameters:
                            compressor_settings = parameters.pop('PhaserOff')
                            parameters['PhaserOn'] = compressor_settings
                        # 当 first_47[8] == 1.0 时，将 "EqualiserOff" 替换为 "EqualiserOn"
                        if first_47[8] == 1.0 and 'EqualiserOff' in parameters:
                            compressor_settings = parameters.pop('EqualiserOff')
                            parameters['EqualiserOn'] = compressor_settings
                        # 更新数据库中的参数值
                        if first_47[0] == 1.0:
                            if 'CompressorOn' in parameters:

                                # 将 first_47[9] 转换为 Threshold 范围的值
                                first_47[9] = float(first_47[9])
                                threshold = -128 + (0 - (-128)) * first_47[9]
                                parameters['CompressorOn']['Threshold'] = threshold

                                # 获取 Ratio 值
                                first_47[11] = float(first_47[11])
                                ratio = get_ratio(first_47[11])
                                if ratio is not None:
                                    parameters['CompressorOn']['Ratio'] = ratio
                                else:
                                    print(f"未找到 first_47[11] = {first_47[11]} 对应的 Ratio 值")

                                parameters['CompressorOn']['Attack'] = first_47[10]
                                parameters['CompressorOn']['Release'] = first_47[12]

                                # 将 first_47[13] 转换为 Makeup 范围的值
                                first_47[13] = float(first_47[13])
                                makeup = -128 + (64 - (-128)) * first_47[13]
                                parameters['CompressorOn']['Makeup'] = makeup

                                parameters['CompressorOn']['Mix'] = first_47[14]

                        if first_47[2] == 1.0:
                            if 'DriverOn' in parameters:
                                parameters['DriverOn']['Distortion'] = first_47[18]
                                # 将 first_47[19] 转换为 Volume 范围的值
                                first_47[19] = float(first_47[19])
                                volume = -64 + (0 - (-64)) * first_47[19]
                                parameters['DriverOn']['Volume'] = volume

                        if first_47[1] == 1.0:
                            if 'ScreamerOn' in parameters:
                                parameters['ScreamerOn']['Drive'] = first_47[15]
                                parameters['ScreamerOn']['Tone'] = first_47[17]
                                # 将 first_47[16] 转换为 Volume 范围的值
                                first_47[16] = float(first_47[16])
                                volume = -64 + (0 - (-64)) * first_47[16]
                                parameters['ScreamerOn']['Level'] = volume

                        if first_47[3] == 1.0:
                            if 'DelayOn' in parameters:
                                parameters['DelayOn']['Feedback'] = first_47[20]

                                parameters['DelayOn']['Delay'] = "450.00"

                                parameters['DelayOn']['Mix'] = first_47[22]

                        if first_47[4] == 1.0:
                            if 'ReverbOn' in parameters:
                                parameters['ReverbOn']['Size'] = first_47[23]
                                parameters['ReverbOn']['Damping'] = first_47[24]
                                parameters['ReverbOn']['Width'] = first_47[25]
                                parameters['ReverbOn']['Mix'] = first_47[26]

                        if first_47[8] == 1.0:
                            if 'EqualiserOn' in parameters:
                                if len(first_47) > 46:
                                    # 将 first_47[40] 转换为 Frequency 范围的值
                                    first_47[40] = float(first_47[40])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[40]
                                    parameters['EqualiserOn']['100hz'] = fz

                                    # 将 first_47[41] 转换为 Frequency 范围的值
                                    first_47[41] = float(first_47[41])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[41]
                                    parameters['EqualiserOn']['200hz'] = fz

                                    # 将 first_47[42] 转换为 Frequency 范围的值
                                    first_47[42] = float(first_47[42])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[42]
                                    parameters['EqualiserOn']['400hz'] = fz

                                    # 将 first_47[43] 转换为 Frequency 范围的值
                                    first_47[43] = float(first_47[43])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[43]
                                    parameters['EqualiserOn']['800hz'] = fz

                                    # 将 first_47[44] 转换为 Frequency 范围的值
                                    first_47[44] = float(first_47[44])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[44]
                                    parameters['EqualiserOn']['1600hz'] = fz

                                    # 将 first_47[45] 转换为 Frequency 范围的值
                                    first_47[45] = float(first_47[45])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[45]
                                    parameters['EqualiserOn']['3200hz'] = fz

                                    # 将 first_47[46] 转换为 Frequency 范围的值
                                    first_47[46] = float(first_47[46])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[46]
                                    parameters['EqualiserOn']['6400hz'] = fz
                                if len(first_47) > 47:
                                    # 将 first_47[47] 转换为 Frequency 范围的值
                                    first_47[47] = float(first_47[47])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[47]
                                    parameters['EqualiserOn']['Level'] = fz

                        if first_47[5] == 1.0:
                            if 'ChorusOn' in parameters:
                                # 将 first_47[27] 转换为 Depth 范围的值
                                first_47[27] = float(first_47[27])
                                depth = 0.010 + (0.050 - 0.010) * first_47[27]
                                parameters['ChorusOn']['Delay'] = depth

                                parameters['ChorusOn']['Depth'] = first_47[28]

                                # 将 first_47[29] 转换为 Frequency 范围的值
                                first_47[29] = float(first_47[29])
                                frequency = 0.05 + (2.00 - 0.05) * first_47[29]
                                parameters['ChorusOn']['Frequency'] = frequency

                                # 将 first_47[30] 转换为 Width 范围的值
                                first_47[30] = float(first_47[30])
                                width = 0.010 + (0.050 - 0.010) * first_47[30]
                                parameters['ChorusOn']['Width'] = width

                        if first_47[6] == 1.0:
                            if 'FlangerOn' in parameters:
                                # 将 first_47[31] 转换为 Delay 范围的值
                                first_47[31] = float(first_47[31])
                                delay = 0.00100 + (0.02000 - 0.00100) * first_47[31]
                                parameters['FlangerOn']['Delay'] = delay

                                parameters['FlangerOn']['Depth'] = first_47[32]

                                # 将 first_47[33] 转换为 Feedback 范围的值
                                first_47[33] = float(first_47[33])
                                feedback = 0.00 + (0.50 - 0.00) * first_47[33]
                                parameters['FlangerOn']['Feedback'] = feedback

                                # 将 first_47[34] 转换为 Frequency 范围的值
                                first_47[34] = float(first_47[34])
                                frequency = 0.05 + (2.00 - 0.05) * first_47[34]
                                parameters['FlangerOn']['Frequency'] = frequency

                                # 将 first_47[35] 转换为 Width 范围的值
                                first_47[35] = float(first_47[35])
                                width = 0.001 + (0.020 - 0.001) * first_47[35]
                                parameters['FlangerOn']['Width'] = width

                        if first_47[7] == 1.0:
                            if 'PhaserOn' in parameters:
                                parameters['PhaserOn']['Depth'] = first_47[36]

                                # 将 first_47[37] 转换为 Feedback 范围的值
                                first_47[37] = float(first_47[37])
                                feedback = 0.00 + (0.09 - 0.00) * first_47[37]
                                parameters['PhaserOn']['Feedback'] = feedback

                                # 将 first_47[38] 转换为 Frequency 范围的值
                                first_47[38] = float(first_47[38])
                                frequency = 0.00 + (2.00 - 0.00) * first_47[38]
                                parameters['PhaserOn']['Frequency'] = frequency

                                # 将 first_47[39] 转换为 Width 范围的值
                                first_47[39] = float(first_47[39])
                                width = 50 + (3000 - 50) * first_47[39]
                                parameters['PhaserOn']['Width'] = width

                        # 将更新后的参数转换为字符串
                        updated_parameters_str = json.dumps(parameters, ensure_ascii=False)

                        # 更新数据库中的记录
                        cursor.execute("UPDATE music_responses SET Parameters =? WHERE SongName =?",
                                       (updated_parameters_str, song_name))
                        conn.commit()

                        # 打印更新后的信息
                        print(f"SongName: {song_name}")
                        print(f"Style: {json.dumps(style, ensure_ascii=False, indent=2)}")
                        print(f"Parameters: {json.dumps(parameters, ensure_ascii=False, indent=2)}")
                        print("-" * 50)
                    except json.JSONDecodeError:
                        print("从数据库读取的 JSON 数据格式错误，请检查数据库数据。")
                else:
                    print(f"未找到与 {userMessageToSend} 匹配的记录")
            except ValueError:
                print("命令行参数无法转换为数字，请检查输入。")
    else:
        print("命令行参数不足，请提供必要的参数")
except sqlite3.Error as e:
    print(f"数据库操作出错: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()