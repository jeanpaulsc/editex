@auth.requires_login()
def index():
   # if len(request.vars)>0:
   #     request.vars.each()
   #     content = db()
    return dict()

@auth.requires_login()
def post():
    return dict(form=SQLFORM(db.comment_post).process(),
                comments=db(db.comment_post).select())