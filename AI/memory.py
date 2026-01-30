from .models import AIConversation

def save_memory(user, question, answer):
    return AIConversation.objects.create(
        user=user,
        question=question,
        answer=answer
    )

def fetch_memory(user, limit=5):
    qs = AIConversation.objects.filter(user=user).order_by("-created_at")[:limit]
    return [(x.question, x.answer) for x in qs][::-1]
