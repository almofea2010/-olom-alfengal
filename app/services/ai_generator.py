import json
import os
import secrets
from typing import Any

from app.models import PostRequest, PostResult
from app.services.prompt_builder import build_prompt


def prepare_post(idea: str, mood: str, cafe_name: str, tone: str) -> dict[str, Any]:
    request = PostRequest(idea=idea, mood=mood, cafe_name=cafe_name, tone=tone)
    if os.getenv("OPENAI_API_KEY", "").strip():
        return _generate_with_openai(request).model_dump()
    return _generate_local(request).model_dump()


def _generate_with_openai(request: PostRequest) -> PostResult:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.95,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "أنت كاتب محتوى كويتي مبتكر ومحرر إعلانات. اكتب نصوصاً محسوسة ومحددة، واكشف الفكرة من أول سطر. ارفض الصياغات العامة والمكررة."},
            {"role": "user", "content": build_prompt(request)},
        ],
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    return PostResult(
        text=str(data.get("text", "")),
        hashtags=[str(tag) for tag in data.get("hashtags", [])],
        call_to_action=str(data.get("call_to_action", "")),
        mode="ai",
    )


def _generate_local(request: PostRequest) -> PostResult:
    cafe = request.cafe_name or "كافيهكم"
    idea = request.idea.rstrip(".!؟")
    mood_lines = {
        "زوارة الخميس": "خلّوا جمعة الخميس تبدأ بشي يفتح السالفة من أول رشفة.",
        "صباح القهوة": "صباحكم يستاهل بداية أهدى وألذ من المعتاد.",
        "أجواء الويكند": "الويكند ما يحتاج خطة كبيرة، يحتاج اختيار يضبط اليوم.",
        "عرض اليوم": "إذا كانت هذي وقفتكم اليوم، خلّوها محسوبة من أولها.",
        "رمضان": "بعد الإفطار، خذوا وقتكم مع نكهة تخلي الجلسة أطول وأحلى.",
        "جلسة الديوانية": "الجلسة الزينة تعرفها من أول ما يدور الفنجال بين الحضور.",
    }
    tone_lines = {
        "حماسي": [
            f"جاهزين لشي يرفع مستوى {idea}؟",
            f"اليوم عندنا سبب قوي يخلي {idea} نجم الجلسة.",
        ],
        "رايق": [
            f"خذوا نفساً هادئاً وخلو {idea} ياخذ وقته.",
            f"بعض الأيام يكفيها {idea} مضبوط ووقت على رواق.",
        ],
        "رسمي خفيف": [
            f"نقدم لكم {idea} بتفاصيل تليق بذوقكم.",
            f"اختياركم اليوم: {idea}، بطريقة مرتبة وواضحة.",
        ],
    }
    sensory_lines = [
        f"في {cafe} نهتم بالتفاصيل اللي تبين من أول تجربة، من النكهة إلى آخر رشفة.",
        "اختيار مناسب للي يبي طعم واضح وجلسة ما تنتهي بسرعة.",
        "الفكرة بسيطة، لكن الفرق يبان لما تكون التفاصيل مضبوطة.",
    ]
    calls_to_action = [
        f"مرّوا على {cafe} وخلو التجربة تحكم.",
        "اطلبوها اليوم وشاركونا أول انطباع.",
        "خلّوا خطوتكم الجاية على مزاجكم.",
    ]
    tone_options = tone_lines.get(request.tone, tone_lines["حماسي"])
    opening = secrets.choice(tone_options)
    sensory = secrets.choice(sensory_lines)
    mood_line = mood_lines.get(request.mood, "اختاروا وقتكم، والباقي علينا.")
    closing = secrets.choice(calls_to_action)
    return PostResult(
        text=f"{opening}\n{mood_line}\n{sensory}",
        hashtags=["#قهوة", f"#{request.mood.replace(' ', '_')}", "#كافيهات_الكويت", "#مزاج_كويتي"],
        call_to_action=closing,
        mode="local",
    )