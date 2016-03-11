def index():
    rows = db(db.segment.id>0).select()
    return dict(rows=rows)
  """ todo: """

""" WRITE """
@auth.requires_login()
def new_problem():
    session.ar=None
    redirect(URL('compose','mcedit'))
    return dict()

def select_segment():
    session.ar=db(db.segment.id==request.args(0)).select().first()
    if session.ar.status=="draft":
        form = SQLFORM(db.segment,record=session.ar,fields=['body'],formstyle='divs',labels={'body':""})
    else:
        form = SQLFORM(db.segment,fields=['body'],formstyle='divs',labels={'body':""})
    if form.process().accepted:
        session.ar=form.vars.id
        response.flash='record added'
    else:
        response.flash='NUCKING FUTS!'
    return    dict(form=form)



def write():
    if len(request.args):
        session.ar=request.args(0)
    if row.owned_by==auth.user_id:
        form = SQLFORM(db.segments,record=request.args(0),fields=['body'], formstyle='divs',labels={'body':""})
    else:
        form = SQLFORM(db.segments,fields=['body','parent'], formstyle='divs',labels={'body':""})
        form.vars.parent=request.args(0)
    return    dict(form=form)

@auth.requires_login()
def new():
    form = SQLFORM(db.segment, fields=['body'], formstyle='divs',labels={'body':""})
    if form.process().accepted:
        response.flash='were good'
    else:
        response.flash='NUCKING FUTS!'
    return    dict(form=form)

def progress():
    rows = db(db.segment.root==request.args(0)).select(orderby='pos')
    return dict(rows=rows)

def mcedit():
    return dict()

""" WORKING  """