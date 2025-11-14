from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Question

# JSON 반환: 모든 질문 가져오기
def get_questions(request):
    # DB에서 질문 순서대로 가져오기
    questions = Question.objects.all().order_by('id')
    
    # Q1, Q2, ... 형식으로 매핑
    data = {f"q{i+1}": {"id": q.id, "question": q.text} for i, q in enumerate(questions)}
    
    return JsonResponse({"questions": data})

# AJAX 요청 시 CSRF 예외 처리
@csrf_exempt
def submit_test(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST 요청만 가능합니다."}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON 형식으로 데이터를 보내주세요."}, status=400)

    questions = Question.objects.all().order_by('id')

    fields = ["백엔드", "프론트엔드", "사이버보안", "게임개발", "사물인터넷", "빅데이터", "인공지능"]
    scores = {field: 0 for field in fields}

    for i, q in enumerate(questions):
        # 순번(Q1, Q2, ...)으로 답변 가져오기
        answer = data.get(f"q{i+1}")
        
        if answer == "예":
            q_fields = [f.strip() for f in q.fields.split(",")]
            for field in q_fields:
                if field in scores:
                    scores[field] += 1

    max_score = max(scores.values())
    best_fields = [field for field, score in scores.items() if score == max_score]

    return JsonResponse({
        "best_fields": best_fields,
        "scores": scores
    })