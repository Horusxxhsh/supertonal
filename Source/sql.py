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
    # ���ӵ����ݿ�
    conn = sqlite3.connect(r'E:\c++\juceproject\juceEffector\supertonal\Builds\VisualStudio2022\music_info.db')
    cursor = conn.cursor()

    # ��ȡindex��ֵ
    if len(sys.argv) > 2:
        chat_message = sys.argv[1]  # ��ȡ��������c++������ĵ�һ������
        print(f"Chat message: {chat_message}")
        parts = chat_message.split(',')
        if len(parts) < 48:
            print("�����в����ָ���б��Ȳ��� 48���������롣")
        else:
            first_47 = parts[:48]
            try:
                # �� first_47[0] �� first_47[8] ת��Ϊ������
                for i in range(9):
                    first_47[i] = float(first_47[i])

                # ��ȡuserMessageToSend��ֵ�����д���
                userMessageToSend = sys.argv[2]  # ��ȡ��������c++������ĵڶ�������
                print(f"userMessageToSend: {userMessageToSend}")

                # ��ѯƥ��ļ�¼
                cursor.execute("SELECT SongName, Style, Parameters FROM music_responses WHERE SongName =?",
                               (userMessageToSend,))
                row = cursor.fetchone()

                if row:
                    song_name = row[0]
                    try:
                        style = json.loads(row[1])
                        parameters = json.loads(row[2])

                        # �� first_47[0] == 1.0 ʱ���� "CompressorOff" �滻Ϊ "CompressorOn"
                        if first_47[0] == 1.0 and 'CompressorOff' in parameters:
                            compressor_settings = parameters.pop('CompressorOff')
                            parameters['CompressorOn'] = compressor_settings
                        # �� first_47[1] == 1.0 ʱ���� "ScreamerOff" �滻Ϊ "ScreamerOn"
                        if first_47[1] == 1.0 and 'ScreamerOff' in parameters:
                            compressor_settings = parameters.pop('ScreamerOff')
                            parameters['ScreamerOn'] = compressor_settings
                            # �� first_47[2] == 1.0 ʱ���� "DriverOff" �滻Ϊ "DriverOn"
                        if first_47[2] == 1.0 and 'DriverOff' in parameters:
                            compressor_settings = parameters.pop('DriverOff')
                            parameters['DriverOn'] = compressor_settings
                        # �� first_47[3] == 1.0 ʱ���� "DelayOff" �滻Ϊ "DelayOn"
                        if first_47[3] == 1.0 and 'DelayOff' in parameters:
                            compressor_settings = parameters.pop('DelayOff')
                            parameters['DelayOn'] = compressor_settings
                            # �� first_47[4] == 1.0 ʱ���� "ReverbOff" �滻Ϊ "ReverbOn"
                        if first_47[4] == 1.0 and 'ReverbOff' in parameters:
                            compressor_settings = parameters.pop('ReverbOff')
                            parameters['ReverbOn'] = compressor_settings
                        # �� first_47[5] == 1.0 ʱ���� "ChorusOff" �滻Ϊ "ChorusOn"
                        if first_47[5] == 1.0 and 'ChorusOff' in parameters:
                            compressor_settings = parameters.pop('ChorusOff')
                            parameters['ChorusOn'] = compressor_settings
                        # �� first_47[6] == 1.0 ʱ���� "FlangerOff" �滻Ϊ "FlangerOn"
                        if first_47[6] == 1.0 and 'FlangerOff' in parameters:
                            compressor_settings = parameters.pop('FlangerOff')
                            parameters['FlangerOn'] = compressor_settings
                        # �� first_47[7] == 1.0 ʱ���� "PhaserOff" �滻Ϊ "PhaserOn"
                        if first_47[7] == 1.0 and 'PhaserOff' in parameters:
                            compressor_settings = parameters.pop('PhaserOff')
                            parameters['PhaserOn'] = compressor_settings
                        # �� first_47[8] == 1.0 ʱ���� "EqualiserOff" �滻Ϊ "EqualiserOn"
                        if first_47[8] == 1.0 and 'EqualiserOff' in parameters:
                            compressor_settings = parameters.pop('EqualiserOff')
                            parameters['EqualiserOn'] = compressor_settings
                        # �������ݿ��еĲ���ֵ
                        if first_47[0] == 1.0:
                            if 'CompressorOn' in parameters:

                                # �� first_47[9] ת��Ϊ Threshold ��Χ��ֵ
                                first_47[9] = float(first_47[9])
                                threshold = -128 + (0 - (-128)) * first_47[9]
                                parameters['CompressorOn']['Threshold'] = threshold

                                # ��ȡ Ratio ֵ
                                first_47[11] = float(first_47[11])
                                ratio = get_ratio(first_47[11])
                                if ratio is not None:
                                    parameters['CompressorOn']['Ratio'] = ratio
                                else:
                                    print(f"δ�ҵ� first_47[11] = {first_47[11]} ��Ӧ�� Ratio ֵ")

                                parameters['CompressorOn']['Attack'] = first_47[10]
                                parameters['CompressorOn']['Release'] = first_47[12]

                                # �� first_47[13] ת��Ϊ Makeup ��Χ��ֵ
                                first_47[13] = float(first_47[13])
                                makeup = -128 + (64 - (-128)) * first_47[13]
                                parameters['CompressorOn']['Makeup'] = makeup

                                parameters['CompressorOn']['Mix'] = first_47[14]

                        if first_47[2] == 1.0:
                            if 'DriverOn' in parameters:
                                parameters['DriverOn']['Distortion'] = first_47[18]
                                # �� first_47[19] ת��Ϊ Volume ��Χ��ֵ
                                first_47[19] = float(first_47[19])
                                volume = -64 + (0 - (-64)) * first_47[19]
                                parameters['DriverOn']['Volume'] = volume

                        if first_47[1] == 1.0:
                            if 'ScreamerOn' in parameters:
                                parameters['ScreamerOn']['Drive'] = first_47[15]
                                parameters['ScreamerOn']['Tone'] = first_47[17]
                                # �� first_47[16] ת��Ϊ Volume ��Χ��ֵ
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
                                    # �� first_47[40] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[40] = float(first_47[40])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[40]
                                    parameters['EqualiserOn']['100hz'] = fz

                                    # �� first_47[41] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[41] = float(first_47[41])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[41]
                                    parameters['EqualiserOn']['200hz'] = fz

                                    # �� first_47[42] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[42] = float(first_47[42])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[42]
                                    parameters['EqualiserOn']['400hz'] = fz

                                    # �� first_47[43] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[43] = float(first_47[43])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[43]
                                    parameters['EqualiserOn']['800hz'] = fz

                                    # �� first_47[44] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[44] = float(first_47[44])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[44]
                                    parameters['EqualiserOn']['1600hz'] = fz

                                    # �� first_47[45] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[45] = float(first_47[45])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[45]
                                    parameters['EqualiserOn']['3200hz'] = fz

                                    # �� first_47[46] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[46] = float(first_47[46])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[46]
                                    parameters['EqualiserOn']['6400hz'] = fz
                                if len(first_47) > 47:
                                    # �� first_47[47] ת��Ϊ Frequency ��Χ��ֵ
                                    first_47[47] = float(first_47[47])
                                    fz = -15.00 + (15.00 - (-15.00)) * first_47[47]
                                    parameters['EqualiserOn']['Level'] = fz

                        if first_47[5] == 1.0:
                            if 'ChorusOn' in parameters:
                                # �� first_47[27] ת��Ϊ Depth ��Χ��ֵ
                                first_47[27] = float(first_47[27])
                                depth = 0.010 + (0.050 - 0.010) * first_47[27]
                                parameters['ChorusOn']['Delay'] = depth

                                parameters['ChorusOn']['Depth'] = first_47[28]

                                # �� first_47[29] ת��Ϊ Frequency ��Χ��ֵ
                                first_47[29] = float(first_47[29])
                                frequency = 0.05 + (2.00 - 0.05) * first_47[29]
                                parameters['ChorusOn']['Frequency'] = frequency

                                # �� first_47[30] ת��Ϊ Width ��Χ��ֵ
                                first_47[30] = float(first_47[30])
                                width = 0.010 + (0.050 - 0.010) * first_47[30]
                                parameters['ChorusOn']['Width'] = width

                        if first_47[6] == 1.0:
                            if 'FlangerOn' in parameters:
                                # �� first_47[31] ת��Ϊ Delay ��Χ��ֵ
                                first_47[31] = float(first_47[31])
                                delay = 0.00100 + (0.02000 - 0.00100) * first_47[31]
                                parameters['FlangerOn']['Delay'] = delay

                                parameters['FlangerOn']['Depth'] = first_47[32]

                                # �� first_47[33] ת��Ϊ Feedback ��Χ��ֵ
                                first_47[33] = float(first_47[33])
                                feedback = 0.00 + (0.50 - 0.00) * first_47[33]
                                parameters['FlangerOn']['Feedback'] = feedback

                                # �� first_47[34] ת��Ϊ Frequency ��Χ��ֵ
                                first_47[34] = float(first_47[34])
                                frequency = 0.05 + (2.00 - 0.05) * first_47[34]
                                parameters['FlangerOn']['Frequency'] = frequency

                                # �� first_47[35] ת��Ϊ Width ��Χ��ֵ
                                first_47[35] = float(first_47[35])
                                width = 0.001 + (0.020 - 0.001) * first_47[35]
                                parameters['FlangerOn']['Width'] = width

                        if first_47[7] == 1.0:
                            if 'PhaserOn' in parameters:
                                parameters['PhaserOn']['Depth'] = first_47[36]

                                # �� first_47[37] ת��Ϊ Feedback ��Χ��ֵ
                                first_47[37] = float(first_47[37])
                                feedback = 0.00 + (0.09 - 0.00) * first_47[37]
                                parameters['PhaserOn']['Feedback'] = feedback

                                # �� first_47[38] ת��Ϊ Frequency ��Χ��ֵ
                                first_47[38] = float(first_47[38])
                                frequency = 0.00 + (2.00 - 0.00) * first_47[38]
                                parameters['PhaserOn']['Frequency'] = frequency

                                # �� first_47[39] ת��Ϊ Width ��Χ��ֵ
                                first_47[39] = float(first_47[39])
                                width = 50 + (3000 - 50) * first_47[39]
                                parameters['PhaserOn']['Width'] = width

                        # �����º�Ĳ���ת��Ϊ�ַ���
                        updated_parameters_str = json.dumps(parameters, ensure_ascii=False)

                        # �������ݿ��еļ�¼
                        cursor.execute("UPDATE music_responses SET Parameters =? WHERE SongName =?",
                                       (updated_parameters_str, song_name))
                        conn.commit()

                        # ��ӡ���º����Ϣ
                        print(f"SongName: {song_name}")
                        print(f"Style: {json.dumps(style, ensure_ascii=False, indent=2)}")
                        print(f"Parameters: {json.dumps(parameters, ensure_ascii=False, indent=2)}")
                        print("-" * 50)
                    except json.JSONDecodeError:
                        print("�����ݿ��ȡ�� JSON ���ݸ�ʽ�����������ݿ����ݡ�")
                else:
                    print(f"δ�ҵ��� {userMessageToSend} ƥ��ļ�¼")
            except ValueError:
                print("�����в����޷�ת��Ϊ���֣��������롣")
    else:
        print("�����в������㣬���ṩ��Ҫ�Ĳ���")
except sqlite3.Error as e:
    print(f"���ݿ��������: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()