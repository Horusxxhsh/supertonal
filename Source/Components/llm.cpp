#include "llm.h"
#include <cstdlib>
#include <sstream>

// 定义一个函数用于从环境变量中读取并还原类型
template<typename T>
T readEnvWithType(const std::string& key) {
    const char* envValue = std::getenv(key.c_str());
    if (envValue == nullptr) {
        return T(); // 返回默认值
    }
    std::string valueStr = envValue;
    size_t colonPos = valueStr.find(':');
    if (colonPos == std::string::npos) {
        return T(); // 返回默认值
    }
    std::string type = valueStr.substr(0, colonPos);
    std::string value = valueStr.substr(colonPos + 1);

    T result;
    std::istringstream iss(value);
    iss >> result;
    return result;
}

//定义一个函数用于存储环境变量并添加类型信息
void storeEnvWithType(const std::string& key, const juce::String& value, const std::string& type) {
    std::string envStr = key + "=" + type + ":" + value.toStdString();
    putenv(const_cast<char*>(envStr.c_str()));
    juce::Logger::writeToLog("Stored Environment Variable: " + juce::String(envStr));
}




// 示例：将环境变量 Compressor_on 中的值赋值给另一个 int 类型的变量
void assignCompressorOnValue() {
    bool f_FeedbackValue = readEnvWithType<bool>("Compressor_on");
    // 现在 compressorOnValue 包含了环境变量 Compressor_on 的值
    if (f_FeedbackValue) {
        juce::Logger::writeToLog("f_Feedback value=true");
    }
}

