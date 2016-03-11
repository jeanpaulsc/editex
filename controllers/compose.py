def index():
    rows = db(db.segment.id>0).select()
    return dict(rows=rows)

""" WRITE """
@auth.requires_login()
def new_problem():
    body=request.vars.body
    form = SQLFORM(db.segment)  #,fields=['body'],formstyle='divs',labels={'body':""})
    if form.process().accepted:
        db(db.segment.id==form.vars.id).update(segnum=form.vars.id)
        response.flash=form.vars.segment_body
    return dict(form=form)

@auth.requires_login()
def append_txt():
    segnum = request.args(0)
    form = SQLFORM(db.segment,fields=['body'],formstyle='divs',labels={'body':""})
    if form.process().accepted:
        id = form.vars.id
        db(db.segment.id==form.vars.id).update(segnum=segnum,parent_id=None,category='txt')
        response.flash='record added'
    return dict(form=form)

@auth.requires_login()
def append_tex():
    segnum = request.args(0)
    form = SQLFORM(db.segment,fields=['body'],formstyle='divs',labels={'body':""})
    if form.process().accepted:
        id = form.vars.id
        db(db.segment.id==form.vars.id).update(segnum=segnum,parent_id=None,category='tex')
        response.flash='record added'
    return dict(form=form)

""" READ """
@auth.requires_login()
def show_problem():
    session.cur_owner = ""
    rows = db(db.segment.segnum==request.args(0)).select()
    return dict(rows=rows)

@cache.action()
def download():
    return response.download(request, db)

""" WORKING  """