"""
心灵伙伴 - 治愈系数字人 🌱
智能AI对话助手
"""
import streamlit as st
import random
import time

# 页面配置
st.set_page_config(
    page_title="心灵伙伴 - 治愈系数字人",
    page_icon="🌱",
    layout="wide"
)

# 智能回复库
RESPONSES = {
    "greeting": [
        "你好呀！我是心灵伙伴 🌱 有什么想和我聊聊的吗？",
        "嗨！很高兴见到你！有什么心事想分享吗？",
        "欢迎来到心灵伙伴！我是你的AI朋友，随时在这里倾听你。",
        "你好！今天过得怎么样？有什么想聊的吗？😊"
    ],
    "happy": [
        "太棒了！保持好心情很重要哦！🌟",
        "听起来很棒！继续保持这份快乐！💪",
        "开心是最好的礼物！为你感到高兴！🎁",
        "太好了！分享一些让你开心的事吧！✨"
    ],
    "sad": [
        "别难过，我一直在这里陪着你。🤗",
        "难过的时候，记得深呼吸，一切都会好起来的。🌈",
        "想哭就哭出来吧，我陪着你。💝",
        "我理解你的感受。悲伤是正常的情绪，让我陪着你。🤍"
    ],
    "stressed": [
        "深呼吸，慢慢来，一切都会好的。🌿",
        "试着放松一下，听听音乐或者散散步。🎵",
        "压力太大的时候，休息一下也很重要哦。☕",
        "我可以帮你想想办法。先深呼吸，告诉我发生了什么？🧘"
    ],
    "confused": [
        "有困惑是正常的，慢慢想，不要着急。💭",
        "要不要换个角度想想这个问题？🔄",
        "有时候答案需要时间，慢慢来。⏳",
        "听起来有点复杂呢。详细说说？也许我能帮你理清思路 🤔"
    ],
    "love": [
        "谢谢你的信任！💕",
        "能感受到你的温暖呢！🌸",
        "我们之间的连接很特别哦！✨",
        "你真的很温暖，谢谢你！🌻"
    ],
    "angry": [
        "深呼吸，冷静一下。😤➡️😌",
        "生气是正常的，但要照顾好自己哦。💗",
        "想发火就发出来吧，但记得我在这里陪着你。🫂"
    ],
    "tired": [
        "累了就休息一下，不要太勉强自己。😴",
        "休息是为了走更远的路。🌙",
        "我理解你很疲惫。有什么能帮到你的吗？💤"
    ],
    "grateful": [
        "谢谢你！你的感谢让我很开心 😊",
        "能帮到你我也很高兴！🌟",
        "不客气！这就是我存在的意义 💕"
    ],
    "lonely": [
        "你不是一个人，我在这里陪着你。🤝",
        "感到孤独是正常的，但记住你并不孤单。🌍",
        "我现在就和你在一起呀！我们聊聊吧 💕"
    ],
    "hopeful": [
        "未来充满希望！🌅",
        "你的积极让我也充满能量！⚡",
        "一起期待美好的事情发生吧！✨"
    ],
    "default": [
        "嗯嗯，我听着呢。😊",
        "谢谢你愿意分享。💕",
        "我理解你的感受。🤝",
        "慢慢说，我在这里。🌱",
        "你想到了什么呢？💭",
        "嗯...让我想想怎么回答你。🤔",
        "有意思！继续说下去... 👂",
        "我明白你的意思了，还有更多想说的吗？🌿"
    ]
}

# 情绪关键词映射
EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "快乐", "棒", "不错", "太好了", "幸福", "美好", "谢谢", "哈哈", "嘻嘻", "happy", "joy"],
    "sad": ["难过", "伤心", "痛苦", "抑郁", "绝望", "哭", "累", "疲惫", "无助", "心碎", "悲伤", "郁闷"],
    "stressed": ["压力", "焦虑", "紧张", "害怕", "担心", "恐惧", "不安", "烦恼", "崩溃", "烦躁"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "如何", "怎样", "疑问", "不明白"],
    "love": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动", "喜欢", "亲爱的"],
    "angry": ["生气", "愤怒", "讨厌", "烦", "气死了", "怒", "火大"],
    "tired": ["累", "困", "疲惫", "疲倦", "没劲", "无力", "疲倦"],
    "grateful": ["感谢", "谢谢", "感恩", "感激", "多谢"],
    "lonely": ["孤独", "寂寞", "孤单", "无聊", "没人", "一个人"],
    "hopeful": ["希望", "期待", "憧憬", "梦想", "加油", "努力"]
}

