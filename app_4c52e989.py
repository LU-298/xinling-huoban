"""
心灵伙伴 - 治愈系数字人 🌱
接入DeepSeek大模型 - 超级智能版
"""
import streamlit as st
import time
import os

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

def get_deepseek_response(user_message, emotion):
    """获取DeepSeek智能回复"""
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        
        # 系统提示词
        system_prompt = f"""你是"心灵伙伴"，一个温暖、专业、富有同理心的AI心理健康陪伴助手。

【你的特点】
- 温暖善良，像知心朋友一样聊天
- 善于倾听，能感知用户的情绪变化
- 回复简短温馨，30-80字左右
- 会用emoji增加亲切感
- 必要时给出实用的心理建议

【用户当前情绪】
{emotion}

【注意事项】
- 不要说教，像朋友聊天一样自然
- 如果用户有心理困扰，引导他们寻求专业帮助
- 保持积极乐观，但也要理解用户的真实感受
- 回复要简洁自然，像真人聊天

请用温暖的方式回复。"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.85
        )
        return response.choices[0].message.content, True
        
    except Exception as e:
        return f"抱歉，现在连接有点问题。💭 也许是网络原因，再试一次好吗？", False

# 情绪检测
EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻", "好开心", "兴奋", "激动", "棒极了"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "疲惫", "心碎", "悲伤", "郁闷", "不开心", "沮丧", "失落"],
    "stressed": ["压力", "焦虑", "紧张", "害怕", "担心", "恐惧", "不安", "烦恼", "崩溃", "烦躁"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "疑问", "搞不懂", "糊涂"],
    "love": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动", "甜蜜"],
    "angry": ["生气", "愤怒", "讨厌", "烦", "气死了", "怒", "火大", "不爽"],
    "tired": ["累", "困", "疲惫", "疲倦", "没劲", "无力", "精神不振"],
    "grateful": ["感谢", "谢谢", "感恩", "感激", "多谢"],
    "lonely": ["孤独", "寂寞", "孤单", "无聊", "一个人", "没人陪"],
    "hopeful": ["希望", "期待", "憧憬", "梦想", "加油", "努力", "未来"]
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "neutral"

def get_emotion_emoji(emotion):
    emojis = {
        "happy": "😊", "sad": "😢", "stressed": "😰", "confused": "🤔",
        "love": "🥰", "angry": "😤", "tired": "😴", "grateful": "🙏",
        "lonely": "🥺", "hopeful": "🌅", "neutral": "🤗"
    }
    return emojis.get(emotion, "🤗")

def get_emotion_name(emotion):
    names = {
        "happy": "开心", "sad": "难过", "stressed": "焦虑", "confused": "困惑",
        "love": "温暖", "angry": "生气", "tired": "疲惫", "grateful": "感恩",
        "lonely": "孤独", "hopeful": "期待", "neutral": "平静"
    }
    return names.get(emotion, "平静")

# CSS
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #e8f5e9, #c8e6c9, #a5d6a7); }
h1 { color: #2e7d32 !important; text-align: center; font-size: 2.5em !important; }
.stButton > button { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-radius: 25px; font-size: 16px; padding: 10px 20px; border: none; }
.stButton > button:hover { background: linear-gradient(135deg, #45a049, #3d8b40); }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 💚 DeepSeek智能增强版")

st.success("✅ DeepSeek API已连接 - 使用DeepSeek大模型")

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我接入了DeepSeek超级AI大脑，现在可以：\n• 像真人一样聊天 💬\n• 回答各种问题 📚\n• 陪你倾诉心事 💕\n• 感知你的情绪 😊\n• 给你温暖的回应 🌈\n\n有什么想和我聊聊的吗？"}
    ]
    st.session_state.current_emotion = "neutral"

# 布局
col1, col2 = st.columns([1, 2])

with col1:
    emoji = get_emotion_emoji(st.session_state.current_emotion)
    emotion_name = get_emotion_name(st.session_state.current_emotion)
    st.markdown(f"""
    ### 🤖 数字人
    
    <div style="background:white; padding:25px; border-radius:25px; text-align:center; box-shadow:0 8px 30px rgba(0,0,0,0.1);">
        <div style="width:140px; height:160px; background:linear-gradient(145deg,#f5f5f5,#d0d0d0); border-radius:70px; margin:0 auto; position:relative;">
            <div style="position:absolute; top:45px; left:50%; transform:translateX(-50%); display:flex; gap:8px;">
                <div style="width:42px; height:32px; border:4px solid #333; border-radius:8px;"></div>
                <div style="width:42px; height:32px; border:4px solid #333; border-radius:8px;"></div>
            </div>
            <div style="position:absolute; top:50px; left:50%; transform:translateX(-50%); display:flex; gap:12px;">
                <div style="width:24px; height:24px; background:#333; border-radius:50%;"></div>
                <div style="width:24px; height:24px; background:#333; border-radius:50%;"></div>
            </div>
            <div style="position:absolute; top:95px; left:50%; transform:translateX(-50%);">
                <svg width="45" height="22" viewBox="0 0 45 22">
                    <path d="M 3 8 Q 22 20 41 8" stroke="#333" stroke-width="3" fill="none" stroke-linecap="round"/>
                </svg>
            </div>
        </div>
        <div style="width:130px; height:55px; background:linear-gradient(145deg,#f5f5f5,#c0c0c0); border-radius:28px; margin:-12px auto 0; position:relative;">
            <div style="position:absolute; top:8px; left:50%; transform:translateX(-50%); width:38px; height:38px; background:radial-gradient(circle,#4CAF50,#2E7D32); border-radius:50%; animation:breath 3s infinite;"></div>
        </div>
        <style>@keyframes breath{{0%,100%{{transform:translateX(-50%) scale(1)}}50%{{transform:translateX(-50%) scale(1.15)}}}}</style>
        <div style="margin-top:18px; padding:12px; background:linear-gradient(135deg,#e8f5e9,#c8e6c9); border-radius:12px; font-size:16px;">
            {emoji} {emotion_name}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    **✨ 超级能力：**
    - 🧠 DeepSeek AI大脑
    - 💬 智能对话
    - 😊 情绪感知  
    - 💡 暖心建议
    """)

with col2:
    st.markdown("### 💬 对话")
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='background:#4CAF50; color:white; padding:15px; border-radius:15px; margin:10px 0; max-width:85%; margin-left:auto;'>👤 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:white; padding:15px; border-radius:15px; margin:10px 0; max-width:85%; box-shadow:0 3px 15px rgba(0,0,0,0.1); white-space:pre-wrap;'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
    
    user_input = st.text_input("输入消息...", placeholder="说点什么吧...", label_visibility="collapsed")
    
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        if st.button("🚀 发送", use_container_width=True):
            if user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                emotion = detect_emotion(user_input)
                st.session_state.current_emotion = emotion
                
                with st.spinner("🤔 DeepSeek思考中..."):
                    response, success = get_deepseek_response(user_input, emotion)
                
                st.session_state.messages.append({"role": "bot", "content": response})
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = [
                {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我接入了DeepSeek超级AI大脑，可以像真人一样和你聊天！\n\n有什么想和我聊聊的吗？😊"}
            ]
            st.session_state.current_emotion = "neutral"
            st.rerun()

st.markdown("---")
st.markdown("*💚 记住，你并不孤单。我一直在这里陪着你。*")
