@auth.requires_login()
def index():
    try:
        meta_id = session.cur_meta_id
        redirect('edit','segments')
    except Exception, e:
        response.flash='%s' % e
    if auth.has_membership('mentors'):
        rows = db(db.meta.reviewed_by==auth.user_id).select()
        if len(rows)==1:
            session.cur_meta_id==rows.first().id
            redirect('edit','segments')
        elif len(rows)==0:
            response.flash='There are no documents submitted for you at this time'
        else:
            response.flash='Select a document to view'
    if auth.has_membership('pupils'):
        rows = db(db.meta.created_by==auth.user_id).select()
        if len(rows)==1:
            session.cur_meta_id==rows.first().id
            redirect('edit','segments')
        elif len(rows)==None:
            response.flash='Create a document'
            redirect(URL(c='edit',f='new_document'))
        else:
            response.flash='Select or create a document'
    rows = db(db.meta.id>0).select()
    return dict(rows=rows)

@auth.requires_login()
def title_form():
    response.flash = 'please fill the title'
    form = FORM('Title:',
              INPUT(_name='body', requires=IS_NOT_EMPTY()),
              INPUT(_name='category', value='title'),
              INPUT(_type='submit'))
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('segments'))
    elif form.errors:
        response.flash = 'form has errors'
        redirect(URL('segments'))
    return dict(form=form)

def next():
    if form.process().accepted:
        session.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
        redirect(URL('title_form'))
    return dict()


@auth.requires_login()
def new_root():
    form = SQLFORM(db.segment)

    session.rank = 1000

    if form.process().accepted:
        session.cur_meta_id=form.vars.id
        redirect(URL(c='edit',f='segments'))
    else:
        response.flash='form has errors'
    return dict(form=form)

def indent():
    modu(7,2)
    response.flash='k'
    return dict()

def modu(x,y):
    response.flash= x%y
    return dict()

@auth.requires_login()
def segments():
    if len(request.args)>0:
        session.cur_meta_id = request.args(0)
    try:
        meta = db(db.meta.id==session.cur_meta_id).select().first()
        segs = db(db.segment.meta_id==session.cur_meta_id).select()
    except Exception, e:
        response.flash="error: %s" % e
        redirect(URL('edit','index'))
    return dict(meta=meta,segs=segs)

@auth.requires_login()
def txt():
    session.seg_cat = 'txt'
    print "in txt"
    if len(request.args) > 0:
        form = SQLFORM(db.segment, request.args(0))
    else:
        form = SQLFORM(db.segment)
    if form.process().accepted:
        redirect('segments')
    else:
        print 'error'
        response.flash='failure to insert record'
    return dict(form=form.process())

def segtex():
    session.seg_cat = 'tex'
    if len(request.args)>0:
        seg2edit = request.args(0,cast=int)
        form=SQLFORM(db.segment,record=request.args(0,cast=int))
    else:
        seg2edit = 0
        form=SQLFORM(db.segment)
    try:
        meta = db(db.meta.id==session.cur_meta_id).select().first()
        segs = db(db.segment.meta_id==session.cur_meta_id).select()
    except Exception, e:
        response.flash="error: %s" % e
        redirect('edit','index')
    if form.process().accepted:
        print "TeX form accepted"
        redirect(URL('edit','segments'))
    else:
        print 'error'
        response.flash='failure to insert record'
    return dict(form=form,meta=meta,segs=segs,seg2edit=seg2edit)

def segtxt():
    session.seg_cat = 'txt'
    if len(request.args)>0:
        seg2edit = request.args(0,cast=int)
        form=SQLFORM(db.segment,record=request.args(0,cast=int))
    else:
        seg2edit = 0
        form=SQLFORM(db.segment)
    try:
        meta = db(db.meta.id==session.cur_meta_id).select().first()
        segs = db(db.segment.meta_id==session.cur_meta_id).select()
    except Exception, e:
        response.flash="error: %s" % e
        redirect('edit','index')
    if form.process().accepted:
        print "txt form accepted"
        redirect(URL('edit','segments'))
    else:
        print 'error'
        response.flash='failure to insert record'
    return dict(form=form,meta=meta,segs=segs,seg2edit=seg2edit)

def texonly():
    session.seg_cat = 'tex'
    form=SQLFORM(db.segment,record=request.args(0))
    if form.process().accepted:
        print "TeX form accepted"
        redirect('segments')
    else:
        print 'error'
        response.flash='failure to insert record'
    return dict(form=form)

@auth.requires_login()
def TeX():
    print "in TeX.load"
    if len(request.args) > 0:
        form = SQLFORM(db.segment, request.args(0))
    else:
        form = SQLFORM(db.segment)
    if form.process().accepted:
        print "TeX form accepted"
        redirect('segments')
    else:
        print 'error'
        response.flash='failure to insert record'
    return dict(form=SQLFORM(db.segment))

@auth.requires_login()
def foot_bar():
    if auth.has_membership('mentors'):
        redirect('review_bar')
    return dict()

@auth.requires_membership('pupils')
def commit_document():
    #set meta status to review
    db(db.meta.id==session.cur_meta_id).update(doc_state='review')
    #invite inspection from mentor via email
    mail.send('somebody@example.com',
        'review request',
        ('Progress has been posted for your review at http://tuerimind.pythonanywhere.com/editex/edit/index',
        "<html>Progress has been posted for your review <a href='http://tuerimind.pythonanywhere.com/editex/edit/index'>HERE</a></html>"))
    form = SQLFORM(db.msg)
    return dict(form=form)

@auth.requires_membership('mentors')
def return_submission():
    #set meta status to review
    db(db.meta.id==session.cur_meta_id).update(doc_state='review')
    #invite inspection from mentor via email
    mail.send('somebody@example.com',
        'review request',
        ('Progress has been posted for your review at http://tuerimind.pythonanywhere.com/editex/edit/index',
        "<html>Progress has been posted for your review <a href='http://tuerimind.pythonanywhere.com/editex/edit/index'>HERE</a></html>"))
    form = SQLFORM(db.msg)
    return dict(form=form)

def buttonset():
	bset = ['¬','∀','∃','∄','∧','∨','∴','+','−','±','×','∗','÷','∙','√','∞','∏','∑', '←','→','↔','⇐','⇒','⇔','…','―','(',')','[',']','{','}','⎡','⎤','⎣','⎦', '∝','∩','∪','⊂','⊄','⊃','⊅','⊆','⊇','∈','∉','∋','∍','∅','⊕','⊗']
	return dict(bset=bset)

def btest():
	bset = ['≤','≥','≠','≡','≅','≈','∼','∞']
	return dict(bset=bset)

def b3():
	bset = ['¬','∀','∃','∄']
	return dict(bset=bset)