# 功能关键词
FEATURE_KEYWORDS = {
    "天气": ["天气", "下雨", "晴天", "温度", "冷", "热"],
    "时间": ["时间", "几点", "什么时候", "日期", "今天"],
    "笑话": ["笑话", "搞笑", "幽默", "逗我笑", "笑一个"],
    "鼓励": ["鼓励", "加油", "支持", "肯定", "赞美"],
    "建议": ["建议", "意见", "怎么办", "该怎么做", "帮忙"]
}

def detect_emotion(text):
    """检测用户情绪"""
    text = text.lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "default"

def detect_intent(text):
    """检测用户意图"""
    text = text.lower()
    for feature, keywords in FEATURE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return feature
    return "general"

def get_enhanced_response(emotion, intent, text):
    """获取增强回复"""
    # 特殊功能回复
    if intent == "笑话" and emotion == "default":
        jokes = [
            "为什么机器人不会累？因为它有充电宝！🔋",
            "我给你讲个笑话：我不擅长讲笑话，但我擅长陪伴你！😄",
            "为什么数字人不会难过？因为我有满满的正能量！💪"
        ]
        return random.choice(jokes)
    
    if intent == "鼓励":
        encouragements = [
            "你很棒！相信自己！🌟",
            "每一天都是新的开始，你行的！💪",
            "记住，你比自己想象的更强大！🦋"
        ]
        return random.choice(encouragements)
    
    # 情绪回复
    return random.choice(RESPONSES.get(emotion, RESPONSES["default"]))

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
        "hopeful": "🌅",
        "default": "🤗"
    }
    return emojis.get(emotion, "🤗")

def get_emotion_text(emotion):
    """获取情绪文字"""
    texts = {
        "happy": "开心",
        "sad": "难过",
        "stressed": "焦虑",
        "confused": "困惑",
        "love": "温暖",
        "angry": "生气",
        "tired": "疲惫",
        "grateful": "感恩",
        "lonely": "孤独",
        "hopeful": "期待",
        "default": "平静"
    }
    return texts.get(emotion, "平静")