EffectParameters extractParameters(const juce::String& jsonString) {
    EffectParameters params;

    // 解析 JSON 字符串
    auto jsonVar = juce::JSON::parse(jsonString);
    if (jsonVar.isVoid()) {
        std::cerr << "Failed to parse JSON." << std::endl;
        return params;
    }

    // 输出解析后的 JSON 数据用于调试
    juce::Logger::writeToLog("Parsed JSON for parameter extraction: " + juce::JSON::toString(jsonVar, true));

    // 获取压缩效果器的参数
    if (jsonVar["Compressor"].isObject()) {
        params.Compressor_on = 1;
        //     storeEnvWithType("Compressor_on", juce::String(params.Compressor_on), "int");
        if (auto* compressor = jsonVar["Compressor"].getDynamicObject()) {
            if (compressor->hasProperty("Threshold")) {
                params.co_threshold = compressor->getProperty("Threshold");
                storeEnvWithType("co_Threshold", juce::String(params.co_threshold), "double");
            }
            if (compressor->hasProperty("Ratio")) {
                params.co_ratio = compressor->getProperty("Ratio");
                storeEnvWithType("co_Ratio", juce::String(params.co_ratio), "int");
            }
            if (compressor->hasProperty("Attack")) {
                params.co_attack = compressor->getProperty("Attack");
                storeEnvWithType("co_Attack", juce::String(params.co_attack), "double");
            }
            if (compressor->hasProperty("Release")) {
                params.co_release = compressor->getProperty("Release");
                storeEnvWithType("co_Release", juce::String(params.co_release), "double");
            }
            if (compressor->hasProperty("Makeup")) {
                params.co_makeup = compressor->getProperty("Makeup");
                storeEnvWithType("co_Makeup", juce::String(params.co_makeup), "double");
            }
        }
    }
    else {
        params.Compressor_on = 0;
        params.co_threshold = 0;
        params.co_ratio = 0;
        params.co_attack = 0;
        params.co_release = 0;
        params.co_makeup = 0;
        //     storeEnvWithType("Compressor_on", juce::String(params.Compressor_on), "int");
    }

    // 获取失真效果器的参数
    if (jsonVar["Driver"].isObject()) {
        params.Driver_on = 1;
        //      storeEnvWithType("Driver_on", juce::String(params.Driver_on), "int");
        if (auto* distortion = jsonVar["Driver"].getDynamicObject()) {
            if (distortion->hasProperty("Distortion")) {
                params.dr_distortion = distortion->getProperty("Distortion");
                storeEnvWithType("dr_Distortion", juce::String(params.dr_distortion), "double");
            }
            if (distortion->hasProperty("Volume")) {
                params.dr_volume = distortion->getProperty("Volume");
                storeEnvWithType("dr_Volume", juce::String(params.dr_volume), "double");
            }
        }
    }
    else {
        params.Driver_on = 0;
        //    storeEnvWithType("Driver_on", juce::String(params.Driver_on), "int");
        params.dr_distortion = 0;
        params.dr_volume = 0;
    }

    // 获取过载效果器的参数Screamer
    if (jsonVar["Screamer"].isObject()) {
        params.Screamer_on = 1;
        //     storeEnvWithType("Screamer_on", juce::String(params.Screamer_on), "int");
        if (auto* overdrive = jsonVar["Screamer"].getDynamicObject()) {
            if (overdrive->hasProperty("Drive")) {
                params.s_drive = overdrive->getProperty("Drive");
                storeEnvWithType("s_Drive", juce::String(params.s_drive), "double");
            }
            if (overdrive->hasProperty("Tone")) {
                params.s_tone = overdrive->getProperty("Tone");
                storeEnvWithType("s_Tone", juce::String(params.s_tone), "double");
            }
            if (overdrive->hasProperty("Level")) {
                params.s_level = overdrive->getProperty("Level");
                storeEnvWithType("s_Level", juce::String(params.s_level), "double");
            }
        }
    }
    else {
        params.Screamer_on = 0;
        params.s_drive = 0;
        params.s_tone = 0;
        params.s_level = 0;
        //       storeEnvWithType("Screamer_on", juce::String(params.Screamer_on), "int");
    }

    // 获取延迟效果器的参数
    if (jsonVar["Delay"].isObject()) {
        params.Delay_on = 1;
        //    storeEnvWithType("Delay_on", juce::String(params.Delay_on), "int");
        if (auto* delayEffect = jsonVar["Delay"].getDynamicObject()) {
            if (delayEffect->hasProperty("Feedback")) {
                params.de_feedback = delayEffect->getProperty("Feedback");
                storeEnvWithType("de_Feedback", juce::String(params.de_feedback), "double");
            }
            if (delayEffect->hasProperty("Delay")) {
                params.de_delay = delayEffect->getProperty("Delay");
                storeEnvWithType("de_Delay", juce::String(params.de_delay), "double");
            }
            if (delayEffect->hasProperty("Mix")) {
                params.de_mix = delayEffect->getProperty("Mix");
                storeEnvWithType("de_Mix", juce::String(params.de_mix), "double");
            }
        }
    }
    else {
        params.Delay_on = 0;
        params.de_feedback = 0;
        params.de_delay = 0;
        params.de_mix = 0;
        //   storeEnvWithType("Delay_on", juce::String(params.Delay_on), "int");
    }

    // 获取混响效果器的参数

    if (jsonVar["Reverb"].isObject()) {
        params.Reverb_on = 1;
        // storeEnvWithType("Reverb_on", juce::String(params.Reverb_on), "int");
        if (auto* reverb = jsonVar["Reverb"].getDynamicObject()) {
            if (reverb->hasProperty("Size")) {
                params.r_size = reverb->getProperty("Size");
                storeEnvWithType("r_Size", juce::String(params.r_size), "double");
            }
            if (reverb->hasProperty("Damping")) {
                params.r_damping = reverb->getProperty("Damping");
                storeEnvWithType("r_Damping", juce::String(params.r_damping), "double");
            }
            if (reverb->hasProperty("Width")) {
                params.r_width = reverb->getProperty("Width");
                storeEnvWithType("r_Width", juce::String(params.r_width), "double");
            }
            if (reverb->hasProperty("Mix")) {
                params.r_mix = reverb->getProperty("Mix");
                storeEnvWithType("r_Mix", juce::String(params.r_mix), "double");
            }
        }
    }
    else {
        params.Reverb_on = 0;
        params.r_size = 0;
        params.r_damping = 0;
        params.r_width = 0;
        params.r_mix = 0;
        //  storeEnvWithType("Reverb_on", juce::String(params.Reverb_on), "int");
    }

    // 获取合唱效果器的参数，此处逻辑未根据提供的 JSON 数据更新，保留原样
    if (jsonVar["Chorus"].isObject()) {
        params.Chorus_on = 1;
        //   storeEnvWithType("Chorus_on", juce::String(params.Chorus_on), "int");
        if (auto* chorus = jsonVar["Chorus"].getDynamicObject()) {
            if (chorus->hasProperty("Delay")) {
                params.ch_delay = chorus->getProperty("Delay");
                storeEnvWithType("ch_Delay", juce::String(params.ch_delay), "double");
            }
            if (chorus->hasProperty("Depth")) {
                params.ch_depth = chorus->getProperty("Depth");
                storeEnvWithType("ch_Depth", juce::String(params.ch_depth), "double");
            }
            if (chorus->hasProperty("Frequency")) {
                params.ch_frequency = chorus->getProperty("Frequency");
                storeEnvWithType("ch_Frequency", juce::String(params.ch_frequency), "double");
            }
            if (chorus->hasProperty("Width")) {
                params.ch_width = chorus->getProperty("Width");
                storeEnvWithType("ch_Width", juce::String(params.ch_width), "double");
            }
        }
    }
    else {
        params.Chorus_on = 0;
        params.ch_delay = 0;
        params.ch_depth = 0;
        params.ch_frequency = 0;
        params.ch_width = 0;
        //  storeEnvWithType("Chorus_on", juce::String(params.Chorus_on), "int");
    }

    // 获取镶边效果器的参数

    if (jsonVar["Flanger"].isObject()) {
        params.Flanger_on = 1;
        // storeEnvWithType("Flanger_on", juce::String(params.Flanger_on), "int");
        if (auto* flanger = jsonVar["Flanger"].getDynamicObject()) {
            if (flanger->hasProperty("Delay")) {
                params.f_delay = flanger->getProperty("Delay");
                storeEnvWithType("f_Delay", juce::String(params.f_delay), "double");
            }
            if (flanger->hasProperty("Depth")) {
                params.f_depth = flanger->getProperty("Depth");
                storeEnvWithType("f_Depth", juce::String(params.f_depth), "double");
            }
            if (flanger->hasProperty("Feedback")) {
                params.f_feedback = flanger->getProperty("Feedback");
                storeEnvWithType("f_Feedback", juce::String(params.f_feedback), "double");
            }
            if (flanger->hasProperty("Frequency")) {
                params.f_frequency = flanger->getProperty("Frequency");
                storeEnvWithType("f_Frequency", juce::String(params.f_frequency), "double");
            }
            if (flanger->hasProperty("Width")) {
                params.f_width = flanger->getProperty("Width");
                storeEnvWithType("f_Width", juce::String(params.f_width), "double");
            }
        }
    }
    else {
        params.Flanger_on = 0;
        params.f_delay = 0;
        params.f_depth = 0;
        params.f_feedback = 0;
        params.f_frequency = 0;
        params.f_width = 0;
        //   storeEnvWithType("Flanger_on", juce::String(params.Flanger_on), "int");
    }

    // 获取相位效果器的参数

    if (jsonVar["Phaser"].isObject()) {
        params.Phaser_on = 1;
        //  storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "int");
        if (auto* phaser = jsonVar["Phaser"].getDynamicObject()) {
            if (phaser->hasProperty("Depth")) {
                params.p_depth = phaser->getProperty("Depth");
                storeEnvWithType("p_Depth", juce::String(params.p_depth), "double");
            }
            if (phaser->hasProperty("Feedback")) {
                params.p_feedback = phaser->getProperty("Feedback");
                storeEnvWithType("p_Feedback", juce::String(params.p_feedback), "double");
            }
            if (phaser->hasProperty("Frequency")) {
                params.p_frequency = phaser->getProperty("Frequency");
                storeEnvWithType("p_Frequency", juce::String(params.p_frequency), "double");
            }
            if (phaser->hasProperty("Width")) {
                params.p_width = phaser->getProperty("Width");
                storeEnvWithType("p_Width", juce::String(params.p_width), "int");
            }
        }
    }
    else {
        params.Phaser_on = 0;
        params.p_depth = 0;
        params.p_feedback = 0;
        params.p_frequency = 0;
        params.p_width = 0;
        //storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "int");
    }

    // 获取均衡效果器的参数

    if (jsonVar["Equaliser"].isObject()) {
        params.Equaliser_on = 1;
        //  storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "int");
        if (auto* equaliser = jsonVar["Equaliser"].getDynamicObject()) {
            if (equaliser->hasProperty("100hz")) {
                params.e_1 = equaliser->getProperty("100hz");
                storeEnvWithType("e_1", juce::String(params.e_1), "double");
            }
            if (equaliser->hasProperty("200hz")) {
                params.e_2 = equaliser->getProperty("200hz");
                storeEnvWithType("e_2", juce::String(params.e_2), "double");
            }
            if (equaliser->hasProperty("400hz")) {
                params.e_4 = equaliser->getProperty("400hz");
                storeEnvWithType("e_4", juce::String(params.e_4), "double");
            }
            if (equaliser->hasProperty("800hz")) {
                params.e_8 = equaliser->getProperty("800hz");
                storeEnvWithType("e_8", juce::String(params.e_8), "double");
            }
            if (equaliser->hasProperty("1600hz")) {
                params.e_16 = equaliser->getProperty("1600hz");
                storeEnvWithType("e_16", juce::String(params.e_16), "double");
            }
            if (equaliser->hasProperty("3200hz")) {
                params.e_32 = equaliser->getProperty("3200hz");
                storeEnvWithType("e_32", juce::String(params.e_32), "double");
            }
            if (equaliser->hasProperty("6400hz")) {
                params.e_64 = equaliser->getProperty("6400hz");
                storeEnvWithType("e_64", juce::String(params.e_64), "double");
            }
            if (equaliser->hasProperty("Level")) {
                params.e_level = equaliser->getProperty("Level");
                storeEnvWithType("e_Level", juce::String(params.e_level), "double");
            }
        }
    }
    else {
        params.Equaliser_on = 0;
        params.e_1 = 0;
        params.e_2 = 0;
        params.e_4 = 0;
        params.e_8 = 0;
        params.e_16 = 0;
        params.e_32 = 0;
        params.e_64 = 0;
        params.e_level = 0;
        //storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "int");
    }

    // 获取噪声门效果器的参数

    if (jsonVar["NoiseGate"].isObject()) {
        params.NoiseGate_on = 1;
        //  storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "int");
        if (auto* noisegate = jsonVar["NoiseGate"].getDynamicObject()) {
            if (noisegate->hasProperty("NoiseGateThreshold")) {
                params.n_noisegatethreshold = noisegate->getProperty("NoiseGateThreshold");
                storeEnvWithType("p_NoiseGateThreshold", juce::String(params.n_noisegatethreshold), "double");
            }
        }
    }
    else {
        params.NoiseGate_on = 0;
        params.n_noisegatethreshold = 0;
        //storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "int");
    }

    if (params.Compressor_on == 1) {
        bool Compressor_on = true;
        storeEnvWithType("Compressor_on", juce::String(params.Compressor_on), "bool");
    }
    else
    {
        bool Compressor_on = false;
        storeEnvWithType("Compressor_on", juce::String(params.Compressor_on), "bool");
    }
    if (params.Driver_on == 1) {
        bool Driver_on = true;
        storeEnvWithType("Driver_on", juce::String(params.Driver_on), "bool");
    }
    else
    {
        bool Driver_on = false;
        storeEnvWithType("Driver_on", juce::String(params.Driver_on), "bool");
    }
    if (params.Screamer_on == 1) {
        bool Screamer_on = true;
        storeEnvWithType("Screamer_on", juce::String(params.Screamer_on), "bool");
    }
    else
    {
        bool Screamer_on = false;
        storeEnvWithType("Screamer_on", juce::String(params.Screamer_on), "bool");
    }
    if (params.Delay_on == 1) {
        bool Delay_on = true;
        storeEnvWithType("Delay_on", juce::String(params.Delay_on), "bool");
    }
    else
    {
        bool Delay_on = false;
        storeEnvWithType("Delay_on", juce::String(params.Delay_on), "bool");
    }
    if (params.Reverb_on == 1) {
        bool Reverb_on = true;
        storeEnvWithType("Reverb_on", juce::String(params.Reverb_on), "bool");
    }
    else
    {
        bool Reverb_on = false;
        storeEnvWithType("Reverb_on", juce::String(params.Reverb_on), "bool");
    }
    if (params.Chorus_on == 1) {
        bool Chorus_on = true;
        storeEnvWithType("Chorus_on", juce::String(params.Chorus_on), "bool");
    }
    else
    {
        bool Chorus_on = false;
        storeEnvWithType("Chorus_on", juce::String(params.Chorus_on), "bool");
    }
    if (params.Flanger_on == 1) {
        bool Flanger_on = true;
        storeEnvWithType("Flanger_on", juce::String(params.Flanger_on), "bool");
    }
    else
    {
        bool Flanger_on = false;
        storeEnvWithType("Flanger_on", juce::String(params.Flanger_on), "bool");
    }
    if (params.Phaser_on == 1) {
        bool Phaser_on = true;
        storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "bool");
    }
    else
    {
        bool Phaser_on = false;
        storeEnvWithType("Phaser_on", juce::String(params.Phaser_on), "bool");
    }
    if (params.Equaliser_on == 1) {
        bool Equaliser_on = true;
        storeEnvWithType("Equaliser_on", juce::String(params.Equaliser_on), "bool");
    }
    else
    {
        bool Equaliser_on = false;
        storeEnvWithType("Equaliser_on", juce::String(params.Equaliser_on), "bool");
    }
    if (params.NoiseGate_on == 1) {
        bool NoiseGate_on = true;
        storeEnvWithType("NoiseGate_on", juce::String(params.NoiseGate_on), "bool");
    }
    else
    {
        bool NoiseGate_on = false;
        storeEnvWithType("NoiseGate_on", juce::String(params.NoiseGate_on), "bool");
    }

    return params;
}


