def index():
    return dict()

def data():
    print 'data'
    if not session.m:
        session.m = []
    if request.vars.q:
        if len(session.m) == 10:
            del(session.m[0])
        session.m.append(request.vars.q)
    return TABLE(*[TR(v) for v in sorted(session.m)]).xml()


def flash():
    response.flash = 'this text should appear!'
    return dict()


def fade():
    return dict()

def store():
    stream = open(filename, 'rb')
    db.myfile.insert(image=db.myfile.image.store(stream, filename), image_file=stream.read())
    return dict()

def retrieve():
    row = db(db.myfile).select().first()
    (filename, stream) = db.myfile.image.retrieve(row.image)
    import shutil
    shutil.copyfileobj(stream,open(filename,'wb'))
    return dict()

def form():
    return dict()

def ajax():
    return dict()

def form2():
    form2 = SQLFORM(db.myform)
    if form2.process().accepted:
        response.flash='record created'
    return dict(form2=form2)

def form5():
    form=SQLFORM(db.myform)
    return dict(form=form)