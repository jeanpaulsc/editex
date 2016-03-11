@auth.requires_login()
def index():
    rows = db(db.segment.owner==auth.user_id).select(order_by='position') or redirect(URL('default','index'))
    return dict(rows=rows)

def new_root():
    form = SQLFORM(db.segment)
    if form process().accepted:
        response.flash='root created'
        redirect('index')
    else:
        response.flash='form has errors'
        return dict(form=form)

def activate_record():
    if len(request.args)>0:
        session.active_record = db(db.segmment.id==request.args(0)).select().first()
    row = session.active_record
    return dict(row=row)

def edit_segment():
    session.active_record = db(db.segmment.id==request.args(0)).select().first()
    if session.active_record.owner==auth.user_id:
        form = SQLFORM(db.segment)
        form.vars.body = session.active_record.body
    return dict(form=form)

def new_section():
    form = SQLFORM(db.segment)
    response.flash="enter a section title"
    if form.process().accepted:
        response.flash="section created"
        cur_meta_root = form.vars.id
    else:
        response.flash="error"
@auth.requires_login()
def append_segment():
    parent = db(db.segment.id==request.args(0))
