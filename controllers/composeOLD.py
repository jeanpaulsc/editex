@auth.requires_login()
def index():
    rows=db(db.segment.id>0).select(orderby='pos')
    if len(rows)>0:
        return dict(rows=rows)
    else:
        return LOAD('compose','new_section')

@auth.requires_login()
def auth_form():
    form = SQLFORM(auth.user,record=4)
    return dict(form=form)

@auth.requires_login()
def new_document():
    session.seg_cat = 'title'
    form=SQLFORM(db.document_root).process()
    if form.process().accepted:
        session.cur_group_id = form.vars.id
        redirect('compose','segtext')
    else:
        response.flash="form has errors"
    return dict(form=form,segs=db(db.segment.group_id==session.cur_group_id).select())

@auth.requires_login()
def segtxt():
    session.seg_cat = 'txt'
    if len(request.args)>0:
        seg2edit = request.args(0,cast=int)
        form=SQLFORM(db.segment,record=request.args(0,cast=int))
    else:
        seg2edit    =    0
        form=SQLFORM(db.segment)
    try:
        segs    =    db(db.segment.group_id==session.cur_group_id).select()
    except    Exception,    e:
        response.flash="error:    %s"    %    e
        redirect('compose','index')
    if    form.process().accepted:
        print    "txt    form    accepted"
        redirect(URL('compose','segments'))
    else:
        print    'error'
        response.flash='failure    to    insert    record'
    return    dict(form=form,segs=segs,seg2edit=seg2edit)

@auth.requires_login()
def    segtex():
    session.seg_cat    =    'tex'
    if    len(request.args)>0:
        seg2edit    =    request.args(0,cast=int)
        form=SQLFORM(db.segment,record=request.args(0,cast=int))
    else:
        seg2edit    =    0
        form=SQLFORM(db.segment)
    try:
        segs    =    db(db.segment.group_id==session.cur_group_id).select()
    except    Exception,    e:
        response.flash="error:    %s"    %    e
        redirect('compose','index')
    if    form.process().accepted:
        print    "TeX    form    accepted"
        redirect(URL('compose','segments'))
    else:
        print    'error'
        response.flash='failure    to    insert    record'
    return    dict(form=form,segs=segs,seg2edit=seg2edit)

def    segment_entry():
    rows    =    db(db.segmnent.root==session.cur_root_id).select(orderby='pos')
    return    dict()

@auth.requires_login()
def    segimg():
    session.seg_cat    =    'img'
    if    len(request.args)>0:
        seg2edit    =    request.args(0,cast=int)
        form=SQLFORM(db.segment,record=request.args(0,cast=int))
    else:
        seg2edit    =    0
    form=SQLFORM(db.segment,fields='image')
    try:
        segs    =    db(db.segment.group_id==session.cur_group_id).select()
    except    Exception,    e:
        response.flash="error:    %s"    %    e
        redirect('compose','index')
    if    form.process().accepted:
        print    "img    form    accepted"
        redirect(URL('compose','segments'))
    else:
        print    'error'
        response.flash='failure    to    insert    record'
    return    dict(form=form,segs=segs,seg2edit=seg2edit)

def new_section():
    form=FORM('Enter New Section Title:',
              INPUT(_name='title', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        id = db.segment.insert(body= form.vars.title,category='title',root='this')
        session.cur_root = id
        return LOAD('compose','list_nodes', ajax=True,target='contents')
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

def new_sectionOLD():
    form    =    SQLFORM(db.segment,fields=['body'])
    if    form.accepts(request,    formname=None):
        session.cur_root_id    =    form.vars.id
        row    =    db(db.segment.id==form.vars.id).select().first()
        row.update_record(root=session.cur_root_id,category='title')

        return    LOAD('compose','segment_entry',    ajax=True)
    elif    form.errors:
        return    TABLE(*[TR(k,    v)    for    k,    v    in    form.errors.items()])

def truncate(x, d):
    return int(x*(10.0**d))/(10.0**d)

def append():
    rows    =    db(db.segment.id==request.args(0)).select()
    session.cur_tier    =    row.tier or 0
    seession.cur_pos    =    row.pos + 10**(-tier)
    form = SQLFORM(db.segments, fields=['body'], formstyle='divs',names={'body':""})
    return    dict(form=form)

def insert():
    print request.args(0)
    if len(equest.args(0) or session.cur_root
    search_id = request.args(0) or session.cur_root
    row    =    db(db.segment.id==search_id).select().first()
    print row
    print 'double asterisk ',  10**(-row.tier)
    session.cur_tier    =    row.tier    +    1
    seession.cur_pos    =    row.pos    +    10**(-row.tier)
    form = SQLFORM(db.segments, fields=['body'], formstyle='divs',names={'body':""})
    return    dict(form=form)

def list_nodes():
    rows    =    db(db.segment.id>0).select(orderby='pos')
    return    dict(rows=rows)

def outdent():
    row = db(db.segment.id==request.args(0)).select().first()
    if row.tier > 0:
        tier = row.tier-1
    else:
        response.flash='selected row is not indented'
    pos = row.pos + 10**(-tier)
    pos=truncate(pos,tier)
    row.update_record(tier=tier,pos=pos)
    return dict(id=row.id,tier=tier,pos=pos)

def indent():
    row = db(db.segment.id==request.args(0)).select().first()
    tier = row.tier+1
    pos = row.pos + 10**(-tier)
    pos=truncate(pos,tier)
    row.update_record(tier=tier,pos=pos)
    return dict(id=row.id,tier=tier,pos=pos)
"""
def mcedit():
    if len(request.args)>0:
        row = db(db.segment.id==request.args(0)).select().first()
    form=FORM(INPUT(_name='textarea'), INPUT(_type='submit'))
    return dict(form=form)"""

def mcedit():
    form=SQLFORM.factory(db.segment)
    if form.process().accepted:
        id = db.client.insert(**db.client._filter_fields(form.vars))
        form.vars.client=id