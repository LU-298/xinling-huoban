"""
心灵伙伴 - 治愈系数字人 🌱
接入AI大模型的智能版本
"""
import streamlit as st
import random
import time
import os

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# 情绪关键词（用于检测用户情绪）
EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻", "好开心"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "疲惫", "心碎", "悲伤", "郁闷", "不开心"],
    "stressed": ["压力", "焦虑", "紧张", "害怕", "担心", "恐惧", "不安", "烦恼"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "疑问"],
    "love": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动"],
    "angry": ["生气", "愤怒", "讨厌", "烦", "气死了", "怒"],
    "tired": ["累", "困", "疲惫", "疲倦", "没劲", "无力"],
    "grateful": ["感谢", "谢谢", "感恩", "感激"],
    "lonely": ["孤独", "寂寞", "孤单", "无聊", "一个人"]
}

def detect_emotion(text):
    """检测用户情绪"""
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "neutral"

def get_emotion_emoji(emotion):
    """获取情绪表情"""
    emojis = {
        "happy": "😊",
        "sad": "😢",
        "stressed": "😰",
        "confused": "🤔",
        "love": "🥰",
        "angry": "😤",
        "tired": "😴",
        "grateful": "🙏",
        "lonely": "🥺",
        "neutral": "🤗"
    }
    return emojis.get(emotion, "🤗")

# 尝试导入Coze API
try:
    from openai import OpenAI
    COZE_AVAILABLE = True
except ImportError:
    COZE_AVAILABLE = False

def get_ai_response(user_message, emotion):
    """获取AI回复"""
    # 获取Coze API配置
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")
    
    if not api_key or not base_url:
        # 如果没有配置，使用预设回复
        fallback_responses = {
            "happy": ["太棒了！保持好心情很重要哦！🌟", "听起来很棒！💪", "开心是最好的礼物！🎁"],
            "sad": ["别难过，我一直在这里陪着你。🤗", "深呼吸，一切都会好起来的。🌈", "我陪着你。💝"],
            "stressed": ["深呼吸，慢慢来，一切都会好的。🌿", "休息一下也很重要哦。☕"],
            "confused": ["有困惑是正常的，慢慢想。💭", "换个角度想想？🔄"],
            "love": ["谢谢你的信任！💕", "能感受到你的温暖呢！🌸"],
            "angry": ["深呼吸，冷静一下。😤➡️😌", "生气是正常的，但要照顾好自己哦。💗"],
            "tired": ["累了就休息一下，不要太勉强自己。😴", "休息是为了走更远的路。🌙"],
            "grateful": ["不客气！能帮到你我也很开心 😊", "谢谢你！🌸"],
            "lonely": ["你不是一个人，我在这里陪着你。🤝", "我们现在在一起聊天呀！💕"],
            "neutral": ["嗯嗯，我听着呢。😊", "谢谢你愿意分享。💕", "我理解你的感受。🤝", "慢慢说，我在这里。🌱"]
        }
        responses = fallback_responses.get(emotion, fallback_responses["neutral"])
        return random.choice(responses), emotion
    
    try:
        # 使用Coze API
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # 构建系统提示词
        system_prompt = f"""你是一个温暖治愈系AI数字人，名字叫"心灵伙伴"。
你的特点是：
1. 温暖、善良、有同理心
2. 善于倾听，能感知用户情绪
3. 回复简短温馨，像朋友聊天
4. 会用emoji增加亲切感
5. 用户当前情绪：{emotion}

请用温暖的方式回复用户说的话，保持简短（50字以内），像朋友聊天一样。"""
        
        response = client.chat.completions.create(
            model="doubao-seed-1-6-251015",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200,
            temperature=0.8
        )
        
        ai_reply = response.choices[0].message.content
        return ai_reply, emotion
        
    except Exception as e:
        # 如果API调用失败，使用预设回复
        fallback_responses = {
            "happy": ["太棒了！🌟", "听起来很棒！💪"],
            "sad": ["别难过，我陪着你。🤗", "深呼吸，一切都会好的。🌈"],
            "stressed": ["深呼吸，慢慢来。🌿"],
            "neutral": ["嗯嗯，我听着呢。😊", "我理解你的感受。🤝"]
        }
        responses = fallback_responses.get(emotion, fallback_responses["neutral"])
        return random.choice(responses), emotion

