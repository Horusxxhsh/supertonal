#pragma once
#include <JuceHeader.h>
#include <iostream>

// 打印提取的参数到日志
//juce::Logger::writeToLog("Extracted Parameters:");
//juce::Logger::writeToLog("Compressor_on: " + juce::String(params.Compressor_on));
//juce::Logger::writeToLog("Driver_on: " + juce::String(params.Driver_on));
//juce::Logger::writeToLog("Screamer_on: " + juce::String(params.Screamer_on));
//juce::Logger::writeToLog("Delay_on: " + juce::String(params.Delay_on));
//juce::Logger::writeToLog("Reverb_on: " + juce::String(params.Reverb_on));
//juce::Logger::writeToLog("Chorus_on: " + juce::String(params.Chorus_on));
//juce::Logger::writeToLog("Ratio: " + juce::String(params.ratio));
//juce::Logger::writeToLog("Attack: " + juce::String(params.attack));
//juce::Logger::writeToLog("Release: " + juce::String(params.release));
//juce::Logger::writeToLog("Makeup: " + juce::String(params.makeup));
//juce::Logger::writeToLog("Distortion: " + juce::String(params.distortion));
//juce::Logger::writeToLog("Volume: " + juce::String(params.volume));
//juce::Logger::writeToLog("Drive: " + juce::String(params.drive));
//juce::Logger::writeToLog("Tone: " + juce::String(params.tone));
//juce::Logger::writeToLog("Level: " + juce::String(params.level));
//juce::Logger::writeToLog("Feedback: " + juce::String(params.feedback));
//juce::Logger::writeToLog("Delay: " + juce::String(params.delay));
//juce::Logger::writeToLog("Mix: " + juce::String(params.mix));
//juce::Logger::writeToLog("Size: " + juce::String(params.size));
//juce::Logger::writeToLog("Damping: " + juce::String(params.damping));
//juce::Logger::writeToLog("Width: " + juce::String(params.width));
//juce::Logger::writeToLog("Depth: " + juce::String(params.depth));
//juce::Logger::writeToLog("Frequency: " + juce::String(params.frequency));




// Coze API密钥
static const juce::String COZE_API_KEY = "pat_VM15JCu2LTk4Hci8PB4QFX7vHy2gXEgheHo03tFvARi8e2r8gC5KcCbjKJURd73F"; // 替换为你的Coze API密钥
static const juce::String API_ENDPOINT = "https://api.coze.cn/v3/chat"; // Coze API端点
static const juce::String RESULT_ENDPOINT = "https://api.coze.cn/v3/chat/result"; // 结果查询API端点

