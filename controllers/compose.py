import datetime

def index():
    rows = db(db.sect.id>0).select(orderby='sid')
    return dict(rows=rows)

def problem_index():             # expects section as session.sect
    print "in problem_index"
    session.section = db(db.sect.id==request.args(0,int)).select().first() or redirect(URL('compose','index'))
    print 'row 10'
    rows = db(db.segment.section_id==request.args(0,int)).select(orderby='problem')
    if len(rows)==0:
        print 'section yields no rows'
        redirect(URL('compose','define_problem'))
    print "form prepared",datetime.datetime.today()
    return dict(rows=rows)

def append_compound():
    session.pid = request.args(0,int)
    form = SQLFORM(db.segments,fields=['body','image'])
    if form.process().accepted:
        db.segment.update(session.pid,comp_id=form.vars.id)
    return dict()

def define_problem():
    print 'in define_problem'
    form = SQLFORM.factory(
        Field('section', 'integer', requires=IS_NOT_EMPTY()),
        Field('problem', 'integer', requires=IS_NOT_EMPTY()),
        Field('subpart'))
    form.vars.section=session.sid
    form.vars.problem=session.pnum
    if form.process().accepted:
        response.flash = 'defaults updated'
        session.sid = int(form.vars.section)
        session.pnum = int(form.vars.problem)
        session.pid = db(db.segment.problem==int(session.pnum)).select().first()
        if not session.prid:
            session.pid = db.segment.insert(status='problem')
            redirect(URL('compose','define_proot',args=session.pid))
        session.subparts = db(db.segment.parent_id==int(session.pnum)).select()
        redirect('compose','define_subs')
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

def define_proot():
    print 'in proot'
    return dict()

def define_subs():
    return dict()

def compounder():
    print 'in controller: compounder'
    form = SQLFORM(db.part,fields=['body','image'])
    rows = db(db.comp_id==session.pid).select()
    if form.process().accepted:
        return LOAD('compose','compounder',ajax=True,ajax_trap=True)
    return dict(form=form,rows=rows)

def compounderOLD():
    if request.args:
        print 'in compounder with new curseg: ', request.args(0)
        session.curseg = request.args(0)
    form = SQLFORM(db.segment,fields=['body','image'])
    rows = db(db.part.comp_id==comp_id).select()
    print len(rows), ' existing found'
    if form.process().accepted:
        print 'record created: ',form.args.id
        return LOAD('compose','compounder',ajax=True,ajax_trap=True)
    return dict(form=form,rows=rows)

def p_comp():
    rows = db(db.select.problem==request.args(0)).select()
    return dict(rows=rows)

def listtest():
    return dict()

def vp():
    rows = db(db.segment.id>0).select()
    return dict(rows=rows)

# testing distinct problem division

def distinct_parts():
    set = db(db.part.id>0)
    print 'set len ',len(set.select())
    rows = db().select(db.part.ALL,orderby=-db.part.parent_id,distinct=False)
    print 'len ',len(rows)
    return dict(rows=rows)

def view_problems():
    rows = db(db.segment.id>0).select()
    return dict(rows=rows)

def seggrid():
    grid = SQLFORM.grid(db.segment)
    return dict(grid=grid)

def partgrid():
    grid = SQLFORM.grid(db.part)
    return dict(grid=grid)

def compound_problem():
    form = SQLFORM(db.segment)
    return dict(form=form)

def compound():
    rows = db(db.compound.problem==request.args(0,int)).select() or redirect('index')
    return dict(rows=rows)

def subsegedit():
    if len(request.args)==0:
        session.pid=request.args(0,int)
    print 'in controller: subsegedit'
    form = SQLFORM(db.segment,fields=['body','image'])
    rows = db(db.segment.parent_id==session.pid).select(orderby='problem')
    if form.process().accepted:
        return LOAD('compose','compounder',ajax=True,ajax_trap=True)
    return dict(form=form,rows=rows)

def compounder():
    print 'in compounder'
    rows = db(db.segment.comp_id==session.pid).select()
    form = SQLFORM(db.segment,fields=['body','image'])
    if form.process().accepted:
        return LOAD('compose','compounder',ajax=True,ajax_trap=True)
    return dict(form=form,rows=rows)


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

def compounder3():
    form = SQLFORM(db.compound)
    if form.accepted:
        response.flash='form accepted'
        return LOAD('compose','compounder',ajax=True,ajax_trap=True)
    else:
        response.flash='form error ', Exception
    return dict(form=form,rows=rows)

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