// 合并多个 JSON 字符串为一个 JSON 对象
juce::var mergeJsonStrings(const juce::StringArray& jsonStrings) {
    juce::var mergedJson = juce::var(new juce::DynamicObject());

    for (const auto& jsonString : jsonStrings) {
        auto jsonVar = juce::JSON::parse(jsonString);
        if (!jsonVar.isVoid()) {
            auto* obj = jsonVar.getDynamicObject();
            if (obj) {
                const auto& properties = obj->getProperties();
                for (int i = 0; i < properties.size(); ++i) {
                    const auto& key = properties.getName(i);
                    mergedJson.getDynamicObject()->setProperty(key, properties.getValueAt(i));
                }
            }
        }
    }

    return mergedJson;
}


// 实现 ChatComponent 类的构造函数
ChatComponent::ChatComponent()
    : juce::Thread("NetworkThread"),  // 初始化网络线程
    sendButton("Send"),
    statusLabel("Status", "Ready")
{
    // 初始化UI组件
    addAndMakeVisible(inputEditor);
    addAndMakeVisible(sendButton);
    addAndMakeVisible(responseEditor);
    addAndMakeVisible(statusLabel);

    sendButton.addListener(this);
    sendButton.setEnabled(true);

    inputEditor.setMultiLine(true);
    responseEditor.setMultiLine(true);
    responseEditor.setReadOnly(true);

    setSize(600, 400);
}

