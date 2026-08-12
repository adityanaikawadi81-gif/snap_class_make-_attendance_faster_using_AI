from src.database.config import supabase 
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def get_all_students():
    respose = supabase.table("students").select("*").execute()
    return respose.data

def check_teacher_exists(uusername):
    response = supabase.table("teachers").select("uusername").eq("uusername",uusername).execute()
    return len(response.data) > 0

def create_teacher(uusername, password, name):

    data = { "uusername" : uusername, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def create_student(new_name , face_embedding=None , voice_embedding = None):
    data = {"name" : new_name , "face_embedding" : face_embedding , "voice_embedding":voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data


def teacher_login(uusername, password):
    response = supabase.table("teachers").select("*").eq("uusername", uusername).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None

def create_subject(sub_name , sub_code , sub_section , teacher_id):
    data = {"name" : sub_name , "subject_code" : sub_code , "section":sub_section , "teacher_id":teacher_id}
    respose = supabase.table("subjects").insert(data).execute()
    return respose.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects

def enroll_student_to_subject(student_id , subject_id):
    data = {"student_id":student_id , "subject_id" :subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def  unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data