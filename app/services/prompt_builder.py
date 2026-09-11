from app.models import PostRequest


def build_prompt(request: PostRequest) -> str:
    cafe = request.cafe_name or "الكافيه"
    return f"""
اكتب نص بوست تسويقي مختلف باللهجة الكويتية للكافيهات.
الفكرة: {request.idea}
الأجواء: {request.mood}
اسم الكافيه: {cafe}
الأسلوب: {request.tone}

أخرج JSON فقط بالمفاتيح التالية:
text: نص قصير من جملتين إلى أربع جمل، مختلف وغير مكرر.
call_to_action: دعوة قصيرة للزيارة أو الطلب.
hashtags: قائمة من 3 إلى 5 هاشتاقات.
لا تخترع أسعاراً أو عروضاً أو معلومات غير مذكورة.
""".strip()