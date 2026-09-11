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
            {"role": "system", "content": "أنت كاتب محتوى كويتي مبتكر، لا تكرر الصياغة."},
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
    openings = [
        f"اليوم المزاج غير مع {request.idea}.",
        f"لما تجتمع أجواء {request.mood} مع {request.idea}، تصير السالفة غير.",
        f"خذوا لكم وقفة حلوة مع {request.idea} في {cafe}.",
    ]
    closings = [
        "مرّوا علينا وخلوها لحظة تستاهل.",
        "ناطرينكم على فنجال يضبط المزاج.",
        "خلّوا جمعتكم تبدأ من عندنا.",
    ]
    opening = secrets.choice(openings)
    closing = secrets.choice(closings)
    return PostResult(
        text=f"{opening}\n{closing}",
        hashtags=["#قهوة", "#كافيهات_الكويت", "#مزاج_كويتي"],
        call_to_action="زورونا اليوم.",
        mode="local",
    )