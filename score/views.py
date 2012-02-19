# Create your views here.
from Oedu import settings
from Oedu.core.models import UserProfile
from Oedu.score.models import Score, Course
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import json

@login_required
def index(request):
    return render_to_response("score/index.html")

@login_required
def score_manager(request):
    return render_to_response("score/scoreManager.html")

@login_required
def get_course_score(request, course_id):
    '''
    url:    /score/course/{course_id}
    get all the scores of a certain course
    '''
    course = get_object_or_404(Course, pk=course_id)
    scores = course.score_set.all().order_by('pk')
    return render_to_response("score/score_popup.html", {'scores': scores, 'course_name' : course.name})

@login_required
def get_course_score_json(request, course_id):
    '''
    url:    /score/course/{course_id}/scores
    get all the scores of a certain course
    '''
    course = get_object_or_404(Course, pk=course_id)
    scores = course.score_set.all().order_by('pk')
    return HttpResponse(serializers.serialize("json", scores), mimetype="application/json")


@login_required
def get_course_list(request):
    courses = Course.objects.all().order_by('grade')
    return HttpResponse(serializers.serialize("json", courses), mimetype="application/json")

@login_required
def get_user_score_json(request, user_id=0):
    '''
    url:    /score/user/{user_id}/scores
    get all the scores of a certain user
    '''   
    user = get_object_or_404(User, pk=user_id)
    scores = user.score_set.all().order_by('pk')
    return HttpResponse(serializers.serialize("json", scores), mimetype="application/json")

@login_required
def get_user_score(request, user_id):
    '''
    url:    /score/user/{user_id}/
    get all the scores of a certain user
    '''   
    user = get_object_or_404(User, pk=user_id)
    scores = user.score_set.all().order_by('pk')
    return render_to_response("score/user_score_popup.html", {'scores': scores, 'user' : request.user, 'student' : user})

@login_required
def get_user_course(reqeust, user_id=0):
    '''
    url:    /score/user/{user_id}/courses
    get all the courses of a certain user
    '''   
    user = get_object_or_404(User, pk=user_id)
    courses = user.course_set.all().order_by('pk')
    return HttpResponse(serializers.serialize("json", courses), mimetype="application/json")

class score_detail:
    '''
    url:    /score/crud/{score_id}
    restful interface of a certain score
    '''

    def __call__(self, request, score_id=0):
        self.request, self.user, self.build_absolute_uri, self.get_ful_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.score_id = score_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()

    @login_required
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain score
            type:   json
            list of a dic:
            sample: [{
                        "pk"        :   1,
                        "models"    :   "score.score",
                        "fields"    :   {
                            "score"     :   90,
                            "course"    :   1,
                            "student"   :   1,
                        }
                    }]
        '''
        s = get_object_or_404(Score, pk=self.score_id)
        return HttpResponse(serializers.serialize("json", [s]), mimetype="application/json")

    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain score
        type: json
        @paramm score:
        '''
        s = get_object_or_404(Score, pk=self.score_id)
        post = json.loads(self.request.raw_post_data)
        try:
            s.score = post.has_key("score") and post["score"] or s.score
            s.save()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")

    @login_required
    def do_PUT(self):
        '''
        http method: POST
        to create a certain score
        @param score:
        @param course: the id of course
        @param user: the id of user
        @return: s.pk or failed
        '''
        put = json.loads(self.request.raw_post_data)
        course = get_object_or_404(Course, pk=put['course'])
        student = get_object_or_404(User, pk=put['user'])
        try:
            s = course.score_set.create(score=put['score'], student=student)
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps(s.pk), mimetype="application/json")

    @login_required
    def do_DELETE(self):
        '''
        http method: DELETE
         to delete a certain status
        @return: success or failed(a dictionary)
        '''
        s = get_object_or_404(Score, pk=self.score_id)
        try:
            s.delete()
        except:
            return HttpResponse("failed", mimetype="application/json")
        return HttpResponse(json.dumps("success"), mimetype="application/json")

class course_detail:
    '''
    url:    /score/course/crud/{course_id}/
    restful interface of a certain course
    '''
    
    def __call__(self, request, course_id = 0):
        self.request, self.user, self.build_absolute_uri, self.get_full_path = \
            request, request.user, request.build_absolute_uri, request.get_full_path
        self.course_id = course_id
        try:
            callback = getattr(self, "do_%s" % request.method)
        except AttributeError:
            pass
        return callback()
    
    @login_required  
    def do_GET(self):
        '''
        http method: GET
        @return: a dictionary of a certain course
            type:    json
            list of a dic:     
            sample:   [{
                        "pk": 2,
                        "model": "score.course", 
                        "fields": {
                            "name": "se", 
                            "description": "se"}
                        }]
        '''
        c = get_object_or_404(Course, pk=self.course_id)
        return HttpResponse(serializers.serialize("json", [c]), mimetype="application/json")
    
    @login_required
    def do_POST(self):
        '''
        http method: POST
        to update a certain course
        type:    json
        @param name:
        @param description: 
        @param grade_point:
        @return: success or failed(a dictionary)
        '''
        c = get_object_or_404(Course, pk=self.course_id)
        post = json.loads(self.request.raw_post_data)
        c.name = post.has_key("name") and post["name"] or c.name
        c.description = post.has_key("description") and post["description"] or c.description
        c.grade_point = post.has_key("grade_point") and post["grade_point"] or c.grade_point
        c.save()
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
    @login_required  
    def do_PUT(self):
        '''
        http method: PUT
        to create a certain course
        type:    json
        @param name: the name of a course
        @param description: the description of course
        @param grade: the grade
        @param grade_point: the grade_point
        @return: course.pk or failed(a dictionary)
        '''
        put = json.loads(self.request.raw_post_data)
        c = Course.objects.create(name=put['name'], description=put['description'],
                                  grade=put['grade'], grade_point=put['grade_point'])
        return HttpResponse(json.dumps(c.pk), mimetype="application/json")
    
    @login_required  
    def do_DELETE(self):
        '''
        http method: DELETE
        to delete a certain course
        @return: success or failed(a dictionary)
        '''
        c = get_object_or_404(Course, pk=self.course_id)
        c.delete()
        return HttpResponse(json.dumps("success"), mimetype="application/json")
    
@login_required
def upload_score(request):
    if request.method == 'GET':
        return render_to_response("test/upload_xlrd.html")
    else:
        file = request.FILES["file"]
        file_path = settings.STATIC_DIR + 'courses_and_scores/' + file.name
        destination = open(file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        import xlrd
        book = xlrd.open_workbook(file_path)
        sheet = book.sheets()[0]
        scores = []
        course_name = sheet.cell(1, 2).value
        grade = int(sheet.cell(1, 4).value)
        grade_point = int(sheet.cell(1,5).value)
        course = Course.objects.get_or_create(name=course_name, grade=grade, grade_point=grade_point)[0]
        for i in range(1, sheet.nrows):
            item = {    'nju_id'    :   sheet.cell(i, 1).value,
                        'score'     :   sheet.cell(i, 3).value,
                    }
            scores.append(item)
        for score in scores:
            user = UserProfile.objects.get(nju_id=score['nju_id'])
            user = user.user
            course.score_set.create(student=user, score=score['score'])
            
        return HttpResponse(json.dumps("success"))