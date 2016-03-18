import datetime

def index():
    rows = db(db.sect.id>0).select(orderby='section')
    return dict(rows=rows)

def select_sect():
    session.active_sid = request.args(0)
    section = db(db.sect.id==session.active_sid).select().first()
    session.section_title = section.title
    session.pid=""
    redirect('compose','section_index')

def problems():             # expects section as args(0)
    if len(request.args) > 0:
        section = db(db.segment.problem==request.args(0)).select().first()
    else:
       section = db(db.segment.problem==1).select().first()
    session.m = []
    rows = ""
    """
    try:
        rows = db(db.segment.parent_id==request.args(0, int)).select()
    except:
        print 'section error'
        redirect('compose','index')"""
    print "form prepared",datetime.datetime.today()
    print
    print 'rows: '
    print rows
    return dict(section=section)

def subsegs():
    if len(request.args)==0:
        rows = db(db.segment.section_id==request.vars['section']).select(orderby='problem')
    else:
        rows = db(db.segment.parent_id==request.args(0)).select(orderby='problem')
    print "in subsegs with args: ",request.args(0)
    print len(rows), 'selected'
    if len(rows)==None:
        return dict()
    return dict(rows=rows)

def new_compound():
    rid = request.args(0)
    print 'id: ', id
    form = SQLFORM(db.compound)
    if form.accepted:
        db.compound.update(rid,next=form.vars.id)
        response.flash='accepted'
        if form.vars.image:
            return IMG(src=form.vars.image)
        else:
            return form.vars.body
    return dict(form=form)
    """
     session.cur_section

    for row in rows:
        rstring=A(row.body,href=URL('show_problem',args=row.id))
        session.m.append(rstring)
    return dict(table=TABLE(*[TR(v) for v in session.m]))
"""

def sub_segments():
    rows = db(db.segment.parent_id==request.args(0,int)).select()
    return dict(rows=rows)

def data():
    rid=0
    if not session.m:
        session.m = []
    if request.vars.q:
        try:
            rid = db.segment.insert(body=request.vars.q)
            rstring=A(request.vars.q,href=URL('show_problem',args=rid))
            session.m.append(rstring)
        except Exception, e:
            response.flash='db error: %s' % e
    return TABLE(*[TR(v) for v in session.m])


def data2():
    rid=0
    if not session.m:
        session.m = []
    if request.vars.image:
        session.m.append(IMG(src=URL('download',args=request.vars.image)))
    else:
        session.m.append(form.vars.body)
    return TABLE(*[TR(v) for v in session.m])

def compounder():
    form = SQLFORM(db.compound)
    if form.accepted:
        response.flash='form accepted'
        return dict() # LOAD('compose','data',vars=form.vars,ajax=True)
    else:
        response.flash='form error ', Exception
    return dict(form=form)

def flash():
    response.flash = 'this text should appear!'
    return dict()

def fade():
    return dict()


def new_section():
    form=SQLFORM(db.sect)
    if form.process().accepted:
        redirect(URL('compose','section_index',args=form.vars.id))
    return dict(form=form)

def append_problem():
    return "jQuery('#problems').append(%s);" % repr(request.vars.body)

""" WRITE """
@auth.requires_login()
def add_problem():
    print 'entered add_problem'
    body=request.vars.body
    print "body: ",body
    bid = db.segment.insert(body=body)
    print "problem inserted"
    return "jquery('#problems').append(%s);" % body

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

def form():
    return dict()