// 实现 ChatComponent 类的 resized 方法
void ChatComponent::resized()
{
    auto area = getLocalBounds().reduced(8);
    auto inputArea = area.removeFromTop(100);
    auto buttonArea = area.removeFromTop(24);
    auto responseArea = area;

    inputEditor.setBounds(inputArea);
    sendButton.setBounds(buttonArea.removeFromRight(80).reduced(2));
    statusLabel.setBounds(buttonArea.reduced(2));
    responseEditor.setBounds(responseArea.reduced(2));
}


void ChatComponent::callAsync(const juce::String& response)
{
    // 使用 callAsync 确保在主线程中更新 UI
    juce::MessageManager::callAsync([this, response]() {
        responseEditor.setText(response, juce::dontSendNotification); // 更新响应内容到 responseEditor
        juce::Logger::writeToLog("Response updated in UI: " + response); // 打印日志
        });
}


// 实现 ChatComponent 类的 buttonClicked 方法
void ChatComponent::buttonClicked(juce::Button* button)
{
    if (button == &sendButton)
    {
        auto message = inputEditor.getText();
        if (message.isNotEmpty())
        {
            userMessageToSend = message; // 保存用户消息
            inputEditor.clear();
            startThread();  // 启动线程
        }
    }
}

// 实现 ChatComponent 类的 run 方法
void ChatComponent::run()
{
    // 获取待发送的用户消息
    auto userMessage = userMessageToSend;
    if (userMessage.isNotEmpty()) {
        juce::Logger::writeToLog("send request: " + userMessage);
    }

    // 构建请求JSON
    juce::var jsonBody = juce::var(new juce::DynamicObject());
    jsonBody.getDynamicObject()->setProperty("bot_id", "7493403625625141311");
    jsonBody.getDynamicObject()->setProperty("user_id", "123");

    juce::var messages = juce::var(juce::Array<juce::var>());
    auto message = juce::var(new juce::DynamicObject());
    message.getDynamicObject()->setProperty("role", "user");
    message.getDynamicObject()->setProperty("content", userMessage);
    message.getDynamicObject()->setProperty("content_type", "text");
    messages.append(message);

    jsonBody.getDynamicObject()->setProperty("additional_messages", messages);
    jsonBody.getDynamicObject()->setProperty("stream", true);

    // 构建请求URL
    juce::URL url(API_ENDPOINT);
    auto jsonStr = juce::JSON::toString(jsonBody, true);
    // 打印请求体
    juce::Logger::writeToLog("send request: " + jsonStr);

    // 构建请求头
    juce::String extraHeaders = "Content-Type: application/json\r\n";
    extraHeaders += "Authorization: Bearer " + COZE_API_KEY + "\r\n";
    extraHeaders += "Accept: application/json\r\n";
    // 打印请求头
    juce::Logger::writeToLog("send requestHeaders: " + extraHeaders);

    int maxRetries = 3;
    int retryCount = 0;

    while (retryCount < maxRetries)
    {
        int statusCode = 0;
        std::unique_ptr<juce::InputStream> stream = url.withPOSTData(jsonStr)
            .createInputStream(juce::URL::InputStreamOptions(juce::URL::ParameterHandling::inPostData)
                .withExtraHeaders(extraHeaders) // 包含请求头
                .withConnectionTimeoutMs(100000)//连接超时时间
                .withResponseHeaders(nullptr)
                .withStatusCode(&statusCode));

        if (stream != nullptr && statusCode == 200)
        {
            auto response = stream->readEntireStreamAsString();
            // 打印 response 内容
            juce::Logger::writeToLog("Received response: " + response);
            handleResponse(response);
            break;
        }
        else
        {
            retryCount++;
            juce::Logger::writeToLog("Request failed with status code: " + juce::String(statusCode) + ". Retrying...");
            juce::Thread::sleep(1000); // 等待 1 秒后重试
        }
    }

    if (retryCount == maxRetries)
    {
        updateStatus("Request failed after multiple attempts");
        juce::Logger::writeToLog("Request failed after multiple attempts");
    }
}