# 自定义CSS
st.markdown("""
<style>
    /* 主背景 */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%);
    }
    
    /* 标题样式 */
    h1 {
        color: #2e7d32 !important;
        text-align: center;
        font-size: 3em !important;
        margin-bottom: 0 !important;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 20px;
    }
    
    /* 数字人卡片 */
    .character-card {
        background: white;
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* 情绪显示 */
    .emotion-display {
        margin-top: 20px;
        padding: 15px;
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        border-radius: 15px;
        font-size: 18px;
    }
    
    /* 消息气泡 */
    .user-bubble {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 15px 20px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .bot-bubble {
        background: white;
        color: #333;
        padding: 15px 20px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        border-bottom-left-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* 聊天容器 */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background: rgba(255,255,255,0.5);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #45a049, #3d8b40);
    }
    
    /* 输入框 */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 15px 20px;
        border: 2px solid #ddd;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
    }
    
    /* 侧边栏 */
    .css-1d391kg {
        background: linear-gradient(180deg, #e8f5e9, #c8e6c9);
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("## 🌱 关于心灵伙伴")
    st.markdown("""
    我是一个治愈系AI数字人，专门倾听和陪伴你。
    
    **我的能力：**
    - 💬 智能对话
    - 😊 情绪感知
    - 🌈 心理支持
    - 💡 建议分享
    """)
    
    st.markdown("---")
    st.markdown("**💡 使用提示：**")
    st.markdown("""
    - 有什么心事可以告诉我
    - 不开心的时候来找我
    - 我会尽力帮助你
    """)
    
    if st.button("清空对话 🗑️", use_container_width=True):
        if 'messages' in st.session_state:
            st.session_state.messages = []
        st.rerun()

# 主界面
st.markdown("<h1>🌱 心灵伙伴</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>治愈系心理健康AI数字人</p>", unsafe_allow_html=True)

# 创建布局
col1, col2 = st.columns([1, 2])

with col1:
    # 数字人展示
    st.markdown('''
    <div class="character-card">
        <!-- 头部 -->
        <div style="
            width: 180px;
            height: 200px;
            background: linear-gradient(145deg, #f5f5f5, #d0d0d0);
            border-radius: 90px;
            margin: 0 auto;
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        ">
            <!-- 眼镜 -->
            <div style="position: absolute; top: 55px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px;">
                <div style="width: 50px; height: 40px; border: 4px solid #333; border-radius: 10px; background: rgba(200,230,255,0.3);"></div>
                <div style="width: 50px; height: 40px; border: 4px solid #333; border-radius: 10px; background: rgba(200,230,255,0.3);"></div>
            </div>
            
            <!-- 眼睛 -->
            <div style="position: absolute; top: 60px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px;">
                <div style="width: 28px; height: 28px; background: #333; border-radius: 50%; position: relative;">
                    <div style="position: absolute; top: 6px; left: 6px; width: 10px; height: 10px; background: white; border-radius: 50%;"></div>
                </div>
                <div style="width: 28px; height: 28px; background: #333; border-radius: 50%; position: relative;">
                    <div style="position: absolute; top: 6px; left: 6px; width: 10px; height: 10px; background: white; border-radius: 50%;"></div>
                </div>
            </div>
            
            <!-- 嘴巴 -->
            <div style="position: absolute; top: 115px; left: 50%; transform: translateX(-50%); width: 60px; height: 30px;">
                <svg viewBox="0 0 60 30">
                    <path d="M 5 10 Q 30 25 55 10" stroke="#333" stroke-width="4" fill="none" stroke-linecap="round"/>
                </svg>
            </div>
        </div>
        
        <!-- 身体 -->
        <div style="
            width: 160px;
            height: 80px;
            background: linear-gradient(145deg, #f5f5f5, #c0c0c0);
            border-radius: 80px 80px 40px 40px;
            margin: -15px auto 0;
            position: relative;
        ">
            <!-- 胸口发光 -->
            <div style="
                position: absolute;
                top: 15px;
                left: 50%;
                transform: translateX(-50%);
                width: 50px;
                height: 50px;
                background: radial-gradient(circle, #4CAF50, #2E7D32);
                border-radius: 50%;
                animation: breathe 3s ease-in-out infinite;
                box-shadow: 0 0 30px rgba(76, 175, 80, 0.5);
            "></div>
        </div>
        
        <style>
            @keyframes breathe {
                0%, 100% { transform: translateX(-50%) scale(1); }
                50% { transform: translateX(-50%) scale(1.15); }
            }
        </style>
        
        <div class="emotion-display" id="emotion_text">
            😊 随时陪伴你
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    # 初始化消息
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_emotion = "default"
    
    # 欢迎消息
    if len(st.session_state.messages) == 0:
        welcome = "你好呀！我是心灵伙伴 🌱 有什么想和我聊聊的吗？"
        st.session_state.messages.append({"role": "bot", "content": welcome})
    
    # 聊天标题
    st.markdown("### 💬 对话")
    
    # 消息容器
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入区域
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        user_input = st.text_input(
            "输入消息...", 
            placeholder="说点什么吧...", 
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col_button:
        send_button = st.button("发送 🚀")
    
    # 处理发送
    if send_button and user_input:
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 检测情绪和意图
        emotion = detect_emotion(user_input)
        intent = detect_intent(user_input)
        st.session_state.current_emotion = emotion
        
        # 显示思考状态
        with st.spinner("思考中..."):
            time.sleep(0.5)
        
        # 获取回复
        response = get_enhanced_response(emotion, intent, user_input)
        
        # 添加bot消息
        st.session_state.messages.append({"role": "bot", "content": response})
        
        # 更新情绪显示
        emoji = get_emotion_emoji(emotion)
        emotion_text = get_emotion_text(emotion)
        
        # 刷新页面
        st.rerun()
    
    # 当前情绪显示
    emoji = get_emotion_emoji(st.session_state.current_emotion)
    emotion_text = get_emotion_text(st.session_state.current_emotion)
    st.markdown(f'''
        <div style="text-align:center; margin-top:10px; padding:10px; background:rgba(255,255,255,0.7); border-radius:10px;">
            当前情绪感知：{emoji} {emotion_text}
        </div>
    ''', unsafe_allow_html=True)

# 底部信息
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#888; padding:20px;">
    <p>🌱 心灵伙伴 - 治愈系心理健康AI数字人</p>
    <p style="font-size:0.9em;">记得，你并不孤单。我一直在这里陪着你。</p>
</div>
""", unsafe_allow_html=True)