# CSS样式
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #e8f5e9, #c8e6c9, #a5d6a7); }
h1 { color: #2e7d32 !important; text-align: center; }
.stButton > button { background: #4CAF50; color: white; border-radius: 20px; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 治愈系心理健康AI数字人（智能版）")

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我可以陪你聊天、倾听你的心事、给你温暖和鼓励。\n\n有什么想和我聊聊的吗？😊"}
    ]
    st.session_state.current_emotion = "neutral"

# 两列布局
col1, col2 = st.columns([1, 2])

with col1:
    emotion = st.session_state.current_emotion
    emoji = get_emotion_emoji(emotion)
    
    st.markdown(f"""
    ### 🤖 数字人展示
    
    <div style="background:white; padding:30px; border-radius:20px; text-align:center; box-shadow:0 5px 20px rgba(0,0,0,0.1);">
        <!-- 头部 -->
        <div style="width:150px; height:170px; background:linear-gradient(145deg,#f5f5f5,#d0d0d0); border-radius:75px; margin:0 auto; position:relative;">
            <!-- 眼镜 -->
            <div style="position:absolute; top:50px; left:50%; transform:translateX(-50%); display:flex; gap:10px;">
                <div style="width:45px; height:35px; border:4px solid #333; border-radius:8px;"></div>
                <div style="width:45px; height:35px; border:4px solid #333; border-radius:8px;"></div>
            </div>
            <!-- 眼睛 -->
            <div style="position:absolute; top:55px; left:50%; transform:translateX(-50%); display:flex; gap:15px;">
                <div style="width:25px; height:25px; background:#333; border-radius:50%;"></div>
                <div style="width:25px; height:25px; background:#333; border-radius:50%;"></div>
            </div>
            <!-- 嘴巴 -->
            <div style="position:absolute; top:100px; left:50%; transform:translateX(-50%);">
                <svg width="50" height="25" viewBox="0 0 50 25">
                    <path d="M 5 10 Q 25 20 45 10" stroke="#333" stroke-width="3" fill="none"/>
                </svg>
            </div>
        </div>
        <!-- 身体 -->
        <div style="width:140px; height:60px; background:linear-gradient(145deg,#f5f5f5,#c0c0c0); border-radius:30px; margin:-10px auto 0; position:relative;">
            <div style="position:absolute; top:10px; left:50%; transform:translateX(-50%); width:40px; height:40px; background:radial-gradient(circle,#4CAF50,#2E7D32); border-radius:50%; animation:breath 3s infinite;"></div>
        </div>
        <style>@keyframes breath{{0%,100%{{transform:translateX(-50%) scale(1)}}50%{{transform:translateX(-50%) scale(1.2)}}}}</style>
        <div style="margin-top:20px; padding:10px; background:#e8f5e9; border-radius:10px;">
            {emoji} 情绪感知
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    **💡 功能说明：**
    - 💬 智能对话
    - 😊 情绪感知
    - 🌈 温暖陪伴
    - 💡 建议分享
    """)

with col2:
    st.markdown("### 💬 对话")
    
    # 显示消息
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"<div style='background:#4CAF50; color:white; padding:15px; border-radius:15px; margin:10px 0; max-width:85%; margin-left:auto;'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:white; padding:15px; border-radius:15px; margin:10px 0; max-width:85%; box-shadow:0 2px 10px rgba(0,0,0,0.1); white-space:pre-wrap;'>{msg['content']}</div>", unsafe_allow_html=True)
    
    # 输入框
    user_input = st.text_input("输入消息...", placeholder="说点什么吧...", label_visibility="collapsed", key="input")
    
    col_send, col_clear = st.columns([1, 1])
    
    with col_send:
        if st.button("🚀 发送", use_container_width=True):
            if user_input:
                # 添加用户消息
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # 检测情绪
                emotion = detect_emotion(user_input)
                st.session_state.current_emotion = emotion
                
                # 显示思考中
                with st.spinner("🤔 思考中..."):
                    time.sleep(0.3)
                    # 获取AI回复
                    response, _ = get_ai_response(user_input, emotion)
                
                # 添加bot回复
                st.session_state.messages.append({"role": "bot", "content": response})
                
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = [
                {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我可以陪你聊天、倾听你的心事、给你温暖和鼓励。\n\n有什么想和我聊聊的吗？😊"}
            ]
            st.session_state.current_emotion = "neutral"
            st.rerun()

# 底部
st.markdown("---")
st.markdown("*💚 记住，你并不孤单。我一直在这里陪着你。*")