// 实现 ChatComponent 类的 createMessage 方法
juce::var ChatComponent::createMessage(const juce::String& role, const juce::String& content)
{
    auto message = juce::var(new juce::DynamicObject());
    message.getDynamicObject()->setProperty("role", role);
    message.getDynamicObject()->setProperty("content", content);
    return message;
}

// 实现 ChatComponent 类的 handleResponse 方法
void ChatComponent::handleResponse(const juce::String& response)
{
    juce::StringArray lines = juce::StringArray::fromLines(response);
    juce::String fullContent;
    juce::StringArray jsonStrings;

    for (const auto& line : lines)
    {
        if (line.isEmpty()) continue;

        if (line.startsWith("event:")) continue; // 忽略事件行

        if (line.startsWith("data:"))
        {
            auto jsonData = line.substring(5).trim(); // 获取数据部分并去除首尾空格

            if (jsonData == "[DONE]")
            {
                updateStatus("Conversation completed");
                break;
            }

            auto jsonResponse = juce::JSON::parse(jsonData);
            if (jsonResponse.isVoid()) {
                // 无效的 JSON 响应
                juce::Logger::writeToLog("Invalid JSON response: " + jsonData);
                continue; // 跳过无效的 JSON 数据
            }

            if (auto* obj = jsonResponse.getDynamicObject())
            {
                // 检查是否为失败消息
                auto status = obj->getProperty("status").toString();
                if (status == "failed")
                {
                    auto lastError = obj->getProperty("last_error");
                    if (auto* errorObj = lastError.getDynamicObject())
                    {
                        juce::String errorMsg = errorObj->getProperty("msg").toString();
                        updateStatus("Request failed: " + errorMsg);
                        juce::Logger::writeToLog("Request failed: " + errorMsg);
                        return;
                    }
                }

                // 获取回复
                auto role = obj->getProperty("role").toString();
                auto type = obj->getProperty("type").toString();
                if (role == "assistant")
                {
                    auto content = obj->getProperty("content").toString();
                    if (type == "answer")
                    {
                        if (!fullContent.startsWith(content))
                        {
                            fullContent += content;
                        }
                    }
                    else if (type == "follow_up")
                    {
                        if (!fullContent.startsWith(content))
                        {
                            fullContent += "\n\nFollow-up: " + content;
                        }
                    }
                }
            }
        }

    }

    // 提取 fullContent 中的 JSON 代码块
    juce::StringArray jsonBlocks;
    bool inJsonBlock = false;
    juce::String currentJsonBlock;
    for (const auto& line : juce::StringArray::fromLines(fullContent))
    {
        if (line.contains("```json"))
        {
            inJsonBlock = true;
            currentJsonBlock = "";
            continue;
        }
        if (line.contains("```"))
        {
            inJsonBlock = false;
            jsonBlocks.add(currentJsonBlock);
            continue;
        }
        if (inJsonBlock)
        {
            currentJsonBlock += line + "\n";
        }
    }

    // 合并 JSON 字符串
    juce::var mergedJson = mergeJsonStrings(jsonBlocks);
    juce::String mergedJsonStr = juce::JSON::toString(mergedJson, true);



    // 调用提取参数的函数
    EffectParameters params = extractParameters(mergedJsonStr);

    // 调用 callAsync 将响应内容打印到用户界面
    callAsync(params.toString());

    assignCompressorOnValue();
    //mFeedbackSliderPtr->setValue(0.2);
}