// 定义效果参数结构体
struct EffectParameters {
    int Compressor_on;//初始值（另）
    int Driver_on;//完成DelayComponent
    int Screamer_on;//初始值（另）
    int Delay_on;//完成DelayComponent
    int Reverb_on;//初始值（另）
    int Chorus_on;//初始值（另）
    int Flanger_on;//初始值（另）
    int Phaser_on;//初始值（另）
    int Equaliser_on;
    int NoiseGate_on;
    double co_mix;
    double co_threshold;//初始值PluginAudioProcessor
    int co_ratio;//初始值PluginAudioProcessor
    double co_attack;//初始值PluginAudioProcessor
    double co_release;//初始值PluginAudioProcessor
    double co_makeup;
    double dr_distortion;//初始值PluginAudioProcessor
    double dr_volume;//初始值PluginAudioProcessor
    double s_drive; //初始值PluginAudioProcessor
    double s_tone;//初始值PluginAudioProcessor
    double s_level;//初始值PluginAudioProcessor
    double de_feedback;//完成DelayComponent
    double de_delay;//完成DelayComponent
    double de_mix;//完成DelayComponent
    double r_size;//初始值PluginAudioProcessor
    double r_damping;//初始值PluginAudioProcessor
    double r_width; //初始值PluginAudioProcessor
    double r_mix;//初始值PluginAudioProcessor
    double ch_delay;//初始值PluginAudioProcessor
    double ch_depth;//初始值PluginAudioProcessor
    double ch_frequency;//初始值PluginAudioProcessor
    double ch_width;//初始值PluginAudioProcessor
    double f_delay;//初始值PluginAudioProcessor
    double f_depth;//初始值PluginAudioProcessor
    double f_feedback;//初始值PluginAudioProcessor
    double f_frequency;//初始值PluginAudioProcessor
    double f_width;//初始值PluginAudioProcessor
    double p_depth;//初始值PluginAudioProcessor
    double p_feedback;//初始值PluginAudioProcessor
    double p_frequency;//初始值PluginAudioProcessor
    double p_width;//初始值PluginAudioProcessor
    double e_1;//初始值PluginAudioProcessor
    double e_2;//初始值PluginAudioProcessor
    double e_4;//初始值PluginAudioProcessor
    double e_8;//初始值PluginAudioProcessor
    double e_16;//初始值PluginAudioProcessor
    double e_32;//初始值PluginAudioProcessor
    double e_64;//初始值PluginAudioProcessor
    double e_level;//初始值PluginAudioProcessor
    double n_noisegatethreshold;//初始值PluginAudioProcessor
    // 添加 toString 方法
    juce::String toString() const {
        return juce::String("Compressor_on: ") + juce::String(Compressor_on) + "\n" +
            "Driver_on: " + juce::String(Driver_on) + "\n" +
            "Screamer_on: " + juce::String(Screamer_on) + "\n" +
            "Delay_on: " + juce::String(Delay_on) + "\n" +
            "Reverb_on: " + juce::String(Reverb_on) + "\n" +
            "Chorus_on: " + juce::String(Chorus_on) + "\n" +
            "Flanger_on: " + juce::String(Flanger_on) + "\n" +
            "Phaser_on: " + juce::String(Phaser_on) + "\n" +
            "Equaliser_on: " + juce::String(Equaliser_on) + "\n" +
            "NoiseGate_on: " + juce::String(NoiseGate_on) + "\n" +
            "co_threshold" + juce::String(co_threshold) + "\n" +
            "co_ratio: " + juce::String(co_ratio) + "\n" +
            "co_attack: " + juce::String(co_attack) + "\n" +
            "co_release: " + juce::String(co_release) + "\n" +
            "co_makeup: " + juce::String(co_makeup) + "\n" +
            "co_mix: " + juce::String(co_mix) + "\n" +
            "dr_distortion: " + juce::String(dr_distortion) + "\n" +
            "dr_volume: " + juce::String(dr_volume) + "\n" +
            "s_drive: " + juce::String(s_drive) + "\n" +
            "s_tone: " + juce::String(s_tone) + "\n" +
            "s_level: " + juce::String(s_level) + "\n" +
            "de_feedback: " + juce::String(de_feedback) + "\n" +
            "de_delay: " + juce::String(de_delay) + "\n" +
            "de_mix: " + juce::String(de_mix) + "\n" +
            "r_size: " + juce::String(r_size) + "\n" +
            "r_damping: " + juce::String(r_damping) + "\n" +
            "r_width: " + juce::String(r_width) + "\n" +
            "r_mix: " + juce::String(r_mix) + "\n" +
            "ch_delay: " + juce::String(ch_delay) + "\n" +
            "ch_depth: " + juce::String(ch_depth) + "\n" +
            "ch_frequency: " + juce::String(ch_frequency) + "\n" +
            "ch_width: " + juce::String(ch_width) + "\n" +
            "f_delay: " + juce::String(f_delay) + "\n" +
            "f_depth: " + juce::String(f_depth) + "\n" +
            "f_feedback: " + juce::String(f_feedback) + "\n" +
            "f_frequency: " + juce::String(f_frequency) + "\n" +
            "f_width: " + juce::String(f_width) + "\n" +
            "p_depth: " + juce::String(p_depth) + "\n" +
            "p_feedback: " + juce::String(p_feedback) + "\n" +
            "p_frequency: " + juce::String(p_frequency) + "\n" +
            "p_width: " + juce::String(p_width) + "\n" +
            "e_1: " + juce::String(e_1) + "\n" +
            "e_2: " + juce::String(e_2) + "\n" +
            "e_4: " + juce::String(e_4) + "\n" +
            "e_8: " + juce::String(e_8) + "\n" +
            "e_16: " + juce::String(e_16) + "\n" +
            "e_32: " + juce::String(e_32) + "\n" +
            "e_64: " + juce::String(e_64) + "\n" +
            "e_level: " + juce::String(e_level) + "\n" +
            "n_noisegatethreshold: " + juce::String(n_noisegatethreshold) + "\n";
    }
};

// 聊天组件
class ChatComponent : public juce::Component,
    public juce::Button::Listener,
    private juce::Thread
{
public:
    ChatComponent();
    void resized() override;
    void buttonClicked(juce::Button* button) override;
private:
    juce::TextEditor inputEditor;
    juce::TextButton sendButton;
    juce::TextEditor responseEditor;
    juce::Label statusLabel;
    juce::String userMessageToSend; // 待发送的用户消息

    void run() override;
    juce::var createMessage(const juce::String& role, const juce::String& content);
    void handleResponse(const juce::String& response);
    void updateStatus(const juce::String& text);
    void callAsync(const juce::String& response);
};

// 主窗口
class MainWindow : public juce::DocumentWindow
{
public:
    MainWindow();
    void closeButtonPressed() override;

private:
    std::unique_ptr<juce::TabbedComponent> tabbedComponent;
};

// 应用程序类
class DeepSeekChatApp : public juce::JUCEApplication
{
public:
    DeepSeekChatApp() = default;
    const juce::String getApplicationName() override;
    const juce::String getApplicationVersion() override;
    void initialise(const juce::String&) override;
    void shutdown() override;

private:
    std::unique_ptr<MainWindow> mainWindow;
};





