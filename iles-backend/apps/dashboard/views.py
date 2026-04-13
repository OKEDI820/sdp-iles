from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.placements.models import InternshipPlacement
from apps.logs.models import WeeklyLog
from apps.evaluations.models import Evaluation

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logs = WeeklyLog.objects.all()
        evaluations = Evaluation.objects.all()
        placements = InternshipPlacement.objects.all()
        if user.role == 'student':
            logs = logs.filter(student=user)
            evaluations = evaluations.filter(weekly_log__student=user)
            placements = placements.filter(student=user)
        data = {
            'total_users': User.objects.count(),
            'total_placements': placements.count(),
            'total_logs': logs.count(),
            'draft_logs': logs.filter(status='draft').count(),
            'submitted_logs': logs.filter(status='submitted').count(),
            'reviewed_logs': logs.filter(status='reviewed').count(),
            'approved_logs': logs.filter(status='approved').count(),
            'total_evaluations': evaluations.count(),
            'average_score': float(evaluations.aggregate(avg=Avg('total_score')).get('avg') or 0),
            
            
        }
<<<<<<< HEAD
        return Response
        
=======
        return Response(data)
>>>>>>> 0b68342d3a4c5c2d987ebccb4c628bf2cf5920c4
       