// 实现 ChatComponent 类的 updateStatus 方法
void ChatComponent::updateStatus(const juce::String& text)
{
    juce::MessageManager::callAsync(
        [this, text]() { statusLabel.setText(text, juce::dontSendNotification); });
}

// 实现 MainWindow 类的构造函数
MainWindow::MainWindow() : DocumentWindow("DeepSeek Chat",
    juce::Colours::lightgrey,
    DocumentWindow::allButtons)
{
    tabbedComponent = std::make_unique<juce::TabbedComponent>(juce::TabbedButtonBar::TabsAtTop);
    tabbedComponent->addTab("Chat", juce::Colours::lightblue, new ChatComponent(), true);

    setContentOwned(tabbedComponent.get(), true);
    centreWithSize(800, 600);
    setVisible(true);
}

// 实现 MainWindow 类的 closeButtonPressed 方法
void MainWindow::closeButtonPressed()
{
    // 确认关闭应用程序
    juce::JUCEApplication::quit();
}

// 实现 DeepSeekChatApp 类的 getApplicationName 方法
const juce::String DeepSeekChatApp::getApplicationName()
{
    return "DeepSeekChat";
}

// 实现 DeepSeekChatApp 类的 getApplicationVersion 方法
const juce::String DeepSeekChatApp::getApplicationVersion()
{
    return "1.0.0";
}

// 实现 DeepSeekChatApp 类的 initialise 方法
void DeepSeekChatApp::initialise(const juce::String&)
{
    mainWindow.reset(new MainWindow());
}

// 实现 DeepSeekChatApp 类的 shutdown 方法
void DeepSeekChatApp::shutdown()
{
    mainWindow = nullptr;
}